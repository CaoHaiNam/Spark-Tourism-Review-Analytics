import os

IN_DOCKER = os.environ.get('IN_DOCKER', False)

# paths
DATA_PATH = 'data/review_mini.csv'

# spark_stream
STREAM_HOST = 'stream' if IN_DOCKER else '0.0.0.0'
STREAM_PORT = 1606

# app
APP_HOST = 'app' if IN_DOCKER else '0.0.0.0'
APP_PORT = 9090

device = 'cpu'
num_labels = 36
tokenizer_name = 'xlm-roberta-base'

# RATING_ASPECTS = ["giai_tri", "luu_tru", "nha_hang", "an_uong", "di_chuyen", "mua_sam"]
RATING_ASPECTS = ["Entertainment", "Accommondation", "Restaurant", "Food", "Communication", "Shopping"]
