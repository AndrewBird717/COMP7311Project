package main

import (
	"context"
	"fmt"
	"log"

	"github.com/libp2p/go-libp2p"
	dht "github.com/libp2p/go-libp2p-kad-dht"
	"github.com/libp2p/go-libp2p/core/peer"
)

func get_bootstrap_node(){

}

func main() {
	ctx := context.Background()

	bs1, err := libp2p.New()
	if err != nil {
		log.Fatal(err)
	}
	defer bs1.Close()

	bs1dht, err := dht.New(ctx, bs1, dht.Mode(dht.ModeServer))
	if err != nil {
		log.Fatal(err)
	}
	defer bs1dht.Close()

	h1, err := libp2p.New()
	if err != nil {
		log.Fatal(err)
	}
	defer h1.Close()

	h1dht, err := dht.New(ctx, h1, dht.Mode(dht.ModeServer))
	if err != nil {
		log.Fatal(err)
	}
	defer h1dht.Close()

	h2, err := libp2p.New()
	if err != nil {
		log.Fatal(err)
	}
	defer h2.Close()

	h2dht, err := dht.New(ctx, h2, dht.Mode(dht.ModeServer))
	if err != nil {
		log.Fatal(err)
	}
	defer h2dht.Close()

	bootstrap := peer.AddrInfo{
		ID:    bs1.ID(),
		Addrs: bs1.Addrs(),
	}

	if err := h1.Connect(ctx, bootstrap); err != nil {
		log.Fatal(err)
	}
	if err := h2.Connect(ctx, bootstrap); err != nil {
		log.Fatal(err)
	}

	if err := h1dht.Bootstrap(ctx); err != nil {
		log.Fatal(err)
	}
	if err := h2dht.Bootstrap(ctx); err != nil {
		log.Fatal(err)
	}

	fmt.Println("Peers in Host 1:", h1dht.RoutingTable().ListPeers())
}

