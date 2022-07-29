# TODO: use namedtuple


class FD:
  """File and Directory
  """
  ROOT_DIRECTORY = 'data'
  FILE_EXTENSION = '.json'


class Tree:
  ROOT = 'root'
  DELIMITER = ' -> '
  LIST_INDEX_WRAPPER = "[{index}]"
  SEARCH_LIMIT = -1
  SEARCH_FILTER = ''


class Key:
  SHOW = 'print'
  SAVE = 'return'
