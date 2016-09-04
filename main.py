from sky_picker import SkyPickerApi
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=5)
def sched_job():
    call = SkyPickerApi()
    call.save_lowest_price()
    return True

sched.start()
