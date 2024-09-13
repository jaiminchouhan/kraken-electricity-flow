import os
from datetime import datetime

from django.core.management.base import BaseCommand

from ingestion.models import MpanCore, MeterReadingType, RegisterReading


class Command(BaseCommand):
    help = 'Import electricity meter readings from a UFF files in a directory'

    def add_arguments(self, parser):
        parser.add_argument('directory_path', type=str,
                            help='The path to the directory')

    def handle(self, *args, **kwargs):
        directory_path = kwargs['directory_path']
        # Log an error if directory not found
        if not os.path.isdir(directory_path):
            self.stdout.write(self.style.ERROR(f"Directory {directory_path} not found"))
            return

        # Process each file in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith('.uff'):
                file_path = os.path.join(directory_path, filename)
                self.process_file(file_path)

    def process_file(self, file_path):
        self.stdout.write(self.style.SUCCESS(f"Processing file: {file_path}"))

        # Check if file exists
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File {file_path} not found"))
            return

        with open(file_path, 'r') as file:
            meter_type = None
            mpan_core = None

            for line in file:
                parts = line.strip().split('|')

                # MpanCore object creation
                if parts[0] == '026':
                    mpan = parts[1]
                    bsc_validation_status = parts[2] if len(parts) > 2 else "Unknown"

                    mpan_core, created = MpanCore.objects.get_or_create(
                        mpan_core_id=mpan,
                        defaults={'bsc_validation_status': bsc_validation_status}
                    )

                    self.stdout.write(self.style.SUCCESS(
                        f"Found MPAN: {mpan}, Status: {bsc_validation_status}"))

                elif parts[0] == '028':
                    # MeterReadingType object creation
                    if mpan_core:
                        meter_id = parts[1]
                        reading_type = parts[2] if len(parts) > 2 else "Unknown"

                        meter_type, created = MeterReadingType.objects.get_or_create(
                            meter_id=meter_id,
                            defaults={'reading_type': reading_type}
                        )

                        if not created:
                            # Update reading_type if the record already exists
                            if meter_type.reading_type != reading_type:
                                meter_type.reading_type = reading_type
                                meter_type.save()

                        self.stdout.write(
                            self.style.SUCCESS(f"Found meter: {meter_id}"))

                elif parts[0] == '030':
                    # RegisterReading object creation
                    if meter_type:
                        reading_type = parts[1]
                        timestamp = datetime.strptime(parts[2], "%Y%m%d%H%M%S")
                        reading_value = float(parts[3])
                        reset_timestamp = None
                        reset_number = None
                        reading_flag = parts[4] if len(parts) > 4 else None
                        reading_method = parts[5] if len(parts) > 5 else None

                        # Check for existing RegisterReading object
                        existing_reading = RegisterReading.objects.filter(
                            meter_register_id=meter_id,
                            timestamp=timestamp,
                            reading=reading_value,
                            md_reset_timestamp=reset_timestamp,
                            md_reset_number=reset_number,
                            reading_flag=reading_flag,
                            reading_method=reading_method
                        ).first()

                        if not existing_reading:
                            # Saving register reading only if it does not already exist
                            RegisterReading.objects.create(
                                meter_register_id=meter_id,
                                timestamp=timestamp,
                                reading=reading_value,
                                md_reset_timestamp=reset_timestamp,
                                md_reset_number=reset_number,
                                reading_flag=reading_flag,
                                reading_method=reading_method,
                                filename=os.path.basename(file_path)
                            )
                            self.stdout.write(self.style.SUCCESS(
                                f"Stored reading for {meter_id} at {timestamp}: {reading_value}"))
                        else:
                            self.stdout.write(self.style.WARNING(
                                f"Reading for {meter_id} at {timestamp} already exists, skipping."))
