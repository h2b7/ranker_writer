import pytest

from run import PageDataTree, Tree


def test_simple_data():
  data = {"a": 1, "b": 2}
  with pytest.raises(StopIteration):
    assert next(PageDataTree(data).tree_by_key(data, 'c'))


def test_nested_simple_data():
  data = {"a": 1, "b": 2, "d": {"c": 3}}

  assert next(PageDataTree(data).tree_by_key(data, 'c')) == PageDataTree.join_tree(
    tree=PageDataTree.join_tree(Tree.ROOT, 'd'), key='c'
  )


def test_simple_data_with_list():
  data = {"a": 1, "b": 2, "d": [{"c": 3}]}

  assert next(PageDataTree(data).tree_by_key(data, 'c')) == PageDataTree.join_tree(
    tree=PageDataTree.join_tree(Tree.ROOT, 'd'),
    key='c',
    list_index=0
  )


def test_simple_data_with_none():
  data = {"a": 1, "b": None, None: 4, "d": [{"c": 3}]}

  assert next(PageDataTree(data).tree_by_key(data, 'c')) == PageDataTree.join_tree(
    tree=PageDataTree.join_tree(Tree.ROOT, 'd'),
    key='c',
    list_index=0
  )


def test_simple_data_for_noreturn():
  data = {"a": 1, "b": None, None: 4, "d": [{"c": 3}]}

  assert next(PageDataTree(data).tree_by_key(data, 'c', result_to='print')) is None


def test_simple_data_value_with_list_index():
  data = {"a": 1, "b": 2, "d": [{"c": 3}]}

  # 'root -> d -> [0] -> c'
  tree = PageDataTree.join_tree(
    tree=PageDataTree.join_tree(Tree.ROOT, 'd'),
    key='c',
    list_index=0
  )

  assert PageDataTree(data).data_by_tree(tree) == 3
