package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/libp2p/go-libp2p"
	dht "github.com/libp2p/go-libp2p-kad-dht"
	"github.com/libp2p/go-libp2p/core/peer"
)

func MakeNode() (host.Host, error){
	h, err := libp2p.New(
		libp2p.ListenAddrStrings(
			"ip4/0.0.0.0/0"
		)
	)
	return h, err
}

func MakeDHT(ctx context.Context, h host.Host, BucketSize int, Alpha int) (*dht.IpfsDHT, error){
	kad, err := dht.New(
		ctx, h,
		dht.Mode(dht.ModeServer),
		dht.ProtocolPrefix(protocol.ID("/COMP7311-atbird")),
		dht.BucketSize(BucketSize),
		dht.Concurrency(Alpha)
		)
		return kad, err
}

func main(){
	ctx := context.Background()
	h, err := MakeNode()
	BucketSize := 20
	Alpha := 3
	if len(os.Args) > 1{
		BucketSize = os.Args[1]
		if len(os.Args) > 2{
			Alpha = os.Args[2]
		}
	}
	dht, dhterr := MakeDHT(ctx, h, BucketSize, Alpha)

	


}



/*


*/