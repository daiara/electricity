# Electricity

A short program to calculate how much to expect on your electric bill

In the UK it's commom for the meter to use two different readings with different rates each, and a fee per day of usage.

To run this program you need to install the pandas library first
> pip install pandas

The first input will be your provider rates which are located on the back of your bill.

Then you need to provide the first set of reads: last months or the day you changed providers - date, day read and night read

It's important to provide those informations as you need an old info and a new info to do the calculations.


Then you need to provide this month's read as well as the date that you did the reading. 

The program will then run it's magic using these two information.


It uses the ```datetime``` to calculate the days between inputs, the ```os``` to check and create a file, the ```csv``` to import the file to the program and ```pandas``` to do the analysis of the data.
