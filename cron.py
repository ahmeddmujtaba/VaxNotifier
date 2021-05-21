from crontab import CronTab

cron = CronTab(user='mujtaa3')
job = cron.new(command = "python3 getTweetsSince.py")
job.minute.every(2)

