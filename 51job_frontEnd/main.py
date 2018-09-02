import logging
import os
import json
import sys
import urllib
import getopt

import requests
from bs4 import BeautifulSoup


if not os.path.exists('data'):
    os.mkdir('data')
if not os.path.exists('logs'):
    os.mkdir('logs')


logging.basicConfig(level=logging.DEBUG,
                    filename='./logs/51job.log',
                    filemode='a',
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

area_num_dict = {
    "全国": "000000",
    "北京": "010000",
    "上海": "020000",
    "广州": "030200",
    "深圳": "040000",
    "武汉": "180200",
    "成都": "090200",
    "南京": "070200",
    "天津": "050000",
    "重庆": "060000",
    "西安": "200200",
    "杭州": "080200"
}

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


def usage():
    """
Usage: main.py [-a|--area,-k|--key,-h|--help]

Description
    -a,--area The area need to be search in 51job web. eg '北京'、'广州'
    -k,--key Search Keyword. eg '前端'、'后端'
    -h,--help Display help infomation

for example:
    python main.py -a 广州 -k 前端
    """


def argConvert():
    try:
        options, args = getopt.getopt(sys.argv[1:], 'a:k:h', [
                                      'area=', 'key=', 'help'])
    except getopt.GetoptError as err:
        print(usage.__doc__)
        sys.exit(1)
    area = None
    key = None
    for name, value in options:
        if name in ('-a', '--area'):
            area = value
        elif name in ('-k', '--key'):
            key = value
        elif name in ('-h', '--help'):
            print(usage.__doc__)
            sys.exit(1)
    if area not in area_num_dict.keys():
        print("暂不支持该区域，支持区域：")
    else:
        area = area_num_dict.get(area)
    if area and key:
        return area, key
    else:
        print(usage.__doc__)
        sys.exit(1)


def detail_page(url):
    global headers, detail_list
    logging.debug('begin scrawl url:'+url)
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        logging.debug('scrawl success')
        html = BeautifulSoup(req.content, from_encoding="gb18030")
        if html.find('div', attrs={'class': 'jt'}):
            job_name = html.find('div', attrs={'class': 'jt'}).find(
                'p').text.strip() if html.find('div', attrs={'class': 'jt'}).find('p') else ''
            publish_time = html.find('div', attrs={'class': 'jt'}).find('span').text.strip(
            ) if html.find('div', attrs={'class': 'jt'}).find('span') else ''
            job_area = html.find('div', attrs={'class': 'jt'}).find('em').text.strip(
            ) if html.find('div', attrs={'class': 'jt'}).find('em') else ''
        else:
            job_name = publish_time = job_area = ''
        job_price = html.find('p', attrs={'class': 'jp'}).text.strip(
        ) if html.find('p', attrs={'class': 'jp'}) else ''
        if html.find('div', attrs={'class': 'jd'}):
            hire_num = html.find('div', attrs={'class': 'jd'}).find('span', 's_r').text.strip(
            ) if html.find('div', attrs={'class': 'jd'}).find('span', 's_r') else ''
            workExp_req = html.find('div', attrs={'class': 'jd'}).find('span', 's_n').text.strip(
            ) if html.find('div', attrs={'class': 'jd'}).find('span', 's_n') else ''
            edu_req = html.find('div', attrs={'class': 'jd'}).find('span', 's_x').text.strip(
            ) if html.find('div', attrs={'class': 'jd'}).find('span', 's_x') else ''
        else:
            hire_num = workExp_req = edu_req = ''
        if html.find('div', attrs={'class': 'rec'}):
            company_name = html.find('div', attrs={'class': 'rec'}).find(
                'p').text.strip() if html.find('div', attrs={'class': 'rec'}).find('p') else ''
            company_type = html.find('div', attrs={'class': 'rec'}).find('div', attrs={'class': 'at'}).text.strip(
            ) if html.find('div', attrs={'class': 'rec'}).find('div', attrs={'class': 'at'}) else ''
            detail_area = html.find('div', attrs={'class': 'rec'}).find('span').text.strip(
            ) if html.find('div', attrs={'class': 'rec'}).find('span') else ''
        else:
            company_name = company_type = detail_area = ''
        job_desc = html.find('div', attrs={'class': 'ain'}).text.strip().replace(
            '\n', '').replace('\r', '') if html.find('div', attrs={'class': 'ain'}) else ''
        job_welfare = html.find('div', attrs={'class': 'welfare'}).text.strip(
        ) if html.find('div', attrs={'class': 'welfare'}) else ''
        return {'url': url,
                'jobName': job_name,
                'publishTime': publish_time,
                'jobArea': job_area,
                'jobPrice': job_price,
                'hireNum': hire_num,
                'workExp': workExp_req,
                'eduReq': edu_req,
                'companyName': company_name,
                'companyType': company_type,
                'detailArea': detail_area,
                'jobDesc': job_desc,
                'jobWelfare': job_welfare
                }
    else:
        logging.debug('scrawl failed')
        return None


def main():
    area, keyword = argConvert()
    page = 1
    global headers, url_list, detail_list
    while True:
        url = 'https://m.51job.com/search/joblist.php?jobarea='+area+'&keyword=' + \
            urllib.parse.quote(keyword)+'&keywordtype=2&pageno='+str(page)
        logging.debug('begin scrawl url:'+url)
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            logging.debug('scrawl success')
            html = BeautifulSoup(req.content)
            job_list = html.find('div', attrs={'class': 'items'}).find_all('a')
            for job in job_list:
                url_list.append(job['href'])
        if html.find('a', attrs={'next'})['href'] == 'javascript:void(0);':
            logging.debug('scrawl failed')
            break
        else:
            page += 1
            logging.debug('scrawl failed,next page')
    f = open('data/url_list.json', 'w')
    f.write(json.dumps(url_list))
    f.close()
    for url in url_list:
        detail_data = detail_page(url)
        if detail_data:
            detail_list.append(detail_data)
    f = open('data/detail_list.json', 'w', encoding='utf-8')
    f.write(json.dumps(detail_list, ensure_ascii=False, indent=2))
    f.close()


if __name__ == '__main__':
    main()
