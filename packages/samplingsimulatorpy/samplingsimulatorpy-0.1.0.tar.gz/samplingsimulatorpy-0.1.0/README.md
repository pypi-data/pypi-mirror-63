## samplingsimulatorpy 

![build](https://github.com/UBC-MDS/samplingsimulatorpy/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/UBC-MDS/samplingsimulatorpy/branch/master/graph/badge.svg)](https://codecov.io/gh/UBC-MDS/samplingsimulatorpy) ![Release](https://github.com/UBC-MDS/samplingsimulatorpy/workflows/Release/badge.svg)

[![Documentation Status](https://readthedocs.org/projects/samplingsimulatorpy/badge/?version=latest)](https://samplingsimulatorpy.readthedocs.io/en/latest/?badge=latest)


`samplingsimulatorpy` is a Python package intended to assist those teaching or learning basic statistical inference.

### Authors

| Name             | GitHub                                          |
| ---------------- | ----------------------------------------------- |
| Holly Williams   | [hwilliams10](https://github.com/hwilliams10)   |
| Lise Braaten     | [lisebraaten](https://github.com/lisebraaten)   |
| Tao Guo          | [tguo9](https://github.com/tguo9)               |
| Yue (Alex) Jiang | [YueJiangMDSV](https://github.com/YueJiangMDSV) |

### Overview

This package allows users to generate virtual populations which can be sampled from in order to compare and contrast sample vs sampling distributions for different sample sizes.  The package also allows users to sample from the generated virtual population (or any other population), plot the distributions, and view summaries for the parameters of interest.

## Installation:

```
pip install -i https://test.pypi.org/simple/ samplingsimulatorpy
```


## Function Descriptions

- `generate_virtual_pop` creates a virtual population.
    - **Inputs** : distribution function (i.e. `np.random.lognormal`, `np.random.binomial`, etc), the parameters required by the distribution function, and the size of the population.
    - **Outputs**: the virtual population as a tibble
- `draw_samples` generates samples of different sizes
    - **Inputs** : population to sample from, the sample size, and the number of samples
    - **Outputs**: returns a tibble with the sample number in one column and value in a second column.
- `plot_sample_hist` creates sample distributions for different sample sizes.
    - **Inputs** : population to sample from, the samples to plot, and a vector of the sample sizes
    - **Outputs**: returns a grid of sample distribution plots
- `plot_sampling_dist` creates sampling distributions for different sample sizes.
    - **Inputs** : population to sample from, the samples to plot, and a vector of the sample sizes
    - **Outputs**: returns a grid of sampling distribution plots
- `stat_summary`: returns a summary of the statistical parameters of interest
    - **Inputs**: population, samples, parameter(s) of interest
    - **Outputs**: summary tibble


#### How do these fit into the Python ecosystem?

To the best of our knowledge, there is currently no existing Python package with the specific functionality to create virtual populations and make the specific sample and sampling distributions described above. We do make use of many existing Python packages and expand on them to make very specific functions. These include:
 - `scipy.stats` to get distribution functions
 - `np.random` to generate random samples
 - [Altair](https://altair-viz.github.io/) to create plots

 Python `pandas` already includes some summary statistics functions such as `.describe()`, however our package will be more customizable.  Our summary will only include the statistical parameters of interest and will provide a comparison between the sample, sampling, and true population parameters.

### Dependencies

- python = "^3.7"
- pandas = "^1.0.1"
- numpy = "^1.18.1"
- altair = "^4.0.1"

## Usage

#### `generate_virtual_pop`

``` 
from samplingsimulatorpy import generate_virtual_pop
generate_virtual_pop(size, distribution_func, *para)
```

**Arguments:**

  - `size`: The number of samples
  - `distribution_func`: The distribution that we are generating samples from
  - `*para`: The arguments required for the distribution function

**Example:**

`pop = generate_virtual_pop(100, np.random.normal, 0, 1)`

#### `draw_samples`

``` 
from samplingsimulatorpy import draw_samples
draw_samples(pop, reps, n_s)
```

**Arguments:**

  - `pop` the virtual population as a data frame
  - `reps` the number of replication for each sample size as an integer
    value
  - `n_s` the sample size for each one of the samples as a list

**Example:**

`samples = draw_samples(pop, 3, [5, 10, 15, 20])`

#### `plot_sample_hist`

``` 
from samplingsimulatorpy import plot_sample_hist
plot_sample_hist(pop, samples)
```

**Arguments:**

  - `pop` the virtual population as a data frame
  - `samples` the samples as a data frame

**Example:**

`plot_sample_hist(samples)`

#### `plot_sampling_hist`

``` 
from samplingsimulatorpy import plot_sampling_hist
plot_sampling_hist(pop, samples)
```

**Arguments:**

  - `samples` the samples as a data frame

**Example:**

`plot_sampling_hist(samples)`

#### `stat_summary`

``` 
from samplingsimulatorpy import stat_summary
plot_sampling_hist(pop, samples, parameter)
```

**Arguments**

  - `population` The virtual population
  - `samples` The drawed samples
  - `parameter` The parameter(s) of interest

**Example**

`stat_summary(pop, samples, ['np.mean', 'np.std'])`

### Example Usage Scenario

```python
from samplingsimulatorpy import generate_virtual_pop,
                                draw_samples,
                                plot_sample_dist,
                                plot_sampling_dist,
                                stat_summary
# create virtual population
pop = generate_virtual_pop(100, np.random.normal, 0, 1)
# take samples
samples = draw_samples(pop, 3, [10, 20])
# plot sample histogram
plot_sample_hist(pop, samples)
```
![](img/sample_dist_output.png)

```python
# plot sampling distribution
plot_sampling_hist(samples)
```
![](img/sampling_dist_output.png)

```python
# compare mean and standard deviation
stat_summary(pop, samples, ['np.mean', 'np.std'])
```

![](img/stat_summary_output.png)

### Documentation
The official documentation is hosted on Read the Docs: <https://samplingsimulatorpy.readthedocs.io/en/latest/>

### Credits
This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).
