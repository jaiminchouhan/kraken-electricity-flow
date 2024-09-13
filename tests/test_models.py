from django.test import TestCase

from ingestion.models import MpanCore, MeterReadingType, RegisterReading


class AdminSearchTest(TestCase):
    def setUp(self):
        MpanCore.objects.create(mpan_core_id='1234567890',
                                bsc_validation_status='V')
        MeterReadingType.objects.create(meter_id='MTR123', reading_type='B')
        RegisterReading.objects.create(meter_register_id='D14D02345',
                                       timestamp='2024-03-01 12:00:00', reading=16580.0,
                                       filename='file1')

    def test_search_mpan_core(self):
        mpan_core = MpanCore.objects.get(mpan_core_id="1234567890")

        self.assertEqual(mpan_core.bsc_validation_status, 'V')

    def test_search_meter_reading_type(self):
        reading_type = MeterReadingType.objects.get(meter_id="MTR123")

        self.assertEqual(reading_type.reading_type, 'B')

    def test_search_register_reading(self):
        reading = RegisterReading.objects.get(meter_register_id="D14D02345")

        self.assertEqual(reading.reading, 16580.0)
