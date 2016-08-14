from collections import namedtuple
from math import floor, log
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
    self.weight = 1
    self.alpha = 0.75 # arbitrary constant between 0.5 and 1

  def update(self):
    self.weight = 1 + sum([child.weight for child in self.children()])

  def children(self):
    return [node for node in [self.left, self.right] if node]

  # should never be called unless there's a non-weight-balanced ancestor
  def rebalance(self):
    if self.is_weight_balanced():
      self.parent.rebalance()
    else:
      self.rebuild()

  def is_weight_balanced(self):
    child_weights = [child.weight for child in self.children()]
    return max(child_weights) <= self.alpha * self.weight

  def flatten(self):
    left = self.left.flatten() if self.left else []
    right = self.right.flatten() if self.right else []
    return left + [self.value] + right

  def rebuild(self):
    values = self.flatten()
    tree = self.build(values)
    self.value = tree.value
    if tree.left:
      self.left = tree.left
      self.left.parent = self
    if tree.right:
      self.right = tree.right
      self.right.parent = self
    self.update()

  def build(self, values):
    if len(values) == 0:
      return None
    midpoint = int(len(values) / 2)
    root = self.__class__(values[midpoint], self.key)
    left_vals, right_vals = [values[0: midpoint], values[midpoint + 1:]]
    left, right = self.build(left_vals), self.build(right_vals)
    if left:
      root.left = left
      left.parent = root
    if right:
      root.right = right
      right.parent = root
    root.update()
    return root

  def add(self, new_val, size=None, depth=0):
    # while allowing elements with equal keys is compatible with searchability if such elements are only found in each others' left subtree, never in the right, this is not compatible with maintaining a balanced tree
    if self.key(new_val) == self.key(self.value):
      return None
    self.weight += 1
    size = size or self.weight
    is_greater = self.key(new_val) > self.key(self.value)
    if is_greater and self.right:
      self.right.add(new_val, size=size, depth=depth+1)
    elif self.left and not is_greater:
      self.left.add(new_val, size=size, depth=depth+1)
    else:
      node = self.__class__(new_val, key=self.key)
      node.parent = self
      if is_greater:
        self.right = node
      else:
        self.left = node
      if depth + 1 > floor(log(size, 1.0 / self.alpha)):
        self.rebalance()
    self.update()

Event = namedtuple('Event', ['name', 'start_time', 'finish_time'])

class IntervalTree(BinarySearchTree):
  def __init__(self, event, key=lambda ev: [ev.start_time, ev.finish_time, ev.name]):
    super().__init__(event, key=key)
    self.max = event.finish_time

  def update(self):
    super().update()
    self.max = max([self.finish_time()] + [node.max for node in self.children()])

  def start_time(self):
    return self.value.start_time

  def finish_time(self):
    return self.value.finish_time

  def query(self, t):
    shadow_maxes = {}
    results = set()

    def max_with_none(lst):
      non_none = [i for i in lst if i is not None]
      return max(non_none) if non_none else None

    # may be None
    def shadow_max(node):
      if not node:
        return None
      elif node.value in shadow_maxes:
        return shadow_maxes[node.value]
      else:
        return node.max

    # half-open interval
    # if at least one overlapping interval is present, this finds the one furthest left in the tree, ie with the earliest start time
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
      shadow_maxes[next_result.value] = max_with_none([shadow_max(node) for node in next_result.children()])
      current = next_result.parent
      while current:
        candidate_maxes = [shadow_max(node) for node in [current.left, current.right] if node]
        if current not in results:
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
