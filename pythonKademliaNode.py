import hashlib
from kademlia.network import Server
import asyncio
import time
import sys
from pathlib import Path
import json


#usage . MonontonicID ExperimentID Port BS_Node HeldKeys DesiredKeys
MonotonicID = sys.argv[1]
ExperimentID = sys.argv[2]
Port = sys.argv[3]
BS_IP = sys.argv[4]
BS_Port = sys.argv[5]
HeldKeys = json.loads(sys.argv[6])
DesiredKeys = json.loads(sys.argv[7])

def keepRunning():
    return True

async def Start_Peer_Node():

    node = Server()
    await node.listen(int(Port))

    await node.bootstrap([(BS_IP, int(BS_Port))])

    return node

def log_times(times):
    logdir = Path("ExperimentLogs") / str(ExperimentID)
    logdir.mkdir(parents=True, exist_ok=True)
    filepath = logdir / f"{MonotonicID}.txt"
    with filepath.open("w", encoding="utf-8") as file:
        file.write("Start \n")
        for key, value in times.items():
            file.write(f"{value} \n")
        file.flush()

def log_time(time):
    logdir = Path("ExperimentLogs") / str(ExperimentID)
    logdir.mkdir(parents=True, exist_ok=True)
    filepath = logdir / f"{MonotonicID}.txt"
    with filepath.open("w", encoding="utf-8") as file:
        file.write(f"{time} \n")
        file.flush()   

async def Publish_KVs(node, myKV):

    for key, value in myKV.items():
        new_val = hashlib.sha1(str(key).encode("utf-8")).hexdigest()
        await node.set(key, new_val)

async def Get_KVs(node, desired_KV):
    result_KV = {}
    times = {}
    i = 0
    while (i < len(desired_KV) and keepRunning) or keepRunning:
        start = time.time_ns()
        temp = await node.get(desired_KV[i])
        end = time.time_ns()
        if temp != None:
            result_KV[desired_KV[i]] = temp
            times[desired_KV[i]] = end - start
            desired_KV.pop(i)
            log_time(end- start)
        else:
            i += 1
    return result_KV, times


        

async def main():

    node = await Start_Peer_Node()
    await Publish_KVs(node, HeldKeys)
    retrieved_KVs, times = await Get_KVs(node, DesiredKeys)
    log_times(times)
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    print("UPUPUP")
    asyncio.run(main())
