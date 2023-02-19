import threading

# shared variable
counter = 0

# create a lock object
lock = threading.Lock()

# thread function
def increment():
    global counter

    # acquire the lock
    lock.acquire()

    # increment the counter
    counter += 1

    # release the lock
    lock.release()

# create threads
threads = []
for i in range(10):
    t = threading.Thread(target=increment)
    threads.append(t)

# start threads
for t in threads:
    t.start()

# wait for threads to finish
for t in threads:
    t.join()

# print the final value of the counter
print("Counter value:", counter)