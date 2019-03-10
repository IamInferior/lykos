from collections import defaultdict, OrderedDict
WARN_IDLE_TIME=600
PM_WARN_IDLE_TIME=899
KILL_IDLE_TIME=900
MAX_PRIVMSG_TARGETS = 4
HOST = "irc.rizon.net"
PORT = 6697
USE_SSL = True
NICK = "werewolfbot-beta"
IDENT = "werewolfbot-beta"
REALNAME = "werewolfbot-beta"
USERNAME = NICK
PASS = "mafiabotissmart"
SASL_AUTHENTICATION = True

CHANNEL = "##werewolves-beta"

CMD_CHAR = "!"

ENABLE_DEADCHAT = False

# If your server requires a connection password, or your services package expects
# a different format if authenticating to NickServ via the PASS command, modify this.
# The default should work fine on Atheme-based services packages.
#
# Note: Do not put the account and password here; they will be automatically substituted
#       from the USERNAME (or NICK) and PASS variables on the top of the file.

SERVER_PASS = "{account}:{password}"

OWNERS = ("uid57206@*","*@things.to.baron.mind",)  # The comma is required at the end if there is only one owner.
OWNERS_ACCOUNTS = ("SirN","Dubslav",)

ADMINS = ()
ADMINS_ACCOUNTS = ()

RULES = "https://werewolf.chat/Freenode:Rules"

ALLOWED_NORMAL_MODE_COMMANDS = []  # Debug mode commands to be allowed in normal mode
OWNERS_ONLY_COMMANDS = [] # Commands that should only be allowed for owners, regardless of their original permissions

DISABLE_DEBUG_MODE_REAPER = True
DISABLE_DEBUG_MODE_STASIS = True
DISABLE_DEBUG_MODE_TIMERS = True
DISABLE_DEBUG_MODE_TIME_LORD = False

ALT_CHANNELS = ""
ALLOWED_ALT_CHANNELS_COMMANDS = []

DEV_CHANNEL = "##werewolves-beta" # Important: Do *not* include the message prefix!
DEV_PREFIX = "" # The prefix to send to the dev channel (e.g. "+" will send to "+#dev-chan")
PASTEBIN_ERRORS = False  # If DEV_CHANNEL is set, errors will be posted there.

LOG_CHANNEL = "" # Log !fwarns to this channel, if set


IGNORE_HIDDEN_COMMANDS = True  # Ignore commands sent to @#channel or +#channel
ALLOW_NOTICE_COMMANDS = False  # Allow "/notice #channel !command" to be interpreted as a command
ALLOW_PRIVATE_NOTICE_COMMANDS = True  # Allow "/notice botnick command" to be interpreted as a command

CHANGING_HOST_QUIT_MESSAGE = "Changing host"


USE_UTC = True  # If True, logs will use the UTC time, else local time.


# %Y is the year, %m is the month, %d is the day, %H = hour, %M = minute, and %S = seconds.
# {tzname} and {tzoffset} can both be used - the timezone name (like UTC) and offset (+0000), respectively.
TIMESTAMP_FORMAT = "[%Y-%m-%d %H:%M:%S{tzoffset}]"

# you can simply uncomment the following lines. For other networks, you can set the appropriate
# values manually.
#
# Note: Do not put the account and password here; they will be automatically substituted
#       from the USERNAME (or NICK) and PASS variables on the top of the file.

#NICKSERV = "service@rizon.net"
#NICKSERV_IDENTIFY_COMMAND = "IDENTIFY {account} {password}"
#NICKSERV_GHOST_COMMAND = ""
#NICKSERV_RELEASE_COMMAND = ""
#NICKSERV_REGAIN_COMMAND = ""
#CHANSERV = "x@channels.undernet.org"
#CHANSERV_OP_COMMAND = "OP {channel}"

# vim: set ft=python:
