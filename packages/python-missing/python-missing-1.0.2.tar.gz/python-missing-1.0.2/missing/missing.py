# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 20:12:14 2020

@author: hp
"""

import pandas as pd
import sys
import numpy as np

class Missing:
    def __init__(self,filename,header=None):
        self.data = pd.read_csv(filename,header=header)
        self.d = self.data.iloc[:,:].values
        self.head = self.d[0,:]
        self.d = self.d[1:,:]
        self.d = self.d.astype("float64")
        self.features = len(self.d[0])
        self.samples = len(self.d)
    def impute(self,outfilename="out.csv"):
        for i in range(0,self.features):
            s = 0
            buff = []
            for j in range(0,self.samples):
                if np.isnan(self.d[j,i]):
                    buff.append(j)
                else:
                    s += self.d[j,i]
            for k in buff:
                self.d[k,i] = (s/(self.samples-len(buff)))
        f = open(outfilename,'w')
        f.write(",".join(self.head)+"\n")
        for i in range(0,self.samples):
            f.write(",".join([str(w) for w in self.d[i]])+"\n")
        f.close()
                
def main():
    try:
        filename = sys.argv[1]
        obj = Missing(filename)
        obj.impute()
    except:
        print("Exception occurred")
if __name__=="__main__":
    main()