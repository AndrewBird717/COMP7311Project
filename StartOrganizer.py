import json
import subprocess
import sys
import random
import hashlib
import time
from pathlib import Path
from mininet.net import Mininet
from mininet.node import OVSSwitch

PYTHON = ".venv/bin/python"

host_count = 40
BS_count = 1
Alpha = int(sys.argv[1])#3
BucketSize = int(sys.argv[2])#12
HeldKeysPerNode = int(sys.argv[3])#12
DesiredKeysPerNode = int(sys.argv[4])#100
KeyRange = int(sys.argv[5])#250
UpPercentage = int(sys.argv[6])#100

AllHeldKeys = set()

# Add as many hosts as you want
def Get_HeldKeys_JSON():#Deprec
    res = {}
    for i in range(HeldKeysPerNode):
        temp = random.randint(1, KeyRange)
        res[temp] = hashlib.sha1(str(temp).encode()).hexdigest()
    json_d = json.dumps(res)
    return json_d

def Get_DesiredKeys_JSON():#Deprec
    res = {}
    for i in range(HeldKeysPerNode):
        temp = random.randint(1, KeyRange)
        res[temp] = None
    json_d = json.dumps(res)
    return json_d

def GetHeldDict():
    res = {}
    for i in range(HeldKeysPerNode):
        temp = random.randint(1, KeyRange)
        while temp in res:
            temp = random.randint(1, KeyRange)
        AllHeldKeys.add(temp)
        res[temp] = hashlib.sha1(str(temp).encode()).hexdigest()
    return res
        

def GetDesiredDict(HeldDict):
    res = {}
    for i in range(DesiredKeysPerNode):
        temp = random.randint(1, KeyRange)
        while temp in res or temp in HeldDict or temp not in AllHeldKeys:
            temp = random.randint(1, KeyRange)
        res[temp] = None
    return res



def GetKeysJSON():
    HeldDict = GetHeldDict()
    DesiredDict = GetDesiredDict(HeldDict)
    HeldJSON = json.dumps(HeldDict)
    DesiredJSON = json.dumps(DesiredDict)
    return HeldJSON, DesiredJSON


if __name__ == "__main__":
    #print(Get_DesiredKeys_JSON())
    #print(Get_HeldKeys_JSON())
    #input("stop")

    net = Mininet(
        topo=None,
        build=False,
        controller=None,
        switch=OVSSwitch
    )

    # Create one switch
    switch = net.addSwitch("s1", failMode="standalone")



    for i in range(host_count + BS_count):
        host = net.addHost(f"h{i+1}")
        net.addLink(host, switch)
        print(f"made {i}th")

    # Start network
    net.build()
    net.start()
    print("Created hosts:", [h.name for h in net.hosts])

    for host in net.hosts:
        print(host.name, host.IP())
    try:

        processes = {}

        ExperimentID = time.time()

        for i, host in enumerate(net.hosts):
            if i < BS_count:
                if i == 0:
                    processes[i] = host.popen(f"{PYTHON} pythonKademliaBootstrapNode.py {i} {ExperimentID} 8000")
                    time.sleep(1)
                    continue
                BS_IP = net.hosts[i-1].IP()
                processes[i] = host.popen(f"{PYTHON} pythonKademliaBootstrapNode.py {i} {ExperimentID} 8000 {BS_IP} 8000")
                time.sleep(1)
            else:
                Held, Desired = GetKeysJSON()
                BS_IP = net.hosts[random.randint(0, BS_count-1)].IP()
                processes[i] = host.popen([
                    PYTHON, "pythonKademliaNode.py", str(i), str(ExperimentID),
                    "8000", BS_IP, "8000",
                    Held, Desired, str(Alpha), str(BucketSize), UpPercentage], stderr=None)        
                time.sleep(2)

        for i, process in processes.items():
            print(
                f"Node {i}: PID={process.pid}, "
                f"Exit code={process.poll()}"
            )
        input("Hit enter to end (All nodes have been created)...")
    except KeyboardInterrupt:
        print("\nStopping experiment...", flush=True)
    finally:
        for process in processes.values():
            if process.poll() is None:
                process.terminate()

        for process in processes.values():
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

    net.stop()