Script to get a json `key_tree` by `key` and saving the content of the `key` by `key_tree`
- yet another parser (not searched the www for scripts that may solve my task)
```json
{"a": 1, "b": 2, "d": {"c": 3}}		# 'root -> d -> c'
{"a": 1, "b": 2, "d": [{"c": 3}]}	# 'root -> d -> c'
```

#### Dependencies
```bash
pip -V		# 22.1.1
python -V	# 3.10.5
pytest -V	# 6.2.5
```

#### Start
```bash
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
│   └── run.py
├── tests
│   ├── __init__.py
│   ├── test_get_page_data.py
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
- [ ] check for multiple keys
- [ ] check for keys by value
- [ ] handle errors on searching for a non string key
- [ ] handle errors on request and parsing
	- [ ] check for no url
- [ ] fix errors on reading and writing to the json file without filename
	- [ ] add tests

Coding process: https://youtu.be/DkBAIKMN7x0
