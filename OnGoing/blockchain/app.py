from flask import Flask
from flask import request
from flask import render_template
from blockchain import Blockchain
from uuid import uuid4

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    return 'New Block'

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return "New transaction"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return response


if __name__ == '__main__':
    app.run()
