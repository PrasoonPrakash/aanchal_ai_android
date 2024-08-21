import pickle
import sys
import pandas as pd

with open('model/model.pkl', 'rb') as file:
    model = pickle.load(file)
name=sys.argv[1]
df=pd.read_csv("csvFiles/"+name+"_data.csv")
yp=model.predict(df)

if(yp[0]==0):
    print("yes")
else:
    print("no")