import os
from plugin_helpers.utils import memoize

class TestCommand(object):
  def __init__(self, context):
    self.context = context

  def result(self):
    if not self.context: return

    return ' '.join([
      self._elixir(),
      self._mix(),
      'local.hex',
      '--force',
      '&&',
      self._elixir(),
      self._mix(),
      'test'
    ])

  @memoize
  def _elixir(self):
    if self.context.from_settings("check_for_kiex"):
      return os.path.join(self.context.from_settings("paths_kiex"), "elixir")
    else:
      return os.path.join(self.context.from_settings("paths_system"), "elixir")

  @memoize
  def _mix(self):
    if self.context.from_settings("check_for_kiex"):
      return os.path.join(self.context.from_settings("paths_kiex"), "mix")
    else:
      return os.path.join(self.context.from_settings("paths_system"), "mix")

