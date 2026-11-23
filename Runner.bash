#Usage: . NodeCount=10 BSCount=1 Alpha=3 K=20 UpPercentage=100
           $1          $2        $3     $4    $5

NodeCount="${1:-10}"
BS_Count="${1:-10}"
Alpha="${1:-10}"
K="${1:-10}"
UpPercentage="${1:-10}"


result=$(python3 ./StartOrganizer.py NodeCount BS_Count Alpha K UpPercentage)
if ! result; then
    echo "StartOrganizer.py had an error or did not return an ExperimentID"
    exit
fi


