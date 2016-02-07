#!/usr/bin/env python

import requests
import csv
import re


fcc_data_url = "https://consumercomplaints.fcc.gov/hc/theme_assets/513073/200051444/Telemarketing_RoboCall_Weekly_Data.csv"


def _download_unwanted_call_log(fcc_data_url):
    """
    Data is pulled from https://consumercomplaints.fcc.gov/hc/en-us/articles/205239443-Data-on-Unwanted-Calls
    The headers are:
     [0]   Phone Issues: The type of unwanted call the consumer is complaining about.
     [1]   Time of Issue: The time that the consumer indicates the unwanted call occurred.
     [2]   Caller ID Number: The telephone number the consumer indicates appeared on their caller ID.
     [3]   Advertiser Business Phone Number: The telephone number the consumer indicates the advertiser provided during the call.
     [4]   Type of Call or Message (Robocalls): The type of unwanted robocall the consumer identified (abandoned, autodialed live voice, prerecorded voice, or text message).
     [5]   Type of Call or Message (Telemarketing): The type of unwanted telemarketing call the consumer identified (abandoned, email, live voice, prerecorded voice, or text message).
     [6]   State: The state that the consumer that received the call is located in.
     [7]   Date (Ticket Date of Issue): The date the consumer states the indicated violation occurred.
     [8]   Date (Ticket Created): The date the complaint was submitted to the FCC.
    """
    filename = fcc_data_url.split("/")[-1]
    r = requests.get(fcc_data_url)
    call_log = []
    for row in r.iter_lines():
        call_log.append(row)
    return filename, call_log


def _scrub_telephone_numbers(call_log):
    robo_caller_tn = []
    tmp_file = csv.reader(call_log)
    for row in tmp_file:
        try:
            if row[2]:
                scrubbed_number = re.sub("-", "", row[2])
                if len(scrubbed_number) > 9:
                    robo_caller_tn.append(scrubbed_number)
        except:
            pass  # Silent fail
    return robo_caller_tn


def _write_tn_list(phone_number_list, filename):
    with open(filename, "w") as f:
        for tn in phone_number_list:
            f.write(tn)
            f.write("\n")
    return 0


filename, call_log = _download_unwanted_call_log(fcc_data_url)
phone_number_list = _scrub_telephone_numbers(call_log)
_write_tn_list(phone_number_list, filename)
print "Your robo list has been written to {}".format(filename)
