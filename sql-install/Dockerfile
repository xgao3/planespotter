FROM python:3.6-alpine
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY connect.py .
COPY MASTER.txt.gz /root/
COPY ACFTREF.txt.gz /root/
CMD [ "python", "-u" , "./connect.py" ]

