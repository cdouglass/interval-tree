from calendar import BinarySearchTree, Event, IntervalTree
from random import randint
import unittest

class TestBinarySearchTree(unittest.TestCase):
  def test_create_bst_with_duplicate(self):
    tree = BinarySearchTree(5)
    self.assertIsNone(tree.right)
    self.assertIsNone(tree.left)
    for v in [3, 5, 6]:
      tree.add(v)
    self.assertEqual(5, tree.value)
    self.assertEqual(6, tree.right.value)
    self.assertEqual(3, tree.left.value)
    self.assertEqual(5, tree.left.right.value)

  def test_bst_with_custom_comparator(self):
    tree = BinarySearchTree([3, 2, 1], lambda lst: lst[-1])
    lists = [[1, 2, 3, 4, 5], [0, 0, 10], [2, 0]]
    for lst in lists:
      tree.add(lst)
    self.assertEqual(lists[0], tree.right.value)
    self.assertEqual(lists[1], tree.right.right.value)
    self.assertEqual(lists[2], tree.left.value)

class TestIntervalTree(unittest.TestCase):

  def setUp(self):
    self.ev1 = Event('ev1', 0, 10)
    self.ev2 = Event('ev2', -5, 15)
    self.ev3 = Event('ev3', -2, 2)
    self.ev4 = Event('ev4', 11, 13)
    self.tree = IntervalTree(self.ev1)
    self.tree.add(self.ev2)
    self.tree.add(self.ev3)
    self.tree.add(self.ev4)

  def test_create_interval_tree(self):
    tree = IntervalTree(self.ev1)
    self.assertEqual(10, tree.max)
    self.assertIsNone(tree.left)
    self.assertIsNone(tree.right)
    tree.add(self.ev2)
    self.assertEqual(self.ev2, tree.left.value)
    self.assertEqual(15, tree.max)
    self.assertTrue(isinstance(tree.left, IntervalTree))
    tree.add(self.ev3)
    self.assertEqual(self.ev3, tree.left.right.value)
    self.assertTrue(isinstance(tree.left.right, IntervalTree))
    self.assertEqual(15, tree.max)
    self.assertEqual(15, tree.left.max)
    self.assertEqual(2, tree.left.right.max)

  def test_unsuccessful_query(self):
    self.assertEqual(set(), self.tree.query(20))

  def test_query_with_single_result(self):
    self.assertEqual(set([self.ev2]), {node.value for node in self.tree.query(10)})
    self.assertEqual(set([self.ev2]), {node.value for node in self.tree.query(-3)})

  def test_query_with_two_results(self):
    self.assertEqual(set([self.ev1, self.ev2]), {node.value for node in self.tree.query(3)})

  def test_query_with_three_results(self):
    self.assertEqual(set([self.ev1, self.ev2, self.ev3]), {node.value for node in self.tree.query(1)})

  def test_query_with_result_in_right_subtree(self):
    self.assertEqual(set([self.ev2, self.ev4]), {node.value for node in self.tree.query(12)})

  def test_another_query(self):
    a, b, c, d, e = [Event('a', 0, 100), Event('b', 50, 60), Event('c', 10, 90), Event('d', 85, 110), Event('e', 45, 55)]
    tree = IntervalTree(a)
    for node in [b, c, d, e]:
      tree.add(node)
    self.assertEqual(set([a, b, c, e]), {node.value for node in tree.query(50)})

class FuzzIntervalTree(unittest.TestCase):
  # t > 0
  def make_interval_set(self, t, n_matches, n_nonmatches):
    top = 10000
    events = []
    for i in range(n_matches):
      start = randint(0, t)
      end = randint(t, top)
      name = "match_%s" %i
      events.append(Event(name, start, end))
    for j in range(n_nonmatches):
      if randint(0, 1):
        start = randint(0, t - 1)
        end = randint(start, t - 1)
      else:
        start = randint(t, top)
        end = randint(start, top)
      name = "nonmatch_%s" %j
      events.append(Event(name, start, end))
    return events

  def test_query_counts(self):
    t = 5000
    events = self.make_interval_set(t, 4, 3)
    tree = IntervalTree(events[0])
    for event in events[1:]:
      tree.add(event)
    matches = tree.query(t)
    for match in matches:
      print(match.value.name)
    print("...........")
    for event in events:
      print("%s %s %s" %(event.name, event.start_time, event.finish_time) )
    self.assertEqual(4, len(matches))

if __name__ == "__main__":
  unittest.main()
