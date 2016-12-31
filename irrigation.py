##
# Author: Vincent Steffens
# Email:  vincesteffens@gmail.com
# Date:   17 Dec 2016
##

from __future__ import print_function
import sys
import os
import math

def init():
   if len(sys.argv) != 2:
      print("Error: Program takes one argument. {} arguments given".\
            format(len(sys.argv)))
      print("Usage: $ python irrigation.py file.csv")
      exit()


def get_rainfall():
   lines = []

   filename = sys.argv[len(sys.argv) - 1]
   if os.path.isfile(filename):
      with open(filename) as f:
         for line in f:
            if not line.startswith('#'):
               line = float(line.rstrip('\r\n').split(',')[1])
               lines.append(line)

   return lines


def net_irrigation_wheat(precip, mean_precip, irrigation = 0):
   return 24 + 0.5 * (precip - mean_precip)


def net_irrigation_corn(precip, mean_precip, irrigation = 0):
   return 12 + 0.5 * (precip - mean_precip)


def corn_production(pre, mean_pre):
   thing_one = (- 157.9887  
                + 20.73612 * net_irrigation_wheat(pre, mean_pre) 
                - 0.2900359 * net_irrigation_wheat(pre, mean_pre) ** 2 
                + 1.977787 * pre ** 2 
                - 0.4966157 * math.log(pre) * pre ** 2 
                - 0.0000205 * (net_irrigation_wheat(pre, mean_pre) * pre) 
                ** 3 
                + 0.00000309 * math.log(net_irrigation_wheat(pre, mean_pre) 
                * pre) * (net_irrigation_wheat(pre, mean_pre) * pre) ** 3)

   thing_two = 211 # Should be hardcoded for now

   return min(thing_one, thing_two)


def wheat_production(pre, mean_pre):
   thing_one = (- 58.10471
                + 8.075576 * net_irrigation_corn(pre, mean_pre) - 0.1041257 
                * net_irrigation_corn(pre, mean_pre) ** 2
                + 0.9682407 * pre ** 2
                - 0.2498325 * math.log(pre) * pre ** 2
                - 0.0009477 * (net_irrigation_corn(pre, mean_pre) * pre) 
                ** 2
                + 0.00000121 * (net_irrigation_corn(pre, mean_pre) * pre) 
                ** 3)

   thing_two = 75 # Should be hardcoded for now

   return min(thing_one, thing_two) 


# Execution starts here
init()

# Read precipitation data into a list
rainfall_by_year = get_rainfall()

#Calculate mean precipitation
total_precip = 0
mean_precip = 0
for year in rainfall_by_year:
   total_precip = total_precip + year
mean_precip = total_precip / len(rainfall_by_year)

print("Wheat Irrigation, Wheat Production, ", end = "")
print("Corn Irrigation, Corn Production")
for rainfall in rainfall_by_year:
   wi = net_irrigation_wheat(rainfall, mean_precip) 
   wp = wheat_production(rainfall, mean_precip)
   ci = net_irrigation_corn(rainfall, mean_precip)
   cp = corn_production(rainfall, mean_precip)
   print('{0:2.3f} {1:17.3f} {2:17.3f} {3:17.3f}'.\
         format(wi, wp, ci, cp))

