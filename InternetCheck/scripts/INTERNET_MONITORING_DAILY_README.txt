
Daily Internet Monitoring — Quick Start
======================================

1) Logging (one CSV per day)
   Run this every 5 minutes with cron:
     */5 * * * * /usr/bin/python3 /PATH/TO/test_internet_daily.py --host 8.8.8.8 --samples 5 --out /home/harish-r/InternetCheck/logs

   This writes files like:
     /home/harish-r/InternetCheck/logs/2025-08/latency_2025-08-08.csv

2) Plotting a given day's CSV
     /usr/bin/python3 /PATH/TO/plot_daily.py /home/harish-r/InternetCheck/logs/2025-08/latency_2025-08-08.csv

   Add a daily cron to render yesterday's plot:
     5 0 * * * /usr/bin/python3 /PATH/TO/plot_daily.py $(/usr/bin/find /home/harish-r/InternetCheck/logs -type f -name "latency_$(/bin/date -d 'yesterday' +\%F).csv") --out /home/harish-r/InternetCheck/plots/latency_$(/bin/date -d 'yesterday' +\%F).png

Notes:
- Files are grouped by month folder for tidiness (YYYY-MM).
- Timestamps are local time (ISO-8601).
- You can adjust --samples and --timeout to tune measurement duration.
