import json
import logging
import os
import requests

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='zhuanlan.log',
                filemode='w')

def main(keyword,count=0,time=1,step=10):
    url = "https://www.zhihu.com/api/v4/search_v3"
    querystring = {"t": "column", "q": keyword, "correction": "1",
                   "search_hash_id": "392f7cdc8a9b2bc4641542fbdacdfeae",
                   "offset": str(count), "limit": str(step)}
    headers = {
        'cache-control': "no-cache",
        'authorization': "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        'cookie': "aliyungf_tc=AQAAAGr5bRtPNgUAVLKc0+DbDXmRlMsh; d_c0=\"APCiDi7r-AyPTtdbkMMQSFSL0870XD_XZQI=|1515643079\"; _xsrf=abff6595-d20f-4719-ac2c-b90dc630227c; l_n_c=1; q_c1=159dbe0fb70c4fb1b8db7e6223c20f5b|1515643079000|1515643079000; r_cap_id=\"N2RjNmZlYTEwYmI2NDg1Njk4YWM3N2JkYzA5NjIyMzg=|1515643079|062b4cea8ebe9820f2bce154f42059cf31872f30\"; cap_id=\"NjJjNzQ3ZWJkNjVjNDMyNzliMzA2MjVlOTI4NGQwMzQ=|1515643079|c83a7b6fe1abcb7d800cd56a33bb44b36387c6e3\"; l_cap_id=\"NWE1ZTlmZjU4ZjkzNDMzNWIxZjM4ODhiZDVkN2E0MzY=|1515643079|098aad15d35f9241db0cf49e2127fb25af2c4563\"; n_c=1; _zap=096857c0-a0b7-4ccb-b04b-f3af00f70fc7"
    }
    req = requests.request("GET", url, headers=headers, params=querystring)
    if req.status_code==200:
        f = open('data/'+keyword+'_'+str(time)+'.json','w')
        f.write(json.dumps(json.loads(req.content),ensure_ascii=False,indent=2))
        f.close()
        data = json.loads(req.content)
        count+=len(data['data'])
        if not data['paging']['is_end']:
            main(keyword,count,time+1)
    else:
        logging.error('request status error,status code:'+str(
            req.status_code)+'\nrespones:'+str(req.content))
if __name__=='__main__':
    if not os.path.exists('data'):
        os.mkdir('data')
    main(keyword='nlp')
