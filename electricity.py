from datetime import datetime, date
import csv, os
import pandas as pd

print("THE ELECTRIC BILL PROGRAM\n")

def get_parameters(reading, time, day_in, night_in):
    date_rd = datetime.strptime(reading[0][0], "%d.%m.%Y")
    date_out = time - date_rd #How many days since the last reading
    day_out = day_in - reading[0][1] #This day reading minus the last day reading
    night_out = night_in - reading[0][2] #This night reading minus the last night reading
    
    return date_out.days, day_out, night_out

def fare(day, night, days):
    rates = pd.read_csv("rates.csv").values.tolist()
    day_fare = round(((int(rates[0][0]) * day) / 100), 2) 
    night_fare = round(((int(rates[0][1]) * night) / 100), 2)
    month_fare = round(((int(rates[0][2]) * days) / 100), 2)
    total_cost = round((day_fare + night_fare + month_fare),2)
    #After tests with my previous bills, I noticed that they round every amount before adding them up.
    #The round in total_cost is just to make sure that it will come back a 00.00 value
    return total_cost

def readings():
    date = input("When did you do the reading? (dd.mm.yyyy) ")
    day = int(input("How much was the day reading? "))
    night = int(input("How much was the night reading? "))
    return date, day, night

if not os.path.isfile("rates.csv"): #This will creat the first csv file with the provider rates
    print("It looks like this is your first time using this program. Please proceed:\n")
    day_rate= input("How much is the day unit rate? xx.xx pence/kWh ")
    night_rate= input("How much is the night unit rate? xx.xx pence/kWh ")
    daily_rate= input("How much is the standing charge rate? xx.xx pence/day ")

    data = [[day_rate,night_rate,daily_rate]]
    save = pd.DataFrame(data=data, columns=['Day','Night','Daily'])
    save.to_csv("rates.csv", index=False) #This block saves those values using pandas to create a dataframe 
    

if not os.path.isfile("electricity.csv"): #This creates the csv
    print("\nAnd for your first readings:\n") #If this one is your first input ever
    date, day, night = readings()
    print("Okay. So we will save this for you til next month.")

    data = [[date,day,night]] #This block saves the first csv info
    save = pd.DataFrame(data=data, columns=['Date','Day','Night']) 
    save.to_csv("electricity.csv", index=False)

    
else:
    electricity = pd.read_csv("electricity.csv") #Reads the existing csv with your last readings
    reading = electricity.tail(1).values.tolist()
    print("Hello and welcome back!\n")
    date, day, night = readings()
    dt = datetime.strptime(date, "%d.%m.%Y")

    days, day_reading, night_reading = get_parameters(reading, dt, day, night)
    total = fare(day_reading, night_reading, days)
    vat = round((total * 0.05),2) 

    print("\nOkay, so...\nYour bill is $%s\nYour expenses were %s \nand your VAT was %s \nAnd that's it =] " % ((total + vat), total, vat))

    data = [[date,day,night]] #This block appends the info to the csv file, so you will always save your readings and you might use it for a different kind of analysis in the future
    save = pd.DataFrame(data=data, columns=['Date','Day','Night'])
    save_df = electricity.append(save)
    save_df.to_csv("electricity.csv", index=False)
