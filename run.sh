# eval "$(conda shell.bash hook)"
# conda activate add-std
python fake_stream.py & 
python spark_app.py &
python app.py