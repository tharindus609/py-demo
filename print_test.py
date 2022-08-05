import time

limit = 10
print("Test")
for x in range(limit):
    print("{0} out of {1}".format(x, limit), end='\r', flush=True)
    if x+1 == limit:
        print()
    time.sleep(1)
