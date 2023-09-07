# A 10-Year Metocean Dataset for Laguna Madre, Texas Including for the Study of Extreme Cold Events

## Content

This is a data repository. Its main goal is to provide processed and machine learning ready data. This repository contains both raw and post process Air Temperature (ATP) and Water Temperature (WTP). Additionally of containing the data, this repository also contains the code used to process the data.

(Something about where it came from... and tell them to see more details in the publication)

#### The contributions of this repository: 

1. The raw ATP and WTP data from 3 South Texas TCOON stations.
    - [South Bird Island](https://tidesandcurrents.noaa.gov/stationhome.html?id=8776139)
    - [Packery Channel](https://tidesandcurrents.noaa.gov/stationhome.html?id=8775792)
    - [Baffin Bay](https://tidesandcurrents.noaa.gov/stationhome.html?id=8776604)
2. The final product of cleaned ATP and WTP data.
3. The data cleaning code.
4. A report of missing data for each station (before and after cleaning)

## Publication
Journal paper currently under review. Once it is published, the citation will be added here.

### Installation
1. Install miniconda </br>
    wget https://docs.conda.io/en/latest/miniconda.html </br>
    ./Miniconda3-latest-Linux-x86_64.sh
2. Install packages using pip </br>
   numpy == 1.23.2 </br>
   pandas == 1.4.3 </br>

### Quick start

**How to generate cleaned temperature data**

    python dataPreprocessing_main.py \
        -d data/ \   # Path to directory with input ATP and WTP files
        -o out/ \    # Path to directory to write cleaned output files
        -s 2009 \    # First year to process
        -e 2023      # Final year to process

**Example run**

    $ python dataPreprocessing_main.py -d data/ -o out/ -s 2009 -e 2022
    Water & Air Temp PreProcessing Pipeline
      Input data directory: data/
      Output data directory: out/
      Processing years 2009 - 2022.

    Year 2009  (1 / 14)
    Year 2010  (2 / 14)
    Year 2011  (3 / 14)
    Year 2012  (4 / 14)
    Year 2013  (5 / 14)
    Year 2014  (6 / 14)
    Year 2015  (7 / 14)
    Year 2016  (8 / 14)
    Year 2017  (9 / 14)
    Year 2018  (10 / 14)
    Year 2019  (11 / 14)
    Year 2020  (12 / 14)
    Year 2021  (13 / 14)
    Year 2022  (14 / 14)

### Input Data

- Inputs are ATP and WTP files where each year has a single file.
- The raw input files are available in `data/`.

Example ATP file (2009, South Bird Island):

    $ head -n 5 data/airTemperature/southBirdIsland/lighthouse/southBirdIsland_2009.csv 
    #date+time,013-atp
    "01-01-2009 0000",NA
    "01-01-2009 0100",NA
    "01-01-2009 0200",NA
    "01-01-2009 0300",NA

Example WTP file (2009, South Bird Island):

    $ head -n 5 data/waterTemperature/southBirdIsland/lighthouse/southBirdIsland_2009.csv 
    #date+time,013-wtp
    "01-01-2009 0000",17.9
    "01-01-2009 0100",NA
    "01-01-2009 0200",NA
    "01-01-2009 0300",NA

### Output Data

- This repo produced cleaned ATP & WTP data.
- The output data is generated with `dataPreprocessing_main.py`.
- Pre-computed output files are available in `out/`.
- Missing data reports are in `out/missingValues/`.

Example output file (2012):

    $ head -n 5 out/atp_and_wtp_2012.csv
    dateAndTime,packeryATP_lighthouse,npsbiWTP_lighthouse
    01-01-2012 0000,18.8,17.7
    01-01-2012 0100,18.9,17.6
    01-01-2012 0200,18.7,17.5
    01-01-2012 0300,19.7,17.4
