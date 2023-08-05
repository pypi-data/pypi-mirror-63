import time
from pynput import keyboard

DATA = []
OLD_DATA = []
def reset_data():
    global DATA
    global OLD_DATA
    OLD_DATA.append(DATA)
    DATA = []

class Key:
    def __init__(self, name: str):
        self.name = name
        self.times = []
        self.add_new_press()
        self.state = True

    def get_current_time(self):
        return time.time()

    def add_new_press(self):
        self.times.append([self.get_current_time()])

    def add_new_release(self):
        self.times[-1].append(self.get_current_time())

    def __str__(self):
        return 'Key {}: {}.'.format(repr(self.name), self.times)

    def get_name(self):
        return self.name

    def get_attributes(self):
        ret = [self.name]
        for i in self.times:
            ret.append(i[1]-i[0])
        return ret

    def summe(self):
        return sum([i[1]-i[0] for i in self.times]), len(self.times)

def on_press(key):
    global DATA
    if key == keyboard.Key.esc:
        return False
    if key not in [i.get_name() for i in DATA]:
        DATA.append(Key(key))
    else:
        for i in DATA:
            if i.get_name() == key and len(i.times[-1]) == 2:
                i.add_new_press()

def on_release(key):
    global DATA
    if key == keyboard.Key.esc:
        return False
    for i in DATA:
        if key == i.get_name():
            i.add_new_release()

def print_results():
    global DATA
    print('_____________________________________________________________')
    print('|  Key       |  pressed for (seconds)  |  pressed n time(s)  |')
    print('|============+=========================+=====================|')
    for i in DATA:
        summe, n = i.summe()
        print('|  {}       |   {}                  |  {}                  |'.format(i.get_name(),
                                                                                    '{:.2f}'.format(summe),
                                                                                    n))
    if not DATA:
        print('| no key pressed...                                          |')
    print('|------------------------------------------------------------|')

def write_csv(out='output.csv'):
    global DATA
    res = [i.get_attributes() for i in DATA]
    f = open(out, 'w')
    length = 0
    for i in DATA:
        if i.summe()[-1] > length:
            length = i.summe()[-1]
    header = 'key, '
    for i in range(length):
        header += str(i) + ', '
    header += 'sum'
    print(header, file=f)
    for i in res:
        line = ''
        sum = 0
        for e in range(length+1):
            try:
                line += str(i[e]) + ', '
            except IndexError:
                line += ', '
            try:
                sum += i[e]
            except (TypeError, IndexError):
                sum = sum
        line += str(sum)
        print(line, file=f)
    f.close()

def run_interactive():
    import os

    print('entering interactive mode of Keytime', end='')
    for i in range(20):
        time.sleep(0.1)
        print('. ', end='')
    print('\n')
    while True:
        csv = input('Would you like to save collected data in a csv file? (y, n) ')
        if csv == 'y' or csv == 'n':
            print()
            break
        else:
            print()
            print('Invalid input.')
            continue
    if csv == 'y':
        while True:
            csv = input('Please enter full path for csv (default: {}): '.format(os.getcwd()))
            if os.path.exists(csv):
                print()
                csv = os.path.join(csv, 'output.csv')
                print('Saving csv at {}'.format(csv))
                break
            if csv == '':
                print()
                csv = os.path.join(os.getcwd(), 'output.csv')
                print('Saving csv at default location: {}'.format(csv))
                break
            else:
                print()
                while True:
                    csv = input(
                        'Path does not exist. Would you like to save csv in your current working directory? (y, n) ')
                    if csv == 'y' or csv == 'n':
                        break
                    else:
                        print()
                        print('Invalid input.')
                        continue
                if csv == 'y':
                    a = os.getcwd()
                    csv = os.path.join(a, 'output.csv')
                    print()
                    print('csv will be saved at {}'.format(csv))
                    break
                else:
                    continue
                break
        return csv
    else:
        return None



def run(interactive=False):
    csv = None
    if interactive:
        csv = run_interactive()
    print()
    print('Keytime is now running!')
    print()
    global DATA
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    print_results()
    if csv:
        write_csv(csv)
    reset_data()
    while True:
        print()
        again = input('Would you like to run Keytime again? (y, n) ')
        if again == 'y' or again == 'n' or again == '':
            break
        else:
            continue
    if again == 'n' or again == '':
        print()
        print('Exit Keytime')
        return None
    else:
        run(interactive)

if __name__ == '__main__':
    run()
