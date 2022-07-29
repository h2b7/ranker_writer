#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from typing import Optional

# TODO: FD
from config import Tree
from utils import FileIO

from run import PageDataTree


def main(input_filepath: str, output_filepath: str,
         key: str, tree: str, limit: Optional[int]):
    file_io = FileIO(input_filepath)
    file_data = file_io.load()

    pdt = PageDataTree(file_data)

    if limit:
      Tree.SEARCH_LIMIT = limit

    if key:
      pdt_tree = pdt.tree_by_key(
        key=key,
        result_to=('return' if output_filepath else 'print')
      )
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
