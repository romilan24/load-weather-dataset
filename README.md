This data was generated using a forks of https://github.com/Karlheinzniebuhr/the-weather-scraper and https://github.com/jikaczmarski/caiso-data-downloader.  Adjustments were made to aggregate 5-minute interval data to hourly averages and then scrubbed using the preprocessing.py script attached.

**Assumptions**
- Using weather stations KCASANFR698, KCASANJO17, KCABAKER271, KCAELSEG23, KCARIVER117 to serve as represetation of major load serving areas in CAISO
- We swap missing data between SF and SJ as it was determined to have .9155 correlation
- All other missing data is of two types: daylight savings time (2021-03-14', '2022-03-13', '2023-03-12') or missing from source which is www.wunderground.com; we fill in these values using interpolation (see preprocessing.py)
