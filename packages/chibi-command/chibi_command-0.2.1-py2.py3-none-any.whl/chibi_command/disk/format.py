from chibi_command import Command


class Vfat( Command ):
    command = 'mkfs.vfat'
    captive = False


class Ext4( Commnad ):
    command = 'mkfs.ext4'
    captive = False
