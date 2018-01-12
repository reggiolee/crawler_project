import sqlite3
import requests


word = input('请输入职位关键字：')
db = sqlite3.connect('大街网' + word + ".db")
cursor = db.cursor()
try:
    cursor.execute("""CREATE TABLE `data`  (
        `id` INTEGER PRIMARY KEY autoincrement,
        `comphref` varchar(255) NULL DEFAULT NULL,
        `compname` varchar(255) NULL DEFAULT NULL,
        `corpid` int(11) NULL DEFAULT NULL,
        `hascomment` int(11) NULL DEFAULT NULL,
        `industry` varchar(255) NULL DEFAULT NULL,
        `jobhref` varchar(255) NULL DEFAULT NULL,
        `jobname` varchar(255) NULL DEFAULT NULL,
        `jobseq` int(11) NULL DEFAULT NULL,
        `pubcity` varchar(10) NULL DEFAULT NULL,
        `pubcomp` varchar(25) NULL DEFAULT NULL,
        `pubedu` varchar(10) NULL DEFAULT NULL,
        `pubex` varchar(10) NULL DEFAULT NULL,
        `salary` varchar(25) NULL DEFAULT NULL,
        `scalename` varchar(25) NULL DEFAULT NULL,
        `datetime` varchar(50) NULL DEFAULT NULL
        )""")
except:
    pass

s = requests.Session()
s.get('https://so.dajie.com/job/search')
headers = {
    'Referer': 'https://so.dajie.com/job/search',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/63.0.3239.108 Safari/537.36'
}
url = 'https://so.dajie.com/job/ajax/search/filter?keyword=%s&page=1' % word
rsp = s.get(url, headers=headers).json()
"""
rsp: {
    'result': 0,
    'data': {
        'total': '827',
        'city': {},
        'totalPage': 28,
        'list': [{})
    }
}
"""
data = rsp['data']
pages = data['totalPage']
for page in range(0, pages):
    if page == 0:
        pass
    else:
        url = 'https://so.dajie.com/job/ajax/search/filter?keyword=%s&page=' % word
        url += str(page + 1)
        rsp = s.get(url, headers=headers).json()
        data = rsp['data']
    items = data['list']
    for item in items:
        sql = '''INSERT INTO data(comphref, compname, corpid, hascomment, industry, jobhref, 
            jobname, jobseq, pubcity, pubcomp, pubedu, pubex, salary, scalename, datetime) 
            VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")''' % (
            item.get('compHref'), item.get('compName'), item.get(
                'corpId'), item.get('hasComment'), item.get('industryName'),
            item.get('jobHref'), item.get('jobName'), item.get(
                'jobseq'), item.get('pubCity'), item.get('pubComp'),
            item.get('pubEdu'), item.get('pubEx'), item.get('salary'), item.get(
                'scaleName'), '2018-01-08 ' + item.get('time')
        )
        cursor.execute(sql)
    db.commit()
