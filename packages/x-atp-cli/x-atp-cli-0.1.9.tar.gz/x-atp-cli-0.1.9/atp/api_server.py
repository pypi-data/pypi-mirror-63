import os
import uuid
import configparser
from pathlib import Path


def create_profile(tmp_dir, url):
    config = configparser.ConfigParser()
    file = 'config.ini'
    config.read(tmp_dir / file)
    config.add_section('ATP-Server')
    config.set('ATP-Server', 'platform_url', url)
    config.set('ATP-Server', 'platform_ip', '127.0.0.1')
    config.set('ATP-Server', 'case_git_url', 'http://192.168.5.29:8090/lincongzhi/atp_sweetest.git')
    config.set('ATP-Server', 'case_git_user', 'hekaiyou')
    config.set('ATP-Server', 'case_git_pass', 'm504@504m')
    with open(tmp_dir / file, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    with open(tmp_dir / 'run.py', 'w', encoding='utf-8') as file_obj:
        file_obj.write(run_file_code)


def api_server(url):
    cwd_dir = Path.cwd()
    uuid_str = uuid.uuid4().hex
    tmp_dir_name = cwd_dir / ('x_atp_api_server_%s' % uuid_str)
    os.mkdir(str(tmp_dir_name))
    create_profile(tmp_dir=tmp_dir_name, url=url)
    print('cd x_atp_api_server_%s\npython run.py' % uuid_str)


run_file_code = '''
import os
import time
import shutil
import xlrd
import configparser
import requests
import redis
from git import Repo
from x_sweetest import Autotest
config_file = 'config.ini'
config = configparser.RawConfigParser()
config.read(config_file, encoding='utf-8')
PLATFORM_URL = dict(config.items('ATP-Server'))['platform_url']
PLATFORM_IP = dict(config.items('ATP-Server'))['platform_ip']
CASE_GIT_URL = dict(config.items('ATP-Server'))['case_git_url']
CASE_GIT_USER = dict(config.items('ATP-Server'))['case_git_user']
CASE_GIT_PASS = dict(config.items('ATP-Server'))['case_git_pass']
CASE_GIT_PASS = CASE_GIT_PASS.replace('@', '%40')
url_index = CASE_GIT_URL.find('//') + 2
ATP_CASE_GIT = CASE_GIT_URL[:url_index] + CASE_GIT_USER + ':' + CASE_GIT_PASS + '@' + CASE_GIT_URL[url_index:]
POOL = redis.ConnectionPool(host=PLATFORM_IP, port=6379, db=0, decode_responses=True)
REDIS_POOL = redis.Redis(connection_pool=POOL)
def mkdir_and_del(srcpath):
    if os.path.isdir(srcpath):
        shutil.rmtree(srcpath)
    os.mkdir(srcpath)
def reset_file_tree(file_name, project_name):
    """
    Copy the `file_name` file in GitLab's `project_name` project directory to the execution directory
    """
    case_path = os.path.join(os.getcwd(), "git_case")
    lib_dst_path = os.path.join(
        case_path, project_name + "-Project", "api", file_name)
    # Determine if there is an `lib_dst_path` directory in the GitLab repository
    if os.path.isdir(lib_dst_path):
        lib_src_path = os.path.join(os.getcwd(), file_name)
        # Determine if there is a `lib_src_path` directory under the execution directory
        if os.path.isdir(lib_src_path):
            shutil.rmtree(lib_src_path)
        shutil.copytree(lib_dst_path, lib_src_path)
def pull_case():
    git_case_path = os.path.join(os.getcwd(), "git_case")
    if os.path.isdir(git_case_path):
        print(" *_* 发现 git_case 目录, 执行更新最新用例流程 ……")
        repo = Repo.init(path=git_case_path)
        remote = repo.remote()
        remote.pull()
        print(" ^_^ 已更新 GitLab 仓库中 git_case 项目的用例")
    else:
        print(" @_@ 找不到 git_case 目录, 执行下载新用例流程 ……")
        Repo.clone_from(url=ATP_CASE_GIT, to_path=git_case_path)
        print(" ^_^ 已下载 GitLab 仓库中 git_case 项目的用例")
    time.sleep(3)
def all_mkdir_copy(test_project):
    reset_file_tree(file_name="lib", project_name=test_project)
    reset_file_tree(file_name="data", project_name=test_project)
    reset_file_tree(file_name="element", project_name=test_project)
    reset_file_tree(file_name="testcase", project_name=test_project)
    reset_file_tree(file_name="files", project_name=test_project)
    mkdir_and_del(srcpath=os.path.join(os.getcwd(), "JUnit"))
    mkdir_and_del(srcpath=os.path.join(os.getcwd(), "report"))
    mkdir_and_del(srcpath=os.path.join(os.getcwd(), "details"))
def exec_api_test(test_name):
    plan_name = test_name
    book = xlrd.open_workbook('testcase/' + test_name + '-TestCase.xlsx')
    sheet_list = book.sheet_names()
    sheet_name = sheet_list
    desired_caps = {'platformName': 'api'}
    server_url = ''
    sweet = Autotest(plan_name, sheet_name, desired_caps, server_url)
    sweet.plan()
    details_file = open('details/details.txt', 'w', encoding='utf-8')
    details_file.write(str(sweet.report_data))
    details_file.close()
def up_exec_file_report(sheet_name, quequ_id):
    files_report = None
    files_junit = None
    for _root, _dirs, files in os.walk(os.path.join('report', sheet_name)):
        files_report = files[0]
    for _root, _dirs, files in os.walk('JUnit'):
        files_junit = files[0]
    exec_file_report_url = 'autotask/task/exec/file/report/'
    with open(os.path.join('report', sheet_name, files_report), 'rb') as fp1:
        files_report_obj = fp1.read()
    with open(os.path.join('JUnit', files_junit), 'rb') as fp2:
        files_junit_obj = fp2.read()
    with open(os.path.join('details', 'details.txt'), 'rb') as fp3:
        files_details_obj = fp3.read()
    files_obj = {
        'file_obj': (quequ_id + '.xlsx', files_report_obj),
        'file_obj_junit': (quequ_id + '.xml', files_junit_obj),
        'file_obj_details': (quequ_id + '.txt', files_details_obj)
    }
    requests.post(PLATFORM_URL + exec_file_report_url, files=files_obj)
if __name__ == '__main__':
    mkdir_and_del(srcpath=os.path.join(os.getcwd(), "log"))
    mkdir_and_del(srcpath=os.path.join(os.getcwd(), "snapshot"))
    while True:
        time.sleep(3)
        try:
            length = REDIS_POOL.llen("queu_api")
            localtime = time.asctime(time.localtime(time.time()))
            if length > 0:
                print(localtime + " →_→ 发现有新任务")
                value = REDIS_POOL.lpop("queu_api")
                print(value)
                pull_case()
                queque_id = value.split(',')[0]
                test_project = value.split(',')[1]
                test_name = value.split(',')[2]
                print("平台队列标识: " + queque_id)
                print("测试项目名称: " + test_project)
                print("测试用例名称: " + test_name)
                print("重置 Sweetest 测试运行环境 ……")
                all_mkdir_copy(test_project=test_project)
                print("Sweetest 测试运行环境就绪, 开始执行 ……")
                exec_api_test(test_name=test_name)
                print("Sweetest 测试完成, 上传测试报告 ……")
                up_exec_file_report(sheet_name=test_name, quequ_id=queque_id)
                print("测试报告上传完毕, 继续监听Redis数据库")
            else:
                print(localtime + " -_- 没有发现任务")
        except Exception as exce:
            print(exce)
'''
