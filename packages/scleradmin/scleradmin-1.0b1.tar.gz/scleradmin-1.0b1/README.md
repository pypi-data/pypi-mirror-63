# Sclera Platform Administration Tool

[Sclera](https://scleradb.com) is a stand-alone SQL processor with native support for machine learning, data virtualization and streaming data.

This tool installs Sclera as an independent application with an interactive command-line shell.

**Prerequisite:** Sclera requires [Java version 8 or higher](https://java.com/en/download/help/download_options.xml).

*We recommend against installing Sclera with root/admin permissions. Sclera does not need root access for installation or at runtime.*

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

## Installing Sclera Core Packages and Shell

The following command installs Sclera:

    > scleradmin --install --root <sclera-root>

In the above, `<sclera-root>` is the directory where you want Sclera to be installed. This directory must not exist before installation, it is created by the command (this is a safeguard againt accidental overwrites). The contents of the directory after installation are described [later in this document](#root-directory-structure).

The installation involves downloading core sclera components and associated libraries. This might take a few minutes; you can monitor the progress by viewing the generated logs in `<sclera-root>/install/log/install.log`.

### Using the Shell

The shell can be started using the following command:

    > <sclera-root>/bin/sclera

This starts the shell, wherein you can interactively run queries. When done, you can terminate the session by typing `Control-D`.

    Welcome to Sclera 4.0

    > select "Hello, world!" as greeting;
    ---------------
     GREETING
    ---------------
     Hello, world!
    ---------------
    (1 row)

    > ^D
    Goodbye!

For details on using the shell, please refer to the [Command Line Shell Reference](https://scleradb.com/docs/interface/shell).

### Root Directory Structure

After installation, the root directory has the following structure:

    [<sclera-root>]
      bin/
        sclera.cmd         # executable command file (generated for Windows systems)
        sclera             # executable bash (generated for Linux, macOS, and other Unix-based systems)
      config/
        sclera.conf        # configuration file
      extlib/              # directory for additional libraries, plugins (initially empty)
      home/
        assets/
          data/            # data stored by the embedded temporary database (H2), etc.
        history            # shell command history
        log/
          sclera.log       # execution log, contains details of runtime progress
      install/
        boot/              # specification files for sclera components (core or plugin)
        launcher*.jar      # SBT launcher, used for installing sclera components
        log/
          install.log      # installation log, contains details of installation progress
      lib/                 # installation artifacts (jars, etc.) of installed components and their dependencies

## Plugin Management

Sclera provides [a variety of plugins](https://scleradb.com/docs/setup/components) that can be added using `scleradmin`. The command syntax is:

    > scleradmin --add <plugins> --root <sclera-root>

In the above, `<plugins>` is a space-separated list of plugins to be added, and `<sclera-root>`, [as earlier](#installing-sclera-core-packages-and-shell), is the root directory. For instance, to install the [Sclera - CSV File Connector](https://scleradb.com/docs/setup/components#sclera-csv-file-connector) and [Sclera - Text File Connector](https://scleradb.com/docs/setup/components#sclera-text-file-connector) plugins, to the Sclera instance installed at `/path/to/sclera` the command is: 

    > scleradmin --add sclera-csv-plugin sclera-textfiles-plugin --root /path/to/sclera

To remove installed plugins, the syntax is similar. The following command removes the plugins installed above:

    > scleradmin --remove sclera-csv-plugin sclera-textfiles-plugin --root /path/to/sclera

You can specify a list of plugins to add and another list of plugins to remove in the same command.

## Updating Installed Packages and Plugins

The following command updates Sclera's core packages as well as the plugins to the latest version:

    > scleradmin --update --root <sclera-root>

where `<sclera-root>`, [as mentioned earlier](#installing-sclera-core-packages-and-shell), is the root directory.
