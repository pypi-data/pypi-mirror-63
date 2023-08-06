from chibi_command import Command
from chibi_hybrid.chibi_hybrid import Chibi_hybrid


class Mount( Command ):
    command = 'mount'
    captive = True


class Umount( Command ):
    command = 'umount'
    captive = True
