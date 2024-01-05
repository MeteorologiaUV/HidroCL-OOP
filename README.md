# HidroCL database maintainer

----

[![pythonversion](https://img.shields.io/badge/python-v3.10-blue?style=plastic&logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-3100/)
[![packageversion](https://img.shields.io/badge/r-v4.1.2-blue?style=plastic&logo=r&logoColor=9cf)](https://anaconda.org/conda-forge/r-base?version=4.2.1)
![packageversion](https://img.shields.io/badge/version-v0.0.14-blue?style=plastic)

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
# for running tests
conda install -c conda-forge jupyter
```

Install R and the following packages:
```bash
sudo R
> install.packages(c('terra', 'sf', 'exactextractr', 'tibble'))
> quit()
```

Then:

```
pip install .
```
or

```
cd dist
pip install hidrocl-0.0.14.tar.gz 
```

Check if hidrocl/products/Rfiles are copied to
`env_name/lib/python3.10/site-packages/hidrocl/products/Rfiles`,
if not, copy them manually. **This is quite important** (I'm gonna
work on it when I have time)

**R package needed for sf/terra warning messages**

```bash
R -e 'install.packages("codetools", dependencies = TRUE)'
```

## Configuration

### Set project path

````python
import hidrocl
hidrocl.set_project_path('/path/to/project')
print(hidrocl.paths.gfs)
>>> '/path/to/project/forecasted'
````

## Usage

### Upload database

First, set project path (`workflow/server/config.py`):

````python
project_path = '/path/to/project'
````

The project path should have the following structure:

 - base
   - boundaries
     - Agr_ModisSinu.shp
     - HidroCL_boundaries_sinu.shp
     - HidroCL_boundaries_utm.shp
     - HidroCL_boundaries.shp
     - HidroCL_north.shp
     - HidroCL_south.shx
 - databases
   - discharge (optional)
   - forecasted (with all databases inside)
   - observed (with all databases inside)
   - staic (optional)
 - logs (empty or with all logs inside)
 - pcdatabases
   - discharge (optional)
   - forecasted (with all databases inside)
   - observed (with all databases inside)
   - staic (optional)
 
Then, run the following command:

````bash
python workflow/server/run_all.py
````