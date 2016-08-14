from collections import namedtuple
import sys

class Calendar():
  def __init__(self):
    self.event_tree = None

  def clear(self):
    self.event_tree = None

  def add(self, event):
    if self.event_tree is None:
      self.event_tree = IntervalTree(event)
    else:
      self.event_tree.add(event)

  def query(self, t):
    if self.event_tree is None:
      return []
    else:
      return sorted([node.value for node in self.event_tree.query(t)], lambda ev: ev.name)

class BinarySearchTree():
  def __init__(self, value, key=lambda x: x):
    self.key = key
    self.value = value
    self.left = self.right = None

  def add(self, new_val):
    subtree = 'right' if self.key(new_val) > self.key(self.value) else 'left'
    if getattr(self, subtree) is None:
      node = self.__class__(new_val, key=self.key)
      setattr(self, subtree, node)
    else:
      getattr(self, subtree).add(new_val)

Event = namedtuple('Event', ['name', 'start_time', 'finish_time'])

class IntervalTree(BinarySearchTree):
  def __init__(self, event, key=None): # key included for consistency with superclass, but not used
    super().__init__(event, key=lambda ev: ev.start_time)
    self.max = event.finish_time

  def start_time(self):
    return self.value.start_time

  def finish_time(self):
    return self.value.finish_time

  def add(self, event):
    self.max = max(self.max, event.finish_time)
    super().add(event)

  # half-open interval
  # if at least one overlapping interval is present, this finds the one with the earliest start time
  def search(self, t):
    if self.left and self.left.max > t:
      result = self.left.search(t)
      if result:
        return result
    elif self.start_time() <= t < self.finish_time():
      return self
    elif self.right:
      return self.right.search(t)
    else:
      return None

  # not yet efficient at all
  def query(self, t):
    results = set()
    if self.start_time() <= t < self.finish_time():
      results.add(self)
    if self.left:
      results.update(self.left.query(t))
    if self.right:
      results.update(self.right.query(t))
    return results

def main(filename):
  calendar = Calendar()
  with open(filename) as f:
    for line in f:
      output = line.strip()
      tokens = line.split()
      if len(tokens) > 0:
        command = tokens[0]
        if command == "CLEAR":
          calendar.clear()
        elif command == "ADD":
          event = Event(tokens[1], int(tokens[2]), int(tokens[3]))
          calendar.add(event)
        elif command == "QUERY":
          t = int(tokens[1])
          results = [event.name for event in calendar.query(t)]
          output = "QUERY %s: %s" %(t, ' '.join(results))
      print(output)

if __name__ == "__main__":
  if len(sys.argv) > 1:
    main(sys.argv[1])
  else:
    print("Missing required argument!\n usage: python3 calendar.py input_file")
