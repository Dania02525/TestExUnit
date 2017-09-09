import sys, os.path, imp, sublime, sublime_plugin

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CODE_DIRS = [
  'plugin_helpers',
  'exunit',
]
sys.path += [BASE_PATH] + [os.path.join(BASE_PATH, f) for f in CODE_DIRS]

from exunit.exunit_print import exunit_print
from exunit.execute_test import ExecuteTest
from exunit.task_context import TaskContext

class TestCurrentFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    exunit_print("Running ExUnit")
    context = TaskContext(self, edit, test_target_is_file = True)
    ExecuteTest(context).current()

class TestCurrentLineCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    exunit_print("Running ExUnit")
    context = TaskContext(self, edit)
    ExecuteTest(context).current()
