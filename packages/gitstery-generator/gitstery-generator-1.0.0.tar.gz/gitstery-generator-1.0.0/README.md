[![PyPI version](https://badge.fury.io/py/gitstery.svg)](https://badge.fury.io/py/gitstery)

# The Git Murder Mystery Generator
This project _generates_ a "gitstery" git repository.

**NOTICE:** This is not the Git Murder Mystery repository. For that, please visit
https://github.com/nivbend/gitstery.

# Install
```
pip install gitstery-generator
```
Or clone this repository and then `pip install .`/`python setup.py install`.

# Usage
To generate a new repository at `/tmp/gitstery`:
```
gitstery generate /tmp/gitstery
```

To verify a repository:
```
gitstery verify /tmp/gitstery
gitstery verify https://github.com/nivbend/gitstery.git
gitstery verify git@github.com:nivbend/gitstery.git
```

If you have your own fork of the gitstery repository you'd like to update:
```
gitstery push /tmp/gitstery <your repository URL>
```
Or:
```
gitstery generate --push /tmp/gitstery
```

The following environment variables replace some commonly used values:
| Environment Variable   | Usage                                                     |
|:-----------------------|:----------------------------------------------------------|
| `GITSTERY_TEMP_DIR`    | The directory in which to generate the new repository     |
| `GITSTERY_TARGET_REPO` | The URL of the remote repository                          |
| `GITSTERY_SEED`        | The random seed to use (useful for reproducible "builds") |

# Data
* English:
  * List of given names: [Social Security's top 1000 names for 2018](https://www.ssa.gov/OACT/babynames/).
  * List of surnames: [2000 US Census](https://www.census.gov/topics/population/genealogy/data/2000_surnames.html)

# Acknowledgments
The "murder mystery" repository this project generates was inspired by similar projects:
* [SQL Murder Mystery](https://mystery.knightlab.com/).
* [The Command Line Murders](https://github.com/veltman/clmystery).
