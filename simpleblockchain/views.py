import re
from uuid import uuid4

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from simpleblockchain.serializers import TransactionSerializer, NodesSerializer
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

class TransactionView(APIView):
    """
    Make a transaction in the blockchain.
    """
    serializer_class = TransactionSerializer

    def post(self, request, format=None):

        transaction = TransactionSerializer(data=request.data)
        
        if transaction.is_valid():
            #Create a new Transaction
            index = blockchain.new_transaction(transaction.data)
            response = {
                'message': 'Transaction will be added to Block {}: the next mined.'.format(index)
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

    serializer_class = NodesSerializer

    def post(self, request, format=None):

        values = NodesSerializer(data=request.data)

        if values.is_valid():

            def return_ip_nodes(ips_string):
                """
                Separates every IP node string
                :param ips_string: <str> String of the node or nodes to add
                :return: <list> List of each node strings
                """
                pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:\:\d{1,5})?")
                ips = pattern.findall(ips_string)
                return ips

            blockchain.register_node(return_ip_nodes(values.data["node"]))

            response = {
                'message': 'New node have been added',
                'total_nodes': list(blockchain.nodes),
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        response = {
            'message': 'Error: Please supply a valid IP of node'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

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



