# -*- coding: utf-8 -*-

import sys
import logging
import socket

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def tcp_send(
    h_auth,
    h_data
    ):
    try:
        logging.info("target_host ->" + h_auth["target_host"] + "target_port ->" + str(h_auth["target_port"]))
        logging.info("send_data ->" + str(h_data))

        target_host = h_auth["target_host"]
        target_port = h_auth["target_port"]

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_host, target_port))
        #client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
        #logging.info(h_data.encode("utf-8"))
        client.send(h_data.encode("utf-8"))
        #client.send(b"ABCDEF")
        response = client.recv(4096)
        logging.info(response.decode("utf-8"))
        #print('\n')
        #print(response)

    except Exception as exp:
        logging.info(" ".join(map(str, exp.args)))
    except:
        logging.info(sys.exc_info())

def udp_send(
        h_auth,
        h_data
):
    try:
        logging.info("target_host ->" + h_auth["target_host"] + "target_port ->" + str(h_auth["target_port"]))
        logging.info("send_data ->" + str(h_data))

        target_host = h_auth["target_host"]
        target_port = h_auth["target_port"]

        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto(h_data.encode("utf-8"), (target_host, target_port))
        #client.sendto(b"AAABBBCCC", (target_host, target_port))
        data, addr = client.recvfrom(4096)
        logging.info(data.decode("utf-8"))
        #print('\n')
        #print(data)

    except Exception as exp:
        logging.info(" ".join(map(str, exp.args)))
    except:
        logging.info(sys.exc_info())
