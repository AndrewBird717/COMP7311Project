import hashlib
from kademlia.network import Server
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

async def Start_Peer_Node():

    node = Server()
    await node.listen(int(Port))

    await node.bootstrap([(BS_IP, int(BS_Port))])

    return node

async def Publish_KVs(node, myKV):
    for key, value in myKV.items():
        await node.set(key, value)

async def Get_KVs(node, desired_KV):
    result_KV = {}
    times = {}
    i = 0
    while i < len(desired_KV) and keepRunning():
        start = time.time_ns()
        temp = await node.get(desired_KV[i])
        end = time.time_ns()
        if temp != None:
            result_KV[desired_KV[i]] = temp
            times[desired_KV[i]] = end - start
            desired_KV.pop(i)
        else:
            i += 1
    return result_KV, times

def log_times(times):
    logdir = Path("ExperimentLogs") / str(ExperimentID)
    logdir.mkdir(parents=True, exist_ok=True)
    filepath = logdir / f"{MonotonicID}.txt"
    with filepath.open("w", encoding="utf-8") as file:
        for key, value in times.items():
            file.write(f"{value} \n")
        file.flush()
        

async def main():
    myKV = {}
    desired_KV = []

    node = await Start_Peer_Node()
    await Publish_KVs(node, myKV)
    retrieved_KVs, times = await Get_KVs(node, desired_KV)
    log_times(times)
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    print("UPUPUP")
    asyncio.run(main())
