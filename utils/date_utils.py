import datetime

import pandas as pd


class ConvertDate:
    minute = 60
    hour = 60
    day_hours = 24
    year_days = 365

    def convert_display_date(self, target_datetime):
        datetime_now = datetime.datetime.now()
        subtracted_second = (datetime_now - target_datetime).total_seconds()

        if subtracted_second < self.minute:
            return '数秒前'
        elif subtracted_second // self.minute < self.hour:
            minutes = int(subtracted_second // self.minute)
            return str(minutes) + '分前'
        elif subtracted_second <= self.minute * self.hour * self.day_hours:
            hours = int(subtracted_second // (self.minute * self.hour))
            return str(hours) + '時間前'
        elif subtracted_second <= self.minute * self.hour * self.day_hours * self.year_days:
            days = int(subtracted_second //
                       (self.minute * self.hour * self.day_hours))
            return str(days) + '日前'
        elif subtracted_second <= self.minute * self.hour * self.day_hours * self.year_days:
            years = int(subtracted_second // (self.minute *
                        self.hour * self.day_hours * self.year_days))
            return str(years) + '年前'

    def convert_datetime_duration(timestamp, duration):
        converted_datetime = ''
        if duration == '1M':
            converted_datetime = pd.to_datetime(
                datetime.datetime.strftime(timestamp, '%Y-%m-%d %H:%M'))
        elif duration == '5M':
            format_datetime = datetime.datetime.strftime(
                timestamp, '%Y-%m-%d %H:%M')
            if int(format_datetime[-1:]) < 5:
                converted_datetime = pd.to_datetime(format_datetime[:-1] + '0')
            else:
                converted_datetime = pd.to_datetime(format_datetime[:-1] + '5')
        elif duration == '10S':
            format_datetime = datetime.datetime.strftime(
                timestamp, '%Y-%m-%d %H:%M:%S')
            second = (int(format_datetime[-2:]) // 10) * 10
            formation_date = format_datetime[:-2] + str(second)
            converted_datetime = pd.to_datetime(formation_date)
        return converted_datetime
