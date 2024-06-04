import airbot
import argparse
import pickle
import functools
import asyncio
import websockets

async def handler(robot, args, websocket):
    await websocket.send("Welcome to the WebSocket server!")
    async for message in websocket:
        try:
            joints = pickle.loads(message)
            print(joints)
            robot.set_target_joint_mit(joints, [0,0,0,0,0,0], [100,100,100,10,10,10], [1,1,1,0.2,0.2,0.2])
        except Exception as e:
            print(e)

async def main(args):
    robot = airbot.create_agent(can_interface=args.master, end_mode='gripper')
    f = functools.partial(handler, robot, args)
    async with websockets.serve(f, args.host, int(args.port)):
        await asyncio.Future()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send data to the airbot')
    parser.add_argument("-m", "--master", help="Sender CAN Interface", default='can0')
    parser.add_argument("-H", "--host", default='0.0.0.0')
    parser.add_argument("-p", "--port", help="Serial port", default='18188')
    parser.add_argument("-b", "--baudrate", help="Serial baudrate", default=9600)
    args = parser.parse_args()
    asyncio.run(main(args))
