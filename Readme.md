# Sublime Text 3 Test ExUnit

Exunit test runner for sublime text 3

## Motivation

I really liked the [TestRspec](https://github.com/astrauka/TestRSpec) ST3 plugin for ruby, so I decided to port it to elixir

## Installation
  
  With [Package Control](http://wbond.net/sublime_packages/package_control)

1. Run “Package Control: Install Package” command, find and install `Test ExUnit` plugin.
2. Restart SublimeText editor

Manually:

1. Clone this git repository into your packages folder (in SublimeText, Preferences -> Browse Packages to open this folder)
2. Restart SublimeText editor

## Configuration

Find settings in "Preferences -> Package Settings -> TestExUnit"

[Default settings](https://github.com/Dania02525/TestExUnit/blob/master/Preferences.sublime-settings)

## Key bindings

Find bindings in "Preferences -> Package Settings -> TestExUnit"

[Default bindings](https://github.com/Dania02525/TestExUnit/blob/master/Default.sublime-keymap)

## Notes

Be sure to configure your elixir path in package settings- this has been tested with kiex, but please report problems with other configurations by creating GH issue

## Acknowledgments

Inspired by https://github.com/astrauka/TestRSpec

Parts that are taken:
* basically everything except using mix instead of rspec
