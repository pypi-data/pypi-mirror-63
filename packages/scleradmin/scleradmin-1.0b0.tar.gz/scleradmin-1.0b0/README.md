# Sclera Platform Administration Tool

A tool to install [Sclera](https://github.com/scleradb/sclera) command line, and add/remove add-on plugins.

## Usage

```
       scleradmin [-h] [--install] [--add plugin [plugin ...]]
                  [--remove plugin [plugin ...]] [--update] [--root rootdir]
                  [--overwrite]

Sclera Platform Administration

optional arguments:
  -h, --help            show this help message and exit
  --install             install Sclera in the root directory
  --add plugin [plugin ...]
                        add plugins
  --remove plugin [plugin ...]
                        remove plugins
  --update              update Sclera and installed plugins to the latest version
  --root rootdir        root directory location (if not specified, will use
                        $SCLERA_ROOT if present, otherwise ~/sclera)
  --overwrite           overwrite root directory if present

In --add and --remove above, 'plugin' has the format 'org:name:version', where
'org:' and ':version' are optional. When not specified, 'org' defaults to
'com.scleradb' and 'version' defaults to the latest installable version.

Sclera requires Java version 8 or higher.
```
