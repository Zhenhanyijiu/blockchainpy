# 从blockchain API中得到未花费的输出
import json
import requests
# 样例地址
address = '1Dorian4RoXcnBv9hnQ4Y2C1an6NJ4UrjX'
# API网址是：https://blockchain.info/unspent?active=<address>
# 它返回一个JSON对象，其中包括一个包含着UTXO的“unspent_outputs”列表，就像这样：
#{ "unspent_outputs":[
#{
# tx_hash":"ebadfaa92f1fd29e2fe296eda702c48bd11ffd52313e986e99ddad9084062167",
# "tx_index":51919767,
# "tx_output_n": 1,
# "script":"76a9148c7e252f8d64b0b6e313985915110fcfefcf4a2d88ac",
# "value": 8000000,
# "value_hex": "7a1200",
# "confirmations":28691
# },
# ...
#]}
resp = requests.get('https://blockchain.info/unspent?active=%s' % address)
utxo_set = json.loads(resp.text)["unspent_outputs"]
for utxo in utxo_set:
	print("%s:%d - %ld Satoshis" % (utxo['tx_hash'], utxo['tx_output_n'], utxo['value']))