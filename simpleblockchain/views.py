from uuid import uuid4

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from simpleblockchain.serializers import TransactionSerializer
from simpleblockchain.blockchain import Blockchain

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-','')

#Instantiate the Blockchain
blockchain = Blockchain()

class MinningView(APIView):
    """
    Mines a new block in the blockchain.
    """
    def get(self, request, format=None):
        # We run the proof of work algoritm to get the next proof
        last_block = blockchain.last_block
        last_proof = blockchain.last_block['proof']
        proof = blockchain.proof_of_work(last_proof)

        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin
        blockchain.new_transaction({
            'sender': "0", 
            'recipient': node_identifier,
            'amount': 1
        })

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

class Transaction(APIView):
    """
    Make a transaction in the blockchain.
    """
    def post(self, resquest, format=None):
        values = JSONParser().parse(request)    

        transaction = TransactionSerializer(data=values)

        if transaction.is_valid():
            #Create a new Transaction
            index = blockchain.new_transaction(transaction.data)
            response = {
                'message': 'Transaction will be added to Block {}'.format(index)
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        response = {
            'message': 'Missing values'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class FullChainView(APIView):
    """
    Shows the complete Blockchain.
    """
    def get(self, request, format=None):
        response = { 
            'chain' : blockchain.chain, 
            'length': len(blockchain.chain)
        }
        return Response(response)

class RegisterNodesView(APIView):
    """
    Registers each node with a connection in Blockchain.
    """
    def post(self, request, format=None):
        values = JSONParser().parse(request)

        nodes = values.get('nodes')
        if nodes is None:
            response = {
                'message': 'Error: Please supply a valid list of nodes'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        for node in nodes:
            blockchain.register_node(node)

        response = {
            'message': 'New nodes have been added',
            'total_nodes': list(blockchain.nodes),
        }

        return Response(response, status=status.HTTP_201_CREATED)

class ConsensusView(APIView):
    """
    Resolve conflics with the transactions.
    """
    def get(self, request, format=None):
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



