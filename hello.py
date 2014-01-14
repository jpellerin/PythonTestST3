import os
import re
import sublime, sublime_plugin


TEST_FUNC_RE = re.compile(r'(\s*)def\s+(test_\w+)\s?\(')
TEST_CASE_RE = re.compile(r'(\s*)class\s+(\w+)')


class ExampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "Hello, World!")


class RunPythonTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        command, wdir = self.get_test_command()
        #self.view.insert(edit, 0, command)
        print(command)
        print(wdir)
        # turn on language/theme for output panel somehow
        self.view.window().run_command("exec", {"cmd": [command],
                                                "shell": True,
                                                "working_dir": wdir})
        # find files in output and make them open file links
        # somehow...

    def get_test_command(self):
        settings = self.view.window().active_view().settings().get(
            "python_test") or {}
        command = [settings.get('command', 'nose2')]
        wdir = settings.get('working_dir', self.view.window().folders()[0])
        for testname in self.get_test_selections(wdir):
            command.append(testname)
        return ' '.join(command), wdir

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
