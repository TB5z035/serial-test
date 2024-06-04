import airbot
from messenger import SerialMessenger
import argparse
import pickle

def send(args):
    sender = SerialMessenger(args.port, args.baudrate)
    robot = airbot.create_agent(can_interface=args.master)
    while True:
        joints = robot.get_current_joint_q()
        sender.send(pickle.dumps(joints) + b'\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send data to the airbot')
    parser.add_argument("-m", "--master", help="Sender CAN Interface", default='can0')
    parser.add_argument("-p", "--port", help="Serial port", default='/dev/ttyUSB0')
    parser.add_argument("-h", "--host", help="Websocket host", default='localhost')
    parser.add_argument("-b", "--baudrate", help="Serial baudrate", default=9600)
    args = parser.parse_args()
    send(args)
    
