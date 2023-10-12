import os

from src.run import GetPageData, DATA_DIRECTORY, JSON_EXTENSION


def test_join_path():
  filename = 'dt'

  assert GetPageData().join_path(filename) == os.sep.join(
    (DATA_DIRECTORY, f"{filename}{JSON_EXTENSION}")
  )


def test_join_path_with_extension():
  """Testing extension duplication
  """
  filename = 'dt.json'

  assert GetPageData().join_path(filename) == os.sep.join(
    (DATA_DIRECTORY, filename)
  )


def test_join_path_with_dirname():
  """Testing extension duplication
  """
  filename = os.path.join(DATA_DIRECTORY, 'dt.json')
  assert GetPageData().join_path(filename) ==  filename
