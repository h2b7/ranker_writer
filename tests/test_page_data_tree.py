from run import PageDataTree, Tree


def test_simple_data():
  data = {"a": 1, "b": 2}
  assert PageDataTree(data).tree_by_key(data, 'c') is None


def test_nested_simple_data():
  data = {"a": 1, "b": 2, "d": {"c": 3}}

  assert PageDataTree(data).tree_by_key(data, 'c') == PageDataTree.join_tree(
    *(Tree.ROOT, 'd', 'c')
  )


def test_simple_data_with_list():
  data = {"a": 1, "b": 2, "d": [{"c": 3}]}

  assert PageDataTree(data).tree_by_key(data, 'c') == PageDataTree.join_tree(
    *(Tree.ROOT, 'd', 'c')
  )


def test_simple_data_with_none():
  data = {"a": 1, "b": None, None: 4, "d": [{"c": 3}]}

  assert PageDataTree(data).tree_by_key(data, 'c') == PageDataTree.join_tree(
    *(Tree.ROOT, 'd', 'c')
  )


def test_simple_data_for_noreturn():
  data = {"a": 1, "b": None, None: 4, "d": [{"c": 3}]}

  assert PageDataTree(data).tree_by_key(data, 'c', result_to='print') is None
