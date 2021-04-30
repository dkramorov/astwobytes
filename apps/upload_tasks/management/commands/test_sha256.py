#-*- coding:utf-8 -*-
import sys
import time
from hashlib import sha256
import logging

from apps.main_functions.date_time import calc_elapsed_time
from django.core.management.base import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)

MAX_NONCE = sys.maxsize - 1

def SHA256(text):
    return sha256(text.encode('ascii')).hexdigest()

@calc_elapsed_time
def mine(block_number,
         transactions,
         prev_hash,
         zero_count):
    """Генерируем хэши пока первые цифры не будут нулями"""
    prefix_str = '0' * zero_count
    for nonce in range(MAX_NONCE):
        text = '%s%s%s%s' % (block_number, transactions, prev_hash, nonce)
        new_hash = SHA256(text)
        if new_hash.startswith(prefix_str):
            logger.info('nonce is %s, width %s leading zeros' % (nonce, zero_count))
            return new_hash

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--demo_mode',
            action = 'store_true',
            dest = 'demo_mode',
            default = False,
            help = 'Set demo mode')
        parser.add_argument('--cat_id',
            action = 'store',
            dest = 'cat_id',
            type = str,
            default = False,
            help = 'Set cat tag for update')
    def handle(self, *args, **options):
        transactions = '''
            test1->test2->20,
            test3->test3->45
        '''
        difficulty = 6
        new_hash = mine(15, transactions, '000000x%s' % SHA256('ABC'), difficulty)
        print(new_hash)

"""
import hashlib, struct

ver = 2
prev_block = "000000000000000117c80378b8da0e33559b5997f2ad55e2f7d18ec1975b9717"
mrkl_root = "871714dcbae6c8193a2bb9b2a69fe1c0440399f38d94b3a0f1b447275a29978a"
time_ = 0x53058b35 # 2014-02-20 04:57:25
bits = 0x19015f53

# https://en.bitcoin.it/wiki/Difficulty
exp = bits >> 24
mant = bits & 0xffffff
target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
target_str = target_hexstr.decode('hex')

nonce = 0
while nonce < 0x100000000:
    header = ( struct.pack("<L", ver) + prev_block.decode('hex')[::-1] +
          mrkl_root.decode('hex')[::-1] + struct.pack("<LLL", time_, bits, nonce))
    hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()
    print nonce, hash[::-1].encode('hex')
    if hash[::-1] < target_str:
        print 'success'
        break
    nonce += 1
"""

# ------
# https://bitcoin.stackexchange.com/questions/92705/stratum-protocol-problem-with-implementation-in-python/92722#92722
# ------

# http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html
#import socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect(("us1.ghash.io", 3333))
#sock.send("""{"id": 1, "method": "mining.subscribe", "params": []}\n""")
#print sock.recv(4000)
#sock.send("""{"params": ["kens_1", "password"], "id": 2, "method": "mining.authorize"}\n""")
#print sock.recv(4000)
