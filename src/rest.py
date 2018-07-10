from flask import Flask, request
import requests
from blockchain.blockchain import *
from blockchain.block import *

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/new_transaction',methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["author","content"]
    for field in required_fields:
        if not tx_data.get(field):
            return "invalid transaction data", 404

    tx_data["timestamp"] = time.time()
    blockchain.add_new_transaction(tx_data)
    return "Success",201

@app.route('/chain',methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),"chain": chain_data})

@app.route('/mine',methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    return "Block #{} is mined.".format(result)

@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions) 

@app.route('/last')
def get_last():
    return json.dumps(blockchain.last_block().index)

peers = set()
@app.route('/add_nodes',methods=['POST'])
def register_new_peers():
    nodes = request.get_json()
    if not nodes:
        return "invalid request", 400
    for node in nodes:
        peers.add(node)
    return "Success", 201



@app.route('/add_block',methods=['POST'])
def validate_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"], block_data["transactions"],block_data["timestamp"], block_data["previous_hash"]])
    proof = block_data['hash']
    added = blockchain.add_block(block,proof)

    if not added:
        return "The block was discarded", 400
    
    return "Block added to the chain", 201

def announce_new_block(block):
    for peer in peers:
        url = "http://{}/add_block".format(peer)
        requests.post(url,data = json.dumps(block.__dict__,sort_keys=True))



def consensus():
    """ with multiple nodes comes multiple chains we need to define a simple mechanism to
    choose the correct chain , here we will choose the longer one """
    global blockchain

    longest_chain = None
    current_len = len(blockchain)

    for node in peers:
        response.get('http://{}/chain'.format(node)) 
        length = response.json()['length']
        chain = response.json()['chain']
        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain
        if longest_chain:
            blockchain = longest_chain
            return True
        
        return False


app.run(debug=True, port=8080)