# Unit Tests

## Create a file for enviorment variables

First create a `.env` file here with

```ini
API_KEY="XXXXXXXXXX"
HOST=http://127.0.0.1:8001
TIMEOUT=24
```

## Running the tests

To run one test, for example `test_distritos.py`, run:

```bash
python3 -m unittest tests.test_distritos
```

To run all tests, run:

```bash
python3 -m unittest discover tests
```
