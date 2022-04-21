# Weekly And Monthly
Weeks and Months are two incompatible units. Their greatest common denominator is a day. This library takes datapoints and analyses them in order to produce weekly and monthly averages.

# Usage
Write a python class that inherits the Abstract Base Class `DataPoint`. Create a instance of `MonthlyAndWeeklyStatistics` and call `consider(data_point)` for each datapoint you want to include.
Now use the `print_cvs()` to get the values for your spreadsheet.
