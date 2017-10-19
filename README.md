#README#

## simpleifdef Sublime Text 3 plugin ##

This plugin automatically scans current file, searches
for matching #ifdef-#else-#endif and remembers their
position. Then, if the cursor enters one of those lines,
all other corresponding lines are highlighted. Keywords
 #ifdef, #ifndef, #if, #else, #elif, #endif are supported

![screenshot](https://github.com/rumly111/simpleifdef/raw/master/2017-10-19_17-19-06.gif)

I tried to make it as simple as possible, so there is
(almost) no error checking.

## Installation ##
Via Package Control, or copy simpleifdef.py to 
~/.config/sublime-text-3/Packages/User/

## Project GitHub ##
https://github.com/rumly111/simpleifdef

## Author ##
Joseph Botosh <rumly111@gmail.com>