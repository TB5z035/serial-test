import airbot
import argparse
import pickle
import functools
import asyncio
import websockets

async def handler(robots, args, websocket):
    robot_left, robot_right = robots
    await websocket.send("Welcome to the WebSocket server!")
    async for message in websocket:
        try:
            info = pickle.loads(message)
            robot_left.set_target_joint_mit(info['left'], [0,0,0,0,0,0], [100,100,100,10,10,10], [1,1,1,0.2,0.2,0.2])
            robot_left.set_target_end(info['left_end'])
            robot_right.set_target_joint_mit(info['right'], [0,0,0,0,0,0], [100,100,100,10,10,10], [1,1,1,0.2,0.2,0.2])
            robot_right.set_target_end(info['right_end'])
        except Exception as e:
            print(e)

async def main(args):
    robot_left = airbot.create_agent(can_interface=args.left, end_mode='gripper')
    robot_right = airbot.create_agent(can_interface=args.right, end_mode='gripper')
    f = functools.partial(handler, (robot_left, robot_right), args)
    async with websockets.serve(f, args.host, int(args.port)):
        await asyncio.Future()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send data to the airbot')
    parser.add_argument("-l", "--left", help="Sender CAN Interface", default='can0')
    parser.add_argument("-r", "--right", help="Sender CAN Interface", default='can1')
    parser.add_argument("-H", "--host", default='0.0.0.0')
    parser.add_argument("-p", "--port", help="Serial port", default='18188')
    parser.add_argument("-b", "--baudrate", help="Serial baudrate", default=9600)
    args = parser.parse_args()
    asyncio.run(main(args))
