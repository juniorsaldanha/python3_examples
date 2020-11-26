import time
import asyncio

def is_prime(num):
    # Function to return if num is prime number or not
    return not any(num//i == num/i for i in range(num-1, 1, -1))

async def get_highest_prime(num):
    # Function to return the highest prime number from 0 to N
    print(f"Highest prime below {num}")
    for i in range(num-1, 0, -1):
        if is_prime(i):
            print(f"⮞ Highest prime below {num} is {i}")
            return i
        await asyncio.sleep(0.01)
    return None

async def start():
    # Function to start three async functions
    time0 = time.time()
    await asyncio.wait([
        get_highest_prime(1000000),
        get_highest_prime(100000),
        get_highest_prime(10000)
    ])
    print(f"Took {round(1000*(time.time()-time0),2)} ms")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    loop.close()