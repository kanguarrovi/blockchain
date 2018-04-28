from uuid import uuid4

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from simpleblockchain.blockchain import Blockchain

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-','')

#Instantiate the Blockchain
blockchain = Blockchain()

@api_view(['GET'])
def mine(request, format=None):

    if request.method == 'GET':
        # We run the proof of work algoritm to get the next proof
        last_block = blockchain.last_block
        last_proof = blockchain.last_block['proof']
        proof = blockchain.proof_of_work(last_proof)

        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin
        blockchain.new_transaction(
            sender = "0",
            recipient = node_identifier,
            amount = 1,
        )

        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message' : "New Block Forged",
            'index' : block['index'],
            'transactions' : block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }

        return Response(response, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def new_transaction(request, format=None):
    if request.method == 'POST':
        values = JSONParser().parse(request)
        print(values)

        #Check that the required fields are in the POST'ed data
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return 'Missing values', 400

        #Create a new Transaction
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

        response = {'message': 'Transaction will be added to Block {}'.format(index)}

        return Response(response, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def full_chain(request, format=None):
    if request.method == 'GET':
        response = {
            'chain' : blockchain.chain,
            'length': len(blockchain.chain)
        }
        return Response(response)

@api_view(['POST'])
def register_nodes(request):
    values = JSONParser().parse(request)

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }

    return Response(response, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def consensus(request):
    
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return Response(response)

