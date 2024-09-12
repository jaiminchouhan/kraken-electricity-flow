import os
from django.core.management.base import BaseCommand
from ingestion.models import MpanCore, MeterReadingType, RegisterReading
from datetime import datetime


class Command(BaseCommand):
    help = 'Import electricity meter readings from a UFF file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the UFF file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File {file_path} not found"))
            return

        with open(file_path, 'r') as file:
            meter = None

            for line in file:
                parts = line.strip().split('|')

                if parts[0] == '026':
                    # This is an MPAN or Meter ID line
                    mpan = parts[1]
                    mpan_core, created = MpanCore.objects.get_or_create(
                        mpan_core_id=mpan)
                    self.stdout.write(self.style.SUCCESS(f"Found MPAN: {mpan}"))

                elif parts[0] == '028':
                    # This is a meter serial number line
                    if mpan_core:
                        meter_id = parts[1]
                        meter_type, created = MeterReadingType.objects.get_or_create(
                            meter_id=meter_id)
                        self.stdout.write(
                            self.style.SUCCESS(f"Found meter: {meter_id}"))

                elif parts[0] == '030':
                    # This is a meter reading line
                    if meter_type:
                        reading_type = parts[1]
                        timestamp = datetime.strptime(parts[2], "%Y%m%d%H%M%S")
                        reading_value = float(parts[3])
                        reset_timestamp = None
                        reset_number = None
                        reading_flag = parts[4] if len(parts) > 4 else None
                        reading_method = parts[5] if len(parts) > 5 else None

                        # Saving register reading
                        RegisterReading.objects.create(
                            meter_register_id=meter_id,
                            timestamp=timestamp,
                            reading=reading_value,
                            md_reset_timestamp=reset_timestamp,
                            md_reset_number=reset_number,
                            reading_flag=reading_flag,
                            reading_method=reading_method,
                            filename=os.path.basename(file_path)  # Store the filename
                        )
                        self.stdout.write(self.style.SUCCESS(
                            f"Stored reading for {meter_id} at {timestamp}: {reading_value}"))
