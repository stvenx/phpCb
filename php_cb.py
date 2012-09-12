import sublime, sublime_plugin, re, subprocess,os,sys
from subprocess import Popen
from subprocess import PIPE
built_in_plugins = os.path.join(sublime.packages_path(), 'PhpCb')
if not built_in_plugins in sys.path:
    sys.path.append(built_in_plugins)
class PhpCbCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        FILE = self.view.file_name()
        path=sublime.packages_path()+'\\PhpCb'
        if FILE[-3:] == 'php':
            allFile = sublime.Region(0, self.view.size())
            AllFileText = self.view.substr(allFile).encode('utf-8')
            tmpFile=path+"\\temp.php"
            tfp=open(tmpFile,"w");
            tfp.writelines(AllFileText)
            tfp.close()
            cmd="phpcb.exe"+" --space-after-if --optimize-eol --space-after-switch --space-after-while --space-before-start-angle-bracket --space-after-end-angle-bracket --extra-padding-for-case-statement  --align-equal-statements --force-large-php-code-tag --glue-amperscore --change-shell-comment-to-double-slashes-comment --indent-with-tab --force-large-php-code-tag --force-true-false-null-contant-lowercase --comment-rendering-style PEAR --padding-char-count 1 "+'"'+tmpFile+'"'
            p=Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
            stdout, stderr = p.communicate(AllFileText)
            #os.remove(tmpFile)
            if len(stderr) == 0:
                self.view.replace(edit, allFile, self.fixup(stdout))
            else:
                self.show_error_panel(self.fixup(stderr))

    # Error panel & fixup from external command
    # https://github.com/technocoreai/SublimeExternalCommand
    def show_error_panel(self, stderr):
        panel = self.view.window().get_output_panel("php_code_beautifier_errors")
        panel.set_read_only(False)
        edit = panel.begin_edit()
        panel.erase(edit, sublime.Region(0, panel.size()))
        panel.insert(edit, panel.size(), stderr)
        panel.set_read_only(True)
        self.view.window().run_command("show_panel", {"panel": "output.php_code_beautifier_errors"})
        panel.end_edit(edit)

    def fixup(self, string):
        return string.decode('utf-8')
        return re.sub(r'\r\n|\r', '\n', string.decode('utf-8'))
