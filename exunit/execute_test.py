from plugin_helpers.utils import memoize
from exunit.output import Output
from exunit.test_command import TestCommand

# shamelessly ripped off from: https://github.com/astrauka/TestRSpec/blob/master/rspec/execute_spec.py

class ExecuteTest(object):
  def __init__(self, context):
    self.context = context

  def current(self):
    self._validate_can_run_test()
    self._prepare_output_panel()
    self._execute(self._command_hash())

  def _validate_can_run_test(self):
    if not self.context.project_root(): return self._notify_missing_project_root()
    if not self.context.is_test_file(): return self._notify_not_test_file()

  def _prepare_output_panel(self):
    self.context.log("Error occurred, see more in 'View -> Show Console'")
    self.context.log("Project root {0}".format(self.context.project_root()))
    self.context.log("Test target {0}".format(self.context.test_target()))
    self.context.display_output_panel()

  def _execute(self, command_hash):
    self._before_execute()
    self.context.log("Executing {0}\n".format(command_hash.get("shell_cmd")))
    self.context.window().run_command("exec", command_hash)

  def _before_execute(self):
    self.context.window().run_command("save")

  def _notify_missing_project_root(self):
    self.context.log(
      "Could not find '{0}/' folder traversing back from {1}".format(
        self.context.from_settings("test_folder"),
        self.context.file_name()
      ),
      level=Output.Levels.ERROR
    )
    self.context.display_output_panel()

  def _notify_not_test_file(self):
    self.context.log(
      "Trying to test not a test file: {0}".format(self.context.file_name()),
      level=Output.Levels.ERROR
    )
    self.context.display_output_panel()

  @memoize
  def _command_hash(self):
    add_to_path = self.context.from_settings("test_add_to_path", "")
    append_path = "export PATH={0}:$PATH;".format(add_to_path) if add_to_path else ""

    command = "({append_path} cd {project_root} && {test_command} {target})".format(
      append_path = append_path,
      project_root = self.context.project_root(),
      test_command = TestCommand(self.context).result(),
      target = self.context.test_target()
    )
    pannel_settings = self.context.from_settings("panel_settings", {})
    env = self.context.from_settings("env", {})

    return {
      "shell_cmd": command,
      "working_dir": self.context.project_root(),
      "env": env,
      "file_regex": r"([^ ]*\.exs):?(\d*)",
      "syntax": pannel_settings.get("syntax"),
      "encoding": pannel_settings.get("encoding", "utf-8")
    }
