# HidroCL database maintainer

----

[![pythonversion](https://img.shields.io/badge/python-v3.10-blue?style=plastic&logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-3100/)
[![packageversion](https://img.shields.io/badge/r-v4.1.2-blue?style=plastic&logo=r&logoColor=9cf)](https://anaconda.org/conda-forge/r-base?version=4.2.1)
![packageversion](https://img.shields.io/badge/version-v0.0.13-blue?style=plastic)

**Python minimum version**: 3.10

## Data download

*to do: add description about data downloading* 

## Data extraction

*to do: add description about data extraction*

**Note**: In macOS, the command for running R is `RScript`, while in Linux is `Rscript`.

**Access to documentation [here](https://aldotapia.github.io/HidroCL-OOP/)**


----



Installation commands:
**Environment creation and first steps:**
```bash
# installing Python and R
conda create -n hidrocl_test python=3.10
conda activate hidrocl_test
# installing needed R packages
conda install -c conda-forge r-sf r-terra r-exactextractr r-tibble
# for running tests
conda install -c conda-forge jupyter
pip install .
```

**R package needed for sf/terra warning messages**

```bash
R -e 'install.packages(c("codetools","tibble") dependencies = TRUE)'
```

## Configuration

### Set project path

````python
import hidrocl
hidrocl.set_project_path('/path/to/project')
print(hidrocl.paths.gfs)
>>> '/path/to/project/forecasted'
````