# Weekly And Monthly
Weeks and Months are two incompatible units. Their greatest common denominator is a day. This library takes datapoints and analyses them in order to produce weekly and monthly metrics.

# Usage
Write a python class that inherits the Abstract Base Class `DataPoint`. Create a instance of `MonthlyAndWeeklyStatistics` and call `consider(data_point)` for each datapoint you want to include. Once all datapoints have been considered, retrieve the weekly and monthly stats by calling `past_weeks()` and `past_months_this_year()`.
