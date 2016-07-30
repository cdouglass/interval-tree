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
      return sorted([node.value for node in self.event_tree.query(t)], key = lambda ev: ev.name)

class BinarySearchTree():
  def __init__(self, value, key=lambda x: x):
    self.key = key
    self.value = value
    self.left = self.right = self.parent = None

  def add(self, new_val):
    subtree = 'right' if self.key(new_val) > self.key(self.value) else 'left'
    if getattr(self, subtree) is None:
      node = self.__class__(new_val, key=self.key)
      node.parent = self
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

  def query(self, t):
    shadow_maxes = {}
    results = set()

    def max_with_none(lst):
      non_none = [i for i in lst if i is not None]
      if len(non_none) > 0:
        return max(non_none)
      else:
        return None

    # may be None
    def shadow_max(node):
      if not node:
        return None
      elif node.value in shadow_maxes:
        return shadow_maxes[node.value]
      else:
        return node.max

    # half-open interval
    # if at least one overlapping interval is present, this finds the one with the earliest start time
    def shadowed_search(node, t):
      if shadow_max(node.left) and shadow_max(node.left) > t:
        result = shadowed_search(node.left, t)
        if result:
          return result
      elif node.start_time() <= t < node.finish_time() and (node not in results):
        return node
      elif node.right:
        return shadowed_search(node.right, t)
      else:
        return None
     
    next_result = shadowed_search(self, t)
    while next_result:
      results.add(next_result)
      shadow_maxes[next_result.value] = max_with_none([shadow_max(node) for node in [next_result.left, next_result.right] if node])
      current = next_result.parent
      while current:
        candidate_maxes = [shadow_max(node) for node in [current.left, current.right] if node]
        if current.value not in shadow_maxes:
          candidate_maxes.append(current.finish_time())
        shadow_maxes[current.value] = max_with_none(candidate_maxes)
        current = current.parent
      next_result = shadowed_search(self, t)
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
