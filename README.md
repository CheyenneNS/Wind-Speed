# Picarro: Windspeed Coding Challenge

This repository contains code for a Command Line Interface (CLI) program to gather wind velocity data from San Jose Ca. 

## How It Works
The Windspeed program uses DocOpt to create the main CLI. 
Users are required to provide a runtime for the program, given in minutes or hours. Unit options are optional with the default unit being miles per hour.

The program queries the Open Weather Map API for windspeed data in San Jose California and outputs results to the terminal. 
When windspeed variables change - either in speed or direction - new results are updated to the terminal. 

## Getting Started

### Build

Using Git, fork or download the main repository and navigate to the root directory of the project, then simply run

```sh
$ make develop 
```
The develop command will create and activate the virtual environment, then install the required packages form the requirements.txt file. 

### Run

Once, the development environment is set, one can run WindSpeed and set the program runtime by:

```sh
$ make serve time=--minutes=int
```

Or to allow the program to run for hours 

```sh
$ make serve time=--hours=int
```

Unit options can also be specified

```sh
$ make serve time=—hours=int units=metric=True
```

### Test

Unit tests are provided in the testImpl.py file within the source directory. 

To run tests:
```sh
$ make test
```


##  Further Documentation 

* [`docopt`]: https://pypi.org/project/docopt

* [`Open Weather Map API`]: https://openweathermap.org/current


