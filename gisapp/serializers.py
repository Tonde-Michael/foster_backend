# In gisapp/serializers.py
from rest_framework import serializers

from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon

from .models import Parcel, Payment

class ParcelSerializer(serializers.ModelSerializer):
    # Map to frontend expected names (they already match)
    coordinates = serializers.SerializerMethodField()
    
    class Meta:
        model = Parcel
        fields = [
            'id', 'upn', 'plot_no', 'owner', 'street_nam', 
            'land_use', 'area', 'registration_date', 'year_registered',
            'phone', 'email', 'coordinates'
        ]
        # These are the fields that can be written to
        read_only_fields = ['id', 'coordinates']
    
    def get_coordinates(self, obj):
        """Convert PostGIS geometry to Leaflet [lat, lng] format"""
        if obj.geom and obj.geom.geom_type == 'MultiPolygon':
            try:
                # Get the first polygon's outer ring
                coords = obj.geom.coords[0][0]
                # Convert from [lng, lat] to [lat, lng] for Leaflet
                return [[coord[1], coord[0]] for coord in coords]
            except (IndexError, TypeError):
                return []
        return []
    
    def create(self, validated_data):
        """Handle creation with geometry from request data"""
        # Get the geometry from the request (not in validated_data)
        request = self.context.get('request')
        geom_data = None
        
        if request and hasattr(request, 'data'):
            geom_data = request.data.get('geom')
        
        # Create the parcel instance without geom first
        parcel = Parcel(**validated_data)
        
        # Add geometry if provided
        if geom_data:
            try:
                # Convert the GeoJSON to a GEOS geometry
                geom_str = str(geom_data).replace("'", '"')
                geom = GEOSGeometry(geom_str)
                parcel.geom = geom
            except Exception as e:
                print(f"Error creating geometry: {e}")
        
        parcel.save()
        return parcel
    
    def update(self, instance, validated_data):
        """Handle update with geometry from request data"""
        # Update regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Get geometry from request
        request = self.context.get('request')
        if request and hasattr(request, 'data'):
            geom_data = request.data.get('geom')
            if geom_data:
                try:
                    geom_str = str(geom_data).replace("'", '"')
                    geom = GEOSGeometry(geom_str)
                    instance.geom = geom
                except Exception as e:
                    print(f"Error updating geometry: {e}")
        
        instance.save()
        return instance


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'parcel', 'amount', 'payment_date', 'reference']
    