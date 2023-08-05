# Windows Oracle Finder

"Windows Oracle Finder" is a module for python scirpts in order to find the correct version of the "Oracle Client" or "Oracle Instant Client" to use.

## Purpose

The purpose of this module is not to be deployed to live system like webservers or similar. Following the guidelines of the oracle connection modules (like [cx_Oracle](https://oracle.github.io/python-cx_Oracle/)) is strongly recommended.

This module is intended for use in scripts that are running on different client machines, that the oracle installation could be different in each one or has many oracle installations.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine on a windows system.

### Prerequisites

In order to install this module you need to have:

* A Windows Operating System
* Python >= 3

### Installing

Installation is pretty forward and it is done through pip

```
pip install windows-oracle-finder
```

A basic use can be achieved like:

```
import find_oracle

find_oracle.safely_set_oracle_path(None)
```


## Built With

* [logzero](https://logzero.readthedocs.io/en/latest/) - A simple library for easy logging (could change it to standard logging module)
* [pefile](https://github.com/erocarrera/pefile) - A way to identify if a dll is 32bit or 64bit
* [pywin32](https://github.com/mhammond/pywin32) - Helper functions to get the certain OS specific data

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Charalampos Gkikas** - *Initial work* - [hargikas](https://github.com/hargikas)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

