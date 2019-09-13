# nozzle-calibration
School project that aims to find a method of identifying fuel nozzles with miscalibrated gauges. Work is based on simulated data sets.

## Prerequisites

### Data
Download data files. 
```
$ cd data
$ ./downloadData.sh [Google Drive id] # sh... it's a secret 🤫
```

### Python dependencies
```
make install
# alternatively, if you also want to install dev dependencies
make install-all
```
## What's left to do? 

- [x] Design the basic flow and the algorithm that detects broken nozzles
- [x] Calculate balance for every time window in the historical data
- [ ] Generate erroneous transactions
- [ ] Perfect the integration with tank truck supplies ⛽ - currently there are some mistakes
- [ ] Verify the results

<img src="https://i.chzbgr.com/full/7135493632/h6E511564/" width="250">

