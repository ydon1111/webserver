from django.db import models

# Create your models here.
class CSVData(models.Model):
    csv_info = models.FloatField(default=0.0)
    csv_file = models.FileField(upload_to='PPI/',null=True)