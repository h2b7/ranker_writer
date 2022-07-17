import os
import json
import argparse
from typing import Optional, NoReturn

from utils import FileIO
from config import FD, Tree


class PageDataTree:

  def __init__(self, data: json):
    self.data = data

  # TODO: check for other types
  @staticmethod
  def join_tree(tree: str, key: str, list_index: Optional[int] = None):
    keys = [tree]

    if list_index is not None:
      keys.append(Tree.LIST_INDEX_WRAPPER.format(index=list_index))

    keys.append(key)

    return Tree.DELIMITER.join(keys)

  def process_result(self, result: str, result_to: str) -> Optional[NoReturn]:
    # NOTE: python's new feature
    match result_to:
      case 'print':
        print(result)

    if Tree.SEARCH_LIMIT:
      Tree.SEARCH_LIMIT -= 1

    if Tree.SEARCH_LIMIT == 0:
      exit()

  def tree_by_key(self, data: Optional[dict] = None, key: str = '',
                        ans: str = Tree.ROOT, list_index: Optional[int] = None,
                        result_to: str = 'return') -> Optional[str]:
    """Returns str: ex. A -> B -> C -> *key
    """
    if data is None:
      data = self.data

    if isinstance(data, list):
      # NOTE: list doesn't have a key
      # TODO: square braces around key
      for idx, item in enumerate(data):
        fnd = self.tree_by_key(item, key, ans, list_index=idx, result_to=result_to)
        if fnd:
          if (result_to == 'return'):
            return fnd
          self.process_result(fnd, result_to)
          continue

    # TODO: multiple keys ??
    if isinstance(data, dict):
      for data_key, data_value in data.items():
        if data_key == key:
          fnd = self.join_tree(ans, data_key, list_index)
          if (result_to == 'return'):
            return fnd
          self.process_result(fnd, result_to)
          continue

        if data_key is None:
          continue
        if data_value is None:
          continue

        fnd = self.tree_by_key(
          data_value, key,
          self.join_tree(ans, data_key, list_index),
          list_index=list_index, result_to=result_to
        )
        if fnd:
          if (result_to == 'return'):
            return fnd
          self.process_result(fnd, result_to)

  def data_by_tree(self, tree: str) -> dict:
    if Tree.ROOT:
      tree = tree.replace(
        self.join_tree(Tree.ROOT, ''), '', 1
      )

    tree_keys = tree.split(Tree.DELIMITER)
    inner_data = self.data

    for key in tree_keys:
      if key.startswith(Tree.LIST_INDEX_WRAPPER[0]):
        inner_data = inner_data[int(key[1:-1])]
      else:
        inner_data = inner_data[key]

    return inner_data


def main(input_filepath: str, output_filepath: str,
         key: str, tree: str, limit: Optional[int]):
    file_io = FileIO(input_filepath)
    file_data = file_io.load()

    pdt = PageDataTree(file_data)

    if limit:
      Tree.SEARCH_LIMIT = limit

    if key:
      if limit:
        pdt_tree = pdt.tree_by_key(key=key, result_to='print')
      else:
        pdt_tree = pdt.tree_by_key(key=key, result_to='return')
    else:
      pdt_tree = tree

    if output_filepath:
      # use parsed (generated) tree to get the data (value for `key`)
      tree_data = pdt.data_by_tree(pdt_tree)

      file_io.dump(tree_data, output_filepath)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='JSON Tree parser')
  parser.add_argument('-i', type=str, help='[i]nput filepath')
  parser.add_argument('-o', type=str, help='[o]utput filepath')
  parser.add_argument('-k', type=str, help='[k]ey to search (generate) tree for')
  parser.add_argument('-t', type=str, help='[t]ree to save the data from')
  parser.add_argument('-l', type=int, help='[l]limit stdout')
  args = parser.parse_args()

  input_filepath = args.i
  output_filepath = args.o
  key = args.k
  tree = args.t
  limit = args.l

  if not input_filepath:
    print('Input filepath required')
    exit()
  if (not key) and (not tree):
    print('Key or Tree is required')
    exit()

  main(input_filepath, output_filepath, key, tree, limit)
