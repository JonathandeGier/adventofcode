from collections import Counter, defaultdict
from datetime import datetime
from itertools import groupby
from colorama import Fore
from dateutil.relativedelta import relativedelta
from Table import Table
from time import time

class Day4(Table):

    def __init__(self):
        self.day = 4
        self.title = "Repose Record"
        self.input = self.getInput(self.day)

    def get_logs(self):
        logs = []
        for line in self.input.splitlines():
            datetime_string, action = line.split('] ')
            datetime_string = datetime_string[1:]

            time = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
            time = time + relativedelta(years=500)  # the timestamp function gives error for 1518, so shift everything to the current year

            logs.append((time, action.split(' ')[1]))

        sorted_logs = sorted(logs, key=lambda x: x[0].timestamp())

        grouped_logs = defaultdict(lambda: [])
        for log in sorted_logs:
            date = (log[0].month, log[0].day)

            if log[1][0] == '#':
                if date in grouped_logs:
                    tmp = log[0] + relativedelta(days=1)
                    date = (tmp.month, tmp.day)
                
            grouped_logs[date].append(log)


        dense_logs = {}
        for date in grouped_logs:
            log = grouped_logs[date]
            dense_log = (int(log[0][1][1:]), [])

            for i in range(1, len(log), 2):
                dense_log[1].append((log[i][0].minute, log[i+1][0].minute))

            dense_logs[date] = dense_log
            
        return dense_logs

    def solve(self):
        start_time = time()

        logs = self.get_logs()

        # Strategy 1:
        # calculate the minutes asleep per guard
        sleep = defaultdict(lambda: 0)
        for day in logs:
            log = logs[day]
            guard = log[0]

            day_sleep = 0
            for session in log[1]:
                day_sleep += (session[1] - session[0])
            sleep[guard] += day_sleep

        # get the guard who sleeps the most
        max_sleep = max(sleep.values())
        max_sleep_guard = [guard for guard, value in sleep.items() if value == max_sleep][0]
        
        # calculate which minute the guard sleeps the most
        guard_logs = [log for log in logs.values() if log[0] == max_sleep_guard]
        minutes_asleep = []
        for day_logs in guard_logs:
            for session in day_logs[1]:
                minutes_asleep.extend(range(session[0], session[1]))

        minute_count = Counter(minutes_asleep)
        sleep_minute = minute_count.most_common()[0][0]

        part1 = max_sleep_guard * sleep_minute

        # Strategy 2:
        guards = set([log[0] for _, log in logs.items()])
        
        part2 = ''
        most_common_count = 0
        for guard in guards:
            guard_logs = [log for log in logs.values() if log[0] == guard]
            minutes_asleep = []
            for day_logs in guard_logs:
                for session in day_logs[1]:
                    minutes_asleep.extend(range(session[0], session[1]))

            minute_count = Counter(minutes_asleep)
            most_common = minute_count.most_common()
            if len(most_common) == 0:
                continue

            most_common = most_common[0]

            if most_common[1] > most_common_count:
                most_common_count = most_common[1]
                part2 = guard * most_common[0]


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day4()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
