from smart_contracts import contract_register
from contract_built_in_tools import *
import json
import random
import traceback
from logger import *
set_logger(__name__)
logger = logging.getLogger(__name__)

@contract_register
def rkvs_about(data):
    return {'code': 101,
     'data': [
      {'key': 'about', 'name': '关于', 'desp': '这是一个RKVS合约，用于将键值对保存到区块链中。'},
       {'key': 'about', 'name': '发布者', 'desp': 'RDPStudio'}, {'key': 'about', 'name': '版本', 'desp': '1.0'}, 
       {'key': 'about', 'name': '更新时间', 'desp': '2022-01-10'},
       {'key': 'service', 'name': '查询键值对', 'desp': '查询键值对内容。','function': 'get' , 'input': [{'name': '键', 'n1': "key", 'desp': '请输入数据键'}]},
       {'key': 'service', 'name': '插入或更新键值对', 'desp': '插入或更新键值对。','function': 'mod' , 'input': [{'name': '键', 'n1': "key", 'desp': '请输入数据键'},{'name': '值', 'n1': "value", 'desp': '请输入数据值'},{'name': '密码', 'n1': "pass", 'desp': '请输入合约密码'}]}
       ]}

@contract_register
def rkvs_mod(data):
    data = json.loads(data)
    if data["pass"] != "XXX":
        return {'code': 100, 'data': '密码错误'}
    if data["key"] == "":
        return {'code': 100, 'data': '键不能为空'}
    if data["value"] == "":
        return {'code': 100, 'data': '值不能为空'}
    del data["pass"]
    block = {'provoider': 'rkvs', 'key': data["key"], 'value': data["value"]}
    id = new_block(json.dumps(block))
    return {'code': 101, 'data': id}

@contract_register
def rkvs_service_mod(data):
    data = json.loads(data.replace("'", '"'))
    try:
        if data["pass"] != "XXX":
            return {'code': 100, 'data': '密码错误'}
        if data["key"] == "":
            return {'code': 100, 'data': '键不能为空'}
        if data["value"] == "":
            return {'code': 100, 'data': '值不能为空'}
        del data["pass"]
        block = {'provoider': 'rkvs', 'key': data["key"], 'value': data["value"]}
        endkvs = new_block(json.dumps(block))
        return str([{'name': '返回数据', 'desp': endkvs}])
    except Exception as e:
        logger.error(traceback.format_exc())
        return str([{'name': '返回数据', 'desp': '查询失败'}])

@contract_register
def rkvs_get(data):
    historyofkvs = get_block_by_bjson("key|" + str(data) + "|provoider|rkvs")
    endkvs = json.loads(str(historyofkvs["data"][-1]["data"]).replace('\'', '"'))
    if endkvs["provoider"] != "rkvs":
        return {'code': 100, 'error': 'invalid call'}
    endkvs["bid"] = historyofkvs["data"][-1]["index"]
    endkvs["hash"] = historyofkvs["data"][-1]["hash"]
    endkvs["timestamp"] = historyofkvs["data"][-1]["timestamp"]
    return {'code': 101, 'data': endkvs}

@contract_register
def rkvs_service_get(data):
    data = json.loads(data.replace("'", '"'))
    data = data["key"]
    try:
        historyofkvs = get_block_by_bjson("key|" + str(data) + "|provoider|rkvs")
        endkvs = json.loads(str(historyofkvs["data"][-1]["data"]).replace('\'', '"'))
        if endkvs["provoider"] != "rkvs":
            return {'code': 100, 'error': 'invalid call'}
        endkvs["bid"] = historyofkvs["data"][-1]["index"]
        endkvs["hash"] = historyofkvs["data"][-1]["hash"]
        endkvs["timestamp"] = historyofkvs["data"][-1]["timestamp"]
        return str([{'name': '返回数据', 'desp': endkvs}])
    except Exception as e:
        logger.error(traceback.format_exc())
        return str([{'name': '返回数据', 'desp': '查询失败'}])