import requests
import json

s = requests.session()


def login(username,password):
    login_url = 'https://shisu.blackboardchina.cn/webapps/login/'
    header = {
        'Host': 'shisu.blackboardchina.cn',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Cookie': ''
    }
    data = {
        'user_id': username,
        'password': password,
        'login': '登录',
        'action': 'login',
        'new_loc': '/webapps/portal/execute/defaultTab'
    }
    s.post(login_url, data = data, headers = header)
    if '欢迎' in s.get('https://shisu.blackboardchina.cn').text[:100]:
        return True


def refresh_task():
    # 日历视图链接
    calendar_url = 'https://shisu.blackboardchina.cn/webapps/calendar/calendarData/selectedCalendarEvents?start=&end=&course_id=&mode=personal'
    task_list = []
    for every_task in json.loads(s.get(calendar_url).text):
        task_list.append({'task_subject': every_task['calendarName'], 'task_content': every_task['title'],'task_date': every_task['endDate'][:-1] + '+0000'})
    return task_list
