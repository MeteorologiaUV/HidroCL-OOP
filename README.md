# HidroCL database maintainer

----

[![pythonversion](https://img.shields.io/badge/python-3.10-blue?style=plastic&logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-3100/)
![packageversion](https://img.shields.io/badge/version-0.0.1-blue?style=plastic)

## Data download

*to do: add description about data downloading* 

## Data extraction

*to do: add description about data extraction*

----

## To do list

- [ ] complete README.md
- [x] hidrocl basic variable
  - [x] add old code
  - [x] adapt code to modules approach
  - [X] test locally
  - [X] test on nas
    > **Notes:**
    > 
    > Values in Pixel count aren't consistent with `NA` values in the database.
- [ ] GLDAS_NOAHH25_3H processing 
- [ ] GPM_3IMERGHHL processing
- [ ] MCD12Q1 processing
- [ ] MCD15A2H processing
- [ ] MCD43A3 processing
- [ ] MOD09A1 processing
- [ ] MOD10A2 processing
- [ ] MOD13Q1 processing
- [ ] MOD16A2 processing
- [ ] PERSIANN processing
- [ ] Download functions refactoring
  - [ ] PERSIANN (FTP approach)
  - [ ] Earthdata (API approach)
  - [ ] MODIS web scraping (include?)
  - [ ] test download functions  
- [ ] Add documentation
- [ ] Add tests
- [ ] Add examples
- [ ] Add flowcharts

----

## Changelog

### [0.0.1] - 2022-08-18
#### Added
- HidroCLVariable object refactored from [hidroclabc.py](https://github.com/aldotapia/HidroCL-DBCreation/blob/main/Class%20tests/hidroclabc.py)
- [local](https://github.com/aldotapia/HidroCL-OOP/blob/main/local_tests.ipynb) and [nas](https://github.com/aldotapia/HidroCL-OOP/blob/main/nas_tests.ipynb) tests for HidroCLVariable object