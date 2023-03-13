from threading import Thread
import threading
import time
import hazelcast


def set_data():
    # Connect to Hazelcast cluster.
    client = hazelcast.HazelcastClient()

    # Get or create the "distributed-map" on the cluster.
    distributed_map = client.get_map("distributed-map")

    # Put "key", "value" pair into the "distributed-map" and wait for
    # the request to complete.
    # distributed_map.set("key", "value").result()
    tasks = set()
    for i in range(1000):
        tasks.add(distributed_map.set(str(i), "value"))

    for t in tasks:
        t.result()
    # # Try to get the value associated with the given key from the cluster
    # # and attach a callback to be executed once the response for the
    # # get request is received. Note that, the set request above was
    # # blocking since it calls ".result()" on the returned Future, whereas
    # # the get request below is non-blocking.
    # get_future = distributed_map.get("key")
    # get_future.add_done_callback(lambda future: print(future.result()))

    # Do other operations. The operations below won't wait for
    # the get request above to complete.

    print("Map size:", distributed_map.size().result())

    # Shutdown the client.
    client.shutdown()


def check_data():
        # Connect to Hazelcast cluster.
    client = hazelcast.HazelcastClient()

    # Get or create the "distributed-map" on the cluster.
    distributed_map = client.get_map("distributed-map")

    # Try to get the value associated with the given key from the cluster
    # and attach a callback to be executed once the response for the
    # get request is received. Note that, the set request above was
    # blocking since it calls ".result()" on the returned Future, whereas
    # the get request below is non-blocking.
    tasks = set()
    for i in range(1000):
        tasks.add(distributed_map.get(str(i)))

    for t in tasks:
        if t.result() != "value":
            print("Map Corrupted!!")
            client.shutdown()
            return
    print("Map is fine!!")


    # Shutdown the client.
    client.shutdown()


def write_no_lock():
    print("Starting no lock write")
    # Connect to Hazelcast cluster.
    client = hazelcast.HazelcastClient()

    # Get or create the "distributed-map" on the cluster.
    no_lock_map = client.get_map("no-lock-map")
    key = "test_val"

    for i in range(1000):
        val = no_lock_map.get(key).result()
        # time.sleep(5)
        val += 1
        no_lock_map.put(key, val)

    print("Result value is", no_lock_map.get(key).result())


def write_pessimistic_lock():
    print("Starting pessimistic write")
    # Connect to Hazelcast cluster.
    client = hazelcast.HazelcastClient()

    # Get or create the "distributed-map" on the cluster.
    lock_map = client.get_map("lock-map")
    key = "test_val"

    for i in range(1000):
        lock_map.lock(key).result()
        try:
            value = lock_map.get(key).result()
            value += 1
            lock_map.put(key, value).result()
        finally:
            lock_map.unlock(key)

    print("Result value is", lock_map.get(key).result())


def write_optimistic_lock():
    print("Starting optimistic write")
    # Connect to Hazelcast cluster.
    client = hazelcast.HazelcastClient()

    optimistic_map = client.get_map("optimistic-map")
    key = "test_val"

    for i in range(100):
        while True:
            oldValue = optimistic_map.get( key ).result()
            new_value = oldValue +1
            if optimistic_map.replace_if_same( key, oldValue, new_value ).result():
                break

    print("Result value is", optimistic_map.get(key).result())


def write_async(func, map_name):
    client = hazelcast.HazelcastClient()
    map = client.get_map(map_name)
    map.put("test_val", 0).result()

    th1 = Thread(target=func)
    th2 = Thread(target=func)
    th3 = Thread(target=func)
    th1.start()
    th2.start()
    th3.start()
    th1.join()
    th2.join()
    th3.join()
    

def start_queue_writer(sleep_interval):
    client = hazelcast.HazelcastClient()

    q = client.get_queue("tasks")
    print("strated queue writer")
    counter = 0
    while True:
        time.sleep(sleep_interval)
        counter += 1
        print("Producer: adding task #" + str(counter))
        try:
            if not q.add("This is task #" + str(counter)).result():
                raise Exception("Can not add task #{}!!!".format(counter))
        except Exception as e:
            print(e)
            continue
        print("Task #{} added".format(counter))
    
def start_queue_reader():
    client = hazelcast.HazelcastClient()
    q = client.get_queue("tasks")
    print("strated queue reader")   
    while True:
        t = q.take().result()
        print("Consumer " + str(threading.get_ident()) + ": " + str(t))


def start_writer_first(num_of_readers):
    w_th = Thread(target=start_queue_writer, args=[1])
    readers = []
    for r in range(num_of_readers):
        readers.append(Thread(target=start_queue_reader))

    w_th.start()
    time.sleep(5)
    for reader in readers:
        reader.start()
    w_th.join()


def start_reader_first():
    w_th = Thread(target=start_queue_writer, args=[5])
    r1_th = Thread(target=start_queue_reader)
    r2_th = Thread(target=start_queue_reader)

    r1_th.start()
    time.sleep(5)
    w_th.start()
    r2_th.start()
    w_th.join()


def start_only_writer():
    start_queue_writer(1)


def start_only_reader():
    start_queue_reader()


# set_data()
# check_data()

# write_async(write_no_lock, "no-lock-map")
# write_async(write_pessimistic_lock, "lock-map")
# write_async(write_optimistic_lock, "optimistic-map")

start_writer_first(2)

