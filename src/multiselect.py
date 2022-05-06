""" Python MultiSelect UI for Windows Terminal

Simple multiselect UI for Windows Terminal in single file, without depending
on any external package.

.. author:: SpringMaple <springmaple@live.com.my>
"""
import msvcrt


class _MultiSelect:
    def __init__(self, options, selected_indexes):
        self.options = options
        self.current_index = 0
        self.selected_indexes = set(selected_indexes or [])
        self.newlines_count = 0

    def display_options(self):
        self.newlines_count = 0
        print('')
        print('Controls: [UP/DOWN] move | [SPACE] de/select | [ENTER] apply | [CTRL-C/ESC] cancel')
        print('')
        self.newlines_count += 3
        for index, option in enumerate(self.options):
            print('=>', end=' ') if self.current_index == index else print('  ', end=' ')
            print('[X]', end=' ') if index in self.selected_indexes else print('[ ]', end=' ')
            print(option)
            self.newlines_count += 1
        print('', end='', flush=True)

    def move_current_index(self, step):
        self.current_index += step
        self.current_index %= len(self.options)

    def toggle_current_index_selection(self):
        if self.current_index in self.selected_indexes:
            self.selected_indexes.remove(self.current_index)
        else:
            self.selected_indexes.add(self.current_index)

    def get_selected_indexes(self):
        return list(sorted(self.selected_indexes))

    def clear_screen(self):
        # https://stackoverflow.com/a/50560686/1640033
        # https://sites.ecse.rpi.edu//courses/CStudio/Old%20MPS%20Labs/MPS_ANSI_Lab_Ex2.pdf
        print(f"\033[{self.newlines_count}A\033[J", end="", flush=True)


class MultiSelectCancelled(Exception):
    def __init__(self):
        """Raised when user cancelled selection process"""


def multiselect(options, selected_indexes):
    """
    :param options - List of option strings.
    :param selected_indexes - List of initial selected indexes.
    :return: List of selected indexes.
    :except MultiSelectCancelled - Raised when user cancelled the selection process.

    e.g.
    selected_indexes = multiselect(['Option1', 'Option2'], [0])
    print(selected_indexes)
    """

    def _wait_key():
        ch = msvcrt.getch()
        # https://docs.python.org/3/library/msvcrt.html#msvcrt.getch
        if ch in (b'\xe0', b'\000'):
            return ch + msvcrt.getch()
        return ch

    _keys = {
        'UP': b'\xe0H',
        'DOWN': b'\xe0P',
        'ESC': b'\x1b',
        'CTRL-C': b'\x03',
        'ENTER': b'\r',
        'SPACE': b' '
    }

    m = _MultiSelect(options, selected_indexes)
    while True:
        m.display_options()
        key = _wait_key()
        m.clear_screen()
        if key == _keys['UP']:
            m.move_current_index(-1)
        elif key == _keys['DOWN']:
            m.move_current_index(1)
        elif key == _keys['SPACE']:
            m.toggle_current_index_selection()
        elif key == _keys['ENTER']:
            return m.get_selected_indexes()
        elif key in (_keys['ESC'], _keys['CTRL-C']):
            raise MultiSelectCancelled()
