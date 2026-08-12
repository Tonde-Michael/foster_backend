from django.contrib.gis.db import models

class Parcel(models.Model):
    id = models.AutoField(primary_key=True)
    geom = models.MultiPolygonField(srid=4326, blank=True, null=True)
    area = models.FloatField(blank=True, null=True, db_column='area')
    upn = models.CharField(max_length=25, blank=True, null=True, db_column='upn')
    plot_no = models.CharField(max_length=254, blank=True, null=True, db_column='plot_no')
    land_use = models.CharField(max_length=254, blank=True, null=True, db_column='land_use')
    street_nam = models.CharField(max_length=254, blank=True, null=True, db_column='street_nam')
    owner = models.CharField(max_length=254, blank=True, null=True, db_column='owner')
    registration_date = models.DateField(blank=True, null=True)
    year_registered = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'parcels'

    def __str__(self):
        return self.upn or f'Parcel {self.id}'


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    reference = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f'Payment {self.id} - {self.amount}'
