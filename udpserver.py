# IS496: Computer Networks (Spring 2022)
# Programming Assignment 1 -  Starter Code
# Name and Netid of each member:
# Member 1: shaojun3
# Member 2: boyu4
# Member 3: xiuyuan7

# Import any necessary libraries below
import socket
import sys
import struct
from pg1lib import *


############## Beginning of Part 1 ##############
BUFFER = 2048


def part1():
    # the hostname by default is student00.ischool.illinois.edu
    # the port by default is 8025
    print("********** PART 1 **********")
    # TODO: fill in the IP address of the host and the port number
    HOSTNAME = 'student00.ischool.illinois.edu'
    try:
        HOST = socket.gethostbyname(HOSTNAME)
    except socket.error as e:
        print("Unknown hostname: %s" % HOSTNAME)

    PORT = 41035
    sin = (HOST, PORT)

    # TODO: create a datagram socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()

    # TODO: Bind the socket to address
    try:
        s.bind(sin)
    except socket.error as e:
        print('Failed to bind socket.')
        sys.exit()

    print("Waiting ...")

    # TODO: receive message from the client and record the address of the client socket
    try:
        bts, client_addr = s.recvfrom(BUFFER)
    except socket.error as e:
        print('Failed to receive messages.')
        sys.exit()

    # TODO: convert the message from byte to string and print it to the screen
    msg = bts.decode()
    print('Client Message: %s' % msg)

    # TODO:
    # 1. convert the acknowledgement (e.g., integer of 1) from host byte order to network byte order
    # 2. send the converted acknowledgement to the client
    ack = socket.htonl(1)
    ack = str(ack).encode()
    try:
        s.sendto(ack, client_addr)
    except socket.error as e:
        print('Failed to send message.')
        sys.exit()

    # TODO: close the socket
    try:
        s.close()
    except socket.error as e:
        print('Failed to close socket.')
        sys.exit()


############## End of Part 1 ##############


############## Beginning of Part 2 ##############
def part2():
    print("********** PART 2 **********")
    # get server hostname
    HOSTNAME = 'student00.ischool.illinois.edu'

    # convert hostname to ip address
    try:
        HOST = socket.gethostbyname(HOSTNAME)
    except socket.error as e:
        print("Unknown hostname: %s" % HOSTNAME)

    # get port number from argument 1
    PORT = int(sys.argv[1])

    # build address data structure
    sin = (HOST, PORT)

    # generate server public key
    s_key = getPubKey()

    # create udp socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()

    # bind socket address with socket descriptor
    try:
        s.bind(sin)
    except socket.error as e:
        print('Failed to bind socket.')
        sys.exit()

    while True:
        print("Waiting ...")
        print()

        # receive client public key
        try:
            c_key, clt_addr = s.recvfrom(BUFFER)
        except socket.error as e:
            print('Failed to receive client public key.')
            sys.exit()

        # encrypt server public key with client public key
        et_s_key = encrypt(s_key, c_key)

        # sent encrypted server public key to client
        try:
            s.sendto(et_s_key, clt_addr)
        except socket.error as e:
            print('Failed to send encrypted server public key to client.')

        print("********** New Message **********")

        # receive encrypted message from client
        try:
            ect_msg, clt_addr = s.recvfrom(BUFFER)
        except socket.error as e:
            print('Failed to receive encrypted message from client.')
            sys.exit()

        # receive client checksum from client
        try:
            c_cksm, clt_addr = s.recvfrom(BUFFER)
        except socket.error as e:
            print('Failed to receive client checksum from client.')
            sys.exit()

        # decrypt encrypted message from client
        msg = decrypt(ect_msg)

        # convert client checksum from bytes to integer
        c_cksm = int(c_cksm.decode())

        # convert client checksum from network byte order to host byte order
        c_cksm = socket.ntohl(c_cksm)

        # print message and client checksum
        print()
        print('Received Message: \n%s' % msg.decode())
        print()
        print('Received Client Checksum: ', c_cksm)

        # calculate server checksum with message
        s_cksm = checksum(msg)

        # print server checksum
        print("Calculated Checksum: ", s_cksm)
        print()

        # compare client and server checksum
        if c_cksm == s_cksm:

            # convert acknowledgement from host byte order to network byte order
            ack = socket.htonl(1)

            # convert acknowledgement from integer to byte
            ack = str(ack).encode()

            # send acknowledgement 1 to client
            try:
                s.sendto(ack, clt_addr)
            except socket.error as e:
                print('Failed to send acknowledgement 1 to client.')
                sys.exit()

        else:

            # convert acknowledgement from host byte order to network byte order
            ack = socket.htonl(0)

            # convert acknowledgement from integer to byte
            ack = str(ack).encode()

            # send acknowledgement 0 to client
            try:
                s.sendto(ack, clt_addr)
            except socket.error as e:
                print('Failed to send acknowledgement 0 to client.')
                sys.exit()

            # report error message
            print("Error: checksum not match.")
            sys.exit()

    # close socket
    try:
        s.close()
    except socket.error as e:
        print('Failed to close socket.')
        sys.exit()

############## End of Part 2 ##############


if __name__ == '__main__':
    if len(sys.argv) == 1:
        part1()
    elif len(sys.argv) == 2:
        part2()
    else:
        print('wrong number of command line arguments, please try again')
