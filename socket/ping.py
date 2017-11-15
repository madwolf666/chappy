import socket
import struct

def checksum(msg):
    # 偶数にしたメッセージ長を得る
    msg_short_len = len(msg) // 2 * 2
    # 2 バイトずつ足し込んでいく
    total = 0
    for i in range(0, msg_short_len, 2):
        total += (ord(msg[i + 1]) << 8) + ord(msg[i])
    # 長さが奇数なら残りも足す
    if len(msg) % 2 != 0:
        total += ord(msg[-1])
    # 2 バイト長で溢れる分を足す
    while (total >> 16) > 0:
        total = (total & 0xffff) + (total >> 16)
    # XXX: 何故この処理が必要なのか分からない...RFC 1071 読んでも見当たらないし
    total = total >> 8 | (total << 8 & 0xff00)
    # 1 の補数を取って 2 バイトに直す
    return ~total & 0xffff

#if __name__ == '__main__':
# ICMP の RAW ソケットを開く
IPPROTO_ICMP = socket.getprotobyname('icmp')
print(IPPROTO_ICMP)
#sock = socket.socket(socket.AF_INET, socket.SOCK_RAW)
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, IPPROTO_ICMP)
# ICMP ヘッダ: type, code, checksum, id, sequence
icmp_header = struct.pack('!BBHHH', 8, 0, 0, 1, 1)
icmp_payload = 'Hello, World!'
# チェックサムを計算する
csum = checksum(icmp_header + icmp_payload)
# ヘッダにチェックサムを当てはめる
icmp_header = struct.pack('!BBHHH', 8, 0, csum, 1, 1)
# ヘッダとデータからパケットを作る
packet = icmp_header + icmp_payload
# ICMP エコー要求を送信する
while packet:
    # パケットを送信する
    sent_bytes = sock.sendto(packet, ('192.168.223.138', 0))
    #sent_bytes = sock.sendto(packet, ('www.google.co.jp', 0))
    # 送りきれなかった分をずらす
    packet = packet[sent_bytes:]
