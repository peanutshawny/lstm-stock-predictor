from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Using past price data and sentiment analysis from news and other documents to predict the S&P500 index using a LSTM RNN. Idea replicated from https://arxiv.org/abs/1912.07700 and https://arxiv.org/abs/1010.3003.',
    author='Shawn Liu',
    license='',
)
