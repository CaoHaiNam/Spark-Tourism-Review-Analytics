FROM python:3.9.13

WORKDIR /

COPY requirements.txt ./

# RUN pip3 install --upgrade pip 

RUN pip install -r requirements.txt 

COPY . .

EXPOSE 5001