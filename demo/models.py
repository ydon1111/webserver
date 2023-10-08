from django.db import models

# Create your models here.


class CSVData(models.Model):
    csv_file = models.FileField(upload_to='csv_files/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.csv_file.name