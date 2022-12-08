#!/usr/bin/env python 

# Python re-write of the Log2Clock.m script - should perform identically.
# I eventually want to combine this with Log2clock.arg.sh - so that it is all contained in one script.

import numpy as np
import matplotlib.pyplot as plt
from math import floor

def main():
	# Load data
    fmout_data = np.loadtxt('/tmp/fmout')
    fmoutepoch_data = np.loadtxt('/tmp/fmoutepoch', dtype='str')
    # Determine ref epoch
    ref_epoch = int(fmoutepoch_data[1]) + float(fmoutepoch_data[2])/24.0
    # Convert fmout timestamps to UT hour values
    UT_hour =  fmout_data[:,1] + fmout_data[:,2]/24.0 + fmout_data[:,3]/1440.0 + fmout_data[:,4]/86400.0 - ref_epoch
    fmout_value = fmout_data[:,5]
    # Generate linear fit to UT vs fmout values
    fit_params = np.polyfit(UT_hour*86400, fmout_value, 1)
    # setup variables for format string
    station_str = fmoutepoch_data[3].capitalize()
    year_str = int(fmoutepoch_data[0])
    doy_str = int(fmoutepoch_data[1])
    hour_str = int(float(fmoutepoch_data[2]))
    min_str = int((float(fmoutepoch_data[2])-floor(float(fmoutepoch_data[2])))*60)
    clockoff_str = fit_params[1]*1e6
    clockrate_str = fit_params[0]*1e6
    # write out string to fmout.fmt file
    format_string = f"##### VEX Format #####\n\tdef {station_str}: clock_early={year_str:.0f}y{doy_str:.0f}d{str(hour_str).zfill(2)}h{str(min_str).zfill(2)}m00s : {-clockoff_str:.4e}  usec  :{year_str:.0f}y{doy_str:.0f}d{str(hour_str).zfill(2)}h{str(min_str).zfill(2)}m00s : {-clockrate_str:.4e} ; enddef;\n\n##### v2d Format #####\nANTENNA {station_str} {{\nclockOffset={-clockoff_str:.4e}\nclockRate={-clockrate_str:.4e}\nclockEpoch={year_str:.0f}y{doy_str:.0f}d{str(hour_str).zfill(2)}h{str(min_str).zfill(2)}m00s\n}}\n"
    with open('/tmp/fmout.fmt', 'w') as format_file:
        format_file.writelines(format_string)
    # generate post script figure
    plt.figure(figsize=(9, 7))
    plt.scatter(UT_hour, fmout_value, marker='o', s=10, color='k')
    plt.plot(UT_hour, np.polyval(fit_params, UT_hour*86400), color='r')
    plt.xlabel('Hours from UT reference time')
    plt.ylabel('Clock offset (sec)')
    plt.axvline(x=0, linestyle='--', linewidth=0.5, c='k')
    plt.savefig('/tmp/fmout.ps', dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    main()
