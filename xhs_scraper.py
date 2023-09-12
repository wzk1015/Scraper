import requests
import re
from bs4 import BeautifulSoup
from functools import partial
import json
from pprint import pprint
from utils import text_contains, class_starts_with, class_contains

# https://michael-shub.github.io/curl2scrapy/
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





class XHSScraper:
    def __init__(self):
        pass

    def extract_post_content(self, url):
        resp = requests.get(url, headers=headers, cookies=cookies)
        if resp.status_code != 200:
            raise ValueError(f"HTTP response failed with status code {resp.status_code}")

        soup = BeautifulSoup(resp.content, 'lxml')
        title = soup.find('meta', attrs={'name': 'og:title'})['content']
        
        meta_content = soup.find('meta', attrs={'name': 'description'}).get('content')

        ori_url = soup.find('meta', attrs={'name': 'og:url'})['content']


        
        scripts = soup.find(partial(text_contains, substr="imageList", tag_name="script")).text
        
        imgs = re.findall(r'"imageList":\[(.*)\]', scripts)
        imgs = imgs[0] if imgs else ''
        imgs = imgs.encode("UTF-8").decode("unicode_escape")
        imgs = re.findall(r'"(https://.*?)"', imgs) + re.findall(r'"(http://.*?)"', imgs)
        imgs = [i + '?imageView2/format/jpg|imageMogr2/strip' for i in imgs if 'avatar' not in i]
        
        tags_str = soup.find_all(partial(class_contains, substr="tag"))
        if tags_str:
            tags = [t.text for t in tags_str]
        else:
            tags = None
        
        regs = [
            r'"user":(\{"avatar":(.*?)\})',
            r'"user":(\{"nickname":(.*?)\})',
            r'"user":(\{"userId":(.*?)\})'
        ]
        user = [item for reg in regs for item in re.findall(reg, scripts)]
        if user:
            user = json.loads(user[0][0])
            nickname = user["nickname"]
            avatar = user["avatar"]
            userId = user["userId"]
        else:
            nickname = None
            avatar = None
            userId = None
        
        interact = re.findall(r'interactInfo":(\{(.*?)\})', scripts)
        
        if interact:
            interact = json.loads(interact[0][0])
            collectedCount = interact['collectedCount']
            commentCount = interact['commentCount']
            shareCount = interact['shareCount']
            likedCount = interact['likedCount']
        else:
            collectedCount = None
            commentCount = None
            shareCount = None
            likedCount = None
        

        date_str = soup.find(attrs={'class': 'date'}).text.split()
        date = date_str[0]
        if len(date_str) > 1:
            city = date_str[1]
        else:
            city = None
        
        resp2 = requests.get(url, headers=headers_ios, cookies=cookies)
        if resp2.status_code != 200:
            raise ValueError(f"HTTP response IOS failed with status code {resp2.status_code}")
        soup2 = BeautifulSoup(resp2.content, 'lxml')
        
        keywords_tags = soup2.find('meta', attrs={'name': 'keywords'})
        if keywords_tags:
            keywords = keywords_tags['content'].split(",")
        else:
            keywords = None
        
        pois_str = soup2.find_all(partial(class_contains, substr="note-poi"))
        if pois_str:
            poi = pois_str[0].text.strip()
        else:
            poi = None
        
        scripts2 = soup2.find(partial(text_contains, substr="commentData", tag_name="script")).text

        raw_comments = re.findall(r'commentData":(\{(.*?)\}),"userOtherNotesData"', scripts2)
        if raw_comments:
            raw_comments = json.loads(raw_comments[0][0])
            # TODO: subcomments?
            comments = [
                {
                    "content": com["content"],
                    "user": com["user"]["nickname"],
                    "is_from_author": com["user"]["userId"] == userId
                }
                for com in raw_comments["comments"]
            ]
        else:
            comments = None

        return {
            "source_platform": "xhs",
            "url": ori_url,
            "title": title,
            "content": meta_content,
            "img_urls": imgs,
            "author": {
                "nickname": nickname,
                "avatar": avatar,
                "userId": userId,
                "city": city
            },
            'liked_count': likedCount,
            'collected_count': collectedCount,
            'comment_count': commentCount,
            'share_count': shareCount,
            "comments" : comments,
            "time": date,
            "tags": tags,
            "keywords": keywords,
            "location": poi
        }


if __name__ == '__main__':
    url = "http://xhslink.com/MpXmXt"
    # url = "https://www.xiaohongshu.com/explore/64fac943000000001f03bb4f"
    pprint(XHSScraper().extract_post_content(url))
