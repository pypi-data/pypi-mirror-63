It's a Live
===========

![](misc/logo.png)

It's a Live is a utility that helps you make live coding demos less error-prone by taking the "live" component and
killing it.

It's a Live lets you write commands and keystrokes in a file, which it will then read and open a new terminal for you.
Every time you press a key, It's a Live will write one character from the file into the terminal, making it look like
you're typing every single command with the practiced ease of a consummate professional.


What it looks like
------------------

This is what it looks like:

![](misc/screenshot.png)

The typing terminal is on the left and the presenter view is on the right.

Here's a screencast of It's a Live in operation. Keep in mind that the presenter is pressing keys randomly after the
program starts:

[![asciicast](https://asciinema.org/a/308560.svg)](https://asciinema.org/a/308560)


Installation
------------

You can install It's a Live with pip:

```
pip install itsalive
```

That's about it.


Usage
-----

Using It's a Live is pretty simple:
Just write some keystrokes or commands in a file and run `itsalive` with it:

```
itsalive <command_file>
```

It's a Live will wait for you to press a key, and, when you do, it will instead emit one character from the command
file. This way, you can type whatever old crap and it will look perfectly rehearsed, every time, with no backspaces
(unless you add them in).  It will also wait for you to press Enter at the end of commands, so you will never skip
ahead to the next command by mistake.

What's more, It's a Live is actually running the commands you're typing, so you have full interoperability with other
programs.

It's a Live also supports various commands:

* `Ctrl+d` will immediately terminate the playback.
* `Ctrl+p` will pause automatic playback and give you control of the terminal. This is useful for doing actually live
  stuff, just make sure to leave everything in a state so that playback can resume later.
* `Ctrl+r` will resume playback.
* `Ctrl+f` will skip forward to the next command.
* `Ctrl+g` will skip back to the previous command.
* `Ctrl+u` will send a `Ctrl+u` keystroke (wiping anything on to the left of the cursor) and rewind the current command.
* `Ctrl+e` will type out the current command in its entirety.


Presenter view
--------------

It's a Live supports a presenter view, which will show the next command to be typed. To launch the presenter view, start
the presentation and run, on a separate terminal:

```
itsalive presenter_view
```

If you want to leave yourself notes, you can add comments to the command file. Comments must start with `##` as the
first thing on the line, and they will not be typed. They will only be shown above the command in the presenter view.


Special commands
----------------

There are special commands you can add to your files. The line must start with them, with no spaces before them.

---

**`##@include <filename>`:** This inserts the contents of `<filename>` at the position of the `include` command. The
file will be typed out, as if you had pasted it in the commands file.

Example: `##@include somefile.py`.

---


License
-------

It's a Live is licensed under the GPL v3 or any later version.


Acknowledgements
---------------

I would like to thank my bestie Ian Cromwell, without whom this project would be nameless.
