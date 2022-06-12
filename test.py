
# SuperFastPython.com
# example of returning a value from a thread
from time import sleep
from threading import Thread
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
# custom thread
class CustomThread(Thread):
    # constructor
    def __init__(self, func, sec):
        # execute the base constructor
        Thread.__init__(self)
        # set a default value
        self.value = None
        self.sec=sec
        self.func=func
 
    # function executed in a new thread
    def run(self):
        # block for a moment
        print("run", self.sec)        
        # store data in an instance variable
        # self.value = 'Hello from a new thread'
        self.value = self.func

def test(num):
    seconds=5-num
    sleep(seconds)
    print("hi", num)
    return num

def runner():
    nums=[1, 2, 3, 4, 5]
    results=[]
    threads= []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for num in nums:
            threads.append(executor.submit(test, num))
            
        for task in as_completed(threads):
            results.append(task.result())
            print(task.result())
    return results 
       
data=runner()
print(data)

nums=[1, 2, 3, 4, 5]
threads=[]

# for num in nums:
#     thread = CustomThread(test(num), num) # create a new thread
#     threads.append(thread)
#     thread.start()# start the thread

# for thread in threads:
#     thread.join() # wait for the thread to finish
#     print(thread.value)


# get the value returned from the thread
