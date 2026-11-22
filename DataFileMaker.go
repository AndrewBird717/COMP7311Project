package main

import(
	"os"
	"strconv"
)

func main(){
	const RecordCount int = 500
	os.Create("./tmp/SimulatedDataFileRegistry/SimulatedDataList1.txt")
	for i := 0 ; i < RecordCount ; i++{
		os.WriteFile("./tmp/SimulatedDataFileRegistry/SimulatedDataList1.txt", []byte("DataFile" + strconv.Itoa(RecordCount)), 0644)

	}


}