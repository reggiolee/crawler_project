import logging
import os
import json

import requests
from bs4 import BeautifulSoup

multiprocess = True
url_list = []
detail_list = []
headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://m.51job.com/search/joblist.php?indtype=32&from=home_keyword&funtype=2539',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }

def detail_page(url):
    global headers,detail_list
    req = requests.get(url,headers=headers)
    if req.status_code==200:
        html = BeautifulSoup(req.content, from_encoding="gb18030")
        if html.find('div',attrs={'class':'jt'}):
            job_name = html.find('div',attrs={'class':'jt'}).find('p').text.strip() if html.find('div',attrs={'class':'jt'}).find('p') else ''
            publish_time = html.find('div',attrs={'class':'jt'}).find('span').text.strip() if html.find('div',attrs={'class':'jt'}).find('span') else ''
            job_area = html.find('div',attrs={'class':'jt'}).find('em').text.strip() if html.find('div',attrs={'class':'jt'}).find('em') else ''
        else:
            job_name = publish_time=job_area= ''
        job_price = html.find('p',attrs={'class':'jp'}).text.strip() if html.find('p',attrs={'class':'jp'}) else ''
        if html.find('div',attrs={'class':'jd'}):
            hire_num = html.find('div',attrs={'class':'jd'}).find('span','s_r').text.strip() if html.find('div',attrs={'class':'jd'}).find('span','s_r') else ''
            workExp_req = html.find('div',attrs={'class':'jd'}).find('span','s_n').text.strip() if html.find('div',attrs={'class':'jd'}).find('span','s_n') else ''
            edu_req = html.find('div',attrs={'class':'jd'}).find('span','s_x').text.strip() if html.find('div',attrs={'class':'jd'}).find('span','s_x') else ''
        else:
            hire_num=workExp_req=edu_req= ''
        if html.find('div',attrs={'class':'rec'}):
            company_name = html.find('div',attrs={'class':'rec'}).find('p').text.strip() if html.find('div',attrs={'class':'rec'}).find('p') else ''
            company_type = html.find('div',attrs={'class':'rec'}).find('div',attrs={'class':'at'}).text.strip() if html.find('div',attrs={'class':'rec'}).find('div',attrs={'class':'at'}) else ''
            detail_area = html.find('div',attrs={'class':'rec'}).find('span').text.strip() if html.find('div',attrs={'class':'rec'}).find('span') else ''
        else:
            company_name=company_type=detail_area=''
        job_desc = html.find('div',attrs={'class':'ain'}).text.strip().replace('\n','').replace('\r','') if html.find('div',attrs={'class':'ain'}) else ''
        job_welfare = html.find('div',attrs={'class':'welfare'}).text.strip() if html.find('div',attrs={'class':'welfare'}) else ''
        return {'url':url,
                'jobName':job_name,
                'publishTime':publish_time,
                'jobArea':job_area,
                'jobPrice':job_price,
                'hireNum':hire_num,
                'workExp':workExp_req,
                'eduReq':edu_req,
                'companyName':company_name,
                'companyType':company_type,
                'detailArea':detail_area,
                'jobDesc':job_desc,
                'jobWelfare':job_welfare
                }


def main():
    page =1
    global headers,url_list,detail_list
    while True:
        url = 'http://m.51job.com/search/joblist.php?jobarea=030200&funtype=2539&indtype=32&from=home_keyword&pageno='+str(page)
        req = requests.get(url,headers=headers)
        if req.status_code==200:
            html = BeautifulSoup(req.content)
            job_list = html.find('div',attrs={'class':'items'}).find_all('a')
            for job in job_list:
                url_list.append(job['href'])
        if html.find('a',attrs={'next'})['href'] =='javascript:void(0);':
            break
        else:
            page+=1
    f = open('data/url_list.json', 'w')
    f.write(json.dumps(url_list))
    f.close()
    for url in url_list:
        detail_data = detail_page(url)
        if detail_data:
            detail_list.append(detail_data)
    f = open('data/detail_list.json', 'w', encoding='utf-8')
    f.write(json.dumps(detail_list,ensure_ascii=False,indent=2))
    f.close()

if __name__=='__main__':
    if not os.path.exists('data'):
        os.mkdir('data')
    main()
