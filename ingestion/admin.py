from django.contrib import admin
from .models import MpanCore, MeterReadingType, RegisterReading

admin.site.register(MpanCore)
admin.site.register(MeterReadingType)
admin.site.register(RegisterReading)