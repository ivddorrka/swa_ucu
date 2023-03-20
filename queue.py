import hazelcast
import threading


def writing(queue_size):
    client = hazelcast.HazelcastClient(
    cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"],
    cluster_name="dev"
    )
    queue = client.get_queue("queue_1").blocking()
    for i in range(queue_size):
        queue.offer(i)
        print(f"Offering i = {i}")
    client.shutdown()
    

def reading(queue_size):
    client = hazelcast.HazelcastClient(
    cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"],
    cluster_name="dev"
    )
    queue = client.get_queue("queue_1").blocking()
    while True:
        i = queue.take()
        print(f"Taking i = {i}")
        if i == queue_size-1:
            queue.put(queue_size-1)
            break
    client.shutdown()


if __name__ == "__main__":
    client = hazelcast.HazelcastClient(
    cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"],
    cluster_name="dev"
    )
    queue = client.get_queue("queue_1").blocking()
    queue.clear()
    que_size = 10
    
    writing_thread1 =  threading.Thread(target=writing, args=(que_size,))
    reading_thread1 =  threading.Thread(target=reading, args=(que_size,))
    reading_thread2 =  threading.Thread(target=reading, args=(que_size,))

    writing_thread1.start()
    reading_thread1.start()
    reading_thread2.start()

    writing_thread1.join()
    reading_thread1.join()
    reading_thread2.join()
    client.shutdown()


