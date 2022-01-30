#! /bin/bash

echo "Executing yapf..."
yapf -r -i .
echo "Executing isort..."
isort .
echo "Done."
