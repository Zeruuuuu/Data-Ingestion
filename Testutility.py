import yaml 
import logging
import os
import pandas as pd
import re


def read_config(file):
  with open(file, 'r') as ymal:
    try:
      config = yaml.load(ymal, Loader=yaml.Loader)
      config['columns'] = list(config['columns'])
      return config
    except yaml.YAMLError as err:
      logging.error(err)


def get_information(df, filepath):
  my_dict = {'columns':0, 'rows':0, 'file size in Mb':0}
  my_dict['rows'] = df.shape[0]
  my_dict['columns'] = df.shape[1]
  my_dict['file size in Mb'] = os.path.getsize(filepath)/1024 ** 2
  my_df = pd.DataFrame(my_dict, index = [0])
  return my_df


def reg(str):
  return re.sub('[^A-Za-z0-9]+', '', str)


def column_validation(df, config):
  df_list = []
  for i in df.columns:
    df_list.append(reg(i))
  df_list = map(lambda x: x.lower(), df_list)
  df_list = sorted(df_list)
  config_list = []
  for i in config['columns']:
    config_list.append(reg(i))
  config_list = map(lambda x: x.lower(), config_list)
  config_list = sorted(config_list)
  if len(df_list) == len(config_list) and df_list == config_list:
    print('validation passed')
    return 1
  else:
    print('validation failed')
    mismatch1 = list(set(config_list).difference(df_list))
    print(f'The columns in YAML config file that not detected in the uploaded data are {mismatch1}')
    mismatch2 = list(set(df_list).difference(config_list))
    print(f'The columns in the uploaded data that not found in config file are {mismatch2}')
    return 0
