#!/usr/bin/env python3

import os
import sys

# Rough script to find where data is being stored/if data is available on the Mt Pleasant network.
# Usage:

# ./findMyData.py <experiment_code> <station_string>

# e.g. './findMyData.py aua090 HbKeYgIsHt'

# Please note - this script is designed to work on the Mt Pleasant network and 
# assumes ssh keys and aliases are setup.

# Manually set the machines you want to search
data_machines_list = ['flexbuf', 'flexbuf-2hb', 'flexbuffhb', 'vc1', 'vc2', 'vc3', 'vc4', 'vc5', 'vc6', 'vc7', 'vc8']

def vbs_search(experiment, station, data_machines):
    scattered_station_lists = ['Hb', 'Ke']
    if station in scattered_station_lists:
        search_string = experiment.lower() + '_' + station.lower() + '*'
        for machine in data_machines:
            vbs_search_command = 'ssh ' + machine + ' vbs_ls ' + search_string
            vbs_query = os.popen(vbs_search_command).read()
            if len(vbs_query) > 2:
                print(experiment + ' ' + station + ' scattered recordings found on ' + machine + '\n')
                return True
                
                
def ls_search(experiment, station, data_machines):
    # Define the locations that typically house data
    data_locations = ['/mnt/*/AUSTRAL/', '/disk3/']
    for machine in data_machines:
        for loc in data_locations:
            ls_search_command = 'ssh ' + machine + ' ls -d ' + loc + experiment.lower() + station.lower() + ' 2>&1' 
            ls_query = os.popen(ls_search_command).read().split('\n')
            if 'cannot access' not in ls_query[0]:
                print(experiment + ' ' + station + ' data found on ' + machine + ' at ' + ls_query[0] + '\n')
                return True
    print('No data for ' + station + ' found.' + '\n')


def main(experiment, station_string):
    # Break station string into a list of 2 character station codes
    station_list = [station_string[idx:idx + 2] for idx in range(0, len(station_string), 2)]
    print('') # give some space
    for stat in station_list:
        print(stat + ':')
        vbs = vbs_search(experiment, stat, data_machines_list)
        if vbs == True: # If Hb data has been found, skip the ls_search
            continue
        else:
            ls_search(experiment, stat, data_machines_list)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
