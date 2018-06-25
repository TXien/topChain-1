from core.database import database
from core.transaction import Transaction
from core.block import Block
from core.genesis import Genesis

#def createFakeTransaction():
#	fakeTransaction = 

def updateDBAccountStatus(block):
	transactions = block['transaction']
	if len(transactions) == 0:
		return 0
	for transaction in transactions:
		if not updateBalanceAndNonce(transaction):
			print('Something wrong when updating account status.')
			return False
	return True

def main():
	fntdb = database()

	currentBlockNum = fntdb.getBlockNumber()
	print('getBlockNumber:', currentBlockNum)
	if currentBlockNum == 0:
		genesisBlock = Genesis.genesis()
		fntdb.createBlock(genesisBlock)
	else:
		while True:
			newBlock = Block()
			while True:
				pendingTran = fntdb.getPendingTransaction()
				if pendingTran == {}:
					print('There is no pending transaction now.')
					continue
				else:
					if not Transaction.verifyTransaction():
						print('Transaction fails to be verified.')
						continue
				newBlock.pushTransactionToArray(pendingTran)

			parentBlock = fntdb.getBlockbyID(currentBlockNum)
			#key?
			newBlock = newBlock_POA(newBlock, parentBlock, key)
			try:
				fntdb.createBlock(newBlock)
			except:
				print('Error occurs when saving block into db.')
				continue
			updateDBAccountStatus(newBlock)





#getBlockNumber
#if(blockNumber == null):
#--getBlockNumber
#genesisBlock
#genesisBlockInsertToDB
#--createGenesisBlock()
#updateGenesisAccountBalance
#else:
#getPendingTransaction
#verifyTransaction
#pushTransactionToArray
#getparentblock
#--getBlock()
#newBlock_POA(blockData,parentblock,key)
#blockStoreToDB
#updateDBAccountStatus
#pack transaction
#stay time

if __name__ == "__main__":
	main()

