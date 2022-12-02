FROM anasty17/mltb:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

COPY bkl-req.txt .
RUN pip3 install --no-cache-dir -r bkl-req.txt
COPY . .

CMD ["bash", "start.sh"]
