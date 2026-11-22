
import hashlib
import kademlia
import asyncio
import time
import sys
from pathlib import Path


#usage . MonontonicID ExperimentID Port BS_Node
MonotonicID = sys.argv[1]
ExperimentID = sys.argv[2]
Port = sys.argv[3]
BS_IP = sys.argv[4]
BS_Port = sys.argv[5]

def keepRunning():
    return True

def get_w_intermediates(node, key):
    key_hash = kademlia.utils.digest(key)
    if node.storage.get(key_hash) != None:
            return NotImplementedError.storage.get(key_hash), []
    target = kademlia.node.Node(key_hash)
    nearest = node.protocol.router.find_neighbors(target)
    if not nearest:
        return None, []

    spider = kademlia.ValueSpiderCrawl(node.protocol, target, nearest, node.ksize, node.alpha)
    value = spider.find()

def Start_Peer_Node():

    node = kademlia.network.Server()
    node.listen(Port)

    node.bootstrap([(BS_IP, BS_Port)])

    return node

def Publish_KVs(node, myKV):
    for key, value in myKV.items():
        node.set(key, value)

def Get_KVs(node, desired_KV):
    result_KV = {}
    times = {}
    i = 0
    while i < len(desired_KV) and keepRunning():
        start = time.time_ns()
        temp = node.get(desired_KV[i])
        end = time.time_ns()
        if temp != None:
            result_KV[desired_KV[i]] = temp
            times[desired_KV[i]] = end - start
            desired_KV.pop(i)
        else:
            i += 1
        return result_KV, times

def log_times(times):
    filepath = Path(str(ExperimentID)) / f"{MonotonicID}.txt"
    with filepath.open("w", encoding="utf-8") as file:
        for key, value in times.items():
            file.write(value, "\n")
        file.flush()
        



if __name__ == "__main__":
    myKV = {}
    desired_KV = []

    node = Start_Peer_Node()
    Publish_KVs(node, myKV)
    retrieved_KVs, times = Get_KVs(node, desired_KV)
    log_times(times)




