import os
import re
import sublime
import sublime_plugin


SYNTAX = {'unittest': 'Packages/PythonTest/PythonTestOutput.tmLanguage'}
SCHEME = {'light': 'Packages/PythonTest/PythonTestOutput.hidden-tmTheme',
          'dark': 'Packages/PythonTest/PythonTestOutputDark.hidden-tmTheme'}
TEST_FUNC_RE = re.compile(r'(\s*)def\s+(test_\w+)\s?\(')
TEST_CASE_RE = re.compile(r'(\s*)class\s+(\w+)')
TB_FILE = r'[ ]*File \"(...*?)\", line ([0-9]*)'


class RunPythonTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = self.view.window().active_view().settings().get(
            "python_test", {})
        command, wdir = self.get_test_command(settings)
        # turn on language/theme for output panel somehow
        panel = self.view.window().create_output_panel('exec')
        panel.settings().set('color_scheme', self.color_scheme(settings))
        self.view.window().run_command(
            "exec", {"cmd": [command],
                     "file_regex": TB_FILE,
                     "shell": True,
                     "quiet": settings.get('quiet', True),
                     "syntax": self.syntax(settings),
                     "working_dir": wdir})

    def get_test_command(self, settings):
        command = [self.executable(settings)]
        for opt in self.get_test_options(settings):
            command.append(opt)
        wdir = settings.get('working_dir', self.view.window().folders()[0])
        for testname in self.get_test_selections(wdir):
            command.append(testname)
        return ' '.join(command), wdir

    def get_test_options(self, settings):
        return settings.get('options', [])

    def get_test_selections(self, wdir):
        mod = self.file_to_module(wdir, self.view.file_name())
        start = 0
        found = False
        for region in self.view.sel():
            tx = self.view.substr(sublime.Region(start, region.begin()))
            test_name = self.find_test_name(tx, region.begin())
            if test_name:
                yield "%s.%s" % (mod, test_name)
                found = True
        if not found:
            yield mod

    def find_test_name(self, tx, point):
        matches = TEST_FUNC_RE.findall(tx)
        if not matches:
            return
        print(matches)
        indent, funcname = matches[-1]
        if not indent:
            return funcname
        # find the enclosing class
        before = self.view.substr(sublime.Region(0, point))
        print(len(before))
        classes = TEST_CASE_RE.findall(before)
        print(classes)
        if not classes:
            return funcname  # this is probably bad
        candidates = [c for i, c in classes if len(i) < len(indent)]
        print(candidates)
        if candidates:
            return "%s.%s" % (candidates[-1], funcname)
        return funcname  # also probably bad

    def file_to_module(self, wd, fn):
        rel_path = os.path.relpath(fn, wd)
        base, _ = os.path.splitext(rel_path)
        return base.replace(os.path.sep, '.')

    def executable(self, settings):
        # account for virtualenv (check python interp path in settings)
        # if set and command is not a full path, make it abs path rel
        # to dir containing python interp -- have a setting to turn
        # this behavior off
        base = settings.get('command', 'nose2')
        ignore_interp = settings.get('ignore_interpreter', False)
        if ignore_interp:
            return base
        interp = self.view.window().active_view().settings().get(
            "python_interpreter", None)
        if not interp:
            return base
        if os.path.isabs(base):
            return base
        root = os.path.dirname(interp)
        return os.path.join(root, base)

    def color_scheme(self, settings):
        name = settings.get('color_scheme', "light")
        return SCHEME.get(name, name)

    def syntax(self, settings):
        name = settings.get('syntax', "unittest")
        return SYNTAX.get(name, name)


class RunPythonProjectTests(RunPythonTestCommand):
    def get_test_selections(self, settings):
        return []
