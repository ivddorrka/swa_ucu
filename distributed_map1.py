import hazelcast
import asyncio


async def async_put_general(map_n, i, str_i):
    map_n.put(i, str_i)


def map_nolocks(map_n, n_values):
    for i in range(n_values):
        asyncio.run(async_put_general(map_n ,i,str(i)))


if __name__ == "__main__":
    client = hazelcast.HazelcastClient(
    cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"],
    cluster_name="dev"
    )

    map_n1 = client.get_map("map_10")
    n_vals = 1000
    map_nolocks(map_n1, n_vals)
    client.shutdown()
