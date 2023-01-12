FROM anasty17/mltb:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
RUN python3.6 -m pip install aiohttp
RUN pip3 install playwright
RUN playwright install chromium
RUN playwright install-deps
COPY . .

CMD ["bash", "start.sh"]
