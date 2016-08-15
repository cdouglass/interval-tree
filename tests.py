from calendar import BinarySearchTree, Event, IntervalTree
from random import randint, seed, shuffle
import unittest

class TestBinarySearchTree(unittest.TestCase):
  def _test_create_bst_with_duplicate(self):
    tree = BinarySearchTree(5)
    self.assertIsNone(tree.right)
    self.assertIsNone(tree.left)
    for v in [3, 5, 6]:
      tree.add(v)
    self.assertEqual(5, tree.value)
    self.assertEqual(6, tree.right.value)
    self.assertEqual(3, tree.left.value)
    self.assertEqual(5, tree.left.right.value)

  def _test_bst_with_custom_comparator(self):
    tree = BinarySearchTree([3, 2, 1])
    setattr(tree, 'key', lambda lst: lst[-1])
    lists = [[1, 2, 3, 4, 5], [0, 0, 10], [2, 0]]
    for lst in lists:
      tree.add(lst)
    self.assertEqual(lists[0], tree.right.value)
    self.assertEqual(lists[1], tree.right.right.value)
    self.assertEqual(lists[2], tree.left.value)

  def _test_shrunken(self):
    new_tree = tree.build(vals)
    self.assertEqual(sorted(vals), sorted(new_tree.flatten()))

  def test_build_adds_every_element_once(self):
    tree = BinarySearchTree(0)
    vals = [5, 0, 0, 5, 0, 1, 5, 5, 5, 0, 5, 5, 0, 2]
    t = tree.build(vals)
    self.assertEqual(sorted(vals), sorted(t.flatten()))

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

  def _test_create_interval_tree(self):
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

  def _test_unsuccessful_query(self):
    self.assertEqual(set(), self.tree.query(20))

  def _test_query_with_single_result(self):
    self.assertEqual(set([self.ev2]), {node.value for node in self.tree.query(10)})
    self.assertEqual(set([self.ev2]), {node.value for node in self.tree.query(-3)})

  def _test_query_with_two_results(self):
    self.assertEqual(set([self.ev1, self.ev2]), {node.value for node in self.tree.query(3)})

  def _test_query_with_three_results(self):
    self.assertEqual(set([self.ev1, self.ev2, self.ev3]), {node.value for node in self.tree.query(1)})

  def _test_query_with_result_in_right_subtree(self):
    self.assertEqual(set([self.ev2, self.ev4]), {node.value for node in self.tree.query(12)})

  def _test_another_query(self):
    a, b, c, d, e = [Event('a', 0, 100), Event('b', 50, 60), Event('c', 10, 90), Event('d', 85, 110), Event('e', 45, 55)]
    tree = IntervalTree(a)
    for node in [b, c, d, e]:
      tree.add(node)
    self.assertEqual(set([a, b, c, e]), {node.value for node in tree.query(50)})

  def _test_one_more(self):
    events = [Event('a', 4354, 5527), Event('b', 3016, 5486), Event('c', 683, 6450), Event('d', 1375, 6181), Event('e', 9301, 9850), Event('f', 1128, 2945), Event('g', 7375, 8347)]
    tree = IntervalTree(events[0])
    for ev in events[1:]:
      tree.add(ev)
    self.assertEqual(set(['a', 'b', 'c', 'd']), {node.value.name for node in tree.query(5000)})


class FuzzIntervalTree(unittest.TestCase):
  # t > 0
  def make_interval_set(self, t, n_matches, n_nonmatches, top=10000):
    events = []
    for i in range(n_matches):
      start = randint(0, t)
      end = randint(t + 1, top)
      name = "match_%s" %i
      events.append(Event(name, start, end))
    for j in range(n_nonmatches):
      if randint(0, 1):
        start = randint(0, t - 1)
        end = randint(start, t - 1)
      else:
        start = randint(t + 1, top)
        end = randint(start + 1, top + 1)
      name = "nonmatch_%s" %j
      events.append(Event(name, start, end))
    shuffle(events)
    return events

  def _randomly_test_query_counts(self):
    t = randint(1, 9999)
    match_count = randint(0, 200)
    nonmatches = randint(0, 200)
    events = self.make_interval_set(t, match_count, nonmatches)
    if len(events) > 0:
      tree = IntervalTree(events[0])
      newtree = tree.build(events)
      matches = newtree.query(t)
      self.assertEqual(match_count, len(matches))

  def _test_query_counts(self):
    #seed(34235251)
    for i in range(1000):
      self.randomly_test_query_counts()

  def _test_querying_densely_overlapping_tree(self):
    for i in range(1000000):
      new_seed = randint(0, i)
      seed(new_seed)
      top = 10
      t = randint(1, top - 1)
      match_count = randint(1, top)
      nonmatches = randint(1, top)
      events = self.make_interval_set(t, match_count, nonmatches, top)
      if len(events) > 0:
        tree = IntervalTree(events[0])
        newtree = tree.build(events)
        matches = newtree.query(t)
        try:
          self.assertEqual(match_count, len(matches))
        except:
          print("failed when seeded with %s" %new_seed)
          print("%s, %s, %s" %(t, match_count, nonmatches))
          for ev in events:
            print("%s, %s, %s" %(ev.name, ev.start_time, ev.finish_time))
          raise

  def _test_even_smaller_failure(self):
    t = 9
    tups = [['nonmatch_4', 1, 1], ['nonmatch_2', 10, 11], ['match_2', 3, 10], ['match_3', 0, 10], ['nonmatch_5', 10, 11], ['match_4', 2, 10], ['nonmatch_1', 5, 6], ['nonmatch_6', 10, 11], ['nonmatch_9', 4, 5], ['nonmatch_3', 6, 8], ['match_0', 7, 10], ['nonmatch_0', 10, 11], ['nonmatch_8', 5, 7], ['nonmatch_7', 10, 11], ['match_1', 5, 10]]
    events = [Event(*tup) for tup in tups]
    tree = IntervalTree(events[0])
    newtree = tree.build(events)
    matches = newtree.query(t)
    self.assertEqual(5, len(matches))

  def _test_smaller_failure(self):
    seed(323840845)
    randint(1, 99)
    randint(0, 63)
    randint(0, 63)
    t = 99
    match_count = 48
    nonmatches = 52
    events = self.make_interval_set(t, match_count, nonmatches, 100)
    if len(events) > 0:
      tree = IntervalTree(events[0])
      newtree = tree.build(events)
      matches = newtree.query(t)
      self.assertEqual(match_count, len(matches))

  def _test_smaller_failure(self):
    seed(323840845)
    randint(1, 99)
    randint(0, 63)
    randint(0, 63)
    t = 99
    match_count = 48
    nonmatches = 52
    events = self.make_interval_set(t, match_count, nonmatches, 100)
    if len(events) > 0:
      tree = IntervalTree(events[0])
      newtree = tree.build(events)
      matches = newtree.query(t)
      self.assertEqual(match_count, len(matches))
 
  def _test_query_with_dense_overlap(self):
    new_seed = 946792606
    top = 200
    seed(new_seed)
    t = randint(1, top - 1)
    match_count = randint(0, 127)
    nonmatches = randint(0, 170)
    events = self.make_interval_set(t, match_count, nonmatches, top)
    if len(events) > 0:
      tree = IntervalTree(events[0])
      newtree = tree.build(events)
      matches = newtree.query(t)
      self.assertEqual(match_count, len(matches))


if __name__ == "__main__":
  unittest.main()
