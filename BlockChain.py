import hashlib
import json
from time import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
from uuid import uuid4
import requests
from flask import Flask, jsonify, request
import math

#构造一个区块链类
class Blockchain(object):
	#两个成员：当前交易成员和链成员，都用列表类型表示
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        # 创建“创世块”
        self.new_block(previous_hash=1,create_time=201805141949, proof=20080514)

    def new_block(self, proof,create_time ,previous_hash=None):
        """
        生成新块
        :param proof: <int> 工作量证明，创建区块的时候需要消耗一定的算力
        :param previous_hash: (Optional) <str> 前一个区块的hash值
		:param create_time: 记录区块创建时间
        :return: <dict> 返回一个新的区块，这个区块block是一个字典结构
        """
        block = {
            # 新block对应的index
            'index': len(self.chain) + 1,
            # 时间戳，记录区块创建的时间
            'timestamp': create_time,
            # 记录当前的交易记录，即通过new_transactions创建的交易，记录在这个新的block里
            'transactions': self.current_transactions,
            # 工作量证明，消耗一定算力才能找到
            'proof': proof,
            # 前一个block对应的hash值
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # 重置当前的交易，用于记录下一次生成区块的当前交易
        self.current_transactions = []
        # 将新生成的block添加到block列表中
        self.chain.append(block)
        # 返回新创建的blcok
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        生成新交易信息，信息将加入到下一个待挖的区块中
        :param sender: <str> 发送者的地址
        :param recipient: <str> 接受者的地址
        :param amount: <int> 交易额度
        :return: <int> 返回新的Block的Id值，新产生的交易将会被记录在新的Block中
        """
        # 简化实现，向交易列表中添加一个字典结构，这个字典中记录交易双方的信息
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        # 返回最后一个区块的index加上1，即对应到新的区块上
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        生成区块的 SHA-256 hash值
        :param block: <dict> Block结构，字典类型
        :return: <str>返回16进制字符串
        """
        # 将block字典结构中‘index’,'timestamp','previous_hash','proof'的值转换成字符串，并拼接起来。
        # 调用sha256函数求取hash值并返回
        block_string=str(block['index'])+str(block['timestamp'])+str(block['previous_hash'])+str(block['proof'])
        return hashlib.sha256(block_string.encode()).hexdigest()

	#装饰器，把方法变成属性，返回链列表结构中最后一个元素
    @property
    def last_block(self):
        return self.chain[-1]
	
    def proof_of_work(self, header_block,difficulty_bits):
        """
        工作量证明POW:
         - 寻求一个proof(32bit)使得sha256(header_block+proof)小于一个目标值
         - 参数difficulty_bits为难度值，值越大，求解难度越大
        :param : header_block: <str> 包含block['index'],block['timestamp'],block['previous_hash']
        :param : difficulty_bits:<int> 1~255之间
        :return: <int>
        """
        proof = 0
        # 定义一个循环，直到valid_proof验证通过，并返回当前的proof
        while self.valid_proof(header_block, proof,difficulty_bits) is False:
            proof += 1
        return proof

	#静态方法，可以用类名直接调用
    @staticmethod
    def valid_proof(header_block, proof,difficulty_bits):
        """
		通过穷举，找到满足目标条件的工作量证明
        验证证明: 验证hash结果小于目标值 2**（256-difficulty_bits）
        :param header_block: <str> 区块头
        :param proof: <int> 当前待验证的证明
        :return: <bool> 满足目标条件返回true
        """
        target_int = 2 ** (256-difficulty_bits)
        input = header_block+str(proof)
        result = hashlib.sha256(input.encode()).hexdigest()
        return int(result,16)<target_int

#实例化一个Flask节点
app = Flask(__name__)

# 为当前节点生成一个全局唯一的地址，使用uuid4方法
node_identifier = str(uuid4()).replace('-', '')

#初始化区块链
blockchain = Blockchain()

# 告诉服务器去挖掘新的区块
@app.route('/mine', methods=['GET'])
def mine():
    #获取区块链最后一个block
    last_block = blockchain.last_block
    #构造区块头header_block
    header_block =''
    #取出索引号并加1，作为新区块的index，接连到区块头
    header_block += str(last_block['index']+1)
    #时间戳：记录创建区块的时间，接连到区块头[时间有些粗略，有待改进]
    create_time = time()
    header_block += str(create_time)
    #取出前一个区块的hash值，接连到区块头
    header_block +=str(last_block['previous_hash'])
    #运行工作量证明和验证算法，得到proof。
    #设置难度值
    difficulty_bits = 20
    proof = blockchain.proof_of_work(header_block,difficulty_bits)
    # 给工作量证明的节点提供奖励.
    # 发送者为 "0" 表明是新挖出的币
    # 接收者是我们自己的节点，即上面生成的node_identifier。实际中这个值可以用用户的账号。
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # 产生一个新的区块，并添加到区块链中
    block = blockchain.new_block(proof,create_time)
    #构造返回响应信息
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

 # 创建一个交易并添加到区块，POST接口可以给接口发送交易数据
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    #获取请求的参数，得到参数的json格式数据
    values = request.get_json()
    print('request parameters:%s'%(values))
    #检查请求的参数是否合法，包含sender,recipient,amount几个字段
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # 使用blockchain的new_transaction方法创建新的交易
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    #构建response信息
    response = {'message': f'Transaction will be added to Block {index}'}
    #返回响应信息
    return jsonify(response), 201

#返回整个区块链，GET接口
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    #服务器运行在5000端口上
    app.run(host='0.0.0.0', port=5000)