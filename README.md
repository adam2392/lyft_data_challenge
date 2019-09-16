Lyft driver model
==============================

A lyft data science challenge from 2019. 


Installation
------------

This project was created with cookiecutter, so ideally, first install Anaconda. Then follow these commands:

    conda create -n lyft
    conda activate lyft
    conda install numpy scipy pandas scikit-learn pytest flake8 pytest-coverage ipykernel matplotlib seaborn
    pip install -r requirements.txt
    
    # needed to run jupyter notebooks in this conda environment
    python -m ipykernel install --name lyft --user 
    
Final Report
------------

See "NCSL_writeup_AL.pdf", or go to reports/ and compile the latex. Everything was done without any special software 
necessary, so any latex reader should work.

All figures corresponding to worthwhile analysis are in reports/figures/.

All notebooks corresponding to analysis done are in notebooks/

In general, notebooks should be able to be run in sequence, but due to storage constraints, there are 
tables not able to be attached and saved. These are generally "interim" tables generated from performing
analysis described in the report. However, all figures were generated at some point from these notebooks.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── rider.py       <- Script to make Fare/Ride Object.
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
