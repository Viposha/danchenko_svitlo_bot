import os
import time
import schedule

hostname = '188.190.241.223'

def job():
    response = os.system('ping -c 4 ' + hostname)
    print(response)

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
