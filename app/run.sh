#!/bin/bash

make data/clean_dataset.csv
uvicorn app.api:app --host "0.0.0.0"