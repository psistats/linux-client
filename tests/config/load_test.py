import unittest
import os
import mock
from psistats import config
from psistats.exceptions import PsistatsException
from psistats.exceptions import FileNotFoundException
import platform
import shutil

class ConfigTest(unittest.TestCase):

    TMP_DIR = os.path.dirname(os.path.realpath(__file__)) + "/tmp"
    

    def setUp(self):
        if os.path.exists(self.TMP_DIR):
            shutil.rmtree(self.TMP_DIR)
        os.makedirs(self.TMP_DIR)

    def tearDown(self):
        if os.path.exists(self.TMP_DIR):
            shutil.rmtree(self.TMP_DIR)

    def test_get_config(self):
        self.assertRaises(FileNotFoundException, config.get_config, 'lskdhglskdghsldghlsdghsldghdslhgdlhgdlsdhgdslhgk.txt')

        mocker = mock.patch.object(config.platform, 'system', return_value='foobar')
        mocker.start()
        self.assertRaises(PsistatsException, config.get_config)
        mocker.stop()

    @mock.patch.object(config.os.path, 'expanduser', return_value = "HOME")
    def test_get_homedir_config_file(self, mock_expanduser):
        self.assertEqual(config.get_homedir_config_file(), "HOME/.psistats/psistats.conf")

    def test_get_linux_config_file(self):
        
        """
        Test when psistats.conf is in the current working directory
        """
        f = open(self.TMP_DIR + "/psistats.conf", "w")
        f.write(" ")
        f.close()

        mock_getcwd = mock.patch.object(config.os, 'getcwd', return_value = self.TMP_DIR)
        mock_getcwd.start()
        self.assertEqual(config.get_linux_config_file(), self.TMP_DIR + "/psistats.conf")

        os.remove(self.TMP_DIR + "/psistats.conf")


        """
        Test when psistats.conf is in $HOME/.psistats/psistats.conf
        """
        os.makedirs(self.TMP_DIR + "/.psistats")

        f = open(self.TMP_DIR + "/.psistats/psistats.conf", "w")
        f.write(" ")
        f.close()
        mock_os_path = mock.patch.object(config.os.path, 'expanduser', return_value = self.TMP_DIR)
        mock_os_path.start()

        self.assertEqual(config.get_linux_config_file(), self.TMP_DIR + "/.psistats/psistats.conf")
        
        os.remove(self.TMP_DIR + "/.psistats/psistats.conf")
        
        """
        Test when psistats.conf is in /etc/psistats.conf
        """
        def isfile_sideeffect(*args):
            if args[0] == "/etc/psistats.conf":
                return True
            else:
                return False

        mock_os_isfile = mock.patch.object(config.os.path, 'isfile', side_effect=isfile_sideeffect)
        mock_os_isfile.start()
        self.assertEqual(config.get_linux_config_file(), "/etc/psistats.conf")
        mock_os_isfile.stop()

        

        """
        get_linux_config_file should throw a FileNotFoundException when it can't find a file
        """
        mock_os_isfile = mock.patch.object(config.os.path, 'isfile', return_value=False)
        mock_os_isfile.start()
        self.assertRaises(FileNotFoundException, config.get_linux_config_file)
        mock_os_isfile.stop()

