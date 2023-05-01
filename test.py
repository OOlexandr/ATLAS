from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.completion import WordCompleter

words = ['close', 'exit', 'add record', 'add birthday', 'add phone', 'change', 'phone', 'days to birthday', 'show all']
words1 = ['closeclose', 'exitclose', 'add close', 'add close', 'add phoneclose']

completer = NestedCompleter.from_nested_dict({
    'exit': WordCompleter(words),
    'phone': WordCompleter(words1, match_middle = True),
    'stop': None
})

while True:
    text = prompt('Input command >>> ', completer=completer)
    if text == "stop":
        break