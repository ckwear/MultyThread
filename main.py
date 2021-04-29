# description :
# 100개의 쓰레드 중에 3개의 쓰레드만 작업이 가능하다.
import itertools
all_parmas = []
def init():
    global all_parmas
    param_grid = {
        'holidays_prior_scale' : list(range(0,10))[1:],
        'weekly_seasonality' : list(range(0,10))[1:],
        # 'fourier_order' : list(range(0,21))[1:],
        'yearly_seasonality': [False],
        'daily_seasonality': [False],
        'seasonality_mode' : ['additive'],
        'using_state': [False]
    }
    # Generate all combinations of parameters
    all_parmas = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]


init()

from threading import Lock
import threading

sem = threading.Semaphore(3)      # 세마포 객체 생성, 3개의 쓰레드로 제한

class RestrictedArea(threading.Thread):
    def run(self):
        print(all_parmas)
        global all_parmas
        for parmas in all_parmas:
            msg = 'Threading Semaphore TEST : %s' % self.getName()
            try:
                sem.acquire()
                Lock.acquire()
                print(msg)
                if parmas['using_state'] == False:
                    parmas['using_state'] = True
                    print(parmas)
            finally:
                Lock.release()
                sem.release()

threads = []

for i in range(100):
    threads.append(RestrictedArea())

for th in threads:
    th.start()          # 쓰레드 시작

for th in threads:
    th.join()           # 종료대기

print('Finish All Threading ')