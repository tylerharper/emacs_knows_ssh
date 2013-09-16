#!/usr/bin/env python2
import sys
import os
import pty
import tty
import re
import select
from StringIO import StringIO
input_line = re.compile(r"\$ ?$")

pid, child_fd = pty.fork()

if pid == 0:
    # self.child_fd = sys.stdout.fileno() # used by setwinsize()
    # self.setwinsize(24, 80)
    # # Do not allow child to inherit open file descriptors from parent.
    # max_fd = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
    # for i in range (3, max_fd):
    #     try:
    #         os.close (i)
    #     except OSError:
    #         pass
    program_name = '/usr/bin/ssh'
    os.execv(program_name, [program_name] + sys.argv[1:])

mode = tty.tcgetattr(pty.STDIN_FILENO)
tty.setraw(pty.STDIN_FILENO)
first_time = True
child_buffer = StringIO()

while True:
    try:
        r, w, e = select.select([child_fd, pty.STDIN_FILENO], [child_fd], [])
        if child_fd in r:
            child_buffer.write(os.read(child_fd, 1000))
            #os.write(pty.STDOUT_FILENO, os.read(child_fd, 1000))
        if pty.STDIN_FILENO in r:
            os.write(child_fd, os.read(pty.STDIN_FILENO, 1000))
        if child_fd in w and child_buffer.getvalue().endswith("$ ") and first_time:
            os.write(child_fd, "function foo () { echo foo; };\r")
            first_time = False

        if (child_fd in r and not first_time) or (child_fd in w and not child_buffer.getvalue().endswith("$ ")):
            os.write(pty.STDOUT_FILENO, child_buffer.getvalue())
            child_buffer.seek(0,0)
            child_buffer.truncate()
    except OSError:
        break

tty.tcsetattr(pty.STDIN_FILENO, tty.TCSAFLUSH, mode)



#     line = read_stdout()
#     while not input_line.match(line):
#         print line
#         line = read_stdout()
#         except_stdin()

#     append_functions
#     give_user_back_stdout_stdin_and_stde
