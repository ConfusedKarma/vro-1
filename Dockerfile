FROM anasty17/mltb:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
python -m playwright install

COPY . .

CMD ["bash", "start.sh"]
