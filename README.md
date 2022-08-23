# HidroCL database maintainer

----

[![pythonversion](https://img.shields.io/badge/python-v3.10-blue?style=plastic&logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-3100/)
[![packageversion](https://img.shields.io/badge/r-v4.1.2-blue?style=plastic&logo=r&logoColor=9cf)](https://anaconda.org/conda-forge/r-base?version=4.2.1)
![packageversion](https://img.shields.io/badge/version-v0.0.2-blue?style=plastic)

## Data download

*to do: add description about data downloading* 

## Data extraction

*to do: add description about data extraction*

----

## To do list

- [ ] complete README.md
- [x] hidrocl basic variable
  - [x] add old code
  - [x] adapt code to modules OOP approach
  - [x] test locally
  - [x] test on nas
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
- [x] MOD13Q1 processing
  - [x] test locally
  - [x] test on nas
- [ ] MOD16A2 processing
- [ ] PERSIANN processing
- [ ] Download functions refactoring
  - [ ] PERSIANN (FTP approach)
  - [ ] Earthdata (API approach)
  - [ ] MODIS web scraping (include?)
  - [ ] test download functions  
- [ ] Add documentation
  - [x] add variables documentation
  - [ ] add products documentation
- [ ] Add tests
- [ ] Add examples
- [ ] Add flowcharts

----
## Packages used

**Conda:**

`rpi2` not working with `sf`: [![packageversion](https://img.shields.io/badge/rpi2-v3.5.1-green?style=plastic)](https://anaconda.org/conda-forge/rpy2?version=3.5.1)

*R Libraries*


[![packageversion](https://img.shields.io/badge/r--terra-v1.5.21-green?style=plastic)](https://anaconda.org/conda-forge/r-terra)
[![packageversion](https://img.shields.io/badge/r--sf-v1.0.6-green?style=plastic)](https://anaconda.org/conda-forge/r-sf)
[![packageversion](https://img.shields.io/badge/r--exactextractr-v0.7.2-green?style=plastic)](https://anaconda.org/conda-forge/r-exactextractr)
[![packageversion](https://img.shields.io/badge/tibble-v3.1.8-green?style=plastic)](https://anaconda.org/conda-forge/r-tibble)

*Interactive code*

[![packageversion](https://img.shields.io/badge/jupyter-v1.0.0-green?style=plastic)](https://anaconda.org/conda-forge/jupyter)

*Python*

[![packageversion](https://img.shields.io/badge/pandas-v1.4.3-green?style=plastic)](https://anaconda.org/conda-forge/pandas)
[![packageversion](https://img.shields.io/badge/rioxarray-v0.12.0-green?style=plastic)](https://anaconda.org/conda-forge/rioxarray)
[![packageversion](https://img.shields.io/badge/matplotlib-v3.5.3-green?style=plastic)](https://anaconda.org/conda-forge/matplotlib)
[![packageversion](https://img.shields.io/badge/geopandas-v0.11.1-green?style=plastic)](https://anaconda.org/conda-forge/geopandas)

*Documentation*

[![packageversion](https://img.shields.io/badge/sphinx-v5.1.1-green?style=plastic)](https://anaconda.org/conda-forge/sphinx)
[![packageversion](https://img.shields.io/badge/sphinx--rtd--theme-v0.4.3-green?style=plastic)](https://anaconda.org/conda-forge/sphinx_rtd_theme)

Installation commands:
**Environment creation and first steps:**
```bash
# installing Python and R
conda create -n hidrocl python=3.10  # R is installed with the r-sf package
conda activate hidrocl
# installing needed R packages
conda install -c conda-forge r-sf r-terra r-exactextractr r-tibble
# for running tests
conda install -c conda-forge jupyter
#  installing python libraries
conda install -c conda-forge pandas rioxarray matplotlib geopandas
#  installing python documentation tool
conda install -c conda-forge sphinx sphinx_rtd_theme
```

**R package needed for sf/terra messages**

```R
install.packages("codetools", dependencies = TRUE)
```

----

## Changelog

### [0.0.2] - 2022-08-22
#### Added
- **MOD13Q1 processing**: temporal folder and file remove actions are commented for testing purposes. After running and analyzing the results, uncomment the actions.


### [0.0.1] - 2022-08-18
#### Added
- HidroCLVariable object refactored from [hidroclabc.py](https://github.com/aldotapia/HidroCL-DBCreation/blob/main/Class%20tests/hidroclabc.py)
- [local](https://github.com/aldotapia/HidroCL-OOP/blob/main/local_tests.ipynb) and [nas](https://github.com/aldotapia/HidroCL-OOP/blob/main/nas_tests.ipynb) tests for HidroCLVariable object