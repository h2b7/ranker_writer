from src.run import PageDataTree, TREE_ROOT


def test_simple_data():
  data = {"a": 1, "b": 2}
  assert PageDataTree(data).tree_by_key(data, 'c') == None


def test_nested_simple_data():
  data = {"a": 1, "b": 2, "d": {"c": 3}}

  assert PageDataTree(data).tree_by_key(data, 'c') == PageDataTree.join_tree(
    *(TREE_ROOT, 'd', 'c')
  )


def test_simple_data_with_list():
  data = {"a": 1, "b": 2, "d": [{"c": 3}]}

  assert PageDataTree(data).tree_by_key(data, 'c') == PageDataTree.join_tree(
    *(TREE_ROOT, 'd', 'c')
  )


def test_simple_data_with_none():
  data = {"a": 1, "b": None, None: 4, "d": [{"c": 3}]}

  assert PageDataTree(data).tree_by_key(data, 'c') == PageDataTree.join_tree(
    *(TREE_ROOT, 'd', 'c')
  )
