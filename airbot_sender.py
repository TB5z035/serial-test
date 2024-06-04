import asyncio
import airbot
import websockets
import argparse
import time
import pickle

async def main(args):
    robot_left = airbot.create_agent(can_interface=args.left)
    robot_right = airbot.create_agent(can_interface=args.right)
    uri = f"ws://{args.host}:{args.port}"
    async with websockets.connect(uri) as websocket:
        while True:
            time.sleep(0.0005)
            await websocket.send(pickle.dumps({
                'left': robot_left.get_current_joint_q(),
                'right': robot_right.get_current_joint_q(),
                'left_end': robot_left.get_current_end(),
                'right_end': robot_right.get_current_end(),
            }))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send data to the airbot')
    parser.add_argument("-l", "--left", help="Sender CAN Interface", default='can0')
    parser.add_argument("-r", "--right", help="Sender CAN Interface", default='can1')
    parser.add_argument("-H", "--host", default='0.0.0.0')
    parser.add_argument("-p", "--port", help="Serial port", default='18188')
    parser.add_argument("-b", "--baudrate", help="Serial baudrate", default=9600)
    args = parser.parse_args()
    asyncio.run(main(args))