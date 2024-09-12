from django.contrib import admin
from .models import MpanCore, MeterReadingType, RegisterReading


@admin.register(MpanCore)
class MpanCoreAdmin(admin.ModelAdmin):
    search_fields = ['mpan_core_id']
    list_filter = ['bsc_validation_status']


@admin.register(MeterReadingType)
class MeterReadingTypeAdmin(admin.ModelAdmin):
    search_fields = ['meter_id']
    list_filter = ['reading_type']


@admin.register(RegisterReading)
class RegisterReadingAdmin(admin.ModelAdmin):
    search_fields = ['meter_register_id', 'filename']
    list_filter = ['timestamp']
