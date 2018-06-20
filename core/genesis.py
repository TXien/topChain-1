import time
import sys
#sys.path.append("../crypto")
#from basic import *#Hash_c
#sys.path.append("./crypto")
#from basic import *

class Genesis:
    def genesis():
        genesis = {
            "version":"sue",
            "config":
                {
                    "version":"init"
                },
            "blockNumber" : "0",
            "timestamp":time.time(),
            "hash":"AC66D1839E1B79F1FB22181B70237F1E45E3D95A512A0790C216328CA2631674",
            "extraData":"",
            "ParentHash":"",
            "Alloc":[{"cxfcb42deca97e4e8339e0b950ba5efa368fe71a55":"300"}]
        }
        return genesis

