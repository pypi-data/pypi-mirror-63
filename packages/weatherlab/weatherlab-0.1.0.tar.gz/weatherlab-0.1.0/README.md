# WeatherLab

An IPython kernel extension to interact with WeatherLab JupyterLab extension to check weather conditions with data from OpenWeatherMap.

![WeatherLab](https://gitlab.com/zodiacfireworks/weatherlab/-/raw/master/weatherlab.gif 'WeatherLab')

## Requirements

- weatherlab >= 0.2.0
- ipython >= 7.13.0

## Install

```bash
pip install weatherlab
jupyter labextension install weatherlab
```

## Usage

This package can be loades using the following command

```
%load_ext weatherlab
```

You can access to the data fetched by WeaterLab extension using the magic line

```
%weather_lab_data
```

or accessing directy to the variable

```
WEATHER_LAB_DATA
```

## Contributing

### Install

```bash
# Clone the repo to your local environment
# Move to weatherlab directory
# Install dependencies
poetry install
# Link your development version of the extension with JupyterLab
poetry run pip install -e .
# Launch jupyter and start making changes
jupyter lab
```
