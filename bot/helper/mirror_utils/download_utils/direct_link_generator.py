from requests import get as rget, head as rhead, post as rpost, Session as rsession
from re import findall as re_findall, sub as re_sub, match as re_match, search as re_search
import requests
import re

from time import sleep
from base64 import b64decode
from http.cookiejar import MozillaCookieJar
from os import path
from urllib.parse import urlparse, unquote
from json import loads as jsnloads
from lk21 import Bypass
from lxml import etree
from cfscrape import create_scraper
import cloudscraper
from bs4 import BeautifulSoup
from base64 import standard_b64encode
from bot import LOGGER, UPTOBOX_TOKEN, CRYPT, UNIFIED_EMAIL, UNIFIED_PASS, HUBDRIVE_CRYPT, KATDRIVE_CRYPT, DRIVEFIRE_CRYPT, XSRF_TOKEN, laravel_session
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import *
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException

fmed_list = ['fembed.net', 'fembed.com', 'femax20.com', 'fcdn.stream', 'feurl.com', 'layarkacaxxi.icu',
             'naniplay.nanime.in', 'naniplay.nanime.biz', 'naniplay.com', 'mm9842.com']


def direct_link_generator(link: str):
    """ direct links generator """
    if 'youtube.com' in link or 'youtu.be' in link:
        raise DirectDownloadLinkException(f"ERROR: Use /{BotCommands.WatchCommand} to mirror Youtube link\nUse /{BotCommands.ZipWatchCommand} to make zip of Youtube playlist")
    elif 'zippyshare.com' in link:
        return zippy_share(link)
    elif 'yadi.sk' in link or 'disk.yandex.com' in link:
        return yandex_disk(link)
    elif 'mediafire.com' in link:
        return mediafire(link)
    elif 'uptobox.com' in link:
        return uptobox(link)
    elif 'osdn.net' in link:
        return osdn(link)
    elif 'github.com' in link:
        return github(link)
    elif 'hxfile.co' in link:
        return hxfile(link)
    elif 'anonfiles.com' in link:
        return anonfiles(link)
    elif 'letsupload.io' in link:
        return letsupload(link)
    elif '1drv.ms' in link:
        return onedrive(link)
    elif 'pixeldrain.com' in link:
        return pixeldrain(link)
    elif 'antfiles.com' in link:
        return antfiles(link)
    elif 'streamtape.com' in link:
        return streamtape(link)
    elif 'bayfiles.com' in link:
        return anonfiles(link)
    elif 'racaty.net' in link:
        return racaty(link)
    elif '1fichier.com' in link:
        return fichier(link)
    elif 'solidfiles.com' in link:
        return solidfiles(link)
    elif 'krakenfiles.com' in link:
        return krakenfiles(link)
    elif is_gdtot_link(link):
        return gdtot(link)
    elif is_unified_link(link):
        return unified(link)
    elif is_udrive_link(link):
        return udrive(link)
    elif is_sharer_link(link):
        return sharer_pw(link)
    elif is_filepress_link(link):
        return filepress(link)
    elif is_sharer_scraper(link):
        return sharer(link)
    elif any(x in link for x in ['terabox', 'nephobox', '4funbox', 'mirrobox', 'momerybox', 'teraboxapp']):
        return terabox(link)
    elif 'rocklinks.net' in link:
        return rock(link)
    elif 'try2link.com' in link:
        return try2link(link)
    elif 'ez4short.com' in link:
        return ez4(link)
    elif 'send.cm' in link:
        return sendcm(link)
    # shareus
    elif "https://shareus.in/" in link:
        return shareus(link)
    elif 'mdisk.me' in link:
        return mdisk(link)
    elif 'gplinks.co' in link:
        return gplinks(link)
    elif 'gofile.io' in link:
        return gofile(link)
    elif 'linkbox' in link:
        return linkbox(link)
    elif 'xpshort.com' in link or 'techymozo.com' in link:
        return xpshort(link)
    elif any(x in link for x in fmed_list):
        return fembed(link)
    elif any(x in link for x in ['sbembed.com', 'watchsb.com', 'streamsb.net', 'sbplay.org']):
        return sbembed(link)
    else:
        raise DirectDownloadLinkException(f'No Direct link function found for {link}')

def zippy_share(url: str) -> str:
    """ ZippyShare direct link generator
    Based on https://github.com/zevtyardt/lk21 """
    return Bypass().bypass_zippyshare(url)

def yandex_disk(url: str) -> str:
    """ Yandex.Disk direct link generator
    Based on https://github.com/wldhx/yadisk-direct """
    try:
        link = re_findall(r'\b(https?://(yadi.sk|disk.yandex.com)\S+)', url)[0][0]
    except IndexError:
        return "No Yandex.Disk links found\n"
    api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
    try:
        return rget(api.format(link)).json()['href']
    except KeyError:
        raise DirectDownloadLinkException("ERROR: File not found/Download limit reached\n")

def uptobox(url: str) -> str:
    """ Uptobox direct link generator
    based on https://github.com/jovanzers/WinTenCermin and https://github.com/sinoobie/noobie-mirror """
    try:
        link = re_findall(r'\bhttps?://.*uptobox\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No Uptobox links found")
    if UPTOBOX_TOKEN is None:
        LOGGER.error('UPTOBOX_TOKEN not provided!')
        dl_url = link
    else:
        try:
            link = re_findall(r'\bhttp?://.*uptobox\.com/dl\S+', url)[0]
            dl_url = link
        except:
            file_id = re_findall(r'\bhttps?://.*uptobox\.com/(\w+)', url)[0]
            file_link = f'https://uptobox.com/api/link?token={UPTOBOX_TOKEN}&file_code={file_id}'
            req = rget(file_link)
            result = req.json()
            if result['message'].lower() == 'success':
                dl_url = result['data']['dlLink']
            elif result['message'].lower() == 'waiting needed':
                waiting_time = result["data"]["waiting"] + 1
                waiting_token = result["data"]["waitingToken"]
                sleep(waiting_time)
                req2 = rget(f"{file_link}&waitingToken={waiting_token}")
                result2 = req2.json()
                dl_url = result2['data']['dlLink']
            elif result['message'].lower() == 'you need to wait before requesting a new download link':
                cooldown = divmod(result['data']['waiting'], 60)
                raise DirectDownloadLinkException(f"ERROR: Uptobox is being limited please wait {cooldown[0]} min {cooldown[1]} sec.")
            else:
                LOGGER.info(f"UPTOBOX_ERROR: {result}")
                raise DirectDownloadLinkException(f"ERROR: {result['message']}")
    return dl_url

def mediafire(url: str) -> str:
    """ MediaFire direct link generator """
    try:
        link = re_findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No MediaFire links found\n")
    page = BeautifulSoup(rget(link).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    return info.get('href')

def osdn(url: str) -> str:
    """ OSDN direct link generator """
    osdn_link = 'https://osdn.net'
    try:
        link = re_findall(r'\bhttps?://.*osdn\.net\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No OSDN links found\n")
    page = BeautifulSoup(
        rget(link, allow_redirects=True).content, 'lxml')
    info = page.find('a', {'class': 'mirror_link'})
    link = unquote(osdn_link + info['href'])
    mirrors = page.find('form', {'id': 'mirror-select-form'}).findAll('tr')
    urls = []
    for data in mirrors[1:]:
        mirror = data.find('input')['value']
        urls.append(re_sub(r'm=(.*)&f', f'm={mirror}&f', link))
    return urls[0]

def github(url: str) -> str:
    """ GitHub direct links generator """
    try:
        re_findall(r'\bhttps?://.*github\.com.*releases\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No GitHub Releases links found\n")
    download = rget(url, stream=True, allow_redirects=False)
    try:
        return download.headers["location"]
    except KeyError:
        raise DirectDownloadLinkException("ERROR: Can't extract the link\n")

def hxfile(url: str) -> str:
    """ Hxfile direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    return Bypass().bypass_filesIm(url)

def anonfiles(url: str) -> str:
    """ Anonfiles direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    return Bypass().bypass_anonfiles(url)

def letsupload(url: str) -> str:
    """ Letsupload direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    try:
        link = re_findall(r'\bhttps?://.*letsupload\.io\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No Letsupload links found\n")
    return Bypass().bypass_url(link)

def fembed(link: str) -> str:
    """ Fembed direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    dl_url= Bypass().bypass_fembed(link)
    count = len(dl_url)
    lst_link = [dl_url[i] for i in dl_url]
    return lst_link[count-1]

def sbembed(link: str) -> str:
    """ Sbembed direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    dl_url= Bypass().bypass_sbembed(link)
    count = len(dl_url)
    lst_link = [dl_url[i] for i in dl_url]
    return lst_link[count-1]

def onedrive(link: str) -> str:
    """ Onedrive direct link generator
    Based on https://github.com/UsergeTeam/Userge """
    link_without_query = urlparse(link)._replace(query=None).geturl()
    direct_link_encoded = str(standard_b64encode(bytes(link_without_query, "utf-8")), "utf-8")
    direct_link1 = f"https://api.onedrive.com/v1.0/shares/u!{direct_link_encoded}/root/content"
    resp = rhead(direct_link1)
    if resp.status_code != 302:
        raise DirectDownloadLinkException("ERROR: Unauthorized link, the link may be private")
    dl_link = resp.next.url
    return dl_link

def pixeldrain(url: str) -> str:
    """ Based on https://github.com/yash-dk/TorToolkit-Telegram """
    url = url.strip("/ ")
    file_id = url.split("/")[-1]
    if url.split("/")[-2] == "l":
        info_link = f"https://pixeldrain.com/api/list/{file_id}"
        dl_link = f"https://pixeldrain.com/api/list/{file_id}/zip"
    else:
        info_link = f"https://pixeldrain.com/api/file/{file_id}/info"
        dl_link = f"https://pixeldrain.com/api/file/{file_id}"
    resp = rget(info_link).json()
    if resp["success"]:
        return dl_link
    else:
        raise DirectDownloadLinkException("ERROR: Cant't download due {}.".format(resp["message"]))

def antfiles(url: str) -> str:
    """ Antfiles direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    return Bypass().bypass_antfiles(url)

def streamtape(url: str) -> str:
    """ Streamtape direct link generator
    Based on https://github.com/zevtyardt/lk21
    """
    return Bypass().bypass_streamtape(url)

def racaty(url: str) -> str:
    """ Racaty direct link generator
    based on https://github.com/SlamDevs/slam-mirrorbot"""
    dl_url = ''
    try:
        re_findall(r'\bhttps?://.*racaty\.net\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No Racaty links found")
    scraper = create_scraper()
    r = scraper.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    op = soup.find("input", {"name": "op"})["value"]
    ids = soup.find("input", {"name": "id"})["value"]
    rapost = scraper.post(url, data = {"op": op, "id": ids})
    rsoup = BeautifulSoup(rapost.text, "lxml")
    dl_url = rsoup.find("a", {"id": "uniqueExpirylink"})["href"].replace(" ", "%20")
    return dl_url

def fichier(link: str) -> str:
    """ 1Fichier direct link generator
    Based on https://github.com/Maujar
    """
    regex = r"^([http:\/\/|https:\/\/]+)?.*1fichier\.com\/\?.+"
    gan = re_match(regex, link)
    if not gan:
      raise DirectDownloadLinkException("ERROR: The link you entered is wrong!")
    if "::" in link:
      pswd = link.split("::")[-1]
      url = link.split("::")[-2]
    else:
      pswd = None
      url = link
    try:
      if pswd is None:
        req = rpost(url)
      else:
        pw = {"pass": pswd}
        req = rpost(url, data=pw)
    except:
      raise DirectDownloadLinkException("ERROR: Unable to reach 1fichier server!")
    if req.status_code == 404:
      raise DirectDownloadLinkException("ERROR: File not found/The link you entered is wrong!")
    soup = BeautifulSoup(req.content, 'lxml')
    if soup.find("a", {"class": "ok btn-general btn-orange"}) is not None:
        dl_url = soup.find("a", {"class": "ok btn-general btn-orange"})["href"]
        if dl_url is None:
          raise DirectDownloadLinkException("ERROR: Unable to generate Direct Link 1fichier!")
        else:
          return dl_url
    elif len(soup.find_all("div", {"class": "ct_warn"})) == 2:
        str_2 = soup.find_all("div", {"class": "ct_warn"})[-1]
        if "you must wait" in str(str_2).lower():
            numbers = [int(word) for word in str(str_2).split() if word.isdigit()]
            if not numbers:
                raise DirectDownloadLinkException("ERROR: 1fichier is on a limit. Please wait a few minutes/hour.")
            else:
                raise DirectDownloadLinkException(f"ERROR: 1fichier is on a limit. Please wait {numbers[0]} minute.")
        elif "protect access" in str(str_2).lower():
          raise DirectDownloadLinkException(f"ERROR: This link requires a password!\n\n<b>This link requires a password!</b>\n- Insert sign <b>::</b> after the link and write the password after the sign.\n\n<b>Example:</b>\n<code>/{BotCommands.MirrorCommand} https://1fichier.com/?smmtd8twfpm66awbqz04::love you</code>\n\n* No spaces between the signs <b>::</b>\n* For the password, you can use a space!")
        else:
            raise DirectDownloadLinkException("ERROR: Error trying to generate Direct Link from 1fichier!")
    elif len(soup.find_all("div", {"class": "ct_warn"})) == 3:
        str_1 = soup.find_all("div", {"class": "ct_warn"})[-2]
        str_3 = soup.find_all("div", {"class": "ct_warn"})[-1]
        if "you must wait" in str(str_1).lower():
            numbers = [int(word) for word in str(str_1).split() if word.isdigit()]
            if not numbers:
                raise DirectDownloadLinkException("ERROR: 1fichier is on a limit. Please wait a few minutes/hour.")
            else:
                raise DirectDownloadLinkException(f"ERROR: 1fichier is on a limit. Please wait {numbers[0]} minute.")
        elif "bad password" in str(str_3).lower():
          raise DirectDownloadLinkException("ERROR: The password you entered is wrong!")
        else:
            raise DirectDownloadLinkException("ERROR: Error trying to generate Direct Link from 1fichier!")
    else:
        raise DirectDownloadLinkException("ERROR: Error trying to generate Direct Link from 1fichier!")

def solidfiles(url: str) -> str:
    """ Solidfiles direct link generator
    Based on https://github.com/Xonshiz/SolidFiles-Downloader
    By https://github.com/Jusidama18 """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
    }
    pageSource = rget(url, headers = headers).text
    mainOptions = str(re_search(r'viewerOptions\'\,\ (.*?)\)\;', pageSource).group(1))
    return jsnloads(mainOptions)["downloadUrl"]

def krakenfiles(page_link: str) -> str:
    """ krakenfiles direct link generator
    Based on https://github.com/tha23rd/py-kraken
    By https://github.com/junedkh """
    page_resp = rsession().get(page_link)
    soup = BeautifulSoup(page_resp.text, "lxml")
    try:
        token = soup.find("input", id="dl-token")["value"]
    except:
        raise DirectDownloadLinkException(f"Page link is wrong: {page_link}")

    hashes = [
        item["data-file-hash"]
        for item in soup.find_all("div", attrs={"data-file-hash": True})
    ]
    if not hashes:
        raise DirectDownloadLinkException(
            f"Hash not found for : {page_link}")

    dl_hash = hashes[0]

    payload = f'------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="token"\r\n\r\n{token}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'
    headers = {
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        "cache-control": "no-cache",
        "hash": dl_hash,
    }

    dl_link_resp = rsession().post(
        f"https://krakenfiles.com/download/{hash}", data=payload, headers=headers)

    dl_link_json = dl_link_resp.json()

    if "url" in dl_link_json:
        return dl_link_json["url"]
    else:
        raise DirectDownloadLinkException(
            f"Failed to acquire download URL from kraken for : {page_link}")

def gdtot(url: str) -> str:
    """ Gdtot google drive link generator
    By https://github.com/xcscxr """

    if CRYPT is None:
        raise DirectDownloadLinkException("ERROR: CRYPT cookie not provided")

    match = re_findall(r'https?://(.+)\.gdtot\.(.+)\/\S+\/\S+', url)[0]

    with rsession() as client:
        client.cookies.update({'crypt': CRYPT})
        client.get(url)
        res = client.get(f"https://{match[0]}.gdtot.{match[1]}/dld?id={url.split('/')[-1]}")
    matches = re_findall('gd=(.*?)&', res.text)
    try:
        decoded_id = b64decode(str(matches[0])).decode('utf-8')
    except:
        raise DirectDownloadLinkException("ERROR: Try in your broswer, mostly file not found or user limit exceeded!")
    return f'https://drive.google.com/open?id={decoded_id}'
  
account = {
   'email': UNIFIED_EMAIL, 
   'passwd': UNIFIED_PASS
}

def account_login(client, url, email, password):
    data = {
        'email': email,
        'password': password
    }
    client.post(f'https://{urlparse(url).netloc}/login', data=data)
    
def gen_payload(data, boundary=f'{"-"*6}_'):
    data_string = ''
    for item in data:
        data_string += f'{boundary}\r\n'
        data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
    data_string += f'{boundary}--\r\n'
    return data_string

def parse_infou(data):
    info = re_findall('>(.*?)<\/li>', data)
    info_parsed = {}
    for item in info:
        kv = [s.strip() for s in item.split(':', maxsplit = 1)]
        info_parsed[kv[0].lower()] = kv[1]
    return info_parsed

def unified(url: str) -> str:
    if (UNIFIED_EMAIL or UNIFIED_PASS) is None:
        raise DirectDownloadLinkException("UNIFIED_EMAIL and UNIFIED_PASS env vars not provided")
    client = cloudscraper.create_scraper(delay=10, browser='chrome')
    client.headers.update({
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    })

    account_login(client, url, account['email'], account['passwd'])

    res = client.get(url)
    key = re_findall('"key",\s+"(.*?)"', res.text)[0]

    ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")

    info_parsed = parse_infou(res.text)
    info_parsed['error'] = False
    info_parsed['link_type'] = 'login' # direct/login
    
    headers = {
        "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
    }
    
    data = {
        'type': 1,
        'key': key,
        'action': 'original'
    }
    
    if len(ddl_btn):
        info_parsed['link_type'] = 'direct'
        data['action'] = 'direct'
    
    while data['type'] <= 3:
        try:
            response = client.post(url, data=gen_payload(data), headers=headers).json()
            break
        except: data['type'] += 1
        
    if 'url' in response:
        info_parsed['gdrive_link'] = response['url']
    elif 'error' in response and response['error']:
        info_parsed['error'] = True
        info_parsed['error_message'] = response['message']
    else:
        info_parsed['error'] = True
        info_parsed['error_message'] = 'Something went wrong :('
        
    if info_parsed['error']:
        raise DirectDownloadLinkException(f"ERROR! {info_parsed['error_message']}")
    
    if urlparse(url).netloc == 'appdrive.info':
        flink = info_parsed['gdrive_link']
        return flink
      
    elif urlparse(url).netloc == 'gdflix.lol':
        flink = info_parsed['gdrive_link']
        return flink
    
    elif urlparse(url).netloc == 'driveapp.in':
        res = client.get(info_parsed['gdrive_link'])
        drive_link = etree.HTML(res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
        flink = drive_link
        return flink
      
    else:
        res = client.get(info_parsed['gdrive_link'])
        drive_link = etree.HTML(res.content).xpath("//a[contains(@class,'btn btn-primary')]/@href")[0]
        flink = drive_link
        info_parsed['src_url'] = url
        return flink

def parse_info(res, url):
    info_parsed = {}
    if 'drivebuzz' in url:
        info_chunks = re_findall('<td\salign="right">(.*?)<\/td>', res.text)
    else:
        info_chunks = re_findall('>(.*?)<\/td>', res.text)
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed
  
def udrive(url: str) -> str:
    if 'katdrive' or 'hubdrive' in url:
      client = rsession()
    else:
      client = cloudscraper.create_scraper(delay=10, browser='chrome')
    
    if "hubdrive" in url:
        if "hubdrive.in" in url:
            url = url.replace(".in",".pro",".cc",".top",".mx",".tv")
        client.cookies.update({'crypt': HUBDRIVE_CRYPT})
    if 'drivehub' in url:
        client.cookies.update({'crypt': KATDRIVE_CRYPT})
    if 'katdrive' in url:
        client.cookies.update({'crypt': KATDRIVE_CRYPT})
    if "kolop" in url:
        if "kolop.icu" in url:
            url = url.replace(".icu",".cyou")
        client.cookies.update({'crypt': KATDRIVE_CRYPT})
    if 'drivefire' in url:
        client.cookies.update({'crypt': DRIVEFIRE_CRYPT})
    if 'drivebuzz' in url:
        client.cookies.update({'crypt': DRIVEFIRE_CRYPT})
        
    res = client.get(url)
    info_parsed = parse_info(res, url)
    
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    
    data = { 'id': file_id }
    
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except: return {'error': True, 'src_url': url}
    
    if 'drivefire' in url:
        decoded_id = res.rsplit('/', 1)[-1]
        flink = f"https://drive.google.com/file/d/{decoded_id}"
        return flink
    elif 'drivehub' in url:
        gd_id = res.rsplit("=", 1)[-1]
        flink = f"https://drive.google.com/open?id={gd_id}"
        return flink
    elif 'drivebuzz' in url:
        gd_id = res.rsplit("=", 1)[-1]
        flink = f"https://drive.google.com/open?id={gd_id}"
        return flink
    else:
        gd_id = re_findall('gd=(.*)', res, re.DOTALL)[0]
 
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url
    flink = info_parsed['gdrive_url']

    return flink

def sharer_pw(url: str)-> str:
    
    client = cloudscraper.create_scraper(delay=10, browser='chrome')
    client.cookies["XSRF-TOKEN"] = XSRF_TOKEN
    client.cookies["laravel_session"] = laravel_session
    
    res = client.get(url)
    token = re.findall("_token\s=\s'(.*?)'", res.text, re.DOTALL)[0]
    data = { '_token': token, 'nl' :1}
    headers={ 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'x-requested-with': 'XMLHttpRequest'}

    try:
        response = client.post(url+'/dl', headers=headers, data=data).json()
        drive_link = response
        return drive_link['url']
    
    except:
        if drive_link["message"] == "OK":
            raise DirectDownloadLinkException("Something went wrong. Could not generate GDrive URL for your Sharer Link")
        else:
            finalMsg = BeautifulSoup(drive_link["message"], "lxml").text
            raise DirectDownloadLinkException(finalMsg)

def rock(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'rocklinks.net' in url:
        DOMAIN = "https://rl.techysuccess.com"
    else:
        DOMAIN = "https://rocklinks.net"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    if 'rocklinks.net' in url:
        final_url = f"{DOMAIN}/{code}?quelle=" 
    else:
        final_url = f"{DOMAIN}/{code}"
    ref = "https://disheye.com/"
    
    h = {"referer": ref}

    resp = client.get(final_url,headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    sleep(10)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("

def try2link(url):
    client = create_scraper()    
    url = url[:-1] if url[-1] == '/' else url    
    params = (('d', int(time.time()) + (60 * 4)),)
    r = client.get(url, params=params, headers= {'Referer': 'https://newforex.online/'})   
    soup = BeautifulSoup(r.text, 'html.parser')
    inputs = soup.find_all("input")
    data = { input.get('name'): input.get('value') for input in inputs }
    sleep(7)    
    headers = {'Host': 'try2link.com', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://try2link.com', 'Referer': url}    
    bypassed_url = client.post('https://try2link.com/links/go', headers=headers,data=data)
    return bypassed_url.json()["url"]

def ez4(url):    
    client = cloudscraper.create_scraper(allow_brotli=False)      
    DOMAIN = "https://ez4short.com"     
    ref = "https://techmody.io/"   
    h = {"referer": ref}  
    resp = client.get(url,headers=h)   
    soup = BeautifulSoup(resp.content, "html.parser")    
    inputs = soup.find_all("input")   
    data = { input.get('name'): input.get('value') for input in inputs }
    h = { "x-requested-with": "XMLHttpRequest" }   
    sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("

def shareus(url):
    token = url.split("=")[-1]
    bypassed_url = "https://us-central1-my-apps-server.cloudfunctions.net/r?shortid="+ token
    response = requests.get(bypassed_url).text
    return response

def terabox(url) -> str:
    if not path.isfile('terabox.txt'):
        raise DirectDownloadLinkException("ERROR: terabox.txt not found")
    try:
        session = rsession()
        res = session.request('GET', url)
        key = res.url.split('?surl=')[-1]
        jar = MozillaCookieJar('terabox.txt')
        jar.load()
        session.cookies.update(jar)
        res = session.request('GET', f'https://www.terabox.com/share/list?app_id=250528&shorturl={key}&root=1')
        result = res.json()['list']
    except Exception as e:
        raise DirectDownloadLinkException(f"ERROR: {e.__class__.__name__}")
    if len(result) > 1:
        raise DirectDownloadLinkException("ERROR: Can't download mutiple files")
    result = result[0]
    if result['isdir'] != '0':
        raise DirectDownloadLinkException("ERROR: Can't download folder")
    return result['dlink']

def mdisk(url: str) -> str:
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    url = url[:-1] if url[-1] == '/' else url
    token = url.split("/")[-1]
    
    
    api = f"https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={token}"
    
    response = requests.get(api, headers=headers).json() 
        
    download_url = response["download"]
    download_url = download_url.replace(" ", "%20")
    
    return download_url

def gofile(url:str) -> str:
    
    api_uri = "https://api.gofile.io" 
    url = url[:-1] if url[-1] == '/' else url
    client = requests.Session()
    
    response  = client.get(f"{api_uri}/createAccount").json()
    
    data = {
        "contentId": url.split("/")[-1],
        "token": response ["data"]["token"],
        "websiteToken": 12345,
        "cache": "true",
    }
    response  = client.get(f"{api_uri}/getContent", params=data).json()
    
    for item in response["data"]["contents"].values():
        content = item
        download_url= content["link"]
       
        return download_url

def sendcm(url:str) -> str:
    
    base_url = "https://send.cm/"
    client = requests.Session()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    }
    
    response  = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    
    inputs = soup.find_all("input")
    file_id = inputs[1]["value"]
    file_name = re.findall("URL=(.*?) - ", response)[0].split("]")[1]
    parse = {"op": "download2", "id": file_id, "referer": url}
    
    resp = client.post(base_url, data=parse, headers=headers, allow_redirects=False)
    download_url = resp.headers["Location"]
    
    return download_url 

def gplinks(url: str):
 
 url = url[:-1] if url[-1] == '/' else url
 token = url.split("/")[-1]
    
 domain ="https://gplinks.co/"
 referer = "https://mynewsmedia.co/"

    
 client = requests.Session()
 vid = client.get(url, allow_redirects= False).headers["Location"].split("=")[-1]
 url = f"{url}/?{vid}"

 response = client.get(url, allow_redirects=False)
 soup = BeautifulSoup(response.content, "html.parser")
    
    
 inputs = soup.find(id="go-link").find_all(name="input")
 data = { input.get('name'): input.get('value') for input in inputs }
    

 sleep(10)
 headers={"x-requested-with": "XMLHttpRequest"}
 bypassed_url = client.post(domain+"links/go", data=data, headers=headers).json()["url"]
 return bypassed_url

def filepress(url):
    cget = create_scraper().request
    try:
        url = cget('GET', url).url
        raw = urlparse(url)
        json_data = {
            'id': raw.path.split('/')[-1],
            'method': 'publicDownlaod',
            }
        api = f'{raw.scheme}://{raw.hostname}/api/file/downlaod/'
        res = cget('POST', api, headers={'Referer': f'{raw.scheme}://{raw.hostname}'}, json=json_data).json()
    except Exception as e:
        raise DirectDownloadLinkException(f'ERROR: {e.__class__.__name__}')
    if 'data' not in res:
        raise DirectDownloadLinkException(f'ERROR: {res["statusText"]}')
    return f'https://drive.google.com/open?id={res["data"]}'

def sharer(url):
    try:
        cget = create_scraper().request
        url = cget('GET', url).url
        raw = urlparse(url)
        res = cget('GET', url)
    except Exception as e:
        raise DirectDownloadLinkException(f'ERROR: {e.__class__.__name__}')
    key = re_findall('"key",\s+"(.*?)"', res.text)
    if not key:
        raise DirectDownloadLinkException("ERROR: Key not found!")
    key = key[0]
    if not etree.HTML(res.content).xpath("//button[@id='drc']"):
        raise DirectDownloadLinkException("ERROR: This link don't have direct download button")
    headers = {
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryi3pOrWU7hGYfwwL4',
        'x-token': raw.hostname,
    }
    data = '------WebKitFormBoundaryi3pOrWU7hGYfwwL4\r\nContent-Disposition: form-data; name="action"\r\n\r\ndirect\r\n' \
        f'------WebKitFormBoundaryi3pOrWU7hGYfwwL4\r\nContent-Disposition: form-data; name="key"\r\n\r\n{key}\r\n' \
        '------WebKitFormBoundaryi3pOrWU7hGYfwwL4\r\nContent-Disposition: form-data; name="action_token"\r\n\r\n\r\n' \
        '------WebKitFormBoundaryi3pOrWU7hGYfwwL4--\r\n'
    try:
        res = cget("POST", url, cookies=res.cookies, headers=headers, data=data).json()
    except Exception as e:
        raise DirectDownloadLinkException(f'ERROR: {e.__class__.__name__}')
    if "url" not in res:
        raise DirectDownloadLinkException('ERROR: Drive Link not found')
    if "drive.google.com" in res["url"]:
        return res["url"]
    try:
        res = cget('GET', res["url"])
    except Exception as e:
        raise DirectDownloadLinkException(f'ERROR: {e.__class__.__name__}')
    if (drive_link := etree.HTML(res.content).xpath("//a[contains(@class,'btn')]/@href")) and "drive.google.com" in drive_link[0]:
        return drive_link[0]
    else:
        raise DirectDownloadLinkException('ERROR: Drive Link not found')

def xpshort(url):
     
    client = requests.session()
    
    
    DOMAIN = "https://push.bdnewsx.com"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    
    final_url = f"{DOMAIN}/{code}"
    
    ref = "https://blog.finsurances.co/"
    
    h = {"referer": ref}
  
    resp = client.get(final_url,headers=h)
    
    soup = BeautifulSoup(resp.content, "html.parser")
    
    inputs = soup.find_all("input")
   
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("

def linkbox(url):
    cget = create_scraper().request
    try:
        url = cget('GET', url).url
        res = cget(
            'GET', f'https://www.linkbox.to/api/file/detail?itemId={url.split("/")[-1]}').json()
    except Exception as e:
        raise DirectDownloadLinkException(f'ERROR: {e.__class__.__name__}')
    if 'data' not in res:
        raise DirectDownloadLinkException('ERROR: Data not found!!')
    data = res['data']
    if not data:
        raise DirectDownloadLinkException('ERROR: Data is None!!')
    if 'itemInfo' not in data:
        raise DirectDownloadLinkException('ERROR: itemInfo not found!!')
    itemInfo = data['itemInfo']
    if 'url' not in itemInfo:
        raise DirectDownloadLinkException('ERROR: url not found in itemInfo!!')
    if "name" not in itemInfo:
        raise DirectDownloadLinkException(
            'ERROR: Name not found in itemInfo!!')
    name = quote(itemInfo["name"])
    raw = itemInfo['url'].split("/", 3)[-1]
    return f'https://wdl.nuplink.net/{raw}&filename={name}'
