# ⛏pyromorphite💎
Process mining in python.

# <a name="get_the_source_code"></a>Get the Source Code
Pyromorphite is actively developed on GitHub, where the code is [always available](https://github.com/xcavation/pyromorphite).

You can clone the public repository:

```
$ git clone git://github.com/xcavation/pyromorphite.git 
```

Once you have a copy of the source, you can embed it in your own Python package, or install it into your site-packages easily:

```
$ cd requests
$ pip install .
```

# Quickstart
This is a quick introduction to Pyromorphite. Before proceeding, make sure that Pyromorphite is [installed](#get_the_source_code).

## Import a Log 📜
Reading in event log files in Pyromorphite is super easy. It supports [XES](http://xes-standard.org/), CSV, and Excel files.

### XES Files
Begin by importing the Pyromorphite module:
```python
>>> import pyromorphite as pm
```

We'll try now to get an xes file from a web repository. For [this](https://data.4tu.nl/repository/uuid:c1e9137e-2877-410d-a76a-21ce7f97a239) dataset:
```python
>>> log = pm.read_xes("https://data.4tu.nl/repository/uuid:c1e9137e-2877-410d-a76a-21ce7f97a239/DATA1")
```

Similarly we would do if we would like to read a local file. Let's assume that under `/path/to/file.xes` lies our file. We can then do:
```python
>>> log = pm.read_xes("/path/to/file.xes")
```

### CSV Files
Although not part of Pyromorphite, reading a csv file can be done with the [pandas]() library.

Begin by import the pandas module:
```python
>>> import pandas as pd
```

We'll try now to get an xes file from a web repository. For [this](https://data.4tu.nl/repository/uuid:d5ccb355-ca67-480f-8739-289b9b593aaf) dataset:
```python
>>> log = pd.read_csv("https://data.4tu.nl/repository/uuid:d5ccb355-ca67-480f-8739-289b9b593aaf/DATA")
```

## Construct a Bag 🎒
Having parsed a log into a pandas `DataFrame` we can simply extract the traces of events, with
togehter with their frequency in the log.

```python
>>> bag = pm.as_bag(log)
```

If we consider that everybody might use different column names, we can specify the case, timestamp
and activity columns when creating the bag in the following way:

```python
>>> bag = pm.as_bag(log, case='CI Name (aff)', time='Actual Start', activity='Change Type')
```

## Does this Trace Conform to the Event Log?
For this task we are going to use a model called [Log Skeleton](https://arxiv.org/abs/1806.08247). 

```python
>>> bag = pm.as_bag(pm.read_xes(os.path.join("B1.xes")))
>>> traces = [("a1", "a4", "a5", "a7")]
>>> pred = pm.skeleton.classify(bag, traces)
>>> [False]
```

**NOTE**: Log `B1.xes` is equal to the multiset <img src="https://render.githubusercontent.com/render/math?math=L_1"/> that can be found [here](https://arxiv.org/abs/1806.08247).