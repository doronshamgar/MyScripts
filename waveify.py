#!/usr/bin/python3
##########################################
# Waveify is a visualization tool for log data.
#
# Usages:
# 1. <some command that outputs the DATASET> | waveify.py
# 2. waveify.py <DATASET_file>
#
# Input:
# the format for each DATASET line is expected to be:
# <time[decimal]> <type[string]> [<name[string]>]
#
# Remarks: 
#   1. points can be out-of-order (in relation to time)
#   2. points will be arranged by <type> index 
#   3. a different step-line will be created in the plot for each <type>
#   4. <name> is optional. will appear on graph point if exist
#
# Example of input DATASET:
#  1 bar   
#  3 foo p1
#  2 bar p2
#
# the resulting plot will contain 2 step-lines, 1 for <bar> and 1 for <foo>.
# the <bar> line will contain a pulse in time 1 and a pulse in time 2 which will also contain <p2> string.
# the <foo> line will contain a pulse in time 3 with <p1> string.
#
##########################################
import matplotlib.pyplot as plt
import numpy as np
import sys, argparse, re, fileinput

parser = argparse.ArgumentParser(description="WAVEIFY - a visualization tool for log data")
parser.add_argument('-f','--files', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
args = parser.parse_args()

#initiate a key-indexed-lists database
database = {}
max_time = 0

def my_lines(ax, pos, *args, **kwargs):
    if ax == 'x':
        for p in pos:
            plt.axvline(p, *args, **kwargs)
    else:
        for p in pos:
            plt.axhline(p, *args, **kwargs)

def parse_input_file():
    global max_time
    
    for line in fileinput.input(args.files):
        m = re.match(r"(\d+)\s+(\S+)\s+(\S*)", line)
        if m:
         #database.append([m.group(1), m.group(2)])
         if m.group(2) not in database:
             database[m.group(2)] = []
         database[m.group(2)].append([m.group(1),m.group(3)])
         if (int(m.group(1)) > max_time):
            max_time = int(m.group(1))
        else:
            print("error parsing line: " + line)
            break

if __name__ == '__main__':
   
   #keyed-list of lists
   waves = {} 
   waves_rep = {}
   t = {}
   parse_input_file()

   for index, (key,val) in enumerate(database.items()):
       #create the wave base (an array of zeros)   
       waves[key] = [0] * (max_time+1)   
       #add the points to the wave
       for p in val:
           waves[key][int(p[0])] = 1   
       #duplicate points for the square wave
       waves_rep[key] = np.repeat(waves[key], 2)
       #create the time scale
       t[key] = 0.5 * np.arange(len(waves_rep[key]))
       #add the line and wave to the plot
       my_lines('y', [0 + (index*2)], color='.5', linewidth=2)
       plt.step(t[key], waves_rep[key]+(index*2), 'r', linewidth = 2, where='post')
       plt.text(0,-0.5+index*2,key)
       for p in val:
           plt.text(int(p[0]),0.5+index*2,p[1])

   #set the y limit of the plot according to the number of waves displayed
   plt.ylim([-1,2*len(database)])
   plt.show()
