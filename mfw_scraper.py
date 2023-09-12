import requests
import re
from bs4 import BeautifulSoup
import bs4
from functools import partial
from pprint import pprint
import http
from utils import text_contains, class_starts_with


def parse_cookie(cookie):
    """
    Return a dictionary parsed from a `Cookie:` header string.
    """
    cookiedict = {}
    for chunk in cookie.split(";"):
        if "=" in chunk:
            key, val = chunk.split("=", 1)
        else:
            # Assume an empty name per
            # https://bugzilla.mozilla.org/show_bug.cgi?id=169091
            key, val = "", chunk
        key, val = key.strip(), val.strip()
        if key or val:
            # unquote using Python's algorithm.
            cookiedict[key] = http.cookies._unquote(val)
    return cookiedict


def parse_header(header_str):
    headers_ = header_str.strip().split('\n')
    new_headers = {}
    for h in headers_:
        if(h[0:1] == ':'):
            single = h[1:].split(": ")
            # headers_ = f"'{single[0]}': '{single[1]}',"
            # print(headers_)
            new_headers[single[0]] = single[1]
        else:
            single = h.split(": ")
            if(len(single) != 1):
                new_headers[single[0]] = single[1]
                # headers_ = f"'{single[0]}': '{single[1]}',"
                # print(headers_)
    # in case receives status code of 304
    new_headers['Cache-Control'] = 'no-cache'
    return new_headers


def parse_header2(header_str):
    header_str = header_str.strip()
    lines = header_str.split("\n")
    new_headers = {}
    for idx in range(0, len(lines), 2):
        new_headers[lines[idx].strip(":")] = lines[idx+1]
    return new_headers
        


# copy from Chrome -> Dev mode -> Network -> Request headers -> raw
raw_header = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Connection: keep-alive
Cookie: isCookie=1; BAIDU_SSP_lcr=https://www.baidu.com/; wakeApp_unshow_baidu=1; mfw_uuid=64eb1da8-8521-9c4d-e53f-549f1707ae9d; __jsluid_s=ebde84ec1319f846cc278e03e1c61bb6; __omc_chl=; uva=s%3A78%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1693130156%3Bs%3A10%3A%22last_refer%22%3Bs%3A6%3A%22direct%22%3Bs%3A5%3A%22rhost%22%3Bs%3A0%3A%22%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1693130156%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22f_host%22%3Bs%3A1%3A%22m%22%3B%7D; __mfwuuid=64eb1da8-8521-9c4d-e53f-549f1707ae9d; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1693130110; __jsluid_h=d48cdf1cd37c526aff0e920e0d2792cd; _r=baidu; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A18%3A%22www.baidu.com%2Flink%22%3Bs%3A1%3A%22t%22%3Bi%3A1693152215%3B%7D; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222023-09-01+15%3A43%3A55%22%3B%7D; __mfwothchid=referrer%7Cgraph.qq.com; __mfwc=referrer%7Cgraph.qq.com; source=ug-seo-baidu; __mfwa=1693130109553.88261.9.1693985801160.1693994064165; __mfwlv=1693994077; __mfwvn=7; PHPSESSID=u26qglteee1rervdl3qjkdcio2; cc=UGD64EB13557721691693994720267; tt=https%3A%2F%2Fm.mafengwo.cn%2Fmweng%2Fwengdetailssr%2Fweng%3Fid%3D1773769193088741; current_url=https%3A%2F%2Fm.mafengwo.cn%2Fmweng%2Fwengdetailssr%2Fweng%3Fid%3D1773769193088741; source_data=%7B%22event_id%22%3A%22UGD64EB13557721691693994720267%22%2C%22uuid%22%3A%2264eb1da8-8521-9c4d-e53f-549f1707ae9d%22%2C%22share_uuid%22%3A%22%22%2C%22wake_way%22%3A%22deeplink%22%2C%22UA%22%3A%22chrome%22%2C%22platform%22%3A%22h5%22%7D; login=mafengwo; mafengwo=a5b3db0014be706dfd526b2caefa7c7d_48962020_64f84f82e0fad5.64753152_64f84f82e0fb18.72235284; mfw_uid=48962020; __omc_r=; isDownClick_adis_baidu=1; uol_throttle=48962020; __mfwb=911a41143380.36.direct; __mfwlt=1693996602; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1693996603
Host: m.mafengwo.cn
Referer: https://m.mafengwo.cn/
If-None-Match: "134d2-HHwHczscw3rZb4benfT8RU07r9Y"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"""


headers = parse_header(raw_header)

raw_headers_redirect = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Cookie: mfw_uuid=64eb1da8-8521-9c4d-e53f-549f1707ae9d; __jsluid_s=031ee6a4fa6fc894672202e65a675654; __omc_chl=; uva=s%3A78%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1693130156%3Bs%3A10%3A%22last_refer%22%3Bs%3A6%3A%22direct%22%3Bs%3A5%3A%22rhost%22%3Bs%3A0%3A%22%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1693130156%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22f_host%22%3Bs%3A1%3A%22m%22%3B%7D; __mfwuuid=64eb1da8-8521-9c4d-e53f-549f1707ae9d; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1693130110; __jsluid_h=20fcae4ddd766728c5073d0f7c2bf67f; _r=baidu; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A18%3A%22www.baidu.com%2Flink%22%3Bs%3A1%3A%22t%22%3Bi%3A1693152215%3B%7D; __mfwothchid=referrer%7Cgraph.qq.com; PHPSESSID=u26qglteee1rervdl3qjkdcio2; login=mafengwo; mafengwo=a5b3db0014be706dfd526b2caefa7c7d_48962020_64f84f82e0fad5.64753152_64f84f82e0fb18.72235284; mfw_uid=48962020; __omc_r=; __mfwc=direct; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A18%3A%22tongji.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222023-09-09+01%3A11%3A32%22%3B%7D; source=ug-direct; tt=https%3A%2F%2Fm.mafengwo.cn%2Fmweng%2Fwengdetailssr%2Fweng%3Fid%3D1761619730137275; current_url=https%3A%2F%2Fm.mafengwo.cn%2Fmweng%2Fwengdetailssr%2Fweng%3Fid%3D1761619730137275; bottom_ad_status=1; cc=UGD64EB13557721691694249515697; source_data=%7B%22event_id%22%3A%22UGD64EB13557721691694249515697%22%2C%22uuid%22%3A%2264eb1da8-8521-9c4d-e53f-549f1707ae9d%22%2C%22share_uuid%22%3A%22%22%2C%22wake_way%22%3A%22deeplink%22%2C%22UA%22%3A%22chrome%22%2C%22platform%22%3A%22h5%22%7D; __mfwa=1693130109553.88261.12.1694245328857.1694252701941; __mfwlv=1694252701; __mfwvn=10; uol_throttle=48962020; __mfwlt=1694254215; __mfwb=c34a29e01b15.4.direct; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1694254216
Host: www.mafengwo.cn
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"""

headers_redirect = parse_header(raw_headers_redirect)

raw_headers_redirect2 = """
:authority:
imfw.cn
:method:
GET
:path:
/l/309965902
:scheme:
https
Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding:
gzip, deflate, br
Accept-Language:
zh-CN,zh;q=0.9
Sec-Fetch-Dest:
document
Sec-Fetch-Mode:
navigate
Sec-Fetch-Site:
none
Sec-Fetch-User:
?1
Upgrade-Insecure-Requests:
1
User-Agent:
Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1
"""
headers_redirect2 = parse_header2(raw_headers_redirect2)

cookies = []


class MFWScraper:
    def __init__(self):
        pass
    
    def _extract_note(self, url):
        resp = requests.get(url, headers=headers, cookies=cookies)
            
        if resp.status_code not in [200]:
            raise ValueError(f"HTTP response failed with status code {resp.status_code}")
        
        soup = BeautifulSoup(resp.content, 'lxml')
        # x = soup.find_all('img')[0]["src"]
        title = soup.find_all(partial(class_starts_with, prefix="css_note_title"))[0].text
        pois = soup.find_all(partial(class_starts_with, prefix="poiAndRelated_poiText"))
        pois = [poi.text for poi in pois]
        
        avatar_url = soup.find(partial(class_starts_with, prefix="avatar_avatar"))["style"]
        avatar_url = re.findall(r"background-image:url\(((.*).jpeg)", avatar_url)
        if avatar_url:
            avatar = avatar_url[0][0]
        else:
            avatar = None
            
        city_str = soup.find_all(partial(class_starts_with, prefix="poiAndRelated_mdd_text"))
        if city_str:
            city = city_str[0].text
        else:
            city = None
        
        author = soup.find_all(partial(class_starts_with, prefix="topbar_textOverFlow"))[0].text
        
        
        text_list = soup.find_all(partial(class_starts_with, prefix="contentParser_note_content"))
        content = text_list[0].text

        interact = soup.find_all(partial(class_starts_with, prefix="bottomBtns_num"))
        likedCount = interact[0].text if interact[0].text != "" else "0"
        commentCount = interact[1].text if interact[1].text != "" else "0"
        collectedCount = interact[2].text if interact[2].text != "" else "0"
        
        
        imgs = [x["src"] for x in soup.find_all(alt="poster")]
        raw_comments = [x.text for x in text_list[1:]]
        comment_authors = soup.find_all(partial(class_starts_with, prefix="reply_textOverFlow"))
        comments = [
            {
                "content": com,
                "user": auth.text.strip("："),
                "is_from_author": auth.text == author
            }
            for com, auth in zip(raw_comments, comment_authors)
        ]
        
        date = soup.find_all(partial(class_starts_with, prefix="time_note_time"))[0].text
        date = date.split()[1]
        
        trip_info_tags = soup.find_all(partial(class_starts_with, prefix="structInfo_strcut_list"))

        if trip_info_tags:
            trip_info_list = []
            for child in trip_info_tags[0].children:
                for child_2 in child.children:
                    trip_info_list.append(child_2.text)
            trip_infos = {}
            for i in range(0, len(trip_info_list), 2):
                trip_infos[trip_info_list[i]] = trip_info_list[i+1] # 可能有“-”，“xxxxx...”
        else:
            trip_infos = None
    
        return {
            "source_platform": "mfw",
            "url": url,
            "title": title,
            "content": content,
            "img_urls": imgs,
            "pois": pois,
            "author": {
                "nickname": author,
                "avatar": avatar,
                "city": city
            },
            'liked_count': likedCount,
            'collected_count': collectedCount,
            'comment_count': commentCount,
            "comments": comments,
            "time": date,
            "trip_infos" : trip_infos
        }

    def extract_post_content(self, url):
        original_url = url
        if "imfw.cn" in url:
            # imfw.cn urls redirects to mafengwo.cn
            resp = requests.get(url, headers=headers_redirect2)
            url = resp.url
        
        if '/mweng/' in url:
            return self._extract_note(url)
        else:
            raise NotImplementedError(f"Unsupported MFW URL: {url}. ") # 仅支持马蜂窝笔记
    
    
    

if __name__ == '__main__':
    urls = [
        "https://imfw.cn/l/303836890", # 笔记 跳转至
        "https://m.mafengwo.cn/mweng/wengdetailssr/weng?id=1761619730137275"
    ]
    for url in urls:
        pprint(MFWScraper().extract_post_content(url))
