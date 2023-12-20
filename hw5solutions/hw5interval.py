import matplotlib.pyplot as plt
import random
from operator import itemgetter

NUM_EVENTS = 200

# Sort by earliest finish time
# create ans array. add event that finishes first
# iterate thru sortedEventList. 
# if eventList at i (next earliest finish time in the list) has start time 
#equal to or greater than finish time of last element in ans[], then append to ans.
# Otherwise i++
# return ans[]
def first_finish(events):
    # augmented uses a list of tuples: (index, start time, end time)
    augmented = [(i,events[i][0],events[i][1]) for i in range(len(events))]
    # sortedList takes in a list and sorts it by finish time, ascending
    sortedList = sorted(augmented, key = itemgetter(2))
    # ans will be the list containing all the tuples
    ans = [sortedList[0]]
    # ffIndicies gets all the indices of ans. first_finish() will return this list
    ffIndices = [sortedList[0][0]]
    #print("ffIndices: "+str(ffIndices))
    i = 1
    # If the start time of the current event starts later the previous one, then append to ans
    # If it interferes then move onto the next index
    while i < NUM_EVENTS:
        #print(i)
        if(sortedList[i][1] > ans[len(ans)-1][2]):
            ans.append(sortedList[i])
            ffIndices.append(sortedList[i][0])
        i += 1
    return ffIndices
    

# (index, start time, end time, duration)
# sort by duration, ascending
# create ans array. add event with smallest duration to ans
# loop thru sortedEventList. nest: loop through ans[]. if next event with smallest
#duration doesnt interfere with any events in ans[], then append to ans[]
# Otherwise i++
# return ans
def shortest_duration(events):
    # Every tuple in augmented contains an extra value: the duration
    augmented = [(i,events[i][0],events[i][1], events[i][1]-events[i][0]) for i in range(len(events))]
    # sort augmented by the duration of the events, ascending. Store in sortedList
    sortedList = sorted(augmented, key = itemgetter(3))
    # First item in the final list will always contain the 1st element. Insert here
    ans = [sortedList[0]]
    # ssIndicies gets all the indices of the final list. shortest_duration will return this list
    sdIndices = [sortedList[0][0]]
    i = 1
    # Loop thru sortedList. Inside the loop, loop thru ans.
    while i < NUM_EVENTS:
        noConflicts = True
        j = 0
        # For every event in sortedLsit, if it doesn't interfere with any event in ans, then append to ans
        while j < len(ans) and noConflicts:
            if( not (sortedList[i][2] < ans[j][1] or ans[j][2] < sortedList[i][1])):
                noConflicts = False
            j += 1
        if(noConflicts):
            ans.append(sortedList[i])
            # Also append the index to the final answer
            sdIndices.append(sortedList[i][0])
        i+=1
    return sdIndices         


# (index, start time, end time, conflicts)
# Use getNumConflicts() to get number of conflicts for every element
# Include in augmented list
# Sort but conflicts, ascending
# create ans array. add event with least conflicts to ans[]
# loop thru sortedEventList. nest: loop through ans[]. if next event with least
#conflicts doesnt interfere with any events in ans[], then append to ans[]
# Otherwise i++
# return ans
def least_conflicts(events):
    # Every tuple in augmented contains an extra value: number of other events it conflicts with.
    augmented = [(i,events[i][0],events[i][1], getNumOfConflicts(i, events)) for i in range(len(events))]
    # Sort the list by number of conflicts, ascending
    sortedList = sorted(augmented, key = itemgetter(3))
    # ans will contain the events for the final answer. lcIndices contains the indices 
    ans = [sortedList[0]]
    lcIndices = [sortedList[0][0]]
    i = 1
    # Loop thru the sorted list. Within the loop, loop thru ans
    while i < NUM_EVENTS:
        noConflicts = True
        j = 0
        # For each event in sortedList, if it doesn't conflict with events in ans, then append to ans
        while j < len(ans) and noConflicts:
            if( not (sortedList[i][2] < ans[j][1] or ans[j][2] < sortedList[i][1])):
                noConflicts = False
            j += 1
        if(noConflicts):
            ans.append(sortedList[i])
            # Also append the index too for the final answer.
            lcIndices.append(sortedList[i][0])
        i += 1
    return lcIndices

# Takes in an element and events list. Returns the total number of other events it conflicts with.
def getNumOfConflicts(idx, events):
    conflicts = 0
    for i in range(len(events)):
        if( not (events[i][1]) < events[idx][0] or events[idx][1] < events[i][0]):
            conflicts += 1
    return conflicts


#proposed = [(420, 480), (420, 510), (450, 550), (480, 570), (510, 540), (540, 570), (540, 630), (570, 630)]

proposed = []
for i in range(NUM_EVENTS):
    # start between 7am and 6pm. 7am is 420 min into the day.
    st = random.randint(420,1080)
    # duration varies from 30 minutes to 4 hours
    dur = random.randint(30,240)
    proposed.append((st,st+dur))

ff_picks = first_finish(proposed)
print("first_finish scheduled "+str(len(ff_picks)))

sd_picks= shortest_duration(proposed)
print("shortest_duration scheduled "+str(len(sd_picks)))

lc_picks = least_conflicts(proposed)
print("least_conflicts scheduled "+str(len(lc_picks)))


colors = ['gray']*NUM_EVENTS
for label in ff_picks:
    colors[label] = 'red'

y = range(len(proposed))
height = [e-s for (s,e) in proposed]
bottoms = [s for (s,e) in proposed]
plt.bar(y, height, width=0.5, bottom=bottoms, align='center', color=colors)
plt.xticks([],[])
plt.show()





