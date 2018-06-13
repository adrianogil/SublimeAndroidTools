import subprocess
import sublime, sublime_plugin

import sys

import codecs

class FilterLogcatErrorsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        current_file = self.view.file_name()

        with codecs.open(current_file, encoding="utf-8-sig", errors='ignore') as f:
            content = f.readlines()

        filtered_content = filter_errors(content)
        scratch_file = self.view.window().new_file()
        scratch_file.set_name('Filtered Logcat - Exceptions')
        scratch_file.set_scratch(True)
        args = {
            'text': filtered_content,
            'line': 0
        }
        scratch_file.run_command('insert_text_on_position', args)
        # scratch_file.set_read_only(True)
        scratch_file.settings().set('word_wrap', False)
        # scratch_file.set_syntax_file("Packages/Diff/Diff.tmLanguage")


class LogcatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        adb_logcat_cmd = "/usr/local/bin/adb shell logcat -d -v time"
        adb_logcat_output = subprocess.check_output(adb_logcat_cmd, shell=True)
        adb_logcat_output = adb_logcat_output.decode('UTF-8')

        scratch_file = self.view.window().new_file()
        scratch_file.set_name('Logcat')
        scratch_file.set_scratch(True)
        args = {
            'text': adb_logcat_output,
            'line': 0
        }
        scratch_file.run_command('insert_text_on_position', args)
        # scratch_file.set_read_only(True)
        scratch_file.settings().set('word_wrap', False)
        # scratch_file.set_syntax_file("Packages/Diff/Diff.tmLanguage")


def filter_errors(lines):
    exception_found = False
    line_number = 1;

    filtered_log = ""

    def is_error(line):
        return line.find("Exception") != -1 or line.find("NullReference") != -1 or \
               line.find("Error") != -1 or line.find("error") != -1 or \
               line.find("ERROR") != -1 or line.find("E/CRASH") != -1

    for line in lines:
      if exception_found and line.find('at ') != -1:
          # filtered_log = filtered_log + "  " + str(line_number) + ": " + line + '\n'
          filtered_log = filtered_log + line
      elif exception_found:
          exception_found = False
    # TODO: parse /E logs
      if is_error(line):
          # filtered_log = filtered_log + "  " + str(line_number) + ": " + line + '\n'
          filtered_log = filtered_log + line
          exception_found = True

      line_number = line_number + 1

    return filtered_log
