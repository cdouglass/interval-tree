#Calendar#

I used a binary search tree of events, ordered by start time and augmented with an additional field, max. The max field of a node contains the latest end time of all events in the tree rooted at that node.

In querying for a given time, I use a search process that finds the matching event with the earliest start date. Each time a match is found, I update a dictionary of shadow values for the max fields, matching each event to the max its node would have if the newly matched node were missing from the calendar.

##Usage##
Install python3 if needed, then run
```
$ python3 calendar.py input.txt
```

##Complexity##

###Add###
####Time####
Adding an element requires navigating down the tree until an empty leaf slot is found. A constant number of operations (comparing start times, updating max) is performed at each level, so this will take time proportional to the depth of the tree. In the average case we expect the tree to be more or less balanced, having height O(log n) where n is the number of events stored in the calendar. Worst-case runtime, when the tree is completely unbalanced, will be O(n). Hereafter I will describe this as O(h).
####Space####
O(1) additional space will be required to store the new event in the calendar. While the event is being added, at each level of the tree a new call to `add` will use a constant amount of stack space as Python does not optimize tail calls. This gives us O(h) space usage.

###Query###
####Time####
If there are k matching events, the search procedure will run k+1 times. As with `add`, each search will take time and space at most proportional to the height of the tree - O(h). Updating the shadow maximum values also involves a constant number of operations for each ancestor of the matched event, so doesn't change the asymptotic complexity. In total runtime will be O(k * h).
####Space####
As with `add`, each of the k+1 searches will require space proportional to the height of the tree. Since the query itself is not recursive, stack usage will not increase in k. The dictionary of shadow values, however, will potentially use constant space for each ancestor of each of the k query results, giving O(k * h) again.

###Clear###
This assigns the calendar's event tree to None. The original tree object is not handled at all (though since there will be no remaining references to it, the garbage collector will deallocate it) so both time and space requirements are O(1).
