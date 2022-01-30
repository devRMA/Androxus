#! /bin/bash

echo "Executing mypy..."
mypy --pretty --namespace-packages .
echo "Executing flake8..."
flake8 --benchmark .
echo "Done."

