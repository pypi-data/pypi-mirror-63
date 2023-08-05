# Changelog


## v0.2.1 (2020-03-10)

### Features

* Add command gutter so empty lines are more obvious. [Stavros Korokithakis]

### Fixes

* Disallow jumping past the last command (and ending playback) [Stavros Korokithakis]

* Don't skip over the last empty command. [Stavros Korokithakis]

* Fix race condition where the socket thread printed things to the screen before curses was set up. [Stavros Korokithakis]

* Add the missing `--address` argument. [Stavros Korokithakis]


## v0.2.0 (2020-03-09)

### Features

* Add curses-based presenter view. [Stavros Korokithakis]

* Add Ctrl+r as a resumption shortcut. [Stavros Korokithakis]

### Fixes

* Only update the presenter view if the command changes. [Stavros Korokithakis]

* Change Ctrl+b to Ctrl+g, as the former clashed with tmux. [Stavros Korokithakis]


## 0.1.3 (2020-03-04)

### Features

* Feat: Add `##@include` directive. [Stavros Korokithakis]


## 0.1.2 (2020-03-04)

### Fixes

* Don't filter lines. [Stavros Korokithakis]


## 0.1.1 (2020-03-04)

### Features

* Add Ctrl-e shortcut. [Stavros Korokithakis]


