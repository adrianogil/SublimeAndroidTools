import subprocess
import sublime, sublime_plugin

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