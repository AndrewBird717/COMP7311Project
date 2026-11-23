import sys
from pathlib import Path
import numpy as np

def GetLookupTimes():
    res = []
    dir = Path(f"ExperimentLogs") / "LookupTimes" / str(sys.argv[1])
    for filepath in dir.iterdir():
        if filepath.is_file():
            data = filepath.read_text(encoding="utf-8")
            split_data = data.split()
            res.append(split_data)
    print(split_data)

def GetMetricsFromDataArr(data_arr):
    print(data_arr)
    print("Mean: ", np.mean(data_arr))
    print("Median: ", np.median(data_arr))
    for percentile in [25, 50, 90, 95, 99]:
        print(f"{percentile}th Percentile: {np.percentile(data_arr, percentile)}\n")




def main():
    print("LOG READER RUNNING...")
    data_arr = GetLookupTimes()
    GetMetricsFromDataArr(data_arr)


if __name__ == "__main__":
    main()