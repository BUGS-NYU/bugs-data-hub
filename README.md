# BUGS Data Hub
The repository contains Python scripts that produce data dumps for different types of datasets.

## Current Available Dataset
1. Course data from [Schedge](https://github.com/BUGS-NYU/schedge)
2. NYU subreddit data

## Run Scripts

1. To get Schedge data, run:
```
    python3 schedge_downloader.py -term -year -full 
```
- Term is of the form: fa, su, sp, ja.
- year is the current year.
- full is whether you would like full data from schedge.

2. To get the latest reddit data, run:
```
    python3 reddit_downloader.py
```

- The data is located in data folder

## Motivation
We hope this can serve as a good resource for NYU students to explore data analysis/science projects

## Development
Please see CONTRIBUTING.md for further information regarding setup and development