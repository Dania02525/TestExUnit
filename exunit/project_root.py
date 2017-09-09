import os

# shamelessly ripped off from: https://github.com/astrauka/TestRSpec/blob/master/rspec/project_root.py

class ProjectRoot(object):
  def __init__(self, file_name, test_folder_name):
    self.file_name = file_name
    self.test_folder_name = test_folder_name

  def result(self):
    if not self.file_name: return
    if not self.test_folder_name: return

    return self._via_inclusion() or self._via_upwards_search()

  def _via_inclusion(self):
    wrapped_folder_name = "/{0}/".format(self.test_folder_name)
    if not wrapped_folder_name in self.file_name: return

    return self.file_name[:self.file_name.rindex(wrapped_folder_name)]

  def _via_upwards_search(self):
    path = self.file_name

    while True:
      (path, current_dir_name) = os.path.split(path)
      if not current_dir_name: return
      if self.spec_folder_name in os.listdir(path): return path
