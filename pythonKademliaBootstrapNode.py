import kademlia
import asyncio
import sys
from pathlib import Path


#usage . MonontonicID ExperimentID Port BS_Node
MonotonicID = sys.argv[1]
ExperimentID = sys.argv[2]
Port = sys.argv[3]


async def Start_Peer_Node():
    node = kademlia.network.Server()
    node.listen(int(Port))

    if len(sys.argv) > 4:
        BS_IP = sys.argv[4]
        BS_Port = sys.argv[5]
        node.bootstrap([(BS_IP, int(BS_Port))])

    return node

async def main():
    node = await Start_Peer_Node()

if __name__ == "__main__":
    asyncio.run(main())



