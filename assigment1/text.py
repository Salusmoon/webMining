

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


store_data = pd.read_excel('/home/salusmoon/Desktop/ws/webMining/transactions.xlsx')

file = open("Transactions.txt", "w")
td = 1

for i in range(len(store_data)):
    if td == store_data["Transaction ID"][i]:
        a=store_data["Product ID"][i]
        file.write(str(a))
        file.write(",")
    else:
        file.write("\n")
        a=store_data["Product ID"][i]
        file.write(str(a))
        file.write(",")
        td = td+1

print(store_data)