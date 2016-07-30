Date range queryer
===============

Design a data structure that keeps track of events on a calendar. The data structure should support the following operations:

- ADD: add a new event to the calendar
- QUERY: Given a point in time, return the list of events that overlap with that point
- CLEAR: clear the calendar of all events

Events have a name (string), start time in seconds (int), and end time in seconds (int). Your solution should scale efficiently with the number of events in the calendar (fast insertion, fast query for 10,000,000s of events of varying lengths across a period of years). A QUERY operation that takes O(n) where n is the number of events in the calendar is not considered efficient. For a given point in time, there typically are no more than 20 events that overlap that point.

Code
----

Write a command-line program that takes as input a file of calendar commands. The commands can take the following form:

```
ADD $ID $START $END
QUERY $TIME

CLEAR
```

$ID is an alphanumeric string with no spaces that uniquely identifies a calendar event. $START and $END are the integer start and end [inclusive, exclusive) times of the event, and $TIME specifies an integer time.

- For every ADD event, your program should echo the ADD event to stdout.
- For every QUERY event, your program should print "QUERY $TIME: ${space-delimited list of IDs of events that overlap the query time, in alphabetical order}".
- For every CLEAR event, your program should print "CLEAR".
- If the program encounters an empty line in the input, then it should print an empty line.

Deliverables
----------

1. The source code for the program described above
1. A README containing the following:
   1. Instructions for compiling and running the program
   1. Runtime and space analysis for each operation (ADD, QUERY, CLEAR)
   1. Justification for why the program satisfies the performance requirements

You can use any programming language or 3rd party libraries you like. However, you should not collaborate directly with anyone else to write the program. You can refer to the sample input and expected output files to debug your program, but do not assume this test case is comprehensive and do not rely on this to test performance.
