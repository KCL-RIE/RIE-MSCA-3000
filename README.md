### RIE-MSCA-3000
> Automatic scheduler for optimal workshop / meeting times.
> Input: .ics calendar --> Output: ideal dates and times for everyone

### Installation
The programs require [Python](https://www.python.org/) 3+ to run.

### Running

- Edit `config.py` and fill in or adapt to your needs.

```bash
make run
```

### Testing

- Run tests:
```bash
make test
```

- Extract code coverage:
```bash
make coverage
```

### Virtualenv Environment

1. Create the virtual environment:
```bash
$ python -m venv .venv
```

2. Activate it:
```bash
$ source .venv/bin/activate
```

3. Install dependencies (in the virtual environment):
```bash
(.venv) $ pip install -e .
(.venv) $ pip install -r requirements.txt
```

### License

MIT

**Free Software 💻**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
