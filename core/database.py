import sys
import json
import pickle
import random
import string
sys.path.append('../trie')
import db
import MerklePatriciaTrie as MPT
sys.path.append("../crypto")
#from crypto import basic
from basic import *
#from crypto import basic
class database:
	def __init__(self):
		#self.pendingTransactionDB = db.DB('pendingTransactionDB')
		self.balanceDB = db.DB('balanceDB')
		self.transactionDB = db.DB('transactionDB')
		self.blockDB = db.DB('blockDB')
		self.rootDB = db.DB('rootDB')
		self.transactionDB.put(b'1234567',pickle.dumps([]))
	def pendingTransaction(self, newTransaction):
		#Insert newTransaction which hasn't verified into the database
		key = b'1234567'
		pending = self.transactionDB.get(key)
		#print(pending)
		pending = pickle.loads(pending)
		requireFee = 500
		if newTransaction['fee'] > requireFee: 
			pending.append(newTransaction)
		"""
		flag = False
		#print(newTransaction)
		for idx, transaction in enumerate(pending):
			if newTransaction['fee'] < transaction['fee']:
		if not flag:
			pending.append(newTransaction)
		"""
		try:
			self.transactionDB.put(key, pickle.dumps(pending))
			return True
		except:
			return False

	def getPendingTransaction(self):
		#Return the pending transaction with the largest fee
		key = b'1234567'
		pendingTransaction = pickle.loads(self.transactionDB.get(key))
		newTransaction = pendingTransaction.pop(0)
		self.transactionDB.put(key, pickle.dumps(pendingTransaction))
		return newTransaction

	def testBalance(self):
		for i in range(5):
			fakeAccount = {}
			fakeAccount['balance'] = {'cic':random.randint(1,100),'now':random.randint(1,100)}
			fakeAccount['nonce'] = random.randint(1,100)
			fakeAccount['address'] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
			print(fakeAccount)
			self.balanceDB.put(fakeAccount['address'].encode(), pickle.dumps(fakeAccount))

	def verifyBalanceAndNonce(self, transaction):
		#Verify whether the balance of the account is enough and the nonce is correct
		#Return true if everything is correct, else false
		address = Key_c.address(transaction["publicKey"])
		#address = 'ilwOop'
		accountData = pickle.loads(self.balanceDB.get(address.encode()))
		
		for coin in transaction['out']:
			if accountData['balance'][coin] < transaction['out'][coin]:
				return False
		if accountData['nonce']+1 != transaction['nonce']:
			return False

		return True

	def updateBalanceAndNonce(self, transaction):
		#Update the balance after if the transaction has been verified
		receiver = transaction["to"]
		receiverAccount = pickle.loads(self.balanceDB.get(receiver.encode()))
		#sender = Key_c.address(transaction["publicKey"])
		sender = 'ilwOop'
		senderAccount = pickle.loads(self.balanceDB.get(sender.encode()))
		#Deal with json

		for coin in transaction['out']:
			senderAccount['balance'][coin] -= transaction['out'][coin]
			receiverAccount['balance'][coin] += transaction['out'][coin]
		senderAccount['nonce'] += 1
		try:
			self.balanceDB.put(sender.encode(), pickle.dumps(senderAccount))
			self.balanceDB.put(receiver.encode(), pickle.dumps(receiverAccount))
			return True
		except:
			return False

	def createTransaction(self, transaction):
		#Push transaction into database
		#Todo: Transaction Trie
		try:
			root = self.rootDB.get(b'TransactionTrie')
		except:
			root = ""
		trie = MPT.MerklePatriciaTrie('testdb', root)
		trie.update(transaction['txid'], transaction)
		new_root = trie.root_hash()
		self.rootDB.put(b'TransactionTrie', new_root)
	"""
	def addTransactionToBlock(blockData, transaction):
		#Push verified transaction into blockData
		blockData['transaction'].append(transaction)
		return blockData
	"""
	def createBlock(self, blockData):
		#Push block into database
		#Todo: Block Trie
		try:
			root = self.rootDB.get(b'BlockTrie')
		except:
			root = ""
		trie = MPT.MerklePatriciaTrie('testdb', root)
		trie.update(blockData['hash'], blockData)
		new_root = trie.root_hash()
		self.rootDB.put(b'BlockTrie', new_root)

