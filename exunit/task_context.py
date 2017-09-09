from plugin_helpers.utils import memoize
from plugin_helpers.project_files import ProjectFiles
from exunit.project_root import ProjectRoot
from exunit.output import Output
import sublime, os

# shamelessly ripped off from https://github.com/astrauka/TestRSpec/blob/master/rspec/task_context.py
class TaskContext(object):
  TEST_FILE_POSTFIX = "_test.exs"

  def __init__(self, sublime_command, edit, test_target_is_file=False):
    self.sublime_command = sublime_command
    self.edit = edit
    self.test_target_is_file = test_target_is_file

  @memoize
  def view(self):
    return self.sublime_command.view

  @memoize
  def file_name(self):
    return self.view().file_name()

  @memoize
  def file_base_name(self):
    return os.path.basename(self.file_name())

  @memoize
  def file_relative_name(self):
    return os.path.relpath(self.file_name(), self.project_root())

  @memoize
  def line_number(self):
    (rowStart, colStart) = self.view().rowcol(self.view().sel()[0].begin())
    (rowEnd, colEnd)     = self.view().rowcol(self.view().sel()[0].end())
    lines = (str) (rowStart + 1)

    if rowStart != rowEnd:
        #multiple selection
        lines += "-" + (str) (rowEnd + 1)

    return lines

  @memoize
  def test_target(self):
    file_relative_name = self.file_relative_name()
    if self.test_target_is_file:
      return file_relative_name
    else:
      return ":".join([file_relative_name, self.line_number()])

  @memoize
  def project_root(self):
    return ProjectRoot(self.file_name(), self.from_settings("test_folder")).result()

  def window(self):
    return self.view().window()

  @memoize
  def output_buffer(self):
    return Output(
      self.view().window(),
      self.edit,
      self.from_settings("panel_settings")
    )

  def output_panel(self):
    return self.output_buffer().panel()

  def log(self, message, level=Output.Levels.INFO):
    self.output_buffer().log("{0}: {1}".format(level, message))

  def display_output_panel(self):
    self.output_buffer().show_panel()

  @memoize
  def _plugin_settings(self):
    return sublime.load_settings("Preferences.sublime-settings")

  @memoize
  def _user_settings(self):
    return sublime.load_settings("TestExUnit.sublime-settings")

  @memoize
  def _view_settings(self):
    return self.view().settings()

  def from_settings(self, key, default_value = None):
    return self._user_settings().get(
      key,
      self._view_settings().get(
        key,
        self._plugin_settings().get(key, default_value)
      )
    )

  def is_test_file(self):
    return self.file_name().endswith(TaskContext.TEST_FILE_POSTFIX)

  def project_files(self, file_matcher):
    return ProjectFiles(
      self.project_root(),
      file_matcher,
      self.from_settings("ignored_directories")
    ).filter()
