# LSTM Flask React Site

[![Build Status](https://travis-ci.org/YaleDHLab/flask-react-boilerplate.svg?branch=master)](https://travis-ci.org/YaleDHLab/flask-react-boilerplate) -> forked from YaleDHLab/flask-react-boilerplate 

## Dependencies

To install the boilerplate dependencies, you can run:

```bash
git clone https://github.com/peanutshawny/lstm-stock-predictor.git
cd lstm-stock-predictor/website
npm install --no-optional
pip install -r requirements.txt
```

## Quickstart

Once the dependencies are installed, you can start the api (Flask backend) with the following command:

```bash
npm run production
```

That will start the server on port 7082. To run the development server (React frontend) with hot module reloading, run:

```bash
npm run start
```

That will start the webpack dev server on port 7081.

## Tests

To run the Javascript tests (located in `src/tests/`), run:

```bash
npm run jest
```

To run the Python tests (located in `server/tests/`), run:

```bash
pytest
```

## Linting

To lint the Javascript files (located in `src`), run:

```bash
npm run lint-js
```

To lint the Python files (located in `server`), run:

```bash
npm run lint-py
```