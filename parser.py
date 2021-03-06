"""
Python version: 2.7

To make this file work, following lib should be installed:
- websocket (https://pypi.python.org/pypi/websocket-client/)

"""

import websocket
import thread
import time
import json
import datetime


def on_message(ws, message):
    """ Function, that creates file and writes proper message to it.
    Also, all corrupted responses will be saved to 'error.txt'.

    List of available options (e.g. : "....format(edited['roll']"):

    ["win"] - win or lose (boolean)
    ["did"] - Game ID
    ["time"] - Time (Unix Timestamp)
    ["nick"] - User Nickname
    ["imgid"] - Coin icon
    ["cur"] - Currency
    ["bet"] - Bet value
    ["tar"] - <49 or >51
    ["roll"] - Value of "tar"
    ["pr"] - Prize

    """

    file_to_write = open('data.txt', 'a')
    error_log = open('error.txt', 'a')
    try:
        edited = json.loads(json.loads(message)['data'])
        file_to_write.write('Roll is {} \n'.format(edited['roll']))
        print 'Roll is {}'.format(edited['roll'])
    except:
        print "OOOPS! Wrong JSON: {}".format(message)
        error_log.write("{}   {}, \n".format(datetime.datetime.now(), message))
        pass


def on_error(ws, error):
    print 'Something went wrong: {}'.format(error)


def on_close(ws):
    print "### closed ###"


def on_open(ws):
    """ Function that authorizes to WS and creates thread """

    def run(*args):
        ws.send('{"event":"pusher:subscribe","data":{"channel":"chat_ru"}}')
        ws.send('{"event":"pusher:subscribe","data":{"channel":"dice"}}')
        while True:
            time.sleep(1)
        print "thread terminating..."
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    appId = "wss://ws.pusherapp.com/app/7e8fd1da535c087cc7f0"
    ws = websocket.WebSocketApp(appId,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()
