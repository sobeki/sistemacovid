import time
from apscheduler.schedulers.background import BackgroundScheduler
from update_data import getDataFiles
# from testCron import test
scheduler = BackgroundScheduler()
scheduler.add_job(getDataFiles, 'interval', hours=6)
# scheduler.add_job(test, 'interval', seconds=3)
scheduler.start()

try:
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()