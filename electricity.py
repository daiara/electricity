from datetime import datetime, date
import csv, os
import pandas as pd

if not os.path.isfile("electricity.csv"): #This creates the csv
    data = pd.DataFrame(columns=["Date","Day","Night"])
    data.to_csv("electricity.csv", index=False)

electricity = pd.read_csv("electricity.csv")
readings = pd.DataFrame(electricity)

def get_parameters(time, day_in, night_in):
    reading = readings.iloc[-1,:].values.tolist()
    date_rd = datetime.strptime(reading[0], "%d.%m.%Y")
    date_out = time - date_rd #How many days since the last reading
    day_out = day_in - reading[1] #This day reading minus the last day reading
    night_out = night_in - reading[2] #This night reading minus the last night reading
    
    return date_out.days, day_out, night_out

def fare(day, night, days):
    #This amounts are a match for my electricity provider. Check the back of your bill to see yours.
    day_fare = round(((14.56 * day) / 100), 2) 
    night_fare = round(((7.10 * night) / 100), 2)
    month_fare = round(((19.47 * days) / 100), 2)
    total_cost = round((day_fare + night_fare + month_fare),2)
    #After tests with my previous bills, I noticed that they round every amount before adding them up.
    #The round in total_cost is just to make sure that it will come back a 00.00 value
    return total_cost

if readings.empty: #If this one is your first input ever
    date = input("When did you do the first reading? (dd.mm.yyyy) ")
    day = input("How much is the day reading? ")
    night = input("How much is the night reading?" )

    print("Okay. So we will save this for you til your next reading. See you in a month :)")
    
else:
    date = input("When did you do this reading? (dd.mm.yyyy) ")
    dt = datetime.strptime(date, "%d.%m.%Y")
    day = int(input("How much is the day reading? "))
    night = int(input("How much is the night reading? "))

    days, day_reading, night_reading = get_parameters(dt, day, night)
    total = fare(day_reading, night_reading, days)
    vat = round((total * 0.05),2) 

    print("\nOkay, so...\nYour bill is $%s\nYour expenses were %s \nand your VAT was %s \nAnd that's it =] " % ((total + vat), total, vat))

#This block below saves the data into your csv so you don't have to do the same input next month
data = [[date,day,night]]
save = pd.DataFrame(data=data, columns=['Date','Day','Night'])
save_df = readings.append(save)
save_df.to_csv("electricity.csv", index=False)

"""
USE THIS ONE FOR TESTS :)
date = '11.07.2019'
dt = datetime.strptime(date, "%d.%m.%Y")
day = int(21542)
night = int(11311)
"""

