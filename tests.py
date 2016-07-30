from calendar import BinarySearchTree, Event, IntervalTree
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
#        5
#      /   \
#     3     6
#       \
#        5

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

if __name__ == "__main__":
  unittest.main()
