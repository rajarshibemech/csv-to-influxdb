import requests
import json
import gzip
import argparse
import csv
import datetime
from os import listdir
from os.path import isfile , join
import sys
from influxdb import InfluxDBClient

epoch = datetime.datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
    return int((dt - epoch).total_seconds() * 1000)

def loadCsv(inputfilename, servername, user, password, dbname, metric, timecolumn, timeformat, tagcolumns, fieldcolumns, usegzip, delimiter, batchsize ,path , deletedb):

    host = servername[0:servername.rfind(':')]
    port = int(servername[servername.rfind(':')+1:])
    client = InfluxDBClient(host, port, user, password, dbname)
    
    print 'The value of deletedb %s'%deletedb
    
    if deletedb=='True':
        print 'Deleting database %s'%dbname
        client.drop_database(dbname)
        print 'Creating database %s'%dbname
        client.create_database(dbname)
        client.switch_user(user, password)
        
        
    

    # format tags and fields
    if tagcolumns:
        tagcolumns = tagcolumns.split(',')
    if fieldcolumns:
        fieldcolumns = fieldcolumns.split(',')
    
    iterations=1 
    
    if path!=None:
        
        files = [f for f in listdir(path) if isfile(join(path, f))]
        iterations=len(files)
        
    print ' The value of iterations %s'%iterations
    
        
        
        
       
        
    for itera in range(iterations):
        if iterations>0 and inputfilename==None:
            inputfilefinal=str(path+'\\'+files[itera])
        else:
            inputfilefinal=inputfilename
        print ' The input filename %s'%inputfilefinal
        # open csv
        datapoints = []
        #inputfile = open(inputfilefinal, 'r')
        count = 0
        with open(inputfilefinal, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            for row in reader:
                #timestamp = unix_time_millis(datetime.datetime.strptime(row[timecolumn],timeformat)) * 1000000 # in nanoseconds
                
                timestamp=row[timecolumn]
                
                print(timestamp)
    
                tags = {}
                for t in tagcolumns:
                    v = 0
                    if t in row:
                        v = row[t]
                    tags[t] = v
    
                fields = {}
                for f in fieldcolumns:
                    v = 0
                    if f in row:
                        v = float(row[f])
                    fields[f] = v
                    
                
                if metric=='auto' and inputfilename==None:
                    input_metric=files[itera][:-4]
                elif metric=='auto' and inputfilename!=None:
                    input_metric=inputfilename
                else:
                    input_metric=metric
                    
    
    
                point = {"measurement": input_metric, "time": timestamp, "fields": fields, "tags": tags}
    
                datapoints.append(point)
                count+=1
                
                if len(datapoints) % batchsize == 0:
                    print 'Read %d lines'%count
                    print 'Inserting %d datapoints...'%(len(datapoints))
                    response = client.write_points(datapoints)
    
                    if response == False:
                        print 'Problem inserting points, exiting...'
                        exit(1)
    
                    print "Wrote %d, response: %s" % (len(datapoints), response)
    
    
                    datapoints = []
                
    
        # write rest
        if len(datapoints) > 0:
            print 'Read %d lines'%count
            print 'Inserting %d datapoints...'%(len(datapoints))
            response = client.write_points(datapoints)
    
            if response == False:
                print 'Problem inserting points, exiting...'
                exit(1)
    
            print "Wrote %d, response: %s" % (len(datapoints), response)
    
        print 'Done'
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Csv to influxdb.')
    
    parser.add_argument('-ph','--path', nargs='?', default=None,
                        help='Path to the csv files directory.')

    parser.add_argument('-i', '--input', nargs='?', required=False, default=None,
                        help='Input csv file.')

    parser.add_argument('-d', '--delimiter', nargs='?', required=False, default=',',
                        help='Csv delimiter. Default: \',\'.')

    parser.add_argument('-s', '--server', nargs='?', default='localhost:8086',
                        help='Server address. Default: localhost:8086')

    parser.add_argument('-u', '--user', nargs='?', default='root',
                        help='User name.')

    parser.add_argument('-p', '--password', nargs='?', default='root',
                        help='Password.')

    parser.add_argument('--dbname', nargs='?', required=True,
                        help='Database name.')

    parser.add_argument('-m', '--metricname', nargs='?', default='value',
                        help='Metric column name. Default: value, Set the value to  auto when using for multiple files to set the file names as the metricname')

    parser.add_argument('-tc', '--timecolumn', nargs='?', default='timestamp',
                        help='Timestamp column name. Default: timestamp.')

    parser.add_argument('-tf', '--timeformat', nargs='?', default='%Y-%m-%d %H:%M:%S',
                        help='Timestamp format. Default: \'%%Y-%%m-%%d %%H:%%M:%%S\' e.g.: 1970-01-01 00:00:00')

    parser.add_argument('--fieldcolumns', nargs='?', default='value',
                        help='List of csv columns to use as fields, separated by comma, e.g.: value1,value2. Default: value')

    parser.add_argument('--tagcolumns', nargs='?', default='host',
                        help='List of csv columns to use as tags, separated by comma, e.g.: host,data_center. Default: host')

    parser.add_argument('-g', '--gzip', action='store_true', default=False,
                        help='Compress before sending to influxdb.')

    parser.add_argument('-b', '--batchsize', type=int, default=5000,
                        help='Batch size. Default: 5000.')
    
    parser.add_argument('-del','--deletedb', default='False',
                        help='Option to delete the database')
    
    
    

    args = parser.parse_args()
    if((args.path!=None) & (args.input!=None)) | ((args.path==None) & (args.input==None)):
        sys.exit("Error, Either both Path and Filename have been specified or none have been specified")
        
    loadCsv(args.input, args.server, args.user, args.password, args.dbname, 
        args.metricname, args.timecolumn, args.timeformat, args.tagcolumns, 
        args.fieldcolumns, args.gzip, args.delimiter, args.batchsize , args.path , args.deletedb)
