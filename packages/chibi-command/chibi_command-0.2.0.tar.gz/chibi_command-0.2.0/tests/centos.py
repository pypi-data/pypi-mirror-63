from unittest import TestCase

from chibi.atlas import Chibi_atlas
from chibi_command import lxc
from chibi_command.nix import Systemctl
from chibi_command.centos import Iptable


class Test_iptable( TestCase ):
    def test_table( self ):
        result = Iptable.table( 'nat' )
        self.assertEqual(
            "iptable --table nat", result.preview() )

    def test_append( self ):
        result = Iptable.table( 'nat' ).append()
        self.assertEqual(
            "iptable --table nat --append ", result.preview() )

    def test_protocol( self ):
        result = Iptable.table( 'nat' ).append().protocol( 'tcp' )
        self.assertEqual(
            "iptable --table nat --append  --protocol tcp", result.preview() )

    def test_protocol( self ):
        result = Iptable.table( 'nat' ).append().protocol( 'tcp' )
        result.in_interface( 'eth1' )
        self.assertEqual(
            "iptable --table nat --append  --protocol tcp --in-interface eth1",
            result.preview() )

    def test_destination_port( self ):
        result = Iptable.table( 'nat' ).append().protocol( 'tcp' )
        result.in_interface( 'eth1' ).destination_port( 8000 )
        self.assertEqual(
            "iptable --table nat --append  --protocol tcp --in-interface eth1"
            " --destination-port 8000",
            result.preview() )

    def test_jump( self ):
        result = Iptable.table( 'nat' ).append().protocol( 'tcp' )
        result.in_interface( 'eth1' ).destination_port( 8000 ).jump( 'DNAT' )
        self.assertEqual(
            "iptable --table nat --append  --protocol tcp --in-interface eth1"
            " --destination-port 8000 --jump DNAT",
            result.preview() )

    def test_to_destination( self ):
        result = Iptable.table( 'nat' ).append().protocol( 'tcp' )
        result.in_interface( 'eth1' ).destination_port( 8000 ).jump( 'DNAT' )
        result.to_destination( "127.0.0.1", 8000 )
        self.assertEqual(
            "iptable --table nat --append  --protocol tcp --in-interface eth1"
            " --destination-port 8000 --jump DNAT "
            "--to-destination 127.0.0.1:8000",
            result.preview() )

    def test_delete( self ):
        result = Iptable.table( 'nat' ).delete()
        self.assertEqual(
            "iptable --table nat --delete ", result.preview() )
