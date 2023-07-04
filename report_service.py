import datetime
import os

class ReportService:

    def __init__(self, log_directory):
        self.log_dir = log_directory

    def get_average_number_of_inferences_per_day(self):
        files = os.listdir(self.log_dir)
        counts = {}
        for f in files:
            try:
                date = self._extract_date_from_name(f)
            except Exception:
                continue
            counts[date] = 0
            with open(os.path.join(self.log_dir, f), 'r') as file:
                for line in file:
                    if 'STARTED BACKEND' in line:
                        counts[date] += 1
        return counts

    def _extract_date_from_name(self, file):
        return file.split('.')[0].split('_')[1]