import os

from run import GetPageData, FD


def test_join_path():
  filename = 'dt'

  assert GetPageData().join_path(filename) == os.sep.join(
    (FD.ROOT_DIRECTORY, f"{filename}{FD.FILE_EXTENSION}")
  )


def test_join_path_with_extension():
  """Testing extension duplication
  """
  filename = 'dt.json'

  assert GetPageData().join_path(filename) == os.sep.join(
    (FD.ROOT_DIRECTORY, filename)
  )


def test_join_path_with_dirname():
  """Testing extension duplication
  """
  filename = os.path.join(FD.ROOT_DIRECTORY, 'dt.json')
  assert GetPageData().join_path(filename) ==  filename
