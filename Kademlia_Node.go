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

//Usage ./Self NodeID ExperimentNum BucketSize Alpha 

func MakeNode() (host.Host, error){
	h, err := libp2p.New(
		libp2p.ListenAddrStrings(
			"ip4/0.0.0.0/0"
		)
	)
	return h, err
}

func log_incoming_request(){
	//write to NodeID file in folder ExperimentNum
}

func log_outgoing_request () {
	
}

func MakeDHT(ctx context.Context, h host.Host) (*dht.IpfsDHT, error){
	hook := func(ctx context.Context, s network.Stream, req *pb.Message) {
		remotePeer := s.Conn().RemotePeer() //returns ID of other node
		msgType := req.GetType() //Enum for msg https://pkg.go.dev/github.com/libp2p/go-libp2p-kad-dht@v0.43.0/pb#Message
		key := string(req.GetKey()) //data key

		
	}

	BucketSize := 20
	Alpha := 3
	if len(os.Args) > 1{
		BucketSize = os.Args[1]
		if len(os.Args) > 2{
			Alpha = os.Args[2]
		}
	}

	kad, err := dht.New(
		ctx, h,
		dht.Mode(dht.ModeServer),
		dht.ProtocolPrefix(protocol.ID("/COMP7311-atbird")),
		dht.BucketSize(BucketSize),
		dht.Concurrency(Alpha),
		dht.OnRequestHook(hook)
		)
		return kad, err
}

func return_to_py(){

}

func main(){
	ctx := context.Background()
	h, err := MakeNode()

	dht, dhterr := MakeDHT(ctx, h, BucketSize, Alpha)



}



/*


*/