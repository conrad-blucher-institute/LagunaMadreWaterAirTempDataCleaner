"""
Author: Marina Vicens Miquel

Big gaps interpolation
"""

"""
replacingMissValWithNearStation() filles the big gaps of missing values with the values from a nearby station
with a correction. This correction consists on averaging the three previous and next values of the gap of
both stations and correcting the value to fill using the difference between both stations.

We are passing as arguments de dataframe(df), the station that we want to interpolate (stationToInterpolate),
and the station that will be use to interpolate the primary station (stationUsedToInterpolate)
"""
def replacingMissValWithNearStation(df, stationToInterpolate, stationUsedToInterpolate):

    
    realValTemp = []


    realVal = []
    interVal = []

    # Starting a counter to count the size of the gap
    counter = 0

    # Going throw each row of the dataframe
    for i in range(len(df)):

        # Checking if the row value is a missing value
        if (df[stationToInterpolate][i] == -999):        
            counter = counter + 1

            # If the current row is the first row of the gap 
            if(counter == 1):          
                firstMissValPos = i  # Storing the position of the first value of the gap

                # Checking if the beginning of the gap does not belong to the first or last three rows. To compute the average of
                # the previous and next three values of the gap we need to make sure we have three values before and after the gap
                if(i < (len(df)-3) and i > 3): 
                    
                    # If the three values before the beginning of the gap does not contain a missing value then we compute the average of them for both the
                    # station that we want to fill and the station used to interpolate the gap. After we compute the difference between the averages
                    if(df[stationToInterpolate][i-1] != -999 and df[stationToInterpolate][i-2] != -999 and df[stationToInterpolate][i-3] != -999):
                        meanPreviousThree = (df[stationToInterpolate][i-1] + df[stationToInterpolate][i-2] + df[stationToInterpolate][i-3]) / 3  
                       
                    # Checking if any of the three values before the beginning of the gap contain a missing value. If so, we set the mean
                    # of the previous values and the differente between stations to a missing value
                    else:
                        meanPreviousThree = -999
                        differenceBetweenStationsStart = -999
                        
                        
                    if(df[stationUsedToInterpolate][i-1] != -999 and df[stationUsedToInterpolate][i-2] != -999 and df[stationUsedToInterpolate][i-3] != -999):    
                        meanPreviousThreeNearStation = (df[stationUsedToInterpolate][i-1] + df[stationUsedToInterpolate][i-2] + df[stationUsedToInterpolate][i-3]) / 3
                        
                    
                    else:
                        meanPreviousThreeNearStation = -999
                        differenceBetweenStationsStart = -999
                        
                    differenceBetweenStationsStart = meanPreviousThreeNearStation - meanPreviousThree
                
                # If the beginning of the gap belongs to the first or last three rows of the dataframe then we set the difference between stations to a missing value
                else:
                    meanPreviousThree = -999
                    meanPreviousThreeNearStation = -999
                    differenceBetweenStationsStart = -999
                    

            # Appending to the list the value of the station that will be used to interpolate the missing value
            realValTemp.append(df[stationUsedToInterpolate][i]) 

        
        # Checking if the current row does not contains missing values
        else:
            
            # If the row does not contain missing values and has a counter greater than 0 means that it is the first row after a gap. Then,
            # we need to study if we can interpolate the gap that just finished
            if (counter > 0):  

                # Checking that we are not in the first or last three rows of the dataframe
                if(i < (len(df)-3) and i > 3):

                    # Appending to the list the value of the station that will be used to interpolate the missing value
                    realVal.extend(realValTemp) 


                    if(df[stationToInterpolate][i+1] != -999 and df[stationToInterpolate][i+2] != -999 and df[stationToInterpolate][i+3] != -999):
                        meanNextThree = (df[stationToInterpolate][i+1] + df[stationToInterpolate][i+2] + df[stationToInterpolate][i+3]) / 3
                        
                    # Computing the average for the first three values after the gap. After computing the difference between the averages
                    # for the stations that we want to fill and the station that will be used to fill the gaps
                    else:
                        meanNextThree = -999
                        differenceBetweenStationsEnd = -999
                        
                    
                    if(df[stationUsedToInterpolate][i+1] != -999 and df[stationUsedToInterpolate][i+2] != -999 and df[stationUsedToInterpolate][i+3] != -999):
                        meanNextThreeNearStation = (df[stationUsedToInterpolate][i+1] + df[stationUsedToInterpolate][i+2] + df[stationUsedToInterpolate][i+3]) / 3
                    

                    else:
                        meanNextThreeNearStation = -999
                        differenceBetweenStationsEnd = -999

                        
                    differenceBetweenStationsEnd = meanNextThreeNearStation - meanNextThree


                    # Checking that the mean value for the next three values after the gap is not a missing value
                    if(meanPreviousThreeNearStation < -100 or meanNextThreeNearStation < -100):
                        explanation = 'do nothing'

                    # If the mean value for the next three values is not a a missing value we need to fill the gap
                    else:
                        
                        # Checking that there are not missing values on the mean
                        if(meanNextThreeNearStation!=-999 and meanNextThree!=-999 and meanPreviousThreeNearStation!=-999 and meanPreviousThree!=-999):

                            # Computing the correction between the station by subtracting the mean for both stations
                            differenceBetweenStationsEnd = meanNextThreeNearStation - meanNextThree
                            avgDifferenceStations = (differenceBetweenStationsStart + differenceBetweenStationsEnd) / 2
                        
                            # If the difference between stations is not a missing value then we fill the gap using the value from the near station 
                            # corrected by adding the difference between the stations
                            if(avgDifferenceStations != -999):
                                if abs(differenceBetweenStationsStart - differenceBetweenStationsEnd) < 1.5:

                                    for j in range(counter):  
    
                                        # Checking that the nearby station does not have a missing value for the current row
                                        if(realValTemp[j] == -999 or realValTemp[j] == -999.0):
                                            newValue = -999
    
                                        else:
                                            newValue = round(realValTemp[j] + avgDifferenceStations,1)
    
                                        # Filling the missing value with a corrected value from the near station
                                        df.at[firstMissValPos + j, stationToInterpolate] = newValue
                                        interVal.append(newValue)  

                                # Empty the list storing the values of the nearby station
                                realValTemp = []

                        
                        # Checking if the gap cannot be interpolated. If so, we fill the missing value with a missing value
                        else:
                            tempVal = -999

                            for k in range(counter):
                                df.at[firstMissValPos + k, stationToInterpolate] = tempVal
                                interVal.append(tempVal)  

                            # Empty the list storing the values of the nearby station    
                            realValTemp = []

            
                # If we are in the first or last three rows of the dataframe we fill the gap with a missing value
                else:
                    tempVal = -999

                    for k in range(counter):
                        df.at[firstMissValPos + k, stationToInterpolate] = tempVal
                        interVal.append(tempVal)  

                    
                    realValTemp = []
           

            # Setting the size of the gap to 0
            counter = 0    

    # Returning the dataframe with the big gaps filled
    return df
   
