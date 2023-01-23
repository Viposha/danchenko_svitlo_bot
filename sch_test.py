import os
import time
import schedule

hostname = '188.190.241.223'
result = [0]

def switch():
    response = os.system('ping -c 4 ' + hostname)
    result.append(response)
    print(result)
    if result[0] == 0 and result[1] == 256:
        print('Світло вимкнули')
    elif result[0] == 256 and result[1] == 0:
        print('Світло ввімкнули')
    else:
        print('працює')
    result.pop(0)
    print(result)

schedule.every(10).seconds.do(switch)

while True:
    schedule.run_pending()
    time.sleep(1)
