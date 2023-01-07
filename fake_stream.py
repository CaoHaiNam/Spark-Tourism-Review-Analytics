import pathlib
import re
import os
import socket
from time import sleep
import pandas as pd
import config
import utils
from transformers import (
    AutoModelForSequenceClassification, 
    AutoTokenizer
)
import sys
import transformers
import torch
import mysql.connector
from datetime import datetime

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', config.STREAM_PORT))
s.listen(1)

device = 'cpu'
num_labels = 36
tokenizer_name = 'xlm-roberta-base'


# connection = mysql.connector.connect(host='localhost',
#                                         database='tourism_review',
#                                         user='namch',
#                                         password='Namch@1234')
params = utils.config_db_params()
connection = mysql.connector.connect(**params)

# RATING_ASPECTS = ["giai_tri", "luu_tru", "nha_hang", "an_uong", "di_chuyen", "mua_sam"]
mycursor = connection.cursor()
if not utils.checkTableExists(connection, 'review'):
    mycursor.execute("CREATE TABLE review (review TEXT, giai_tri INT, luu_tru INT, nha_hang INT, an_uong INT, di_chuyen INT, mua_sam INT, time VARCHAR(20))")

sql = "INSERT INTO review (review, giai_tri, luu_tru, nha_hang, an_uong, di_chuyen, mua_sam, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

model = AutoModelForSequenceClassification.from_pretrained('model', num_labels=num_labels).to(device)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

while True:
    # connect to spark app
    print('\nListening for a client at', config.STREAM_HOST, config.STREAM_PORT)
    conn, addr = s.accept()
    print('\nConnected by ', addr)

    # send lines to client
    try:
        print('\nReading file...\n')
        data = pd.read_csv(config.DATA_PATH)
        for index, row in data.iterrows():
            review = row['review']
            print(review)
            input = tokenizer(review, return_tensors="pt", padding='max_length', truncation=True, max_length=64).to(device)
            logit = model(**input)[0][0]
            predict_results = utils.convert_logit(logit).tolist()
            time = datetime.now()
            # time = time.strftime('%Y-%m-%d %H:%M:%S')
            time = time.strftime('%Y-%m-%d')
            val = (
                    review, 
                    predict_results[0], 
                    predict_results[1],
                    predict_results[2],
                    predict_results[3],
                    predict_results[4],
                    predict_results[5],
                    time    
                )
            mycursor.execute(sql, val)
            connection.commit()
            
            lines = []
            
            for count, r in enumerate(config.RATING_ASPECTS):
                if predict_results[count] > 0:
                    lines.append([r, utils.get_sentiment(predict_results[count])])
            for line in lines:
                mess = line[0] + '||||' + line[1] + '\n'
                # print('Sending lines for ' + row['stock_id'])
                print(line[0])
                conn.send(mess.encode('utf-8'))
            sleep(1.0)
        print('End Of Stream.')
    except socket.error as e:
        print('Error Occured.\n\nClient disconnected.\n')
        print(e)
        conn.close()
