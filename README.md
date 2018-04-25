"# csv-to-influxdb" 
Addition to the csv to influx db module created by @fabio-miranda

# csv-to-influxdb
Simple python script that inserts data points read from a csv file into a influxdb database.
It adds support to load multiple CSV files stored in a directory into influxDB.



## Usage

```
usage: csv-to-influxdb.py [-h]-ph [PATH] -i [INPUT] [-d [DELIMITER]] [-s [SERVER]]
                          [-u [USER]] [-p [PASSWORD]] --dbname [DBNAME]
                          [-m [METRICNAME]] [-tc [TIMECOLUMN]]
                          [-tf [TIMEFORMAT]] [--fieldcolumns [FIELDCOLUMNS]]
                          [--tagcolumns [TAGCOLUMNS]] [-g] [-b BATCHSIZE] -del [DELETEDDB]

Csv to influxdb.

optional arguments:
  -h, --help            show this help message and exit
  -ph [PATH], --path  [PATH]  Path to the directory where all the csv files are stored. This is applicable when inserting multiple csv files into the database. The -i tag should not be supplied.
  
  -i [INPUT], --input [INPUT]
                        Input csv file. Supply this for a single file
  -d [DELIMITER], --delimiter [DELIMITER]
                        Csv delimiter. Default: ','.
  -s [SERVER], --server [SERVER]
                        Server address. Default: localhost:8086
  -u [USER], --user [USER]
                        User name.
  -p [PASSWORD], --password [PASSWORD]
                        Password.
  --dbname [DBNAME]     Database name.
  -m [METRICNAME], --metricname [METRICNAME]
                        'Metric column name. Default: value, Set the value to 'auto' when using for multiple 
                        files to set the file names as the metricname
  -tc [TIMECOLUMN], --timecolumn [TIMECOLUMN]
                        Timestamp column name. Default: timestamp.
  -tf [TIMEFORMAT], --timeformat [TIMEFORMAT]
                        Timestamp format. Default: '%Y-%m-%d %H:%M:%S' e.g.:
                        1970-01-01 00:00:00
  --fieldcolumns [FIELDCOLUMNS]
                        List of csv columns to use as fields, separated by
                        comma, e.g.: value1,value2. Default: value
  --tagcolumns [TAGCOLUMNS]
                        List of csv columns to use as tags, separated by
                        comma, e.g.: host,data_center. Default: host
  -g, --gzip            Compress before sending to influxdb.
  -b BATCHSIZE, --batchsize BATCHSIZE
                        Batch size. Default: 5000.
  -del , --deletedb [DELETEDB] Set this to true if you want to delete any existing DB by the DB name supplied and create a new DB else set to False. Default is False

```

