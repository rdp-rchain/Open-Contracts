import hashlib
from smart_contracts import contract_register
from contract_built_in_tools import *
import json
import random
import traceback
from logger import *
import time
set_logger(__name__)
logger = logging.getLogger(__name__)

def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()

def getnonce(data):
    difficulty = 2
    difficulty_string = '0' * difficulty
    while True:
        for i in range(1, 10000000000000000000000000000000000000000000000000):
            nonce = str(i)
            if sha256(str(data) + nonce)[:difficulty] == difficulty_string:
                return nonce

@contract_register
def subchain0_about(data):
    blockchain = []
    indexs = []
    try:
        mcbc = get_block_by_bjson("provoider|subchain0")["data"]
        for b in mcbc:
            scb = json.loads(str(b["data"]).replace('\'', '"'))
            if scb["index"] not in indexs:
                indexs.append(scb["index"])
                blockchain.append(scb)
    except Exception as e:
        logger.error(traceback.format_exc())
    chainbs = len(blockchain)
    return {'code': 101,
     'data': [{'key': 'about', 'name': '目前区块数量', 'desp': str(chainbs)},
      {'key': 'about', 'name': '关于', 'desp': '这是一个RSCP(RDP Sub Chain Project)合约，用于在热链上操作子链。'},
       {'key': 'about', 'name': '发布者', 'desp': 'RDPStudio'}, {'key': 'about', 'name': '开发者', 'desp': 'RDPStudio'}, {'key': 'about', 'name': '版本', 'desp': '1.0'}, 
       {'key': 'about', 'name': '更新时间', 'desp': '2022-01-14'},
       {'key': 'service', 'name': '查询区块', 'desp': '查询区块数据。','function': 'get' , 'input': [{'name': '区块ID', 'n1': "key", 'desp': '请输入区块号'}]}
       ]}

@contract_register
def subchain0_length(data):
    blockchain = []
    indexs = []
    try:
        mcbc = get_block_by_bjson("provoider|subchain0")["data"]
        for b in mcbc:
            scb = json.loads(str(b["data"]).replace('\'', '"'))
            if scb["index"] not in indexs:
                indexs.append(scb["index"])
                blockchain.append(scb)
    except Exception as e:
        logger.error(traceback.format_exc())
    chainbs = len(blockchain)
    return {'code': 101, 'len': chainbs}

@contract_register
def subchain0_get(data):
    data = data
    try:
        historyofscb = get_block_by_bjson("index|" + str(data) + "|provoider|subchain0")
        endscb = json.loads(str(historyofscb["data"][-1]["data"]).replace('\'', '"'))
        if endscb["provoider"] != "subchain0":
            return {'code': 100, 'error': 'invalid call'}
        endscb["bid"] = historyofscb["data"][-1]["index"]
        endscb["hash"] = historyofscb["data"][-1]["hash"]
        endscb["timestamp"] = historyofscb["data"][-1]["timestamp"]
        return {'code': 101, 'data': endscb}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {'code': 100}

@contract_register
def subchain0_new_block(data):
    blockchain = []
    indexs = []
    try:
        mcbc = get_block_by_bjson("provoider|subchain0")["data"]
        for b in mcbc:
            scb = json.loads(str(b["data"]).replace('\'', '"'))
            if scb["index"] not in indexs:
                indexs.append(scb["index"])
                blockchain.append(scb)
    except Exception as e:
        logger.error(traceback.format_exc())
    if len(blockchain) == 0:
        block = {
            'index': 1,
            'timestamp': time.time(),
            'data': data,
            'prev_hash': '0',
            'vaildtor': 'Node0',
            'nonce': getnonce(data),
            'provoider': 'subchain0'
        }
        block['hash'] = sha256(str(block['index']) + str(block['timestamp']) + block['data'] + block['prev_hash'] + block['vaildtor'] + block['nonce'])
        id = new_block(str(block).replace('"', '\''))
        return {'code': 101, 'data': id, 'index': block['index']}
    block = {
        'index': len(blockchain) + 1,
        'timestamp': time.time(),
        'data': data,
        'prev_hash': blockchain[-1]['hash'],
        'vaildtor': 'Node0',
        'nonce': getnonce(data),
        'provoider': 'subchain0'
    }
    block['hash'] = sha256(str(block['index']) + str(block['timestamp']) + block['data'] + block['prev_hash'] + block['vaildtor'] + block['nonce'])
    id = new_block(str(block).replace('"', '\''))
    return {'code': 101, 'data': id, 'index': block['index']}

@contract_register
def subchain0_service_get(data):
    data = json.loads(data.replace("'", '"'))
    data = data["key"]
    try:
        historyofscb = get_block_by_bjson("index|" + str(data) + "|provoider|subchain0")
        endscb = json.loads(str(historyofscb["data"][-1]["data"]).replace('\'', '"'))
        if endscb["provoider"] != "subchain0":
            return {'code': 100, 'error': 'invalid call'}
        endscb["bid"] = historyofscb["data"][-1]["index"]
        endscb["hash"] = historyofscb["data"][-1]["hash"]
        endscb["timestamp"] = historyofscb["data"][-1]["timestamp"]
        return str([{'name': '返回数据', 'desp': endscb}])
    except Exception as e:
        logger.error(traceback.format_exc())
        return str([{'name': '返回数据', 'desp': '查询失败'}])