FROM anasty17/mltb:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install qbittorrent-api
RUN pip3 install aria2p
RUN pip3 install yt-dlp
COPY . .

CMD ["bash", "start.sh"]
