# Basic neural network training module

Simple collection of functions
to generate training data
for neural networks.

Inspired by [wwwww-wwww's repository](https://github.com/wwww-wwww/vs-dataset/tree/master).

This repository will likely also include my neosr configs
and other stuff in the future.
Currently undecided how much I want to develop this repository.

## Installation

Clone this repository
and install the dependencies
with the following pip command:

```bash
pip install vsnntraining -r requirements.txt
```

Or the preferred method,
using poetry:

```bash
poetry install && poetry add $(cat requirements.txt)
```

For actual training,
refer to a framework like [neosr](https://github.com/muslll/neosr) or similar.

## Example

For an example of how to use this package,
see the [example.py](example.py).
