# CA COVID Map Time-Lapse
A Time-Lapse of COVID cases in California Counties

## Attributions
COVID cases data is queried from https://github.com/datadesk/california-coronavirus-data, provided by to Los Angeles Times, under [their license](https://github.com/datadesk/california-coronavirus-data/blob/master/LICENSE).
Map tiles by [Stamen Design](http://stamen.com) under [CC BY 3.0](http://creativecommons.org/licenses/by/3.0). Data by [OpenStreetMap](http://openstreetmap.org), under [ODbL](http://www.openstreetmap.org/copyright).
 
## Dependencies
Poetry dependency manager: https://python-poetry.org

## To Run
```bash
poetry install
poetry shell
python convidinla/main.py
```
You will need to enter the fips for the county you want (LA is 37, San Diego 73, etc...)
A gif with the timelapse will be created on the same path.
