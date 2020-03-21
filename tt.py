import json
import requests

s = requests.session()


header = {
    'content-type': 'application/json',
    'origin': 'https://www.dida365.com',
    'referer': 'https://www.dida365.com/signin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}


def login(username, password):
    login_url = 'https://api.dida365.com/api/v2/user/signon?wc=true&remember=true'
    login_data = {
        'username': username,
        'password': password
    }
    s.post(login_url, data=json.dumps(login_data), headers=header)
    user_status_utl = 'https://api.dida365.com/api/v2/user/status'
    user_status = s.get(user_status_utl).text
    if user_status[2:8:] == "userId":
        return json.loads(user_status)['inboxId']
    else:
        return False


def get_todo_task_list(inboxid):
    todo_task_list_url = 'https://api.dida365.com/api/v2/batch/check/0'
    todo_task_list = json.loads(s.get(todo_task_list_url).text)['syncTaskBean']['update']
    return todo_task_list


def get_done_task_list(inboxid):
    done_task_list_url = 'https://api.dida365.com/api/v2/project/' + inboxid + '/completed/?from=&to=&limit='
    done_task_list = json.loads(s.get(done_task_list_url).text)
    return done_task_list


def get_all_task_list(inboxid):
    all_task_list = get_todo_task_list(inboxid) + get_done_task_list(inboxid)
    return all_task_list


def delete_task(inbox_id, task_id):
    delete_task_url = 'https://api.dida365.com/api/v2/batch/task'
    delete_data = {
        "add": [],
        "update": [],
        "delete": [{
            "taskId": task_id,
            "projectId": inbox_id
        }]
    }
    if s.post(delete_task_url, data = json.dumps(delete_data), headers = header).text == '{"id2etag":{},"id2error":{}}':
        return True


def add_task(inboxid, title, content, date):
    task_data = {
        'add':
            [{
                'items': [],
                'reminders': [{'id': '', 'trigger': 'TRIGGER:PT0S'}],
                'exDate': [],
                'dueDate': 'null',
                'priority': 0,
                'progress': 0,
                'assignee': 'null',
                'sortOrder': 1,
                'startDate': date,
                'isFloating': 'false',
                'status': 0,
                'projectId': inboxid,
                'modifiedTime': '',
                'title': title,
                'tags': [],
                'timeZone': 'Asia/Beijing',
                'content': content,
                'id': ''
            }],
        'update': [],
        'delete': []
    }
    if str(s.post('https://api.dida365.com/api/v2/batch/task', data=json.dumps(task_data), headers=header)) == '<Response [200]>':
        return True