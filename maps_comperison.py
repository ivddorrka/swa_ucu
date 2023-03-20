import hazelcast
import threading


def pessimistic_lock(nn):
    client = hazelcast.HazelcastClient(
    cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"],
    cluster_name="dev"
    )

    m_n = client.get_map("pessimistic-map").blocking()
    for k in range(nn-1000+1,nn+1):
        
        m_n.lock(k)
        try:
            m_n.put(k, k)
        finally:
            m_n.unlock(k)

    client.shutdown()

def optimistic_lock(nn):
    client = hazelcast.HazelcastClient(
    cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"],
    cluster_name="dev"
    )
    mm = client.get_map("optimistic-map").blocking()
    first = 0
    mm.lock(first)
    mm.put(first,first)
    mm.unlock(first)

    num_red  =0
    for i in range(nn):
        while True:
            try:
                value = mm.get(i)
                value += 1
                if mm.replace(i, value):
                    num_red += 1
                    break
            except TypeError:
                mm.put(i,i)
    print(f"Num replaces in each thread = {num_red}")
    client.shutdown()

def lock_less(nn):
    client = hazelcast.HazelcastClient(
    cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"],
    cluster_name="dev"
    )
    llm = client.get_map("lock-less-map")

    for k in range(nn-1000+1,nn+1):
        llm.put(k, k)
    
    client.shutdown()

if __name__ == "__main__":
    threads_1 = list()
    for i in range(3):
        x = threading.Thread(target=pessimistic_lock, args=(i*1000,))
        threads_1.append(x)
        x.start()

    for thread in threads_1:
        thread.join()
    
    threads_2 = list()
    for i in range(3):
        x = threading.Thread(target=optimistic_lock, args=(1000,))
        threads_2.append(x)
        x.start()

    for thread in threads_2:
        thread.join()
    
    threads_3 = list()
    for i in range(3):
        x = threading.Thread(target=lock_less, args=(i*1000,))
        threads_3.append(x)
        x.start()

    for thread in threads_3:
        thread.join()

