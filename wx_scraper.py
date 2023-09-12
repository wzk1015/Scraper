import requests
import re
from bs4 import BeautifulSoup
import bs4
from functools import partial
import json
from pprint import pprint
from utils import text_contains, class_starts_with

headers = {
    "authority": "edith.xiaohongshu.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
    "origin": "https://www.xiaohongshu.com",
    "referer": "https://www.xiaohongshu.com/",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "x-b3-traceid": "8f7e9cb6b20eb2b4",
    "x-s": "XYW_eyJzaWduU3ZuIjoiNTEiLCJzaWduVHlwZSI6IngxIiwiYXBwSWQiOiJ4aHM\
tcGMtd2ViIiwic2lnblZlcnNpb24iOiIxIiwicGF5bG9hZCI6IjE0YTg1NWRkMTVjY2RlODZlOG\
U2YTk2NGZlMjMyNjg2ZjE4NjhhZmZjN2IwYWU0N2QxN2U2ODExYTZiZDQwMDg3YWM2MmZhMWNhZD\
QxYjVjNjEwYjNmOGE1MjM2ZWYzZmM5ZTNiZmRhMWZhYTFlYjkwZDc0YWEzMWI1NGM3MmNkMGQ3NG\
FhMzFiNTRjNzJjZGFjNDg5YjlkYThjZTVlNDhmNGFmYjlhY2ZjM2VhMjZmZTBiMjY2YTZiNGNjM2N\
iNTlmYjYyODAzMTM3MjIyNmJjN2RkNGJiNGU3NjZiMmNhZmVhMzhkYzc5MWNiYWM3YjdlYzBlYzM1\
ZGQxZTFlNTIxYjQxM2IwNWM1YmY2ZDM0Y2IwODMxODhiZGQyMjgzYzJjYTc1OTllZWQxOTM2ZmFjYT\
AxMjk4OTE1ZjlhNzliZWIyNjZhN2E5YzBkNzkzZjVhYjgzYjgyYmFhODZhOWJhMzY2NjU3ZDgzM\
2Q0YTU2ZWY5ZDFjNmZiMzhkMjE5OSJ9",
    "x-s-common": "2UQAPsHCPUIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0P1PUhAHjIj2eHjwjQ+GnPW/M\
PjNsQhPUHCHdYiqUMIGUM78nHjNsQh+sHCH0H1P/r1+UHVHdWMH0ijP/WhGAPI80+jP/LI4g8Y+nYYP98IqgSl\
JBTk8nMD+gQY+e8j+oSiPdPAPeZIPeHAw/Z9PaHVHdW9H0il+0W7w/cl+/LhPeWMNsQh+UHCHSY8pMRS2LkCGp4\
D4pLAndpQyfRk/SzbyLleadkYp9zMpDYV4Mk/a/8QJf4hanS7ypSGcd4/pMbk/9St+BbH/gz0zFMF8eQnyLSk49S\
0Pfl1GflyJB+1/dmjP0zk/9SQ2rSk49S0zFGMGDqEybkea/8QyDLInpzdPLEgLfT+pb8xn/QaJrRrnflOzMLUnpz3\
PDEonfl+yDME/fkdPSkxz/zwyfYinfMyyDhUag48pMLI/0Qz2rhUp/QOzrphnpzyypkrLg4+zBqAnp4+PDMTnfY+pF\
EinDzz2bSxpfkwyDp7nnkwJLRoz/b+yDFUnS482SkT//pyprEknfMayrMgnfY8pr8Vnnk34MkrGAm8pFpC/p4QPLEo//\
++JLE3/L4zPFEozfY+2D8k/SzayDECafkyzF8x/Dzd+pSxJBT8pBYxnSznJrEryBMwzF8TnnkVybDUnfk+PS8i/nkyJ\
pkLcfS+ySDUnpzyyLEo/fk+PDEk/SzVJpSxngSOzrbC/pz+PFMxagSwJLkx/0QayFEoafSwzMLA/fkyyLMT/fYyJp8i\
/gkiyMSCGAp+pFEknp4+PMSx8Bl82DQVngk+PpkoLgYypr8V/SzQ2bSxLgY+PDS7/S4+PpSTn/QyzrFIn/QQ4FRr/\
gYOzBYknD4z2LMx87k82Dkxnpz0PLRLJBlypMbh/Mz+PSkTzfk8prbh/nk3+rRLz/byyfli/dkVypkgagSwySki/\
0Qb+pSCcfTw2fTCnfknybSx87k8yf4EnnMByrRrnfYOpFki/gk8PDExp/+yzB4C//QzPbSLp/QypMDMnDzByDETnfS\
+2fY3/nkb+LR/a0DjNsQhwsHCHDDAwoQH8B4AyfRI8FS98g+Dpd4daLP3JFSb/BMsn0pSPM87nrldzSzQ2bPAGdb7z\
gQB8nph8emSy9E0cgk+zSS1qgzianYt8p+1/LzN4gzaa/+NqMS6qS4HLozoqfQnPbZEp98QyaRSp9P98pSl4oSzcg\
mca/P78nTTL0bz/sVManD9q9z1J7+xJMcM2gbFnobl4MSUcdb6agW3tF4ryaRApdz3agWIq7YM47HFqgzkanTU4FSk\
N7+3G9PAaL+P8DDA/9LI4gzVP0mrnd+P+nprLFkSyS87PrSk8nphpd4PtMmFJ7Ql4BYcpFTS2bDhJFSeL0bQzgQ/8M8\
7cD4l4bQQ2rL68LzD8p8M49kQcAmAPgbFJDS3qrTQyrzA8nLAqMSDLe80p/pAngbF2fbr8Bpf2drl2fc68p4gzjTQ2o8S\
LM8FNFSba9pDLocEqdkMpLR6pD4Q4f4SygbF4aR889phydbTanTP4FSkzbmoGnMxag8iJaTQweYQygkMcS87JrS9zFGF8g8\
SzbP78/bM4r+QcA4AzBPROaHVHdWEH0iTP0q9+AqIweZINsQhP/Zjw08R",
    "x-t": "1687941558085",
}

cookies = {
    "a1": "188c30f3b150uva5ha3fpqyqlkiemd5ra46b4yh2s30000239061",
    "webId": "7b3ef57181f484cbd9767558c54b442a",
    "gid": "yYYSq8iqi40JyYYSq8iqD4vxy287h02x0qiUKJMAvA1T3Dq8d6f2F4888Jqj8Ky8DiJy0j8y",
    "gid.sign": "WAFuLJ9fLM/MW4L5ofdqxXFPM6U=",
    "webBuild": "2.11.7",
    "xsecappid": "xhs-pc-web",
    "web_session": "030037a3a8bbf037e7dbc8a9e3234a91320b14",
    "websectiga": "634d3ad75ffb42a2ade2c5e1705a73c845837578aeb31ba0e442d75c648da36a",
    "sec_poison_id": "7971d651-c530-420d-b3c9-da774f9c06aa",
}

headers_ios = {
    "authority": "edith.xiaohongshu.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
    "origin": "https://www.xiaohongshu.com",
    "referer": "https://www.xiaohongshu.com/",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/84.0.4147.122 Mobile/15E148 Safari/604.1",
    "x-b3-traceid": "8f7e9cb6b20eb2b4",
    "x-s": "XYW_eyJzaWduU3ZuIjoiNTEiLCJzaWduVHlwZSI6IngxIiwiYXBwSWQiOiJ4aHM\
tcGMtd2ViIiwic2lnblZlcnNpb24iOiIxIiwicGF5bG9hZCI6IjE0YTg1NWRkMTVjY2RlODZlOG\
U2YTk2NGZlMjMyNjg2ZjE4NjhhZmZjN2IwYWU0N2QxN2U2ODExYTZiZDQwMDg3YWM2MmZhMWNhZD\
QxYjVjNjEwYjNmOGE1MjM2ZWYzZmM5ZTNiZmRhMWZhYTFlYjkwZDc0YWEzMWI1NGM3MmNkMGQ3NG\
FhMzFiNTRjNzJjZGFjNDg5YjlkYThjZTVlNDhmNGFmYjlhY2ZjM2VhMjZmZTBiMjY2YTZiNGNjM2N\
iNTlmYjYyODAzMTM3MjIyNmJjN2RkNGJiNGU3NjZiMmNhZmVhMzhkYzc5MWNiYWM3YjdlYzBlYzM1\
ZGQxZTFlNTIxYjQxM2IwNWM1YmY2ZDM0Y2IwODMxODhiZGQyMjgzYzJjYTc1OTllZWQxOTM2ZmFjYT\
AxMjk4OTE1ZjlhNzliZWIyNjZhN2E5YzBkNzkzZjVhYjgzYjgyYmFhODZhOWJhMzY2NjU3ZDgzM\
2Q0YTU2ZWY5ZDFjNmZiMzhkMjE5OSJ9",
    "x-s-common": "2UQAPsHCPUIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0P1PUhAHjIj2eHjwjQ+GnPW/M\
PjNsQhPUHCHdYiqUMIGUM78nHjNsQh+sHCH0H1P/r1+UHVHdWMH0ijP/WhGAPI80+jP/LI4g8Y+nYYP98IqgSl\
JBTk8nMD+gQY+e8j+oSiPdPAPeZIPeHAw/Z9PaHVHdW9H0il+0W7w/cl+/LhPeWMNsQh+UHCHSY8pMRS2LkCGp4\
D4pLAndpQyfRk/SzbyLleadkYp9zMpDYV4Mk/a/8QJf4hanS7ypSGcd4/pMbk/9St+BbH/gz0zFMF8eQnyLSk49S\
0Pfl1GflyJB+1/dmjP0zk/9SQ2rSk49S0zFGMGDqEybkea/8QyDLInpzdPLEgLfT+pb8xn/QaJrRrnflOzMLUnpz3\
PDEonfl+yDME/fkdPSkxz/zwyfYinfMyyDhUag48pMLI/0Qz2rhUp/QOzrphnpzyypkrLg4+zBqAnp4+PDMTnfY+pF\
EinDzz2bSxpfkwyDp7nnkwJLRoz/b+yDFUnS482SkT//pyprEknfMayrMgnfY8pr8Vnnk34MkrGAm8pFpC/p4QPLEo//\
++JLE3/L4zPFEozfY+2D8k/SzayDECafkyzF8x/Dzd+pSxJBT8pBYxnSznJrEryBMwzF8TnnkVybDUnfk+PS8i/nkyJ\
pkLcfS+ySDUnpzyyLEo/fk+PDEk/SzVJpSxngSOzrbC/pz+PFMxagSwJLkx/0QayFEoafSwzMLA/fkyyLMT/fYyJp8i\
/gkiyMSCGAp+pFEknp4+PMSx8Bl82DQVngk+PpkoLgYypr8V/SzQ2bSxLgY+PDS7/S4+PpSTn/QyzrFIn/QQ4FRr/\
gYOzBYknD4z2LMx87k82Dkxnpz0PLRLJBlypMbh/Mz+PSkTzfk8prbh/nk3+rRLz/byyfli/dkVypkgagSwySki/\
0Qb+pSCcfTw2fTCnfknybSx87k8yf4EnnMByrRrnfYOpFki/gk8PDExp/+yzB4C//QzPbSLp/QypMDMnDzByDETnfS\
+2fY3/nkb+LR/a0DjNsQhwsHCHDDAwoQH8B4AyfRI8FS98g+Dpd4daLP3JFSb/BMsn0pSPM87nrldzSzQ2bPAGdb7z\
gQB8nph8emSy9E0cgk+zSS1qgzianYt8p+1/LzN4gzaa/+NqMS6qS4HLozoqfQnPbZEp98QyaRSp9P98pSl4oSzcg\
mca/P78nTTL0bz/sVManD9q9z1J7+xJMcM2gbFnobl4MSUcdb6agW3tF4ryaRApdz3agWIq7YM47HFqgzkanTU4FSk\
N7+3G9PAaL+P8DDA/9LI4gzVP0mrnd+P+nprLFkSyS87PrSk8nphpd4PtMmFJ7Ql4BYcpFTS2bDhJFSeL0bQzgQ/8M8\
7cD4l4bQQ2rL68LzD8p8M49kQcAmAPgbFJDS3qrTQyrzA8nLAqMSDLe80p/pAngbF2fbr8Bpf2drl2fc68p4gzjTQ2o8S\
LM8FNFSba9pDLocEqdkMpLR6pD4Q4f4SygbF4aR889phydbTanTP4FSkzbmoGnMxag8iJaTQweYQygkMcS87JrS9zFGF8g8\
SzbP78/bM4r+QcA4AzBPROaHVHdWEH0iTP0q9+AqIweZINsQhP/Zjw08R",
    "x-t": "1687941558085",
}


class WXScraper:
    def __init__(self):
        pass

    def extract_post_content(self, url):
        resp = requests.get(url, headers=headers, cookies=cookies)
        if resp.status_code != 200:
            raise ValueError(f"HTTP response failed with status code {resp.status_code}")
        
        soup = BeautifulSoup(resp.content, 'lxml')
        title = soup.find('meta', attrs={'property': 'og:title'})['content']
        author = soup.find('meta', attrs={'property': 'og:article:author'})['content']
        if author == "":
            author = None
        profile = soup.find('strong', attrs={'class': 'profile_nickname'}).text
        
        js_content = soup.find('div', attrs={'id': 'js_content'})
        all_contents = []
        for child in js_content.descendants:
            if type(child) == bs4.element.NavigableString:
                all_contents.append(child.get_text())
        
        joined_content = "\n".join(all_contents)

        ori_url = url
        
        scripts = soup.find(partial(text_contains, substr="window.cgiData", tag_name="script")).text
        city_str = re.findall(r"provinceName: '(.*?)'", scripts)
        if city_str:
            city = city_str[0]
        else:
            city = None
            
        scripts2 = soup.find(partial(text_contains, substr="function __setPubTime", tag_name="script")).text
        time_str = re.findall(r"createTime = '(.*?)'", scripts2)
        if time_str:
            time = time_str[0]
        else:
            time = None
        
        
        return {
            "source_platform": "wx",
            "url": ori_url,
            "title": title,
            "content": joined_content,
            "author": {
                "user": author, #作者昵称
                "profile": profile, #公众号名字
                "city": city
            },
            "time": time
        }


if __name__ == '__main__':
    url = "https://mp.weixin.qq.com/s/lk7R1Xg63P5SQgVgiKsKPw"
    
    pprint(WXScraper().extract_post_content(url))
