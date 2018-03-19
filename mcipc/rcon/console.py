"""An interactive console."""

from mcipc.rcon.client import Client

__all__ = ['rconcmd']


PS1 = 'RCON> '
EXIT_COMMANDS = ('exit', 'quit')


def _read(prompt, type_=None, none=False):
    """Reads a string."""

    while True:
        try:
            raw = input(prompt)
        except EOFError:
            if none:
                return None

            continue

        if type_ is not None:
            try:
                return type_(raw)
            except (TypeError, ValueError):
                print(f'Invalid {type_}: {raw}.')
                continue

        return raw


def _login(client, passwd):
    """Performs a login."""

    while not client.login(passwd):
        print('Invalid password.')
        passwd = getpass('Password: ')

    return passwd


def rconcmd(host=None, port=None, passwd=None, *, prompt=PS1):
    """Initializes the console."""
    
    if host is None:
        try:
            host = _read('Host: ')
        except KeyboardInterrupt:
            print('\Aborted...')

    if port is None:
        try:
            port = _read('Port: ', type_=int)
        except KeyboardInterrupt:
            print('\Aborted...')

    with Client(host, port) as client:
        try:
            passwd = _login(client, passwd)
        except (EOFError, KeyboardInterrupt):
            print('\nAborted...')
            return 1

        while True:
            try:
                command = input(prompt)
            except EOFError:
                break
            except KeyboardInterrupt:
                print()
                continue

            command, *args = command.split()

            if command in EXIT_COMMANDS:
                break

            try:
                result = client.run(command, *args)
            except RequestIdMismatchError:
                print('Session timed out. Please login again.')

                try:
                    passwd = _login(client, passwd)
                except (EOFError, KeyboardInterrupt):
                    print()
                    continue