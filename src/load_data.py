import pandas as pd
import glob
import sys
import os

path =r'Results/Scenario-1/' # use your path
allFiles = glob.glob(path + "/*.csv")

frame = pd.DataFrame()
list_ = []
for index in range(len(allFiles)-1):
   df = pd.read_csv(allFiles[index],index_col=None, header=0)
   list_.append(df)

frame = pd.concat(list_)


print(frame)

#single_result = pd.read_csv("Results/Scenario-1/Results-1-1.csv", sep=',')
#print(single_result)