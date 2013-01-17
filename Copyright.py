import sublime, sublime_plugin
import string
import getpass
from datetime import datetime

class CopyrightCommand(sublime_plugin.TextCommand):

    def guess_file_class(self):
        syntax = self.view.settings().get('syntax')

        return syntax.split('/')[1]

    def run(self, edit):
        setting = sublime.load_settings("Copyright.sublime-settings")

        file_type = self.guess_file_class()

        copyright_file = ""
        try:
            copyright_file = open(sublime.packages_path() + '/sublime-xinix/' + file_type + '.copyright').read()
        except:
            copyright_file = open(sublime.packages_path() + '/sublime-xinix/Default.copyright').read()

        file_name = self.view.file_name()
        if file_name != None:
            file_name = file_name.split('/')[-1]
        else:
            file_name = "[noname file]"

        now = datetime.now()

        copyright_template = string.Template(copyright_file)
        d = dict(
            file_name=file_name,
            package_name='arch-php',
            my_name=setting.get('name', getpass.getuser()),
            my_email=setting.get('email', getpass.getuser() + '@localhost'),
            year=now.strftime("%Y"),
            now=now.strftime("%Y-%m-%d %H:%M:%S"),
        )

        copyright = copyright_template.substitute(d)

        point = self.view.line(self.view.sel()[0]).begin()
        self.view.insert(edit, point, copyright);

