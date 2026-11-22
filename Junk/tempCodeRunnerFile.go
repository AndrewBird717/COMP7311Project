package main

import(
	"fmt"

	"github.com/ipfs/go-cid"
 "github.com/libp2p/go-libp2p"
 dht "github.com/libp2p/go-libp2p-kad-dht"
 "github.com/libp2p/go-libp2p/core/host"
 "github.com/libp2p/go-libp2p/core/peer"
)

func main(){
	bs1, errbs1 := libp2p.New()
	bs1dht, errdht0 := dht.New()

	h1, errh1 := libp2p.New(peer.AddrInfo{ID: bs1.ID(), Addrs: bs1.Addrs()})
	h1dh, errdht1 := dht.New()

	h2, errh2 := libp2p.New(peer.AddrInfo{ID: bs1.ID(), Addrs: bs1.Addrs()})
	h2dht, errdht2 := dht.New()

	rt1 := h1dht.RoutingTable()
	peers := rt1.ListPeers()

	fmt.Println("Peers in Host 1: ", peers)
}