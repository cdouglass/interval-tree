#Calendar#

I used a binary search tree of events, ordered by start time and augmented with an additional field, max. The max field of a node contains the latest end time of all events in the tree rooted at that node.

In querying for a given time, I use a search process that always finds the overlapping event that is farthest left in the tree, i.e., the one with the earliest start date. Each time a match is found, I update a dictionary of shadow values for the max fields, matching each event to the max its node would have if the newly matched node were missing from the calendar.

The base search tree is a scapegoat tree without deletion, which means that it is guaranteed to remain height-balanced - its height will always be O(log n). No duplicate elements are allowed.

##Usage##
Make sure python 3 is installed.

To take a file `input_file` as input, run
```
$ python3 calendar.py input_file
```

To run the test suite, run
```
$ python3 tests.py
```

##Complexity##

###Add###
####Time####
Adding an element requires navigating down the tree until an empty leaf slot is found. Most of the time a constant number of operations (comparing start times, updating max) is performed at each level, so this will take time proportional to the height of the tree, which is O(log n). The exception is when adding the new node violates the height-balance property of the scapegoat tree. In this case, the deepest ancestor of that node that is not weight-balanced will be selected as a scapegoat and the subtree rooted at that node will be entirely rebuilt.

Rebuilding a subtree takes time proportional to the size of that subtree. Therefore the worst-case time to add an element is O(n). However a rebuild will be required so rarely that this will not affect the average asymptotic complexity of the add operation.

####Space####
O(1) additional space will be required to store the new event in the calendar. While the event is being added, at each level of the tree a new call to `add` will use a constant amount of stack space as Python does not optimize tail calls. This gives us O(h) = O(log n) space usage. In the rare event that a rebuild is required, the entire subtree being rebuilt will be flattened and all its values stored in memory, giving worst-case O(n) additional space usage.



##Complexity##

###Add###
####Time####
Adding an element requires navigating down the tree until an empty leaf slot is found. Most of the time a constant number of operations (comparing start times, updating max) is performed at each level, so this will take time proportional to the height of the tree, which is O(log n). The exception is when adding the new node violates the height-balance property of the scapegoat tree. In this case, the deepest ancestor of that node that is not weight-balanced will be selected as a scapegoat and the subtree rooted at that node will be entirely rebuilt.

Rebuilding a subtree takes time proportional to the size of that subtree. Therefore the worst-case time to add an element is O(n). However a rebuild will be required so rarely that this will not affect the average asymptotic complexity of the add operation.

####Space####
O(1) additional space will be required to store the new event in the calendar. While the event is being added, at each level of the tree a new call to `add` will use a constant amount of stack space as Python does not optimize tail calls. This gives us O(h) = O(log n) space usage. In the rare event that a rebuild is required, the entire subtree being rebuilt will be flattened and all its values stored in memory, giving worst-case O(n) additional space usage.

###Query###
####Time####
If there are k matching events, the search procedure will run k+1 times. As with `add`, each search will take time and space at most proportional to the height of the tree - O(h). Updating the shadow maximum values also involves a constant number of operations for each ancestor of the matched event, so doesn't change the asymptotic complexity. In total runtime will be O(k * h).

####Space####
As with `add`, each of the k+1 searches will require space proportional to the height of the tree. Since the query itself is not recursive, stack usage will not increase in k. The dictionary of shadow values, however, will potentially use constant space for each ancestor of each of the k query results, giving O(k * h) again.

###Clear###
This assigns the calendar's event tree to None. The original tree object is not handled at all (though since there will be no remaining references to it, the garbage collector will deallocate it) so both time and space requirements are O(1).
