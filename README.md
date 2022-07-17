Script to get a json `key_tree` by `key` and saving the content of the `key` by `key_tree`
```json
{"a": 1, "b": 2, "d": {"c": 3}}		# 'root -> d -> c'
{"a": 1, "b": 2, "d": [{"c": 3}]}	# 'root -> d -> [0] -> c'
```

#### Example (API)
```python3
# WORKDIR=src

import os

from config import FD
from utils import FileIO
from run import PageDataTree


i_filepath = os.path.join(
	FD.ROOT_DIRECTORY, 'ranker_writer-ignore_me.json'
)

file_io = FileIO(i_filepath)
file_data = file_io.load()

pdt = PageDataTree(file_data)
# NOTE: returns the first found `tree`, use `result_to='print'` to print all trees
pdt_tree = pdt.tree_by_key(key='user', result_to='return')

# use parsed (generated) tree to get the data (value for `key`)
user_data = pdt.data_by_tree(pdt_tree)

o_filepath = os.path.join(
	FD.ROOT_DIRECTORY, 'ranker_writer_user_content-ignore_me.json'
)

file_io.dump(user_data, o_filepath)
```

#### Example (CLI)
```bash
# load `input_filepath` and print out the founded tree (with limit if setted)
python src/run.py -i <input_filepath> -k user # -l <search_limit:int>

# save data by tree to the `output_filepath`
python src/run.py -i <input_filepath> -t 'root -> ...' -o <output_filepath>
```

#### Dependencies
```bash
pip -V		# 22.1.1
python -V	# 3.10.5
pytest -V	# 6.2.5
```

#### Start
```bash
# no need to if `requirements.txt` is empty
python -m venv env && source env/bin/activate
pip install -r requirements.txt

# check functions if necessary
pytest .

# run script
python src/run.py
```

#### Script structure
```
.
├── src
│   ├── __init__.py
│   ├── config.py
│   ├── utils.py
│   └── run.py
├── tests
│   ├── __init__.py
│   └── test_page_data_tree.py
├── data
│   ├── key_content-ignore_me.json
│   └── ranker_writer-ignore_me.json
├── README.md
├── CONTRIBUTORS.md
└── requirements.txt
```

#### TODO
- [x] nested json
- [x] json in the list
- [x] check for multiple keys
	- [ ] return multiple keys (iterable result)
	- [ ] unique multiple keys (not every single item in the list)
- [ ] check for keys by value
- [x] access to the data in the list
	- [x] add and get the index from `key_tree`
- [ ] handle errors on searching for a non string key
- [x] fix errors on reading and writing to the json file without filename
	- [x] no need to test for writing
	- [x] raising an error `FileNotFoundError` for not valid input filepath

Coding process: https://youtu.be/DkBAIKMN7x0
