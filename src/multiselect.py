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

    def display_options(self):
        print('Controls: [UP/DOWN] move | [SPACE] de/select | [ENTER] apply | [CTRL-C/ESC] cancel')
        print('')
        for index, option in enumerate(self.options):
            print('=>', end=' ') if self.current_index == index else print('  ', end=' ')
            print('[X]', end=' ') if index in self.selected_indexes else print('[ ]', end=' ')
            print(option)
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

    @staticmethod
    def clear_screen():
        # https://stackoverflow.com/a/50560686/1640033
        print("\033[H\033[J", end="")


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
        m.clear_screen()
        m.display_options()
        key = _wait_key()
        if key == _keys['UP']:
            m.move_current_index(-1)
        elif key == _keys['DOWN']:
            m.move_current_index(1)
        elif key == _keys['SPACE']:
            m.toggle_current_index_selection()
        elif key == _keys['ENTER']:
            m.clear_screen()
            return m.get_selected_indexes()
        elif key in (_keys['ESC'], _keys['CTRL-C']):
            m.clear_screen()
            raise MultiSelectCancelled()
