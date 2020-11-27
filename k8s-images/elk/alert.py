import requests
import json
from elasticsearch import Elasticsearch
import os
import re
import threading


# 获取dsl下所有的py文件，排除pycache
def get_dsls():
    files_list = []
    for root, dirs, files in os.walk(top='dsl'):
        # dirs[:] = [d for d in dirs if d not in "__pycache__"]
        files_list += files
    return files_list


def dingtalk_post(hit, receiver):
    # 钉钉API请求头
    webhook_header = {"Content-Type": "application/json", "charset": "utf-8"}
    # 告警Markdown
    webhook_alert_message_platform = '''
# 状态： {log_level}告警
**主机名：** {hostname}  
**告警模块：** {tag}  
**日志时间：** {log_time}   
**日志等级：** {log_level}  
**日志内容：** {log_message}
'''.format(tag=hit['_source']['tags'][0],
           hostname=hit['_source']['beat']['hostname'],
           log_time=hit['_source']['log_time'],
           log_level=hit['_source']['log_level'],
           log_message=hit['_source']['log_message'])
    # body
    webhook_message = {
        "msgtype": "markdown",
        "markdown": {
            "title":
            '告警: ' + hit['_source']['tags'][0] + hit['_source']['log_level'],
            "text":
            webhook_alert_message_platform
        }
    }
    sendData = json.dumps(webhook_message, indent=1)
    requests.post(url=receiver, data=sendData, headers=webhook_header)


def alert_post(elastic_connection, receivers, dsl):
    elastic_search = elastic_connection.search(scroll='1m', body=dsl)
    while len(elastic_search['hits']['hits']) > 0:
        for hit in elastic_search['hits']['hits']:
            dingtalk_post(hit, receivers[0])
            receivers = (receivers[1:] +
                         [receivers[0]] if len(receivers) > 1 else receivers)
        elastic_scroll_id = elastic_search['_scroll_id']
        elastic_search = elastic_connection.scroll(scroll_id=elastic_scroll_id,
                                                   scroll='1m')


def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    es_URL = "http://10.16.17.40:9200"
    elastic_connection = Elasticsearch(es_URL)
    file_list = get_dsls()
    thread_list = []
    for i in file_list:
        print(i)
        with open(os.path.join('dsl', i), 'r', encoding='utf-8') as f:
            json_info = json.load(f)
            t = threading.Thread(target=alert_post,
                                 args=(
                                     elastic_connection,
                                     json_info['receivers'],
                                     json_info['dsl'],
                                 ))
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()


if __name__ == "__main__":
    main()