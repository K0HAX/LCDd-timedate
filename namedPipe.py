#!/usr/bin/env python3
import os
import signal
import errno
import time
import asyncio
import aiofiles

from lcdproc.server import Server, Screen

class lcdLine:
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.widget.set_text(text)

    def __init__(self, screen, name, x, y):
        self.screen = screen
        self.widget = self.screen.add_string_widget(name, text="", x=x, y=y)


class manager:
    loop = None

    async def readPipe(self, fifoName, lcdLine):
        try:
            os.mkfifo(fifoName)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        async with aiofiles.open(fifoName) as fifo:
            while True:
                data = await fifo.read()
                data = data.strip()
                if len(data) == 0:
                    await asyncio.sleep(0.1)
                    continue
                print(f"{fifoName}: \"{data}\"")
                lcdLine.text = data

    def handler(self, signum, frame):
        print("Cleaning up!")
        os.unlink("fifoOne")
        os.unlink("fifoTwo")
        print("Exiting now!")
        self.loop.stop()

    def run(self):
        line1_widget = lcdLine(screen1, "Line1Widget", x=1, y=1)
        line2_widget = lcdLine(screen1, "Line2Widget", x=1, y=2)
        self.loop.create_task(self.readPipe("1.fifo", line1_widget))
        self.loop.create_task(self.readPipe("2.fifo", line2_widget))
        self.loop.run_forever()

    def __init__(self, screen):
        self.screen = screen
        signal.signal(signal.SIGINT, self.handler)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

if __name__ == "__main__":
    lcd = Server("127.0.0.1", debug=False)
    lcd.start_session()
    screen1 = lcd.add_screen("Screen1")
    screen1.set_heartbeat("off")
    screen1.set_duration(10)
    screen1.set_height(2)
    screen1.set_width(20)
    myManager = manager(screen1)
    myManager.run()

