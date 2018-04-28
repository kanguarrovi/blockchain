import os
import sys

def repetition_mine(port, cant):
	"""
    Calls the mine API a certian cuantity of times.
    :param port: <string> The port where the API is running. 
	:param cant: <int> The cuantity of times the API will be run.
    """
	for x in range(0, cant):
		os.system("curl 127.0.0.1:{}/mine".format(port))

if __name__ == "__main__":
	try:
		repetition_mine(sys.argv[1], int(sys.argv[2]))
	except IndexError:
		print("You must specify a port and a cuantity")
		print("Eg: python miner_script.py 8000 10")
