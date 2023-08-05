# Standardized python visualizations package 'baseplots'
## by Truls Møller

### Date created
2020-03-06

## About
Part of the Data Scientist nanodegree at Udacity (self-chosen and non-mandatory project)

## Files
**Generalplot.py** - Generic plotting class for visualizing data

**Plot1d.py** - Generic plotting class for visualizing data based on one variable.

**Plot2d.py** - Generic plotting class for visualizing data based on two variables.

**test.py** - Unit tests

**test_data.csv** - Test data for unit tests

## Installation

pip install baseplots

## Example Jupyter Notebook

```python
from baseplots import Plot1d, Plot2d

x = Plot1d(df, 'column_name') # initialize 1d plot object
y = Plot2d(df, variable_list) # initialize 2d plot object

x.histplot()    # visualize numerical variable 'column_name'

x.barplot()     # visualize numeri variable 'column_name'

y.scatterplot() # visualize two numerical variables in variable_list

y.boxplot()     # visualize categorical + numerical variable in variable_list
```
