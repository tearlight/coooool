from random import sample
import string

BID_LIST_LEN = 500

def gen_bids():
   bids = []
   for i in range(BID_LIST_LEN):
      bid = ''.join(sample(string.ascii_letters + string.digits, 11))
      bids.append("".join(bid))
   return bids
