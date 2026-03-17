import threading, time, random

spaces = threading.Semaphore(100)
items  = threading.Semaphore(0)
mutex  = threading.Semaphore(1)

buffer = []
buffer_lock = threading.Lock()


def producer_BROKEN(id):
    for _ in range(3):
        p1, p2 = f"P{id}-A", f"P{id}-B"
        buffer.append(p1)
        time.sleep(0.01)          # simulate interleaving
        buffer.append(p2)
        print(f"[BROKEN] Producer {id} placed {p1},{p2} | buffer={buffer}")

def consumer_BROKEN():
    time.sleep(0.05)
    while len(buffer) >= 2:
        p1 = buffer.pop(0)
        p2 = buffer.pop(0)
        print(f"[BROKEN] Consumer packaged {p1},{p2}")

# ── SOLUTION (with semaphores) ──
def producer(id):
    for _ in range(3):
        p1, p2 = f"P{id}-A", f"P{id}-B"
        spaces.acquire()          # need 2 free slots
        spaces.acquire()
        mutex.acquire()           # atomically place the pair
        buffer.append(p1)
        buffer.append(p2)
        mutex.release()
        items.release()           # 2 new particles available
        items.release()
        print(f"[OK] Producer {id} placed {p1},{p2} | buffer size={len(buffer)}")

def consumer():
    for _ in range(6):           
        items.acquire()           
        items.acquire()
        with buffer_lock:
            p1 = buffer.pop(0)
            p2 = buffer.pop(0)
        spaces.release()
        spaces.release()
        print(f"[OK] Consumer packaged {p1},{p2}")

# ── Run PROBLEM first ──
print("=== PROBLEM (no semaphores) ===")
threads = [threading.Thread(target=producer_BROKEN, args=(i,)) for i in range(2)]
threads.append(threading.Thread(target=consumer_BROKEN))
for t in threads: t.start()
for t in threads: t.join()

# reset
buffer.clear()
print("\n=== SOLUTION (with semaphores) ===")
threads = [threading.Thread(target=producer, args=(i,)) for i in range(2)]
threads.append(threading.Thread(target=consumer))
for t in threads: t.start()
for t in threads: t.join()