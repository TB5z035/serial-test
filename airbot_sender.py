import asyncio
import airbot
import websockets
import argparse
import time
import pickle

async def main(args):
    robot = airbot.create_agent(can_interface=args.master)
    uri = f"ws://{args.host}:{args.port}"
    async with websockets.connect(uri) as websocket:
        while True:
            print(robot.get_current_joint_q())
            time.sleep(0.0005)
            await websocket.send(pickle.dumps(robot.get_current_joint_q()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send data to the airbot')
    parser.add_argument("-m", "--master", help="Sender CAN Interface", default='can0')
    parser.add_argument("-H", "--host", default='0.0.0.0')
    parser.add_argument("-p", "--port", help="Serial port", default='18188')
    parser.add_argument("-b", "--baudrate", help="Serial baudrate", default=9600)
    args = parser.parse_args()
    asyncio.run(main(args))