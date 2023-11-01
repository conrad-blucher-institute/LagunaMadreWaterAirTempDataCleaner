"""
Author: Marina Vicens Miquel

The goal of this code is to prepare the cold stunning dataset:
    
    1) Read all the files from both lighthouse and NOAA
    2) Merge all the files into one dataframe
    3) Replacing all the missing values to -999
        Note: I decided to replace all the missing values to -999 to unify them
        since they are found in different ways: ' ', 'NA', 'RM'
    4) Compute the number of missing values for each variable in the dataset
        Note: it is important to do so, them it is possible to compare the number
        of missing values between the data from lighthouse. Also, it
        allows us to understand which stations have more and less missing values
    5) Interpolate the small gaps for each variable
        Note: a small gap is defined as a gap that is smaller or equal to 3h for
        air temperature or 5h for water temperature
    6) Compute the number of missing values for each variable again. Then, we
        can study and compare the number of missing values between the different 
        stations. 
    7) Replacing the missing values of the selected station with the values,
        with certain threshold, from a nearby station.
        Note: we are going to replace the missing values of the station that has
        the smaller number of missing values (step 6) with the values from the
        second station with the less amount of missing values.
    8) Interpolate the small gaps again
        Note: it is important to do small gaps interpolation again, since it is
        possible that after replacing the big gap missing values, we have small
        gaps that we can interpolate
    8) Compute the number of missing values again. This will allows us to 
        understand how helpful or not was the gap filling process. Then, we need
        to evaluate the dataset again
    9) Dropping all the unnecesary columns (for example we have air temperature
        values from both lighthouse and nooa, but we only need the data from
        one of them. We will select the one with best quality data and we will
        remove the other innecessary columns)
    10) Adding 5 days of rows at the begging of the dataset (data from the end
        of the previous year) and five 5 days of rows at the end of the dataset
        (data from the next year). We need to do so, because for hour problem
        we use columns for the past hours. Then, to be able to retrieve 120h 
        values from the beginning of the year, we need this additional columns)
    11) Saving the create file
                                                             
    Note: all of the steps are inside a for loop, then it can perform all the 
    steps in multiple years autmatically
"""

# Importing libraries
import os
import pandas as pd
import numpy as np
from smallGapsInterpolation import interpolatingSmallGaps
from bigGapsInterpolation import replacingMissValWithNearStation
from optparse import OptionParser

# Files
leapYear_dates_template = "dates_leapYear.csv"
normalYear_dates_template = "dates_normalYear.csv"

packeryATP_lighthouse_template = "/airTemperature/packeryChannel/lighthouse/packeryChannel_{}.csv"
baffinATP_lighthouse_template = "/airTemperature/baffinBay/lighthouse/baffinBay_{}.csv"
sbiWTP_lighthouse_template = "/waterTemperature/southBirdIsland/lighthouse/southBirdIsland_{}.csv"
npsbiWTP_lighthouse_template = "/waterTemperature/nationalParkService_southBirdIsland/lighthouse/nationalParkServiceBI_{}.csv"

"""
readingData() reads all the data from different files into an unique dataframe
for each file read. 
We are reading two files that only contain the dates (one for regular years and
another for leap years). The reason for doing data rather than getting that column
from another dataset that we read is that some datasets miss the last couple of 
months of data, and if we use them, we would not have a date for all the year.
So, we read the dates from these datasets to avoid this problem. Once the dates
are read, we replace the default year of the date for the year which all the 
data is from.

We are passing as argument the year that we want to study
"""
def readingData(dataDir, year):

    year_str = str(year)    

    # Reading the data, ATP = air temperature, WTP = water temperature
    packeryATP_lighthouse = pd.read_csv(dataDir + packeryATP_lighthouse_template.format(year_str))
    baffinATP_lighthouse = pd.read_csv(dataDir + baffinATP_lighthouse_template.format(year_str))
    sbiWTP_lighthouse = pd.read_csv(dataDir + sbiWTP_lighthouse_template.format(year_str))
    npsbiWTP_lighthouse = pd.read_csv(dataDir + npsbiWTP_lighthouse_template.format(year_str))
    
    # Reading the dates and replacing the default year for the year from which the data is
    if (year == 2012 or year == 2016 or year == 2020):
        initialDateAndTime = pd.read_csv(dataDir + "/" + leapYear_dates_template) 
        correctDateAndTime = []
        
        for i in range(len(initialDateAndTime)):
            strInitialDate = str(initialDateAndTime.iloc[i][0])
            strNewDate = strInitialDate.replace('2020', str(year))
            correctDateAndTime.append(strNewDate)
    else:
        initialDateAndTime = pd.read_csv(dataDir + "/" + normalYear_dates_template)
        correctDateAndTime = []
        
        for i in range(len(initialDateAndTime)):
            strInitialDate = str(initialDateAndTime.iloc[i][0])
            strNewDate = strInitialDate.replace('2019', str(year))
            correctDateAndTime.append(strNewDate)
    
    # Converting the dates from a list to a dataframe
    dateAndTime = pd.DataFrame(correctDateAndTime)
    
    return packeryATP_lighthouse, baffinATP_lighthouse, sbiWTP_lighthouse, npsbiWTP_lighthouse, dateAndTime

 
"""
merginDataToOneDataframe() combines all the dataframes previously read into one dataframe

We are passing as arguments all the previously create dataframes. Each dataframe contains
a different variable
"""
def mergingDataToOneDataframe(packeryATP_lighthouse, baffinATP_lighthouse, 
                               sbiWTP_lighthouse, npsbiWTP, dateAndTime):
    
    # Creating a dataframe that combines all the dataframes
    df = pd.DataFrame()
    df['dateAndTime'] = dateAndTime
    df['packeryATP_lighthouse'] = packeryATP_lighthouse['005-atp']
    df['baffinATP_lighthouse'] = baffinATP_lighthouse['068-atp']
    df['sbiWTP_lighthouse'] = sbiWTP_lighthouse['013-wtp']
    df['npsbiWTP_lighthouse'] = npsbiWTP['171-wtp']
    
    return df
            
 
"""
replacingMissingValuesWithNeg999() replaces all the missing values with -999.
We do that to unify all the missing values since they can be found in the 
following ways: " ", "RM", "NA"

We are passing as argument the dataframe
"""
def replacingMissingValuesWithNeg999(df):
    
     # Replacing the missing values with -999
     df.replace('RM', -999, inplace=True)
     df.replace('NA', -999, inplace=True)
     df.fillna(-999, inplace=True)
     
     # Converting the type of all the columns except the first one (dates)
     # to a float type
     df[df.columns[1:]] = df[df.columns[1:]].astype(float)
            
     return df
 

"""
countingMissValues() countes the number of missing values for each column and 
write these values into a file
This function computes the number of missing values for each column. Rather
than computing the number of missing values directly, it computes the number
of values different than -999 and substracts this number from the total number
of rows. I did that because for some years we do not have the last two months
of data. Then, there are no rows from that dates, then I would not be able to
count missing values, since they are not missing because they are no rows

We are passing as arguments the dataframe, the year of the dataset, a file input
(this is the title of the file that we will write), and the filename of the file 
that we will create to store the number of missing values
"""  
def countingMissValues(df, year, fileInput, filename):
    
    # Starting counters for the rows with no missing values
    packeryATP_lighthouse_missVal = 0
    baffinATP_lighthouse_missVal = 0
    sbiWTP_lighthouse_missVal = 0
    npsbiWTP_lighthouse_missVal = 0
    
    # Computing the number of rows with no missing values for each column
    for i in range(len(df)):
        if(df['packeryATP_lighthouse'][i] == -999 or df['packeryATP_lighthouse'][i] == np.nan):
            packeryATP_lighthouse_missVal += 1
        if(df['baffinATP_lighthouse'][i] == -999 or df['baffinATP_lighthouse'][i] == np.nan):
            baffinATP_lighthouse_missVal += 1
        if(df['sbiWTP_lighthouse'][i] == -999 or df['sbiWTP_lighthouse'][i] == np.nan):
            sbiWTP_lighthouse_missVal += 1
        if(df['npsbiWTP_lighthouse'][i] == -999 or df['npsbiWTP_lighthouse'][i] == np.nan):
            npsbiWTP_lighthouse_missVal += 1
            
    # Writting the number of missing values into a file
    file = open(filename, 'a') 
    file.write(fileInput + "\n\n")
    file.write(str(year) + '\n\n')
    file.write("Packery Channel Missing Values for the Air Temperature from Lighthouse                                = " 
               + str(packeryATP_lighthouse_missVal) + ' --> ' + str(round((packeryATP_lighthouse_missVal/len(df))*100,4)) + ' %\n')
    file.write("Baffin Bay Missing Values for the Air Temperature from Lighthouse                                     = " 
               + str(baffinATP_lighthouse_missVal) + ' --> ' + str(round((baffinATP_lighthouse_missVal/len(df))*100,4)) + ' %\n')
    file.write("South Bird Island Missing Values for the Water Temperature from Lighthouse                            = " 
               + str(sbiWTP_lighthouse_missVal) + ' --> ' + str(round((sbiWTP_lighthouse_missVal/len(df))*100,4)) + ' %\n')
    file.write("National Park Services - South Bird Island Missing Values for the Water Temperature from Lighthouse   = " 
               + str(npsbiWTP_lighthouse_missVal) + ' --> ' + str(round((npsbiWTP_lighthouse_missVal/len(df))*100,4)) + ' %\n\n\n')
    file.close()


"""
droppingUnnecessaryColumns() drop the columns that we do not longer need

We pass as arguments the dataframe (df) and a list that contains the name
of all the unnecessary columns (unnecessaryColList)
""" 
def droppingUnnecessaryColumns(df, unnecessaryColList):
    
    # Deleting the unnecessary columns
    for i in range(len(unnecessaryColList)):
        del df[unnecessaryColList[i]]
    
    # Returns the dataframe without the deletec columns
    return df
    

"""
addingExtraRows() add rows at the beggining of the dataset (the last 5 days of
the previous year) and at the end of the dataset (the first 5 days of the next
year)
                                                  
We pass as arguments a list that contains all the dataframes that we interpolate 
in the loop                                                  
"""
def addingExtraRows(dfList, year):

    # We use a loop to do it for all the years, except the first and the last year. 
    # We cannot use the first year because we do not have information of the previous
    # year. Similarly, we cannot use the last year, since we do not have information
    # for the next year
    for i in range(len(dfList)-2):
        
        yearBefore = dfList[i].tail(120)    # Adding 5 extra days. This means 24 extra rows per day. Then,  5*24 = 120 extra rows. Then, we are selecting the last 120 of the dataframe
        currentYear = dfList[i+1]           # Selecting the entire dataset for the current year
        yearAfter = dfList[i+2].head(120)   # Adding 5 extra days. This means 24 extra rows per day. Then,  5*24 = 120 extra rows. Then, we are selecting the first 120 of the dataframe

        # Creating a new dataframe that contains data from the previous, current, and next year
        df = pd.DataFrame()
        df = df.append(yearBefore)
        df = df.append(currentYear)
        df = df.append(yearAfter)
        
        # Saving the dataframes
        df.to_csv('year_' + str(year+1+i) + '_withExtraRows.csv', encoding='utf-8', index=False)

    # Returning the dataframe with the extra rows        
    return df
        

"""
main() is the driver of the program. Here we do all the function calls
"""
def main():

    # Parse options
    parser = OptionParser()
    parser.add_option("-d", "--data_dir", 
                      help="Path to directory with air and water temperature input data.",
                      default="unprocessed_data/")
    parser.add_option("-o", "--out_dir",
                      help="Path to directory to store processed dataset.",
                      default="imputed_data/")
    parser.add_option("-q", "--quiet",
                      help="Suppress all print messages.",
                      default=False,
                      action="store_true")
    parser.add_option("-s", "--start_year",
                      help="First year to process.",
                      default=2009,
                      type="int")
    parser.add_option("-e", "--end_year",
                      help="Last year to process.",
                      default=2023,
                      type="int")
    (options, args) = parser.parse_args()

    dataDir = options.data_dir
    outDir = options.out_dir
    isQuiet = options.quiet
    startYear = options.start_year
    endYear = options.end_year

    # Create 'missingValues' directory
    path = outDir + "missingValues/"
    isExist = os.path.exists(path)
    if not isExist:
      os.makedirs(path)

    if not isQuiet:
      print("Water & Air Temp PreProcessing Pipeline")
      print("  Input data directory: {}".format(dataDir))
      print("  Output data directory: {}".format(outDir))
      print("  Processing years {} - {}.".format(startYear, endYear)) 
      print("")
    
    # Defining the first year that we want to study
    year = startYear
    nYears = endYear - startYear
    
    # This loop will prepare the data for the number of years set in the range
    for i in range(nYears + 1):

        if not isQuiet:
          print("    Year {}  ({} / {})".format(year + i, i + 1, nYears + 1))

        # Function call to read the data
        packeryATP_lighthouse, baffinATP_lighthouse, sbiWTP_lighthouse, \
            npsbiWTP_lighthouse, dateAndTime = readingData(dataDir, year+i)
    
        # Function call to merge all the dataframes into one
        df = mergingDataToOneDataframe(packeryATP_lighthouse, baffinATP_lighthouse,
            sbiWTP_lighthouse, npsbiWTP_lighthouse, dateAndTime)
    
        # Function call to set all the missing values to -999
        df = replacingMissingValuesWithNeg999(df)

        # Function call to count the number of missing values
        countingMissValues(df, year+i, 'MISSING VALUES - ORIGINAL DATASET',
                           outDir + 'missingValues/missingValuesOriginalDataset.txt')
        
        # Function call to interpolate the small gaps. Variables to pass are the df's
        # the variables we want to interpolate and gap size (df,'variableName', max gap size)
        df = interpolatingSmallGaps(df, 'packeryATP_lighthouse', 3)
        df = interpolatingSmallGaps(df, 'baffinATP_lighthouse', 3)
        df = interpolatingSmallGaps(df, 'sbiWTP_lighthouse', 5)
        df = interpolatingSmallGaps(df, 'npsbiWTP_lighthouse', 5)
        
        # Function call to count the number of missing values
        countingMissValues(df, year+i, 'MISSING VALUES - SMALL GAPS INTERPOLATED', outDir + 'missingValues/missingValuesSmallGapsInterpolated.txt')
    
        # Function call to fill the big gaps
        df = replacingMissValWithNearStation(df, 'packeryATP_lighthouse', 'baffinATP_lighthouse')  # dataframe, stationToInterpolate, stationUsedToInterpolate
        df = replacingMissValWithNearStation(df, 'npsbiWTP_lighthouse', 'sbiWTP_lighthouse')  # dataframe, stationToInterpolate, stationUsedToInterpolate
        
        # Function call to intepolate the small gaps
        df = interpolatingSmallGaps(df, 'packeryATP_lighthouse', 3)
        df = interpolatingSmallGaps(df, 'npsbiWTP_lighthouse', 5)
        
        # Function call to count the missing values
        countingMissValues(df, year+i, 'MISSING VALUES - BIG GAPS FILLED',
                           outDir + 'missingValues/missingValuesAfterBigGapsFilled.txt')
        
        # Creating a list of the unnecessary columns
        unnecessaryColList = ['baffinATP_lighthouse', 'sbiWTP_lighthouse']
        
        # Function call to drop all the unnecessary columns
        df = droppingUnnecessaryColumns(df, unnecessaryColList)
        
        # Replacing -999 for np.nan
        df.replace(to_replace = -999, value = np.nan, inplace = True)
        
        # Saving final dataframes for the following years [2012-2022]
        if year+i >= 2012 and year+i <= 2022:
            df.to_csv(outDir + 'atp_and_wtp_' + str(year+i) + '.csv', encoding='utf-8', index=False)
        

if __name__ == "__main__":
    main()
