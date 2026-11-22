package main

import(
	"fmt"
	"math/rand/v2"
	"os"

	//"github.com/ipfs/go-cid"
 "github.com/libp2p/go-libp2p"
 //dht "github.com/libp2p/go-libp2p-kad-dht"
 "github.com/libp2p/go-libp2p/core/host"
 //"github.com/libp2p/go-libp2p/core/peer"
)

Args := os.Args[1:]
const BootstrapNodeCount int = 5
var bootstrap_nodes = [BootstrapNodeCount]host.Host{}

func make_bootstrap_nodes(){
	bootstrap_nodes[0], _ = libp2p.New()
	
	for i := 1; i < BootstrapNodeCount; i++ {
		bootstrap_nodes[i], _ = libp2p.New()
	}
}

func get_random_bootstrap_node() host.Host {
	var temp_index int = rand.IntN(BootstrapNodeCount)
	return bootstrap_nodes[temp_index]
}

func make_peer_node() host.Host{
	var new_node, _ := libp2p.New()
	var DHT, _ := 
}

func test1(){
	n1, _ := libp2p.New()
	fmt.Println(n1.Addrs())
	fmt.Println("\n")
	n2, _ := libp2p.New()
	fmt.Println(n2.Addrs())
}




func main(){

}