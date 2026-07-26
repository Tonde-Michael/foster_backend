# diagnose.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
from gisapp.models import Parcel

def diagnose():
    print("="*50)
    print("DATABASE DIAGNOSTIC")
    print("="*50)
    
    # Test 1: Database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✓ Database connection: OK")
    except Exception as e:
        print(f"✗ Database connection: FAILED - {e}")
        return
    
    # Test 2: Check if table exists
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'parcels'
            )
        """)
        exists = cursor.fetchone()[0]
        print(f"✓ Table 'parcels' exists: {exists}")
        
        if not exists:
            print("✗ Table not found!")
            return
    
    # Test 3: Count records with raw SQL
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM parcels')
        count = cursor.fetchone()[0]
        print(f"✓ Records in table (raw SQL): {count}")
    
    # Test 4: Show column names
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='parcels'
        """)
        columns = [row[0] for row in cursor.fetchall()]
        print(f"✓ Columns in table: {', '.join(columns)}")
    
    # Test 5: Try Django ORM
    try:
        orm_count = Parcel.objects.count()
        print(f"✓ Django ORM count: {orm_count}")
    except Exception as e:
        print(f"✗ Django ORM failed: {e}")
        
        # Show the last query
        if connection.queries:
            print(f"  Last query: {connection.queries[-1]['sql']}")
    
    # Test 6: Try to get first record with raw SQL
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT id, "UPN", "Owner" FROM parcels LIMIT 1')
            row = cursor.fetchone()
            if row:
                print(f"✓ Sample record: ID={row[0]}, UPN={row[1]}, Owner={row[2]}")
            else:
                print("✗ No records found in table")
        except Exception as e:
            print(f"✗ Failed to query sample: {e}")

if __name__ == "__main__":
    diagnose()