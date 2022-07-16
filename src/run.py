import os
import json
from typing import Optional, Any

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

  def process_result(self, result: str, result_to: str):
    # NOTE: python's new feature
    match result_to:
      case 'print':
        print(result)

  def tree_by_key(self, data: Optional[Any] = None, key: str = '',
                        ans: str = Tree.ROOT, list_index: Optional[int] = None,
                        result_to: str = 'return') -> str:
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
        # TODO: return key or value ?
        if data_value == key:
          return 'fnd: 2'
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


if __name__ == '__main__':
  target_filepath = os.path.join(
    FD.ROOT_DIRECTORY, 'ranker_writer-ignore_me.json'
  )

  file_io = FileIO(target_filepath)

  target_filename = 'ranker_writer-ignore_me'
  # target_filename = 'test_scratch'

  gpd_data = file_io.load()

  pdt = PageDataTree(gpd_data)
  # pdt_tree = pdt.tree_by_key(key='user', result_to='print')
  pdt_tree = 'root -> props -> pageProps -> listContext -> currentPageData -> listItems -> [2] -> openListItemContributor -> [2] -> user'

  # 'root -> props -> pageProps -> listContext -> currentPageData -> list -> user -> userAccount -> clientIP'
  # ['props', 'pageProps', 'listContext', 'currentPageData', 'list', 'user']
  parent_level = 2
  target_tree = pdt_tree.rsplit(Tree.DELIMITER, maxsplit=parent_level)[0]

  # replaces 'root ->' to ''
  target_tree = target_tree.replace(pdt.join_tree(Tree.ROOT, ''), '')

  target_data = pdt.data_by_tree(target_tree)
  print(target_data)

  # gpd.write_to_json(target_data, 'key_content')
