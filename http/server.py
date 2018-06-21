from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import cgi
import json
import leveldb
import sys
sys.path.append('../trie')
import MerklePatriciaTrie as MPT 

class BlockTrie(object):
	def __init__(self, root_hash):
		self.trie = MPT.MerklePatriciaTrie("testdb", root_hash) 
	def search(self, key):
		value = self.trie.search(key)
		root_hash = self.trie.root_hash()
		return root_hash, value

class TransactionTrie(object):
	def __init__(self, root_hash):
		self.trie = MPT.MerklePatriciaTrie("testdb", root_hash) 

	def search(self, key):
		value = self.trie.search(key)
		root_hash = self.trie.root_hash()
		return root_hash, value

class Handler(BaseHTTPRequestHandler):

	#def __init__(self):
		#self.blockDB = leveldb.LevelDB("testdb")
		#self.tranDB = leveldb.LevelDB("test2db")
	def do_OPTIONS(self):
		self.send_response(200, "ok")
		self.send_header('Access-Control-Allow-Credentials', 'true')
		self.send_header('Access-Control-Allow-Origin', 'http://192.168.0.125:8888')
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
	 
	def do_GET(self):
		db = leveldb.LevelDB("rootdb")
		try:
			method, param = urlparse(self.path).path.split('/')[1:]
		except:
			self.send_error(400, "Too much parameters")
			return

		if method == "getBlock":
			try:
				root = db.Get(b"BlockTrie")
			except:
				root = ""
			#print("root:", root)
			trie = BlockTrie(root)
			root, value = trie.search(param)
			print("value:", value)
			db.Put(b"BlockTrie", root)	

		elif method == "getBlockByID":
			idx_db = leveldb.LevelDB("testdb")
			value = idx_db.Get(str(param).encode()).decode()
			print("value:", value)

		elif method == "getTransaction":
			try:
				root = db.Get(b"TransactionTrie")
			except:
				root = ""
			trie = TransactionTrie(root)
			root, value = trie.search(param)
			db.Put(b"TransactionTrie", root)
		else:
			self.send_error(415, "No such method.")	

		self.send_response(200)
		post_return = {}
		post_return['method'] = method
		post_return['result'] = value
		self.wfile.write(json.dumps(post_return).encode())

	def do_POST(self):
		db = leveldb.LevelDB("rootdb")
		ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
		if ctype == 'application/json':
			length = int(self.headers['content-length'])
			#print(self.rfile.read(length).decode())            
			post_values = json.loads(self.rfile.read(length).decode())
			print(post_values)
			method = post_values.get('method')
			assert isinstance(method, str), "Method must be a string!"

			param = post_values.get('param')
			assert isinstance(param, str), "Parameter must be bytes-like object!"

			#idx = post_values.get('id')
			#assert isinstance(idx, int), "ID must be an integer!"

			if method == "getBlock":
				try:
					root = db.Get(b"BlockTrie")
				except:
					root = ""
				#print("root:", root)
				trie = BlockTrie(root)
				root, value = trie.search(param)
				print("value:", value)
				db.Put(b"BlockTrie", root)
			elif method == "getTransaction":
				try:
					root = db.Get(b"TransactionTrie")
				except:
					root = ""
				trie = TransactionTrie(root)
				root, value = trie.search(param)
				db.Put(b"TransactionTrie", root)
			else:
				self.send_error(415, "No such method.")				
		else:
			self.send_error(415, "Only json data is supported.")
			returnget

		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.send_header('Access-Control-Allow-Credentials', 'true')
		self.send_header('Access-Control-Allow-Origin', 'http://192.168.0.125:8888')
			
		self.end_headers()
		#print("post_values:", post_values)
		post_return = {}
		post_return['method'] = method
		post_return['result'] = value
		self.wfile.write(json.dumps(post_return).encode())
if __name__ == '__main__':
	from http.server import HTTPServer
	server = HTTPServer(("192.168.0.125", 9000), Handler)
	print("Starting server, use <Ctrl-C> to stop")
	server.serve_forever()  