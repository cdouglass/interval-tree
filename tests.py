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
  def test_create_interval_tree(self):
    tree = IntervalTree(Event('ev1', 0, 10))
    self.assertEqual(10, tree.max)
    self.assertIsNone(tree.left)
    self.assertIsNone(tree.right)
    ev2 = Event('ev2', -5, 15)
    tree.add(ev2)
    self.assertEqual(ev2, tree.left.value)
    self.assertEqual(15, tree.max)
    self.assertTrue(isinstance(tree.left, IntervalTree))
    ev3 = Event('ev3', -2, 2)
    tree.add(ev3)
    self.assertEqual(ev3, tree.left.right.value)
    self.assertTrue(isinstance(tree.left.right, IntervalTree))
    self.assertEqual(15, tree.max)
    self.assertEqual(15, tree.left.max)
    self.assertEqual(2, tree.left.right.max)

if __name__ == "__main__":
  unittest.main()
