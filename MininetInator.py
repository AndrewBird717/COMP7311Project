import Mininet
import os

#os.Argv =[ path, nodecnt, k, alpha, nodefail]



if __name__ == "__main__":

    node_count = os.argv[1]
    for i in node_count:
        #start a go node and connect it to mininet