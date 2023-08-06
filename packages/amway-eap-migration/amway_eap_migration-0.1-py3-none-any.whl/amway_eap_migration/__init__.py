import yaml
import boto3
import json
import psycopg2 


def load_yml_file(file_loc):
    """ Function to load yml file from directory """
    with open(file_loc, 'r') as stream:
        config = yaml.safe_load(stream)

    return (config)


def get_config_yml(file_loc):
    yml_config_params=load_yml_file(file_loc)
    return(yml_config_params)


def get_sql_yml(file_loc):
    yml_sql_params=load_yml_file(file_loc)
    return(yml_sql_params)


def elapsedtime(start, end):
    temp = end-start
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    return('%d:%d:%d' %(hours,minutes,seconds))