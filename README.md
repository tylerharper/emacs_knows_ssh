# Problem #

I want to be able to run `edit` on a remote machine and have the file open in my local emacs.  This includes hopping around to different boxes

# Solutions #

## Wrap ssh ##

Only works with ad-hoc multi hops TRAMP introduced in <TRAMP VERSION
FOR AD-HOC MULTI HOPS>.  This version of TRAMP was included in <SOME
EMACS VERSION>.

This allows you to open a terminal and jump around to different ssh
hosts.  When on a machine you can use the edit it command and it will
open that file in your emacs.

    (localmachine)$ ssh some_host
	   (some_host)$ edit some_file # your local emacs will open that file for editing

This setup will also allow you to multihop if you have to.

	(localmachine)$ ssh some_host
	   (some_host)$ ssh some_other_host
	   (some_other_host)$ edit some_file # your local emacs will open that file for editing

### How the magic is supposed to work ###

We overwrite the ssh command with a function.  The function uses the
regular ssh command piping its output to `tee`.  The function will
also write an `edit` bash function on the other machine.  It may copy
the recently created `ssh` function over as well.  The `ssh`
executable must be a bash function so we can copy it around to other
machines.  It could may instiate python with the -c options in the ssh bash function.

The `edit` function will generate some string that outputs the
location of the file that TRAMP can understand.

There will be some `server` watching the ssh output file to look for a file to open.

So three parts:

* ssh function
* edit function
* file watcher and opener

### Thing required ###

* Bash on all accessed machines on login.

### Problems with functions ###

Most applications like ipython can not use a function since they are not bash.  They are executing a file.

## rmate and rsub like thing ##

An executable living on the remote server.  This doesn't really allow
for multiple hops unless you provide a mechanism to copy the file to
the remote machine always.
[rsub](https://github.com/Drarok/rsub/blob/master/rsub.py)

[rmate](https://github.com/aurora/rmate/blob/master/rmate)
