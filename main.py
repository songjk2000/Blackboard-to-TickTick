import tt
import bb
import time

# tt refers to TickTick
# bb refers to Blackboard

tt_username = ''
tt_password = ''
bb_username = ''
bb_password = ''

while True:
    inboxid = tt.login(tt_username, tt_password)
    bb_login = bb.login(bb_username, bb_password)
    if inboxid is not False and bb_login:
        bb_task_list = bb.refresh_task()
        tt_task_list = tt.get_all_task_list(inboxid)
        for every_bb_task in bb_task_list:
            exist = False
            for every_tt_task in tt_task_list:
                if 'content' in every_tt_task:
                    if every_tt_task['title'] == every_bb_task['task_subject'] or every_tt_task['content'] == \
                            every_bb_task['task_content']:
                        exist = True
            if exist:
                print(every_bb_task['task_subject'] + '--' + every_bb_task['task_content'] + '作业【已经存在】')
            else:
                if tt.add_task(inboxid, every_bb_task['task_subject'] + '作业', every_bb_task['task_content'],
                               every_bb_task['task_date']):
                    print(every_bb_task['task_subject'] + '--' + every_bb_task['task_content'] + '作业【添加成功】')
                else:
                    print(every_bb_task['task_subject'] + '--' + every_bb_task['task_content'] + '作业【添加失败】')
        print('----------更新作业完成----------')
        time.sleep(600)
    else:
        if not inboxid:
            print('TickTick 登陆失败')
        if not bb_login:
            print('Blackboard 登陆失败')
        break
