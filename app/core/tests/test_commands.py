from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""

        # use patch to mock the connection handler to just return True
        # everytime its called
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            # call our management command
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # we're mocking the time.sleep to just return True.
    # and pass that mock function into test_wait_function_for_db
    # as an argument.
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # mock OperationalError for 5 times, and the 6th time
            # it will return true
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
