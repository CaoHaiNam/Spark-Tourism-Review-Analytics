import torch
import numpy as np 
import joblib
import pandas as pd
from configparser import ConfigParser

def config_db_params(filename='database.ini', section='mysql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def convert_logit(logit):
    res = []
    for i in range(0, 36, 6):
        x = logit[i:i+6]
        res.append(torch.argmax(x))
    res = torch.stack(res)
    return res

def get_sentiment(score):
    if score >= 4:
        return 'POSITIVE'
    elif score == 3:
        return 'NORMAL'
    else:
        return 'NEGATIVE'

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False