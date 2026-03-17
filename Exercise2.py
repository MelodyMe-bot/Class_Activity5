import threading

# Semaphores: a=1 lets P1 start, b=0 blocks P2, c=0 blocks P3
a = threading.Semaphore(1)
b = threading.Semaphore(0)
c = threading.Semaphore(0)

# ── PROBLEM (no semaphores): output is random ──
def process1_BROKEN(): print("H", end=""); print("E", end="")
def process2_BROKEN(): print("L", end="")
def process3_BROKEN(): print("O", end="")

print("=== PROBLEM (no semaphores) — random output ===")
for _ in range(5):
    threads = [
        threading.Thread(target=process1_BROKEN),
        threading.Thread(target=process2_BROKEN),
        threading.Thread(target=process3_BROKEN),
    ]
    for t in threads: t.start()
    for t in threads: t.join()
    print()  # newline per run

# ── SOLUTION ──
def process1():
    a.acquire()         # wait for permission to start
    print("H", end="")
    print("E", end="")
    b.release()         # signal Process 2 that HE is done

def process2():
    b.acquire()         # wait until after HE
    print("L", end="")
    b.release()         # second L (loops back, re-signals itself ONCE more)
    b.acquire()
    print("L", end="")
    c.release()         # signal Process 3 that LL is done

def process3():
    c.acquire()         # wait until after HELL
    print("O", end="")
    print()             # newline

print("\n=== SOLUTION (with semaphores) — always HELLO ===")
for _ in range(5):
    # Reset semaphores each run
    a = threading.Semaphore(1)
    b = threading.Semaphore(0)
    c = threading.Semaphore(0)
    threads = [
        threading.Thread(target=process1),
        threading.Thread(target=process2),
        threading.Thread(target=process3),
    ]
    for t in threads: t.start()
    for t in threads: t.join()