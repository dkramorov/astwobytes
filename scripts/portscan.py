# -*- coding:utf-8 -*-
#import pyfiglet
import sys
import socket

from concurrent.futures import ThreadPoolExecutor

from simple_logger import logger

def scan(ip: str = '127.0.0.1'):
    #ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    #print(ascii_banner)
    logger.info('processing %s ...' % ip)
    try:
        # will scan ports between 1 to 65,535
        for port in range(1, 65535):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                logger.info('IP {}, Port {} is open'.format(ip, port))
            s.close()
    except KeyboardInterrupt:
        logger.info('\nExiting Program')
        sys.exit()
    except socket.gaierror:
        logger.error('\n%s Hostname Could Not Be Resolved' % ip)
        sys.exit()
    except socket.error:
        logger.error('\n%s Host not responding' % ip)
        sys.exit()

"""
10.10.11.1-10.10.11.254
10.10.10.1-10.10.10.254
"""

if __name__ == '__main__':
    ip_range = ['10.10.11.%s' % i for i in range(1, 255)] + ['10.10.10.%s' % i for i in range(1, 255)]

    with ThreadPoolExecutor(255) as executor:
        results = executor.map(scan, ip_range)

print(results)



