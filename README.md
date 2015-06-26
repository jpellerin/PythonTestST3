PythonTest
==========

Sublime Text 3 package for running python unit tests.

**This first release only comes with built-in support for nose2.**

The output coloring is based on the theme and language files from
https://github.com/lyapun/sublime-text-2-python-test-runner

Installation
------------

This plugin can be installed using package control, or manually. To install manually, clone this repository inside of your sublime packages directory.

Usage
-----

PythonTest runs python tests and shows the output in an output panel. In the panel, filenames in tracebacks are highlighted, and you can double-click them to go to the file and line mentioned.

Tests may be run individually or in groups.

To run individual tests, in a python unit test module, put a caret in some tests and press <kbd>Ctrl</kbd>-<kbd>c</kbd>,<kbd>.</kbd> to run them. Every test method (or test function) containing a caret point will be run, and only those.

To run all of the tests in a module, ensure the caret is outside of any test method or function and press <kbd>Ctrl</kbd>-<kbd>c</kbd>,<kbd>.</kbd>

To run all of the tests in a project, press <kbd>Ctrl</kbd>-<kbd>c</kbd>,<kbd>t</kbd> while viewing any python source file.

Settings
--------

In the global section of a project file, PythonTest respects the `python_interpreter` setting and will use the interpreter path set there to construct command paths when given a relative command path (see below for how to change that).

You can customize the plugin's behavior by adding a `python_test` section to a project file. In that section, the following settings may be specified:

* `command`: "nose2" (default) or the name of or path to a test comman. The test command is executed in a shell, so it may include arguments, for instance `python ./manage.py test` is a valid `command` setting.

* `ignore_interpreter`: False (default). Set to True to ignore the `python_interpreter`
 setting.

* `working_dir`: project root (default) or the path to the directory where test commands should be executed

* `quiet`: True (default) to hide test command details in output

* `color_scheme`: "light" (default) or "dark" or a `.tmTheme` or `.hidden-tmTheme` filename

* `syntax`: "unittest" (default) or Specify a `.tmLanguage` file to set the syntax highlighting language for test output

### Project settings example

```json
{
    "folders":[
        {
            "path":"/home/my_user/my_project/"
        }
    ],
    "settings":{
        "python_test":{
            "command":"python ./manage.py test"
        }
    }
}
```