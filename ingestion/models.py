from django.db import models


class MpanCore(models.Model):
    mpan_core_id = models.CharField(max_length=50, unique=True)
    bsc_validation_status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.mpan_core_id} - {self.bsc_validation_status}"


class MeterReadingType(models.Model):
    meter_id = models.CharField(max_length=50, unique=True)
    reading_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.meter_id} - {self.reading_type}"


class RegisterReading(models.Model):
    meter_register_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    reading = models.FloatField()
    md_reset_timestamp = models.DateTimeField(null=True, blank=True)
    md_reset_number = models.FloatField(null=True, blank=True)
    reading_flag = models.CharField(max_length=50, null=True, blank=True)
    reading_method = models.CharField(max_length=50, null=True, blank=True)
    filename = models.CharField(max_length=255)

    def __str__(self):
        return f"Reading for {self.meter_register_id} at {self.timestamp}: {self.reading}"
