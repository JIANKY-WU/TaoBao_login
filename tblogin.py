import requests
import time
from lxml.html import etree
import re
import pymysql
import json
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor
import random
from save_to_database import Save_to_Mysql
from Proxies import RandomProxies
class TBlogin():
    def __init__(self,username,ua,password):
        self.need_check_url='https://login.taobao.com/member/request_nick_check.do?_input_charset=utf-8'
        self.verify_url='https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F'
        self.st_url='https://login.taobao.com/member/vst.htm?st={}'
        self.username=username
        self.ua=ua
        self.save_to_mysql=Save_to_Mysql()
        self.password=password
        self.timeout=3
        self.item={}
        #use IP proxies
        self.proxies=RandomProxies().get_proxies()
        print(self.proxies)
        self.session=requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            'accept-language': 'zh - CN, zh;q = 0.9'
        }
        self.random_headers=["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        ]
        self.headers = {
            'User-Agent': random.choice(self.random_headers)
        }
        
    def verify_password(self):
        headers={
            #'referer':'https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.5af911d9YccLiv&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            #'cache-control':'max-age=0',
            #'upgrade-insecure-requests':'1',
            #'content-type':'content-type',

        }
        #get from_data on you brower
        from_data={
            'TPL_username': self.username,
            'ncoToken': '1d6a86b5fa3ef3a5e90d96aad8bc49ed6803a5a6',
            'slideCodeShow':'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': 0,
            'newlogin': 0,
            'TPL_redirect_url': 'https://www.taobao.com/',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'loginType': '3',
            'gvfdcname': '10',
            'gvfdcre':'68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D613231626F2E323031372E3735343839343433372E372E3561663931316439674D7443765826663D746F70266F75743D7472756526726564697265637455524C3D68747470732533412532462532467777772E74616F62616F2E636F6D253246',
            'TPL_password_2': self.password,
            'loginASR': 1,
            'loginASRSuc': 1,
            'oslanguage': 'zh-CN',
            'sr':'1920 * 1080',
            'osVer': 'windows | 6.1',
            'naviVer': 'chrome | 79.0394579',
            'osACN': 'Mozilla',
            'osAV': '5.0(Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            'osPF': 'Win32',
            'appkey': '00000000',
            'mobileLoginLink': 'https: // login.taobao.com / member / login.jhtml?spm = a21bo.2017.754894437.1.5af911d9YccLiv & f = top & redirectURL = https: // www.taobao.com / & useMobile = true',

            'um_token': 'TA6A5082D8AE490593D42AF5CC8AAF757C0AD55081C8F24A2757367414B',
            'ua':self.ua,
            }
        try:
            response=self.session.post(self.verify_url,data=from_data,headers=headers,timeout=self.timeout)
            #print(response.text)
            #pattern=re.compile('<script\ssrc="(.*?)"></script>',re.S)
            #st_link_url=re.findall(pattern,response.text)[-1]
            st_link_url=re.search(r'<script src="(.*?)"></script',response.text).group(1)
            self.st_link_url=st_link_url

        except Exception as e:
            print('error ....',e)
    def get_st(self,st_link_url):

        try:
            response=self.session.get(st_link_url,headers=self.headers)
            response.raise_for_status()
            #print(response.text)
            pattern=re.compile('callback\({"code":200.*?st":"(.*?)"}',re.S)
            result=re.findall(pattern,response.text)
            print(result)
            return result[0]
        except Exception as e:
            print('error ........',e)
    def need_check(self):
        data={
            'username':self.username,
            'ua' : '122#GqmjFJXaEEx7sEpZMEpJEJponDJE7SNEEP7rEJ+/5QK+qoQLpo7iEDpWnDEeK51HpyGZp9hBuDEEJFOPpC76EJponDJL7gNpEPXZpJRgu4Ep+FQLpoGUEJLWn4yP7SQEEyuLpERDVhGgprZCnaRx9kb/on+TkEGhFd2qXhJJQUNgwflOrduJ0gtMqIz41QFvUCPq5F+4/89pC1qedtE6FaRfJ7vCfuwROyIY3vKiyxC1nDpFiIzs5Zjj4AVl2PIEwcp72Z5cDEP3DSp1uOLtt8/78Io2JzEEyBSUMUCtDWkZngplul5EELXrGCpibSx5Go3mqWfWEJpanS+ituaHDtVZ85G6JDEERFtDqMfbDEpxnSp1uOIEEL7Z8CLUJ4bEyF3mqW32D5pangL4ul0EDLIL8oL6xN8EyB3mqMV5x4bWyqm0T6WPpGJPnf3NcSSywoNTLPterXn+8aT7GRqDH5yYdWHM65WInRVDzoUUEKlw5kU/r5fKL8WnxvDcRS2DoDAfC6ubor3CZ4ni4w5xCojpREPoMP685tgEBYTXhDkfL9ljl2jjUXtpOMxCELWqL/KtdeQhT4XB3ltxI7evJVXEGZ70UyRIqnL9J0cQWBY8kfm+NHIkM3j6bHacoCet3GcwCKQC9MGtlPKmf+MK1cH+TaTah74eWC8gIDwzGBV06EQSB2ybq+ZiYTx333Vr2+HrJaRPRbHm0d8ZbNUEx/yx88Nitjlvyc+S1OMOiMfohKJNF+Apjsy66b7XdXDRDIUNFPRwhVm9m13lPJy+BBkdCv3FwVuiqxi5zgPvj9hEu29myrxP2bpJo2f6HjfFBICJNDRNQ5nM1MGLLV82EbQlfhiFvl0s2r9f/bwSxYdpwtbne4BZP/fprFmUobZVDdhPkJ9x081GFBEd5Nb9New3ivFXRzEu1e+c0I7YHYPopXchCdoqEffaL2UwMwYKH1NKxSn2xjNV/f9JeVINuEtKu1bSyLqkIYt+3l58oLIfpoSMwLfl2QILWRFvMR1zzH95MwH+HSlD+ZJFmWAiw1QR/jdxI4P59VGO2dq8eaGWfA4ploRPcv/T+XwJj4TA06Ur7k4SDkF47rZT/wRRMe5gSXzlnH05WUsatL3cDeRn0pe1yJGpUpT2QZ9ZC4==',

        }
        res=self.session.post(self.need_check_url,data=data)
        ncode=res.json()['needcode']
        print(ncode)
    def login(self):
        self.need_check()
        st=self.get_st(self.st_link_url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            'Host':'login.taobao.com',
            'Connection':'Keep-Alive'
        }
        try:
            resp=self.session.get(self.st_url.format(st),headers=headers)
            resp.raise_for_status()
            #print(resp.text)
            pattern = re.compile('href.*?"(.*?)"',re.S)
            url=re.findall(pattern,resp.text)
            return url[0]

        except Exception as e:
            print('erro.......',e)
    def get_name(self,url):

            response=self.session.get(url,headers=self.headers)
            html=etree.HTML(response.text)
            name=html.xpath('//div[@class="s-name"]/a/em/text()')
            print(name)
            cookies=requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)

    def get_goods(self):
        url='https://s.taobao.com/search?'
        data={
            'q': 'sony',
            'commend': 'all',
            'ssid': 's5 - e',
            'search_type': 'item',
            'sourceId': 'tb.index',
            'spm': 'a21bo.2017.201856 - taobao - item.1',
            'ie': 'utf8',
            'initiative_id': 'tbindexz_20170306',
        }

        url=url+urlencode(data)
        goods_response=self.session.get(url,headers=self.headers)
        return goods_response.text

    def parse_goods(self,goods_response):
        pattern=re.compile('g_page_config\s=\s(.*?);',re.S)
        result=re.findall(pattern,goods_response)[0]
        ti_pattern=re.compile(r'"raw_title":"(.*?)","pic_url.*?","detail_url":"(.*?)","view_price":"(.*?)",.*?"item_loc"(.*?)","view_sales":"(.*?)","comment_count":"(.*?)","user',re.S)
        detail=re.findall(r'"raw_title":"(.*?)","pic_url.*?","detail_url":"(.*?)","view_price":"(.*?)",.*?"item_loc"(.*?)","view_sales":"(.*?)","comment_count":"(.*?)","user',result)
        url_pattern=re.compile(r'"detail_url":"(.*?)",',re.S)
        urlt=re.findall(url_pattern,goods_response)

        print(result)
        urls = []
        for i in detail:
            g_detail = list(i)
            j_url = g_detail[1].replace(r'\\', '\\')
            j1=j_url.replace(r'\u003d','=')
            j2=j1.replace(r'\u0026','&')
            urls.append(j2)
        time.sleep(1)
        return urls
    def parse_detail_goods(self,url):
        item=self.item
        response = self.session.get(url,headers=self.headers)
        #response=self.session.get(url,proxies=self.proxies,headers=self.headers)# Use Proxy

        html=etree.HTML(response.text)
        item['title']=html.xpath('//*[@id="J_Title"]/h3/text()')[0].strip()
        item['price']=html.xpath('//*[@id="J_StrPrice"]/em[2]/text()')
        item['img_url']=html.xpath('//img[@id="J_ImgBooth"]/@src')
        print(item['title'])
        print(item['price'])
        print(item['img_url'])
        #print(response.text)
        self.save_to_mysql.save(item) # Save to MySQL

if __name__=='__main__':
    pool=ThreadPoolExecutor(10)
    #only you phone number
    username='****'
    #Use the encoded password and ua from browser
    password='*****'
    ua='****'
    loginer=TBlogin(username,ua,password)
    st_link_url=loginer.verify_password()
    url=loginer.login()
    loginer.get_name(url)
    goods_response=loginer.get_goods()
    detail=loginer.parse_goods(goods_response)
     #  test one of urls :

    detail_url = 'https:'+detail[3]
    print(detail_url)
    loginer.parse_detail_goods(detail_url)
    '''
    for url in detail[1:]:
        url='https:'+url
        try:
            th=pool.submit(loginer.parse_detail_goods,(url,))
            res=th.result()
            print(res)
            loginer.parse_detail_goods(url)
        except Exception as e:
            print(e)
    '''



