
import Mininet
import os
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


def Start_Peer_Node():
    node = kademlia.network.Server()
    node.listen(Port)

    if len(sys.argv) > 4:
        BS_IP = sys.argv[4]
        BS_Port = sys.argv[5]
        node.bootstrap([(BS_IP, BS_Port)])

    return node

if __name__ == "__main__":
    node = Start_Peer_Node()




