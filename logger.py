import sys
import logging


class Style:
    '''
    ANSI character codes to printing colors to terminals.
    See: http://en.wikipedia.org/wiki/ANSI_escape_code
    '''

    RESET_ALL = '\x1b[0m'
    BRIGHT = '\x1b[1m'
    DIM = '\x1b[2m'
    NORMAL = '\x1b[22m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'


class Fore:
    '''
    ANSI character codes to printing colors to terminals.
    See: http://en.wikipedia.org/wiki/ANSI_escape_code
    '''

    BLACK = '\x1b[30m'
    BLUE = '\x1b[34m'
    CYAN = '\x1b[36m'
    GREEN = '\x1b[32m'
    LIGHTBLACK_EX = '\x1b[90m'
    LIGHTBLUE_EX = '\x1b[94m'
    LIGHTCYAN_EX = '\x1b[96m'
    LIGHTGREEN_EX = '\x1b[92m'
    LIGHTMAGENTA_EX = '\x1b[95m'
    LIGHTRED_EX = '\x1b[91m'
    LIGHTWHITE_EX = '\x1b[97m'
    LIGHTYELLOW_EX = '\x1b[93m'
    MAGENTA = '\x1b[35m'
    RED = '\x1b[31m'
    RESET = '\x1b[39m'
    WHITE = '\x1b[37m'
    YELLOW = '\x1b[33m'


LEVEL_COLORS = {
    'DEBUG': Fore.BLUE,
    'DEBUGII': Fore.LIGHTBLUE_EX,
    'INFO': Fore.GREEN,
    'DELIMITER': Style.BRIGHT + Fore.LIGHTGREEN_EX,
    'TOPIC': Style.BRIGHT + Style.BOLD + Fore.MAGENTA,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
    'CRITICAL': Fore.RED,
}


class ConsoleOutputLogFormatter(logging.Formatter):
    """
    Conditional LogFormater based on Log message level.
    """

    def template(self, record):
        """
        Return the prefix for the log message. Template for Formatter.

        Parameters
        ----------
        :py:class:`logging.LogRecord` :
            object. this is passed in from inside the
            :py:meth:`logging.Formatter.format` record.

        Returns
        -------
        str
            template for logger message
        """

        def _log_format_onecolor(record):
            """
            Normal console output format
            """

            return LEVEL_COLORS.get(record.levelname)

        def _log_format_notset(record, stylized=True):
            """
            Default log format.
            """

            reset = Style.RESET_ALL

            levelname = {
                'style_before': LEVEL_COLORS.get(record.levelname) + Style.BRIGHT,
                'format': '(%(levelname)s)',
                'style_after': reset,
                'prefix': '',
                'suffix': '',
            }

            name = {
                'style_before': Fore.WHITE + Style.DIM + Style.BRIGHT,
                'format': '%(name)s',
                'style_after': Fore.RESET + Style.RESET_ALL,
                'prefix': ' ',
                'suffix': ' ',
            }

            # format prefix + style_before + message + style_after + suffix
            result = reset
            for i in [levelname, name]:
                result += f"{i['prefix']}{i['style_before']}{i['format']}{i['style_after']}{i['suffix']}"
            result += reset

            return result

        # Template Switcher
        templates = {
            'NOTSET': _log_format_notset,
            'INFO': _log_format_onecolor,
            'DELIMITER': _log_format_onecolor,
            'TOPIC': _log_format_onecolor,
            'WARNING': _log_format_onecolor,
        }

        return templates.get(record.levelname, _log_format_notset)(record)

    def __init__(self, color=True, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record):
        """
        Format Log Message.

        Parameters
        ----------
        :py:class:`logging.LogRecord` :
            object. this is passed in from inside the
            :py:meth:`logging.Formatter.format` record.

        Returns
        -------
        str
            Formated log message.
        """
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        prefix = self.template(record) % record.__dict__

        parts = prefix.split(record.message)
        formatted = prefix + " " + record.message

        # If multiline message, add prefix to each line.
        return formatted.replace("\n", "\n" + parts[0] + " ") + Style.RESET_ALL


def init_logging(debug_lvl=0):
    """
    Logging init.
    """

    # New logging functions
    def topic(self, msg, *args, **kwargs):
        if self.isEnabledFor(TOPIC):
            self._log(TOPIC, msg, args, **kwargs)

    def delimiter(self, msg, *args, **kwargs):
        if self.isEnabledFor(DELIMITER):
            self._log(DELIMITER, msg, args, **kwargs)

    def debugii(self, msg, *args, **kwargs):
        if self.isEnabledFor(DEBUGII):
            self._log(DEBUGII, msg, args, **kwargs)

    # Define custom log levels
    TOPIC = 25
    DELIMITER = 23
    DEBUGII = 15

    # "Register" new loggin levels
    logging.addLevelName(TOPIC, 'TOPIC')
    logging.addLevelName(DELIMITER, 'DELIMITER')
    logging.addLevelName(DEBUGII, 'DEBUGII')

    # "Register" new logging functions
    logging.Logger.topic = topic
    logging.Logger.delimiter = delimiter
    logging.Logger.debugii = debugii

    debug_levels = {
        0: logging.INFO,
        1: 15,               # Something between INFO and DEBUG
        2: logging.DEBUG
    }

    # Prepare Console handler.
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(ConsoleOutputLogFormatter())

    logging.basicConfig(
        level=debug_levels[min(debug_lvl, 2)],
        format='%(message)s',
        handlers=[console_handler]
    )
