# The CDA+ program is hosting weekly meetings. Each CDA+ should attend one meeting per week. 
# However, each CDA+ has different availability for when they can meet. 

# Problem: Given a timetable of the availability of all CDA+ students,
# find the minimal number of meetings needed so that all CDA+ students can attend at least one.
# If there are multiple ways to have this minimal number of meetings, list all of the options.

# this script takes in a downloaded CSV timetable from needtomeet.com.

# ----------------------------------------------------------------------------------------- #

# Change the below filepath to the name of the csv file. 
# If it doesn't work, rename the document using only letters (no spaces, no punctuation) and retry.
FILE = "NeedToMeet – Autumn Quarter CDA+ Meeting.csv"

import pandas

timetable = pandas.read_csv(filepath_or_buffer=FILE, header=[0,1,2], keep_default_na=False)
timetable = timetable.drop(index=0).reset_index(drop=True)

times_that_work = []
one_left_out = []

def get_unavailable(col, attendees):
    return [attendee for attendee in attendees if not timetable.iat[attendee, col]]

def rec_find_meetings(meetings, meetings_left, attendees):
    if not attendees: 
        times_that_work.append(meetings)
    if meetings_left == 0:
        if len(attendees) == 1:
            one_left_out.append(meetings)
        return
    for i in range(meetings[-1] + 1, len(timetable.columns)):
        rec_find_meetings(meetings + [i], meetings_left - 1, get_unavailable(i, attendees))

def find_meetings(meetings_left):
    attendees = list(range(0, len(timetable) - 2))
    for i in range(2, len(timetable.columns)):
        rec_find_meetings([i], meetings_left - 1, get_unavailable(i, attendees))

min_meetings = 0

while not times_that_work:
    min_meetings += 1
    find_meetings(min_meetings)

responses = timetable.iat[len(timetable) - 1, 0]

print("\n" + responses + "\n")

def lookup_meeting_time(col):
    time = timetable.columns[col]
    date = time[0]
    start = time[1]
    end = time[2]
    return date + " from " + start + " to " + end

def print_times(all_times):
    num_options = len(all_times)
    print("There are", num_options, "choices for scheduling multiple meetings:\n")
    for i in range(num_options):
        print("Option", str(i + 1) + ":")
        for meeting in all_times[i]:
            print("  - " + lookup_meeting_time(meeting))
        print()
    print()

print_times(times_that_work)
