#Purpose - This script is going to be run from a validator processor to do the following checks:
# 1 - Check if the headers in the data file and schema file match
# 2 - Validate data file name matches the control file name
# 3 - Validate the MD5 hash value in the control file matches the MD5 hash value of the data file
# 4 - Validate that creation date(Epoch) of file matches with the epoch in the control file

#Import required libraries
import csv
import os
import hashlib
import sys

dataFileName = sys.argv[1]+'.csv'
controlFileName = sys.argv[1]+'.ctr'
schemaFileName = sys.argv[1]+'.schema'

#Function to read the control file into a dictionary
def readFilesToDict(fileName):
    dict1 = {}
    with open(fileName, "r") as infile:
        reader = csv.reader(infile)
        headers = next(reader)       
        for row in reader:
            dict1 = {key: (value) for key, value in zip(headers, row[0:])}
    return dict1

#1 - Check if the headers in the data file and schema file match
with open(dataFileName, "r") as data_stream:
    data_reader = csv.reader(data_stream)
    data_header = next(data_reader)
    data_header_set = set(data_header)

with open(schemaFileName, "r") as schema_stream:
    schema_reader = csv.reader(schema_stream)
    schema_header = next(schema_reader)
    schema_header_set = set(schema_header)

for col_header in data_header_set:
    if col_header not in schema_header_set:
        raise ValueError("Header mismatch : Data File and Schema File")


# 2nd check - Validate data file name matches the control file name

# Read the controlFile into a dictionary
controlDict = readFilesToDict(controlFileName)


if(controlDict['name of file'] != dataFileName):
    raise ValueError("File name mismatch: Data File name in the control file does not match")


#3rd  - Validate the MD5 hash value in the control file matches the MD5 hash value of the data file
with open(dataFileName, "rb") as f:
    bytes = f.read()  # read file as bytes
    readable_hash = hashlib.md5(bytes).hexdigest()
    if(readable_hash != controlDict['md5 hash of file']):
        raise ValueError("MD5 Hash value mismatch: Control file hash value does not match the MD5 hash value of data file")



#4 - Validate that creation date(Epoch) of file matches with the epoch in the control file
modification_time_os = os.path.getctime(dataFileName)
#print(modification_time_os)
if (str(modification_time_os) != controlDict['creation date (epoch) of file']):
    raise ValueError("Last modified time mismatch: Data File and Control file modification time")
else:
    print("All validation checks successful!")

