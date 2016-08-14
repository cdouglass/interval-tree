from collections import namedtuple

class Calendar():
  def __init__(self):
    self.clear()

  def clear(self):
    self.event_tree= None

  def add(event):
    if self.event_tree is None:
      self.event_tree = IntervalTree(event)
    else:
      self.event_tree.add(event)

  def query(t):
    if self.event_tree is None:
      return []
    else:
      return self.event_tree.query(t)

class BinarySearchTree():
  def __init__(self, value, key=lambda x: x):
    self.key = key
    self.value = value
    self.left = self.right = None

  def add(self, new_val):
    subtree = 'right' if self.key(new_val) > self.key(self.value) else 'left'
    if getattr(self, subtree) is None:
      setattr(self, subtree, __class__(new_val, self.key))
    else:
      getattr(self, subtree).add(new_val)

Event = namedtuple('Event', ['name', 'start_time', 'finish_time'])

class IntervalTree(BinarySearchTree):
  def __init__(self, event):
    self.key = lambda ev: ev.start_time
    self.value = event

  def add(self, event):
    pass

  def query(self, t):
    pass


