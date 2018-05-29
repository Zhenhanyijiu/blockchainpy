# author yangyanan
#服务进程负责启动Queue，把Queue注册到网络上，然后往Queue里面写任务
# task_master.py
import random,time,queue
from multiprocessing.managers import BaseManager
#发送任务的队列：
task_queue = queue.Queue()
#接收结果的队列：
result_queue = queue.Queue()
#从BaseManager继承的QueueManager：