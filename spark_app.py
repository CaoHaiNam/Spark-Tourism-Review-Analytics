from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests
import re

# create spark configuration
conf = SparkConf()
conf.setAppName("ReviewStreamApp")
# create spark instance with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# creat the Streaming Context from the above spark context with window size 2 seconds
ssc = StreamingContext(sc, 2)
# setting a checkpoint to allow RDD recovery
ssc.checkpoint("checkpoint_ReviewApp")
# read data from port 9009
dataStream = ssc.socketTextStream("localhost",1606)
# print(1)
# print(dataStream)
# sys.exit()

def aggregate_tags_count(new_values, total_sum):
    total_sum = total_sum if total_sum else (0,0,0,0)
    pos = [field[0] for field in new_values]
    neu = [field[1] for field in new_values]
    neg = [field[2] for field in new_values]
    count = [field[3] for field in new_values]

    return sum(pos)+total_sum[0], sum(neu)+total_sum[1], sum(neg)+total_sum[2], sum(count)+total_sum[3]

def send_df_to_dashboard(df):
    # extract the hashtags from dataframe and convert them into array
    aspects = [str(t.aspect) for t in df.select("aspect").collect()]
    # extract the counts from dataframe and convert them into array
    pos = [str(p.pos) for p in df.select("pos").collect()]
    neu = [str(p.neu) for p in df.select("neu").collect()]
    neg = [str(p.neg) for p in df.select("neg").collect()]
    # initialize and send the data through REST API
    request_data = {'label': str(aspects), 'data_pos': str(pos), 'data_neu': str(neu), 'data_neg': str(neg)}
    print(request_data)
    url = 'http://localhost:5001/updateData'
    response = requests.post(url, data=request_data)

# def print_data(df):
#     # extract the hashtags from dataframe and convert them into array
#     aspects = [str(t.aspect) for t in df.select("aspect").collect()]
#     # extract the counts from dataframe and convert them into array
#     pos = [str(p.pos) for p in df.select("pos").collect()]
#     neu = [str(p.neu) for p in df.select("neu").collect()]
#     neg = [str(p.neg) for p in df.select("neg").collect()]
#     print(type(pos[0]))
#     request_data = {'label': aspects, 'data_pos': pos, 'data_neu': neu, 'data_neg': neg}
#     print(request_data)

def get_sql_context_instance(spark_context):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']

def process_rdd(time, rdd):
    print("----------- %s -----------" % str(time))
    try:
        # Get spark sql singleton context from the current context
        sql_context = get_sql_context_instance(rdd.context)
        # convert the RDD to Row RDD
        # row_rdd = rdd.map(lambda w: Row(aspect=w[0].encode("utf-8"), pos=w[1][0], neu=w[1][1], neg=w[1][2],  aspect_count=w[1][3]))
        row_rdd = rdd.map(lambda w: Row(aspect=w[0], pos=w[1][0], neu=w[1][1], neg=w[1][2],  aspect_count=w[1][3]))
        # create a DF from the Row RDD
        aspects_df = sql_context.createDataFrame(row_rdd)
        # Register the dataframe as table
        aspects_df.registerTempTable("aspects")
        # get the top 10 hashtags from the table using SQL and print them
        aspect_counts_df = sql_context.sql("select aspect, aspect_count, pos, neu, neg from aspects order by aspect_count desc")
        aspect_counts_df.show()
        # call this method to prepare aspect DF and send them
        send_df_to_dashboard(aspect_counts_df)
        # print_data(aspect_counts_df)
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

def split_word(line):
    # return line
    data = line.split("||||")
    aspect = data[0]
    if data[1] == "POSITIVE":
        result = (aspect, 1, 0, 0)
    elif data[1] == "NORMAL":
        result = (aspect, 0, 1, 0)
    else:
        result = (aspect, 0, 0, 1)

    return result

# split each tweet into words
stream_data = dataStream.map(lambda x: split_word(x))
stream_data = stream_data.map(lambda x: (x[0], (x[1], x[2], x[3], 1)))
# adding the count of each hashtag to its last count
stream_data = stream_data.updateStateByKey(aggregate_tags_count)
# do processing for each RDD generated in each interval
stream_data.foreachRDD(process_rdd)
# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()



