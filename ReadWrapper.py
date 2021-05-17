# Header
# Module        :   Core - ReadWrapper.py
# Description   :   Read wrapper Script
# Parameters    :   <data_file_name> <country_code> 
# Sample Input  :   customer_details ind
# Exit Status   :   0 - Success
#                   101 - Incorrect number of arguments passed
#                   103 - Input csv not found
#		      		104 - Error while creating logging file
#                   105 - Error while reading the sql input script
#		            106 - Error while trying to modify and run SQL query
# Author	    : Balagururaja Alagarsamy
# Created Date	: 05/15/2021
# Version	  Modified By					Modified Dt	Description			
# ----------	---------------	-----------	------------------------------
#   1.1	  		Balagururaja Alagarsamy		05/15/2021	Initial Version
#
# --------------------------------------------------------------------------------------------------
import time
import sys
import os
import configparser
import pandas as pd
import logging
from datetime import datetime
import time
import re

# Initialize the variable to store the time taken for execution of the script

start = datetime.now().time().strftime('%H:%M:%S:%f')

# Check if correct number of input parameters are passed to the script

if len(sys.argv) != 3:
    print('Please enter Data file name and Country code to run the Python Readwrapper Script.')
    exit(101)

# Initializing Data file

data_file_name=sys.argv[1].lower()
country_code=sys.argv[2].upper()

print("Execution of Readwrapper.py for "+str(data_file_name))

# Set dictionary for country_code and country_name

country_dictionary={"IND":"INDIA", "UK":"BRITAIN", "US":"NORTHAMERICA", "PHIL":"PHILIPPINES", "NYC":"NEWYORK", "AU":"AUSTRALIA",  "CA":"CANADA", "CN":"CHINA", "SG":"SINGAPORE", "MY":"MALAYSIA"}


def check_config_logon_files():

    # Read config file

    global config
    config = configparser.ConfigParser()
    config.read(os.path.join( os.path.dirname( __file__ ), 'conf', 'config.cfg' ))
    create_logging_file()  # Call the create logger function    
    
def create_logging_file():

    # Create a logging file to store all the logging information and errors
    global filename
    global fail_filename
    try:
        ts=datetime.now().strftime("%Y%m%d_%H%M%S")
        print(str(config['INCU']['DATA_LOG_DIR']))
        filename=str(config['INCU']['DATA_LOG_DIR']+data_file_name+'.'+ts+'.log')
        print(filename)
        fail_filename=str(config['INCU']['DATA_LOG_DIR']+data_file_name+'.'+ts+'.failed.log')
        logging.basicConfig(filename=filename, filemode='a', format='%(levelname)s %(asctime)s :: %(message)s',
                            level=logging.INFO)
        print("Logging file created "+filename)
    except Exception as e:
        print("Error creating logging file "+str(e))
        exit(104)

    logging.info("Execution of Readwrapper.py for "+str(data_file_name))

def get_key(code):
    #Get the Country name as per Country code
    for key, value in country_dictionary.items():
        if code == key:
            return value
    return "Key doesn't exist"
    

def check_read_source_file():

    # Check if input csv exists and store the csv in a data frame

    global metadata_file
    try:
        metadata_path=config['INCU']['DATA_FILE_DIR'] + data_file_name + '.csv'
        print(metadata_path)
        metadata_file=pd.read_csv(metadata_path)
        print('Input file details: \n' ) 
        print(metadata_file)
        #print(metadata_file.values.tolist())
        logging.info('Successfully read input source file')
    except Exception as e:
        print('Script exited due to errors. Please check logging file for more information. ')
        print('Logging file has been renamed to - ' + fail_filename)
        logging.error("Error while reading the input source file: "+str(e))
        os.rename(filename, fail_filename)
        exit(103)

def check_sql_scripts():
    
    # Check if sql_script input file exists

    global sql_input_script_path
    global original_sql_filename
    global original_sql_query

    try:
        original_sql_filename = 'CUSTOMER_DETAILS.SQL'
        sql_input_script_path=config['INCU']['SQL_SCRIPTS_DIR'] + original_sql_filename
        with open(sql_input_script_path, 'r') as file:
            original_sql_query=file.read()
        logging.info('Successfully read sql input script ' + str(sql_input_script_path))
    except Exception as e:
        print('Script exited due to errors. Please check logging file for more information.')
        print('Logging file has been renamed to - '+fail_filename)
        logging.error("Error while reading the sql input script: "+str(e))
        os.rename(filename, fail_filename)
        exit(105)


def modify_run_sql_query():

    try:
        # Modify the input query
        global country_name

        country_name=get_key(country_code)        
        updated_sql_query=original_sql_query.replace("#COUNTRY_NAME#", country_name).replace("#COUNTRY_CODE#", country_code)
        logging.info('Successfully modified the sql query and added country  info - ' + '(' + country_name + ')' + '(' + country_code + ')')

        # Run the modified query
        logging.info(updated_sql_query)
    except Exception as e:
        Error_msg = str(e)
        print('Script exited due to errors. Please check logging file for more information.')
        print('Logging file has been renamed to - '+fail_filename)
        logging.error("Error while trying to modify and run SQL query "+str(e))
        os.rename(filename, fail_filename)
        exit(110)

# All function calls


check_config_logon_files()  # Check if configuration files exist
check_read_source_file()  # Check if input files exist and read the file
check_sql_scripts() # Check if SQL files exist 
modify_run_sql_query() # Run if SQL files exist 


# End the time and store the information in the logging file
end = datetime.now().time().strftime('%H:%M:%S:%f')
total_td = datetime.strptime(end, '%H:%M:%S:%f') - datetime.strptime(start, '%H:%M:%S:%f')
logging.info('Time Taken for the copywrapper script: ' + str(total_td) + ' HH:MM:SS:seconds')
