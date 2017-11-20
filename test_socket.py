import libmct.mct_socket as mct_sockt

a_auth_tcp = {
    "target_host": "127.0.0.1",
    "target_port": 9999
}

a_auth_udp = {
    "target_host": "127.0.0.1",
    "target_port": 80
}

mct_sockt.tcp_send(a_auth_tcp, "あああ")

mct_sockt.udp_send(a_auth_udp, "いいい")
