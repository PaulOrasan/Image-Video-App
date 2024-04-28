import datetime
import os

from predictions_service import PredictionService
from user_service import UserService


class ReportService:

    def __init__(self, log_directory, prediction_service: PredictionService, user_service: UserService):
        self.log_dir = log_directory
        self.ps = prediction_service
        self.us = user_service

    def get_total_number_of_inferences_per_day(self):
        today = datetime.datetime.today()
        today_str = today.strftime('%Y-%m-%d')
        counts = {}
        while True:
            preds = self.ps.find_predictions_by_day(today_str)
            if len(preds) == 0:
                return counts
            counts[today_str] = len(preds)
            today = today - datetime.timedelta(days=1)
            today_str = today.strftime('%Y-%m-%d')

    def get_daily_number_and_total(self):
        users = self.us.find_all_users()
        preds = {u.id: self.ps.find_predictions(u.id) for u in users}
        total = []
        for u in users:
            today = datetime.datetime.today()
            today_str = today.strftime('%Y-%m-%d')
            while True:
                pr = [p for p in preds[u.id] if today_str in str(p.request_time)]
                if len(pr) == 0:
                    break
                total.append([len(pr), len(preds[u.id])])
                today = today - datetime.timedelta(days=1)
                today_str = today.strftime('%Y-%m-%d')
        return total

    def get_latency(self):
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