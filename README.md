# A 10-Year Metocean Dataset for Laguna Madre, Texas Including for the Study of Extreme Cold Events

## Content

The main goal of this data repository is to provide processed and machine learning ready data. The dataset within the repository consists of 10 years of Air Temperature (ATP) and Water Temperature (WTP) measurements from 2012 - 2022 extracted from the Texas Coastal Ocean Observation Network ([TCOON](https://tidesandcurrents.noaa.gov/tcoon.html)). This repository also contains both raw and post-processed data within the Laguna Madre, TX and also contains the code used to process to data.

#### The contributions of this repository: 

1. The raw ATP and WTP data from 3 South Texas TCOON stations. All stations can be accessed at (http://lighthouse.tamucc.edu/pq).
    - [South Bird Island; Station 013](https://tidesandcurrents.noaa.gov/stationhome.html?id=8776139)
    - [Packery Channel; Station 005](https://tidesandcurrents.noaa.gov/stationhome.html?id=8775792)
    - [Baffin Bay; Station 013](https://tidesandcurrents.noaa.gov/stationhome.html?id=8776604)
    - National Park Service - South Bird Island; Station 171
2. The final product of cleaned ATP and WTP data representative of the Upper Laguna Madre, TX system
3. The data cleaning code
4. A report of missing data for each station (before and after cleaning)

## Publication

    White, M. C., Vicens-Miquel, M., Tissot, P., & Krell, E. (2024). A 10-year Metocean dataset for 
    Laguna Madre, Texas, including for the Study of Extreme Cold Events. Data in Brief, 52, 109828.

[Link to publication](https://www.data-in-brief.com/article/S2352-3409(23)00890-9/pdf)

## Repository DOIs

- **v1.0:** [10.5281/zenodo.10064703](https://zenodo.org/records/10064703) 

### Installation
1. Install miniconda </br>
    `wget https://docs.conda.io/en/latest/miniconda.html` </br>
    `./Miniconda3-latest-Linux-x86_64.sh` </br>
2. Install packages using pip </br>
   `numpy == 1.23.2` </br>
   `pandas == 1.4.3` </br>

### Quick start

**How to generate cleaned temperature data**

    python dataPreprocessing_main.py \
        -d unprocessed_data/ \   # Path to directory with input ATP and WTP files
        -o imputed_data/ \       # Path to directory to write cleaned output files
        -s 2009 \                # First year to process
        -e 2023                  # Final year to process

**Example run**

    $ python dataPreprocessing_main.py -d unprocessed_data/ -o imputed_data/ -s 2009 -e 2022
    Water & Air Temp PreProcessing Pipeline
      Input data directory: unprocessed_data/
      Output data directory: imputed_data/
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
- The raw input files are available in `unprocessed_data/`.

Example ATP file (2009, South Bird Island):

    $ head -n 5 unprocessed_data/airTemperature/southBirdIsland/lighthouse/southBirdIsland_2009.csv 
    #date+time,013-atp
    "01-01-2009 0000",NA
    "01-01-2009 0100",NA
    "01-01-2009 0200",NA
    "01-01-2009 0300",NA

Example WTP file (2009, South Bird Island):

    $ head -n 5 unprocessed_data/waterTemperature/southBirdIsland/lighthouse/southBirdIsland_2009.csv 
    #date+time,013-wtp
    "01-01-2009 0000",17.9
    "01-01-2009 0100",NA
    "01-01-2009 0200",NA
    "01-01-2009 0300",NA

### Output Data

- This repo produced cleaned ATP & WTP data.
- The output data is generated with `dataPreprocessing_main.py`.
- Pre-computed output files are available in `imputed_data/`.
- Missing data reports are in `imputed_data/missingValues/`.

Example output file (2012):

    $ head -n 5 imputed_data/atp_and_wtp_2012.csv
    dateAndTime,packeryATP_lighthouse,npsbiWTP_lighthouse
    01-01-2012 0000,18.8,17.7
    01-01-2012 0100,18.9,17.6
    01-01-2012 0200,18.7,17.5
    01-01-2012 0300,19.7,17.4
