from io import StringIO
from django.core.management import call_command
from django.test import TestCase

class TestTodo(TestCase):
    def test_category_list(self):
        response = self.client.get('/category/')
        self.assertEquals(response.status_code, 200)

    def test_tasks_redirect(self):
        response = self.client.get('/category/1')
        self.assertEquals(response.status_code, 301)


class HideTaskTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('hide_task', stdout=out)
        self.assertIn('Expected output', out.getvalue())