import logging
import threading
import time
import random

def thread_function(name):
    t0 = time.time()
    tSleep = random.randint(1,5)
    logging.info(f"Thread {name}  : starting,   sleep_for: {tSleep} sec(s)")
    time.sleep(tSleep)
    logging.info(f"Thread {name}  : finishing,  took: {round((time.time()-t0),2)} sec(s)")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = []
    numThreads = 10
    logging.info("Main    : before creating threads")
    for i in range(numThreads):
        threads.append(threading.Thread(target=thread_function, args=(i+1,)))
    logging.info("Main    : before running threads")
    for th in threads:
        th.start()
    logging.info("Main    : wait for the threads to finish")
    logging.info("Main    : all done")