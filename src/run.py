import os
import json
from typing import Optional, Any

import requests
from bs4 import BeautifulSoup as bs


DATA_DIRECTORY = 'data'
JSON_EXTENSION = '.json'
TREE_ROOT = 'root'
TREE_DELIMITER = ' -> '


class GetPageData:

  def __init__(self, url: str = ''):
    self.url = url

  @staticmethod
  def join_path(filename: str):
    dirname = os.path.dirname(filename)

    # FIXFOR: full_path to the file
    if (not dirname) or (dirname != DATA_DIRECTORY):
      path = os.path.join(DATA_DIRECTORY, filename)
    else:
      path = filename

    if path.endswith(JSON_EXTENSION):
      return path

    return f"{path}{JSON_EXTENSION}"

  def get(self) -> json:
    # TODO: handle error on not finding/returning a json
    soup = bs(requests.get(self.url).text, 'lxml')
    return json.loads(soup.find('script', id='__NEXT_DATA__').text)

  def write_to_json(self, data: dict, write_to: str, indent: int = 4) -> None:
    write_to = self.join_path(write_to)

    with open(write_to, 'w') as ftw:
      ftw.write(json.dumps(data, indent=indent))

  def load_from_json(self, load_from: str = '') -> json:
    load_from = self.join_path(load_from)

    with open(load_from, 'r') as ftr:
      return json.loads(ftr.read())


class PageDataTree:

  def __init__(self, data: json):
    self.data = data

  # TODO: check for other types
  @staticmethod
  def join_tree(*args: tuple[str]):
    return TREE_DELIMITER.join(args)

  def tree_by_key(self, data: Optional[Any] = None, key: str = '', ans: str = TREE_ROOT) -> str:
    """Returns str: ex. A -> B -> C -> *key
    """
    if data is None:
      data = self.data

    if isinstance(data, list):
      # NOTE: list doesn't have a key
      # TODO: square braces around key
      for item in data:
        fnd = self.tree_by_key(item, key, ans)
        if fnd:
          return fnd

    # TODO: multiple keys ??
    if isinstance(data, dict):
      for data_key, data_value in data.items():
        if data_key == key:
          return self.join_tree(ans, data_key)
        if data_key is None:
          continue
        # TODO: return key or value ?
        if data_value == key:
          return 'fnd: 2'
        if data_value is None:
          continue
        fnd = self.tree_by_key(data_value, key, self.join_tree(ans, data_key))
        if fnd:
          return fnd

  def data_by_tree(self, tree: str) -> dict:
    tree_keys = tree.split(TREE_DELIMITER)

    # *pointer
    inner_data = self.data

    for key in tree_keys:
      inner_data = inner_data[key]

    return inner_data


if __name__ == '__main__':
  target_url = "https://www.ranker.com/list/most-important-locations-in-star-wars-universe/john-saavedra"

  gpd = GetPageData(target_url)
  target_filename = 'ranker_writer'

  gpd_data = gpd.get()
  gpd.write_to_json(data=gpd_data, write_to=target_filename)
  gpd_data = gpd.load_from_json(target_filename)

  pdt = PageDataTree(gpd_data)
  pdt_tree = pdt.tree_by_key(key='clientIP')

  # 'root -> props -> pageProps -> listContext -> currentPageData -> list -> user -> userAccount -> clientIP'
  # ['props', 'pageProps', 'listContext', 'currentPageData', 'list', 'user']
  parent_level = 2
  target_tree = pdt_tree.rsplit(TREE_DELIMITER, maxsplit=parent_level)[0]

  # replaces 'root ->' to ''
  target_tree = target_tree.replace(pdt.join_tree(TREE_ROOT, ''), '')

  target_data = pdt.data_by_tree(target_tree)

  gpd.write_to_json(target_data, 'key_content')
