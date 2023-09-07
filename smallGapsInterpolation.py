"""
Author: Marina Vicens Miquel

Small gaps interpolation
"""

"""
interpolatingSmallGaps() interpolates the small gaps. A small gap is defined as a gap of less or equal than 3h for air
temperature and 5h or less for water temperature.
To interpolate we will average the three values previous to the beginning of the gap and the three first values after
the gap. Then, we will linearly interpolate from the average values

We are passing as arguments the dataframe (df), the variable that we want to interpolate(varToInterp), and the size of
the interpolated gap (interpGap)
"""
def interpolatingSmallGaps(df, varToInterp, interpGap):
    
    # Creating a counter to count the size of the gap
    counter = 0  
    
    # Creating a list that contains the  values used to interpolate
    interVal = []
    
    # Creating a loop that goes throw all the rows of the dataframe
    for i in range(len(df)):
        
        # Checking if the row contains a missing value. If so, we start the counter
        if (df[varToInterp][i] == -999):        
            counter = counter + 1

            # Checking if the current row is contains the first valu of the gap. If so, we store the position
            # of the beginning of the gap
            if(counter == 1):          
                firstMissValPos = i

                # We are checking that we are not in the first or last three rows of the dataset. In case we are 
                # in the first or last three rows we will not be able to interpolate these rows since we cannot 
                # average the previous and/or next three rows of the gap. Then, if we are in that scenario, we 
                # will average the mean to -999 and this value will not allow to interpolate this gap later on 
                # the code.
                # If we are withing the addequate range then, we will compute the average of the previous three values
                if(i < (len(df)-3) and i > 3):

                    if (df[varToInterp][i-1] == -999 or df[varToInterp][i-2] == -999 or df[varToInterp][i-3] == -999):
                        meanPreviousThree = -999
                        
                    else:
                        meanPreviousThree = (df[varToInterp][i-1] + df[varToInterp][i-2] + df[varToInterp][i-3]) / 3

                else:
                    meanPreviousThree = -999

        # Checking if the rows do not contain a missing value
        else:
            
            # If the row does not contain a missing value we need to check if this is the first row or not that does
            # not contain a missing values. If counter is greater than 0 means that this is the first row that does
            # not contain a missing value. Then, we need to check if the gap size is smaller or equal than the maximum
            # gap size that we decide that we want to interpolate. If so, it means that we need to interpolate the gap
            # that just finished
            if (counter > 0 and counter <= interpGap):  
                # Checking that we are not in the first or last three rows of the dataset
                if(i < (len(df)-3) and i > 3):
    
                    # Checking if any of the next three rows of the end of the gap has a missing value. If so, we set
                    # the mean of the next three values and the filling values to -999 
                    if (df[varToInterp][i+1] == -999 or df[varToInterp][i+2] == -999 or df[varToInterp][i+3] == -999):
                        meanNextThree = -999
                        stepValue = 0
                        fillingValue = -999

                    # If all of the three rows after the gap does not contain a missing values then, we compute the 
                    # average of the next three values
                    if (df[varToInterp][i+1] != -999 and df[varToInterp][i+2] != -999 and df[varToInterp][i+3] != -999 ):
                        meanNextThree = (df[varToInterp][i+1] + df[varToInterp][i+2] + df[varToInterp][i+3]) / 3

                        # If the mean of the previous three values contains a misisng values then, the filling values 
                        # is set to -999
                        if(meanPreviousThree == -999):
                            stepValue = 0
                            fillingValue = -999

                        # If the previous three values to the beginning of the gap and the next three values after the 
                        # end of the gap do not contain a missing value, then we need to compute the values for the 
                        # missing values. First we need to compute the step value used to linearly interpolate the 
                        # missing values. Then, to find the filling value we need to add the step value to the mean
                        # of the previous three values. Then, we just found the filling value for the first missing
                        # value of the gap
                        else:
                            stepValue = (meanNextThree - meanPreviousThree) / (counter + 1)
                            fillingValue = round(meanPreviousThree + stepValue,1)

                    # This loop will fill the rest of the missing values in the gap
                    for j in range(counter):
                        
                        # Checking that we are not in the first missing value of the gap. If so, the filling value
                        # would be the incremental of the prevous value filled with the step value
                        if j != 0:
                            fillingValue = round(fillingValue + stepValue,1)

                        # Filling the missig gaps
                        df.at[firstMissValPos + j, varToInterp] = fillingValue 
                        interVal.append(fillingValue) 

               
                # If the gap is in the first or last three rows of the dataset, we fill the gap with -999
                else:
                    # Checking if exists a gap
                    if (counter != 0):
                        
                        # Filling the gap with missing values
                        for jj in range(counter):
                                
                            fillingValue = -999
                            df.at[firstMissValPos + jj, varToInterp] = fillingValue 
                            interVal.append(fillingValue) 
                 
                               
            # Setting the counter to 0, the small gap has been interpolated
            counter = 0

    # Returning the dataframe after the small gaps have been interpolated
    return df