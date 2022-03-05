# IS496: Computer Networks (Spring 2022)
# Programming Assignment 1 -  Starter Code
# Name and Netid of each member:
# Member 1: shaojun3
# Member 2: boyu4
# Member 3: xiuyuan7

# Import any necessary libraries below
import socket
import sys
import time
from pg1lib import *

############## Beginning of Part 1 ##############
# TODO: define a buffer size for the message to be read from the UDP socket
BUFFER = 2048


def part1():
    print("********** PART 1 **********")
    # TODO: fill in the hostname and port number
    HOSTNAME = 'student00.ischool.illinois.edu'
    PORT = 41035

    # A dummy message (in bytes) to test the code
    msg = b"Hello World"

    # TODO: convert the host name to the corresponding IP address
    try:
        HOST = socket.gethostbyname(HOSTNAME)
    except socket.error as e:
        print("Unknown hostname: %s" % HOSTNAME)
    sin = (HOST, PORT)

    # TODO: create a datagram socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()

    # TODO: convert the message from string to byte and send it to the server
    try:
        s.sendto(msg, sin)
    except socket.error as e:
        print('Failed to send messages.')
        sys.exit()

    # TODO:
    # 1. receive the acknowledgement from the server
    # 2. convert it from network byte order to host byte order
    try:
        ack, server_addr = s.recvfrom(BUFFER)
    except socket.error as e:
        print('Failed to receive messages.')
        sys.exit()

    ack = int(ack.decode())
    ack = socket.ntohl(ack)

    # TODO: print the acknowledgement to the screen
    print("Acknowledgement: ", ack)

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
    # argument 1 server hostname
    HOSTNAME = sys.argv[1]

    # check hostname and convert to IP address
    try:
        HOST = socket.gethostbyname(HOSTNAME)
    except socket.error as e:
        print("Unknown hostname: %s" % HOSTNAME)
        sys.exit()

    # argument 2 server service port number, convert to integers
    PORT = int(sys.argv[2])

    # build server address data structure
    sin = (HOST, PORT)

    # argument 3 messages, convert to bytes
    msg = sys.argv[3].encode()

    # generate client public key
    c_key = getPubKey()

    # create a socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()

    # send client public key to server
    try:
        s.sendto(c_key, sin)
    except socket.error as e:
        print('Failed to send client public key to server.')
        sys.exit()

    # receive encrypted server public key from server.
    try:
        ect_s_key, svr_addr = s.recvfrom(BUFFER)
    except socket.error as e:
        print('Failed to receive encrypted server public key from server.')
        sys.exit()

    # decrypt server public key
    s_key = decrypt(ect_s_key)

    # calculate client checksum and print to the screen
    c_cksm = checksum(msg)
    print("Checksum sent: ", c_cksm)

    # encrypt message with server public key
    ect_msg = encrypt(msg, s_key)

    # record start time
    start_time = time.time()

    # send encrypted message to server
    try:
        s.sendto(ect_msg, sin)
    except socket.error as e:
        print('Failed to send encrypted message.')
        sys.exit()

    # convert client checksum from host byte order to network byte order
    c_cksm = socket.htonl(c_cksm)

    # convert client checksum from integer to bytes
    c_cksm = str(c_cksm).encode()

    # send client checksum to server
    try:
        s.sendto(c_cksm, sin)
    except socket.error as e:
        print('Failed to send client checksum.')
        sys.exit()

    # receive acknowledgement from server
    try:
        ack, svr_addr = s.recvfrom(BUFFER)
    except socket.error as e:
        print('Failed to receive receive acknowledgement from server.')
        sys.exit()

    # record end time
    end_time = time.time()

    # convert acknowledgement from byte to integer
    ack = int(ack.decode())

    # convert acknowledgement from network byte order to host byte order
    ack = socket.ntohl(ack)

    if ack == 1:

        # calculate round trip time
        rtt = int(round((end_time - start_time) * 1000000))

        # print successful acknowledgemet and rtt
        print("Server has successfully received the message.")
        print('RTT:', '{} {}s'.format(int(round((end_time - start_time) * 1000000)), chr(181)))

    else:

        # report error
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
    # Your program will go with function part1() if there is no command line input.
    # Otherwise, it will go with function part2() to handle the command line input
    # as specified in the assignment instruction.
    if len(sys.argv) == 1:
        part1()
    elif len(sys.argv) == 4:
        part2()
    else:
        print('wrong number of command line arguments, please try again')
