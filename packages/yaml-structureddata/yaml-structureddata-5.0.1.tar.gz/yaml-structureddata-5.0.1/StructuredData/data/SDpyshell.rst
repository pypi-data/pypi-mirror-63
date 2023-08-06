SDpyshell
=========

Introduction
------------

The StructuredData python shell (SDpyshell) provides a simple way to query,
modify, export and import StructuredData. 

The SDpyshell can be started without arguments, you then get a command prompt
where you can enter commands interactively.

It can be started with the "-c" option, where you provide all commands as
parameter for the "-c" option.

It can be started with the "-s" option followed by a number, in this case the
shell runs in *server mode*. Now the user can connect to the shell with "telnet
[hostname] [port]" and issue commands on the telnet prompt.

It can be started as a script interpreter with the well known shebang syntax.
Just put this at the first line of your file::

  #!/usr/bin/env SDpyshell

It will then interpret the rest of the file as SDpyshell commands.

Basic Syntax
------------

SDpyshell has the same syntax as the python (version 2) language. It works like the interactive python interpreter with some extra functions, classes and objects. You can load python modules with the `import` statement and use them in the shell.

For details on python syntax look at 
`Python 2.7 documentation <https://docs.python.org/2.7/>`_.

function calls
++++++++++++++

A function call is a name followed by a list of arguments enclosed in round
brackets. All the arguments are separated by commas `,`.

Here are examples for simple function calls, one with unnamed and one with
named parameters. Named parameters are followed by a "=" and a value::

  myfunction(arg1, arg2, arg3)
  myfunction(arg1, name2=value2, name3=value3)

Two functions can be called in a single line when they are separated by a
semicolon::

  myfunction1(arg1, arg2); myfunction2(arg3, arg4)

You may spread spread arguments to functions across several lines like 
that::

  myfunction(arg1, arg2,
             arg3, arg4)

You may have expressions as a value to a function. The following calls
myfunction with 1 and 5::

  myfunction(1, 2+3)

The brackets decide what the function parameters are. In the following line,
myfunction is called with 1 and 2, the results of myfunction is then added to
3::

  myfunction(1, 2) + 3

Parameter values may also be function calls::

  myfunction(1, myfunction2(3 4))

procedure calls
+++++++++++++++

Procedures are functions that get no arguments. A name on a single line
followed by an opening and closing round bracket is interpreted as a procedure
call. Note that the brackets must not be omitted, here is an example::

  myprocedure()

More than one procedure call in a line have to be separated with a semicolon::

  myprocedure1(); myprocedure2()

string literals
+++++++++++++++

All python string literals are allowed. Simple examples are::

  "a string"
  'a string'
  """a string across
  several lines"""

.. _SDpyshell-basic-function:

Basic function
--------------

The SDpyshell has a global variable "fun.SDC" which is initially an empty
StructuredDataContainer. All operations work with this variable unless the
parameter "sdc" is set to a value different from fun.SDC. 

It is important to know that consecutive read operations *add* data to the
StructuredDataContainer. The old data *is not* deleted when new data is read,
both are merged. If the new data has different values for items already present
in the StructuredDataContainer, they are overwritten with the new values.

.. _SDpyshell-command-layers:

Command layers
--------------

A command is either a *function* or a *procedure*. Both may alter the
StructuredData but functions always return a value where procedures don't. We
call commands that print results to the console but don't return a value
procedures.

There are three layers of commands in SDpyshell:

**functional layer**
  These are functions that return simple data or data structures. The data
  returned usually is not a simple string. These functions are used to *write
  programs*.  Functions that belong to this category start with "fun." like in
  "fun.get".

**text layer**
  These are functions that always return a string that may contain several
  lines of text. The functions in this category are used to *capture* the text
  that the commands in the following category would print to the console.
  Functions that belong to that category start with "txt." like in "txt.get".

**interactive layer**
  Commands in this category are intended to be used in the interactive shell.
  They never return values but may print messages or results of queries to the
  console. These commands *do not* have a leading "fun." or "txt." in their
  name like in "get".

Format Specifications
---------------------

Many commands in SDpyshell allow the user to specify the format of the data
returned. Not all commands support all formats, for details see the
`Commands and Functions`_.

The format is usually specified as a string that consists of format keywords
separated by colon characters. Here is an example::

  "yaml:py:flat"

The following sections list all known format keywords.

Structure Formats
+++++++++++++++++

These format keywords specify the kind of structure that is read from or
written to the file. Only one of these keywords may be part of a format
specification string.

container
  This specifies that a StructuredDataContainer is used.

store
  This specifies that a StructuredDataStore is used.  
types
  This specifies that a StructuredDataTypes structure is used.

Text formats
++++++++++++

These format keywords specify the way the data is represented as text. Only one
of these keywords may be part of a format specification string.

"yaml"
  This stands for the YAML format. Some functions can read or write in this
  format.

"py"
  This stands for the python format. Data in this format is fully compatible
  with python data declarations.

"csv"
  This stands for "comma separated value". Only a StructuredDataStore can be
  written in this format. It cannot be used to read a file.

"raw"
  This stands for "raw python". The value is printed to the console with the
  python "print" command. This format is only available in function "get".

"aligned"
  This is a format where paths are followed by values where all values are
  aligned. This format is only available in functions "find", "ifind", "rxfind",
  "findval", "ifindval" and "rxfindval".

Marking links
+++++++++++++

"marklinks"
  Commands that print paths allow to mark the places in paths that refer to
  data that is referenced in at least one other place. A mark is a star "\*"
  appended to the end of a key. In "a.b*.c" for example, "a.b" is a link, this
  data is referenced somewhere else in the StructuredDataStore.

"hidelinks"
  With this format keyword, links are not marked.

Flat format
+++++++++++

These are format keywords that are used together with `Text formats`_.

"flat"
  This format can be used for writing a StructuredDataStore. In this case the
  command writes path-value pairs instead of a hierarchical structure.

"nonflat"
  This is the usual hierarchical format.

Dry run
+++++++

These format keywords are used at some commands to indicate that the command
should not take any action but only show what it would do.
  
"run"
  This format keyword specifies regular command execution. It is only here to
  have an opposite to "dry-run".

"dry-run"
  This format keyword specifies that the command only shows what it *would* do.

.. _SDpyshell-commands:

Commands and Functions
----------------------

The following text is basically the same the "help" command shows for each
command.

Generic functions
+++++++++++++++++

help
####

help()
::::::

This command for interactive use displays help for a given help topic or
command. If no arguments are given it displays all help topics.

The command takes the following parameters:

- *item*: This specifies the help topic which must be a string. This
  parameter is optional. If it is not provided or *None* the command
  displays a list of all help topics.
- *level*: This specifies the help level. This parameter is mandatory if a
  help topic with the same name occurs at more than one place in the list of
  help topics. It is then used to specify exactly which help topic is
  requested. If you request a topic that is more than once in the list, the
  help command shows you all topics together with their level parameter.

.. _SDpyshell-txt_help:

txt.help()
::::::::::

This command returns the text that `help()`_ prints to the console as a string.
For an explanation of parameters look at the description of `help()`_.

fun.help()
::::::::::

This command is identical to `txt.help()`_.

SDtype
######

fun.SDtype()
::::::::::::

This function returns a string that indicates the type of StructuredData
application currently running. It's main application is to write portable
*extensions* which are python modules that can run in SDpyshell and SDxmlrpc. It
returns one of these strings:

- library: The StructuredData python libraries are called from an unknown
  application.
- SDpyshell: The program running is the SDpyshell.
- SDxmlrpc: The program running is SDxmlrpc.

String and path functions
+++++++++++++++++++++++++

.. _SDpyshell-format:

format
######

format()
::::::::

This command for interactive use formats the given value and prints it to the
screen. It takes the follwoing parameters:

- *val*: This is the value to format.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "raw", "csv", "aligned".  "raw" means that the value is simply
  printed without enclosing quotes or anything. "aligned" means that keys and
  values are column-aligned, this format cannot be applied to all data. Note
  that format "csv" does not produce sensible output for some kinds of data.
  The default is "yaml". 

txt.format()
::::::::::::

This command formats the given value in the way that `format()`_ does but
returns the text instead or printing it. For an explanation of parameters look
at the description of `format()`_.

.. _SDpyshell-string2pathkey:

string2pathkey
##############

string2pathkey()
::::::::::::::::

This command for interactive use converts an arbitrary string to a valid path
key. If the string contains the characters ".[]" a backslash "\\" is prepended
to each character.  This is also the case when the string is "\*", "\*\*" or
"#" since these have a special meaning in path patterns. The result in printed
to the screen. For more information on paths see also :ref:`paths
<reference-Paths>`.

- *st*: This specifies the string to convert.

Here are some examples::

  > string2pathkey('abc')
  abc
  > string2pathkey('a.b.c')
  a\\.b\\.c
  > string2pathkey('ab[3]')
  ab\\[3\\]
  > string2pathkey('*')
  \\*
  > string2pathkey('\\*')
  \\\\*
  > string2pathkey('#')
  \\#
  > string2pathkey('\\#')
  \\\\#

txt.string2pathkey()
::::::::::::::::::::

This function returns the text that `string2pathkey()`_ prints to the console
as a string. For an explanation of parameters look at the description of
`string2pathkey()`_.

fun.string2pathkey()
::::::::::::::::::::

This function returns the text that `string2pathkey()` prints to the console as
a string. For an explanation of parameters look at the description of
`string2pathkey()`_.

pathkey2string
##############

pathkey2string()
::::::::::::::::

This command for interactive use converts a valid pathkey to a string. If the
pathkey contains the characters ".[]" prepended by a backslash "\\", the
backslash is removed at each position. This is also done if the backslash is
followed by "\*", "\*\*" or "#". For more information on paths see also
:ref:`paths <reference-Paths>`.

- *pk*: This specifies the pathkey to convert.

Here are some examples::

  > pathkey2string('abc')
  abc
  > pathkey2string('a\\.b\\.c')
  a.b.c
  > pathkey2string('\\*')
  *
  > pathkey2string('\\#')
  #

txt.pathkey2string()
::::::::::::::::::::

This function returns the text that `pathkey2string()`_ prints to the console
as a string. For an explanation of parameters look at the description of
`pathkey2string()`_.

fun.pathkey2string()
::::::::::::::::::::

This function returns the text that `pathkey2string()`_ prints to the console
as a string. For an explanation of parameters look at the description of
`pathkey2string()`_.

splitpath
#########

splitpath()
:::::::::::

This command for interactive use splits a given path/pattern or a list of
paths/patterns into it's keys. Note that if the pattern contains the wildcards
"\*" or "\*\*" the korrespoding key the symbol *ANYKEY* respective *ANYKEYS*.
These are special gobal variables that represents the wildcard symbols. Note
too that the symbols *ANYKEY* and *ANYKEYS* cannot be printed in YAML format.
The command takes the following parameters:

- *path*: This specifies the path or a list of paths. See also
  :ref:`paths <reference-Paths>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "raw".  "raw" means that the value is simply printed without
  enclosing quotes or anything. The default is "yaml".

Here are some examples::

  > splitpath("01_facility[0].description")
  - 01_facility
  - 0
  - description

  > splitpath("01_facility[0].description", "py")
  ['01_facility', 0, 'description']

  > splitpath("a.*.b", "py")
  ['a', ANYKEY, 'b']


txt.splitpath()
:::::::::::::::

This function returns the text that `splitpath()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`splitpath()`_.

Here is an example::

  > print txt.splitpath("01_facility[0].description")
  - 01_facility
  - 0
  - description

fun.splitpath()
:::::::::::::::

This command splits a given path or a list of paths into it's keys. It returns
a list of strings and integers. The command takes the following parameters:

- *path*: This specifies the path or a list of paths. See also
  :ref:`paths <reference-Paths>`.

Here are some examples::

  > print fun.splitpath("01_facility[0].description")
  ['01_facility', 0, 'description']

  > print fun.splitpath("01_facility[0].description")[2]
  description

joinpath
########

joinpath()
::::::::::

This command for interactive use converts a list of keys to a path. The keys
are either arbitrary strings or the global symbol *ANYKEY* which represents the
"\*" wildcard. The command takes the following parameters:

- *keys*: This is a list of keys. The are joined to form a *path*.  See also
  :ref:`paths <reference-Paths>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "raw".
  "raw" means that the value is simply printed without enclosing quotes or
  anything. The default is "raw".

Here are some examples::

  > joinpath([:01_facility, 0, :description ])
  01_facility[0].description
  > joinpath([:01_facility, :0, :description ])
  01_facility.0.description
  > joinpath([:01_facility, ANYKEY, :description ])
  01_facility.*.description

txt.joinpath()
::::::::::::::

This command returns the text that `joinpath()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`joinpath()`_.

Here are some examples::

  > print txt.joinpath([:01_facility, 0, :description ])
  01_facility[0].description
  > print txt.joinpath([:01_facility, :0, :description ])
  01_facility.0.description

fun.joinpath()
::::::::::::::

This command converts a list of keys to a path and returns the path as a
string. The command takes the following parameters:

- *keys*: This is a list of keys. The are joined to form a *path*.  See also
  :ref:`paths <reference-Paths>`.

Here are some examples::

  > print fun.joinpath([:01_facility, 0, :description ])
  01_facility[0].description
  > get(fun.joinpath([:01_facility, 0, :description ]))
  BESSY II Ring

combinepaths
############

combinepaths()
::::::::::::::

This command for interactive use combines a list of paths to a new single path
and returns it as a string. The command takes the following parameters:

- *paths*: This is a list of paths. These are joined to form a new *path*.
  See also :ref:`paths <reference-Paths>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "raw".
  "raw" means that the value is simply printed without enclosing quotes or
  anything. The default is "raw".

Here is an example::

  > combinepaths(["AB.CD","EF","GH.IJ"])
  AB.CD.EF.GH.IJ

txt.combinepaths()
::::::::::::::::::

This command returns the text that `combinepaths()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`combinepaths()`_.

fun.combinepaths()
::::::::::::::::::

This command converts a list of keys to a path and returns the path as a
string. The command takes the following parameters:

- *paths*: This is a list of paths. The are joined to form a *path*.
  See also :ref:`paths <reference-Paths>`.

Here is an example::

  > print fun.combinepaths(["AB.CD","EF","GH.IJ"])
  AB.CD.EF.GH.IJ

addpaths
########

addpaths()
::::::::::

This command for interactive use combines two paths or a list of paths with a
second path to a new path or path list.  The command takes the following
parameters:

- *path1*: This is the first part of the new path. This parameter may be a
  single path or a list of paths. 
- *path2*: This is the second part of the new path. This parameter may be a
  single path or a list of paths. 
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "raw".
  "raw" means that the value is simply printed without enclosing quotes or
  anything. The default is "raw".

Here are some examples::

  > addpaths("ab.cd", "ef.gh")
  ab.cd.ef.gh
  > addpaths(["ab.cd", "xx.yy"], "ef.gh")
  ['ab.cd.ef.gh', 'xx.yy.ef.gh']
  > addpaths("ab.cd", ["ef.gh", "xx.yy"])
  ['ab.cd.ef.gh', 'ab.cd.xx.yy']

txt.addpaths()
::::::::::::::

This command returns the text that `addpaths()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`addpaths()`_.

fun.addpaths()
::::::::::::::

This function adds two paths. One of the paths arguments may also be a list of paths, in this case the function returns a new list of paths.

- *path1*: This specifies the first path or a list of paths. See also
  :ref:`paths <reference-Paths>`.
- *path2*: This specifies the second path or a list of paths. 

Here are some examples::

  > print fun.addpaths("ab.cd", "ef.gh")
  ab.cd.ef.gh
  > print fun.addpaths(["ab.cd", "xx.yy"], "ef.gh")
  ['ab.cd.ef.gh', 'xx.yy.ef.gh']
  > print fun.addpaths("ab.cd", ["ef.gh", "xx.yy"])
  ['ab.cd.ef.gh', 'ab.cd.xx.yy']

poppath
#######

poppath()
:::::::::

This command for interactive use removes one or more keys from a path or a list
of paths. It takes the following parameters:

- *path*: This specifies the path or a list of paths. See also
  :ref:`paths <reference-Paths>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "raw".  "raw" means that the value is simply printed without
  enclosing quotes or anything. The default is "raw".
- *no*: This parameters specifies the number of keys to remove. It's default is
  1. If this number is positive, keys are removed *from the end* of the path.
  If this number is negative, keys are removed *from the start* of the path.

Here are some examples::

  > poppath("01_facility[0].description")
  01_facility[0]
  > poppath("01_facility[0].description", no=2)
  01_facility
  > poppath("01_facility[0].description", no=-2)
  description


txt.poppath()
:::::::::::::

This command returns the text that `poppath()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`poppath()`_.

fun.poppath()
:::::::::::::

This command removes one or more keys from a path or a list of paths from the
end to the start and returns the new path as a string. It takes the following
parameters:

- *path*: This specifies the path or a list of paths. See also
  :ref:`paths <reference-Paths>`.
- *no*: This parameters specifies the number of keys to remove. It's default is
  1. If this number is positive, keys are removed *from the end* of the path.
  If this number is negative, keys are removed *from the start* of the path.

Here are some examples::

  > print fun.poppath("01_facility[0].description")
  01_facility[0]
  > print fun.poppath("01_facility[0].description", no=2)
  01_facility

substpath
#########

substpath()
:::::::::::

This command for interactive use changes a path or a list of paths according to
a given pattern.  This is a very flexible concept of manipulating paths without
the need to combine several poppath and addpath statements. Each wildcard
("\*") in the pattern is replaced with the matching part of the path.
Non-wildcard parts of the pattern remain unchanged. Please do also have a look
at the examples below.  The command takes the following parameters:

- *path*: This specifies the path or a list of paths. See also
  :ref:`paths <reference-Paths>`.
- *pattern*: This is a path pattern. See also 
  :ref:`patterns <reference-StructuredData-Patterns>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "raw".  "raw" means that the value is simply printed without
  enclosing quotes or anything. The default is "raw".

Here are some examples::

  > substpath("a.b.c.d", "*.X.*.*")
  a.X.c.d
  > substpath("a.b.c.d", "*.X.*.Y")
  a.X.c.Y
  > substpath("a.b.c.d", "*.*")
  a.b
  > substpath("a.b.c.d", "*.*.*.*.e.f")
  a.b.c.d.e.f
  > substpath("a.b.c.d", "*.*.X")
  a.b.X
  > substpath("a.b[3].d", "*.*[4].*")
  a.b[4].d
  > substpath(["a.b.c.d", "e.f.g.h" ], "*.X.*.*")
  ['a.X.c.d', 'e.X.g.h']

txt.substpath()
:::::::::::::::

This command returns the text that `substpath()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`substpath()`_.

.. _SDpyshell-fun.substpath:

fun.substpath()
:::::::::::::::

This command changes a path or a list of paths according to a given pattern.
This is a very flexible concept of manipulating paths without the need to
combine several poppath and addpath statements. Each wildcard ("\*") in the
pattern is replaced with the matching part of the path. Non-wildcard parts of
the pattern remain unchanged. Please do also have a look at the examples of
`substpath()`_.  The command takes the following parameters:

- *path*: This specifies the path or a list of paths. See also
  :ref:`paths <reference-Paths>`.
- *pattern*: This is a path pattern. See also 
  :ref:`patterns <reference-StructuredData-Patterns>`.

Functions for the StructuredDataContainer
+++++++++++++++++++++++++++++++++++++++++

newsdc
######

fun.newsdc()
::::::::::::

This command creates a new StructuredDataContainer and returns a handle to it.
For SDpyshell this handle is the StructuredDataContainer object itself. For
SDxmlrpc the handle is a generated string. You need this command if you intend
to use more than one StructuredDataContainer at a time. All procedures for
interactive use use a global StructuredDataContainer if it is not specified
otherwise.

namedsdc
########

fun.namedsdc()
::::::::::::::

This command is similar to fun.newsdc. It creates a new StructuredDataContainer
and returns a handle to it. With this function, the user can provide a handle
as parameter. Note that makes only a difference for SDxmlrpc. For SDpyshell, the
parameter to this function is ignored.

The command takes the following parameters:

- *arg*: The name that is used as a handle to the new StructuredDataContainer.
  When used from SDpyshell, this name is ignored and the returned handle is the
  StructuredDataContainer object.

locksdc
#######

fun.locksdc()
:::::::::::::

This command locks the given StructuredDataContainer. A locked
StructuredDataContainer may not be modified, trying to modify the object raises
an exception.

The command takes the following parameters:

- *sdc*: The StructuredDataContainer that is to be locked. 

copy
####

copy()
::::::

This command for interactive use returns a copy of a StructuredDataContainer.
Note that this is a *deep* copy, the copied object does never change when the
source is changed later on. These are the parameters of this command:

- *sdc*: The source StructuredDataContainer object. If this parameter is
  omitted, the command creates a copy from the global variable 
  ":ref:`fun.SDC <SDpyshell-basic-function>`".

txt.copy()
::::::::::

This command is identical to `copy()`_.

fun.copy()
::::::::::

This command is identical to `copy()`_.


File I/O
++++++++

lockfile
########

fun.lockfile()
::::::::::::::

This command defines the given file to be read only. Trying to modify this file
raises an exception.

The command takes the following parameters:

- *filename*: The name of the file.

lockdir
#######

fun.lockdir()
:::::::::::::

This command defines the given directory to be read only. Trying to modify this
directory raises an exception.

The command takes the following parameters:

- *dirname*: The name of the directory.

read
####

read()
::::::

This command for interactive use is used to read a StructuredDataContainer, a
StructuredDataStore or StructuredDataTypes from a file. The data read is
usually added to the global variable ":ref:`fun.SDC
<SDpyshell-basic-function>`") which is a StructuredDataContainer. The command
prints the names of the files read to the console.

If this command is issued several times, the new data is added to the data that
was already read. The command takes the following parameters:

- *filename*: The name of the file to read. If this parameter is omitted, the
  program reads all files named "\*.SDCyml" it finds in the current
  directory.
- *formatspec*: The format specification of the file. This is a string of
  format keywords separated by colon ":" characters. See 
  `Format Specifications`_ for details. Allowed format keywords here are:
  "container", "store", "types", "yaml", "py", "flat", "nonflat". The default
  is "container:yaml:nonflat".  - *sdc*: The destination where the new data is
  added. If this parameter is omitted, the data is added to the global
  StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". 

This function always returns the StructuredDataContainer where the data was
added.

Here are some examples::

  read("myfile")
  read("myfile", "py")
  read("myfile", "store")
  my_sdc= read(filename="myfile", formatspec="store:py", sdc=None)

txt.read()
::::::::::

This command is identical to `read()`_ except that it returns the modified
StructuredDataContainer and a list of the names of the files read.

fun.read()
::::::::::

This command is identical to `read()`_ except that it returns the modified
StructuredDataContainer and a list of the names of the files read.

write
#####

write()
:::::::

The command for interactive use write is used to write the data to a file or
the screen as a StructuredDataContainer, a StructuredDataStore or
StructuredDataTypes. The data written is usually taken from the global variable
":ref:`fun.SDC <SDpyshell-basic-function>`") which is a
StructuredDataContainer.  If a file was created the command prints the name of
the file created.  It takes the following parameters:

- *filename*: The name of the file to write. If this parameter is omitted, the
  command prints to the screen.
- *formatspec*: The format specification of the file. This is a string of
  format keywords separated by colon ":" characters. See 
  `Format Specifications`_ for details.  Allowed format keywords here are:
  "container", "store", "types", "yaml", "py", "csv", "flat", "nonflat". The
  default is "container:yaml:nonflat".
- *pattern*: If this parameter is given, it must be a match pattern. Only data
  that matches this pattern is printed. Note that your pattern usually should
  end with ".**" in order get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  write()
  write("myfile," "py")
  write(filename="myfile", formatspec="store:flat")

txt.write()
:::::::::::

This command is identical to `write()`_ except that it doesn't print a message
to the console.

fun.write()
:::::::::::

This command is identical to `write()`_ except that it doesn't print a message
to the console.

rewrite
#######

rewrite()
:::::::::

This command for interactive is used to write date that was read from a
StructuredDataContainer, a StructuredDataStore or StructuredDataTypes back to
the file they were read from. Each time the "read" command is called it
remembers the name of the first file it reads together with the format
(container, store or types). When rewrite is called, it uses that stored
filename to write the data to that file. The idea is to read data with the
"read" command, modify it with the SDpyshell and then write it back without
having to enter the filename a second time. The data is usually taken from the
global variable ":ref:`fun.SDC <SDpyshell-basic-function>`") which is a
StructuredDataContainer. The command writes the name of the created file to the
console. It takes the following parameters:

- *formatspec*: The format specification of the file. This is a string of
  format keywords separated by colon ":" characters. See 
  `Format Specifications`_ for details.  Allowed format keywords here are:
  "container", "store", "types", "yaml", "py", "csv", "flat", "nonflat", "run"
  and "dry-run". The default is "container:yaml:nonflat:run". When "dry-run" is
  given, the command just prints to the screen what file it *would* write to.
- *pattern*: If this parameter is given, it must be a match pattern. Only data
  that matches this pattern is printed. Note that your pattern usually should
  end with ".**" in order get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  rewrite()
  rewrite("dry-run")

Printing
++++++++

pr
##

pr()
::::

This command for interactive is used to print the data as a
StructuredDataContainer, a StructuredDataStore or StructuredDataTypes. The data
printed is usually taken from the global variable ":ref:`fun.SDC
<SDpyshell-basic-function>`") which is a StructuredDataContainer. The command
takes the following parameters:

- *formatspec*: The format specification of the file. This is a string of
  format keywords separated by colon ":" characters. See 
  `Format Specifications`_ for details.  Allowed format keywords here are:
  "container", "store", "types", "yaml", "py", "csv", "flat", "nonflat". The
  default is "container:yaml:nonflat".
- *pattern*: If this parameter is given, it must be a match pattern. Only data
  that matches this pattern is printed. Note that your pattern usually should
  end with ".**" in order get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  pr()
  pr("py")
  pr(formatspec="store:flat")


Generic functions for the StructuredDataStore
+++++++++++++++++++++++++++++++++++++++++++++

clear_store
###########

clear_store()
:::::::::::::

This command for interactive use empties the StructuredDataStore of a
StructuredDataContainer. If called without parameters, the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`" is changed.
This command takes the following parameters:

- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

txt.clear_store()
:::::::::::::::::

This command is identical to `clear_store()`_.

fun.clear_store()
:::::::::::::::::

This command is identical to `clear_store()`_.

refresh_links
#############

refresh_links()
:::::::::::::::

This command for interactive use refreshes the information on links in the
StructuredDataStore that is cached within the StructuredDataStore. Since this
looks at all paths in the StructuredDataStore it may take some time. However,
if you alter a StructuredDataStore by importing data or apply changes directly
at the objects within the StructuredDataStore and intend to get information on
links, you should issue this command.

txt.refresh_links()
:::::::::::::::::::

This command is identical to `refresh_links()`_.

fun.refresh_links()
:::::::::::::::::::

This command is identical to `refresh_links()`_.


Generic functions for StructuredDataTypes
+++++++++++++++++++++++++++++++++++++++++

clear_types
###########

clear_types()
:::::::::::::

This command for interactive use empties the StructuredDataTypes part of a
StructuredDataContainer.  If called without parameters, the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`" is changed.
This command takes the following parameters:

- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

txt.clear_types()
:::::::::::::::::

This command is identical to `clear_types()`_.

fun.clear_types()
:::::::::::::::::

This command is identical to `clear_types()`_.

Querying the data
+++++++++++++++++

paths
#####

paths()
:::::::

The command for interactive use paths is used to print paths found in the
StructuredDataContainer.  The data read is usually read from the global
variable ":ref:`fun.SDC <SDpyshell-basic-function>`") which is a
StructuredDataContainer.  Only paths that match the given pattern are printed.
The command takes the following parameters:

- *pattern*: This specifies the match pattern. 
  Note that only if your pattern ends with ".**" you get all paths that *start*
  with the pattern. If this parameter is omitted it defaults to "*".
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "csv", "raw", "hidelinks", "marklinks". The default is
  "yaml:hidelinks".
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  > paths()
  - id-data
  - id-metadata

  > paths("id-data.U2.names.*")
  - id-data.U2.names.devicename
  - id-data.U2.names.key
  - id-data.U2.names.name
  - id-data.U2.names.prefix

  > paths("id-data.U2.names")
  - id-data.U2.names

  > paths("id-data.U2.names.**")
  - id-data.U2.names
  - id-data.U2.names.devicename
  - id-data.U2.names.key
  - id-data.U2.names.name
  - id-data.U2.names.prefix

txt.paths()
:::::::::::

This command returns the text that `paths()`_ prints to the console as a
string. For an explanation of parameters look at the description of `paths()`_.

Here is an example::

  > print txt.paths("*")
  - id-data
  - id-metadata

fun.paths()
:::::::::::

The command paths is used to return paths found in the StructuredDataContainer
as a list of strings.  The data read is usually read from the global variable
":ref:`fun.SDC <SDpyshell-basic-function>`") which is a StructuredDataContainer.
Only paths that match the given pattern are returned. The command takes the
following parameters:

- *pattern*: This specifies the match pattern. 
  Note that only if your pattern ends with ".**" you get all paths that *start*
  with the pattern. If this parameter is omitted it defaults to "*".
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  > print fun.paths("*")
  ['id-data', 'id-metadata']

  > print fun.paths("id-data.U2.names")
  ['id-data.U2.names']

  > import pprint
  > pprint.pprint(fun.paths("id-data.U2.names", exact_match=False))
  ['id-data.U2.names',
   'id-data.U2.names.devicename',
   'id-data.U2.names.key',
   'id-data.U2.names.name',
   'id-data.U2.names.prefix']

find
####

find()
::::::

This interactive command is used to search the store for a given pattern. It
lists all matching paths together with the data. It usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The
command takes the following parameters:

- *pattern*: If this parameter is given, it must be a match pattern. Only data
  that matches this pattern is printed. Note that your pattern usually should
  end with ".**" in order get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "csv", "aligned", "raw", "hidelinks", "marklinks". In aligned
  format paths and values are printed separated by a colon ":" where the colons
  are aligned in the same column making the output better readable. The default
  for this parameter is "aligned:hidelinks".
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  > find("id-data.U2.names.**")
  id-data.U2.names.devicename: U2IV
  id-data.U2.names.key       : 98
  id-data.U2.names.name      : U2
  id-data.U2.names.prefix    : idcp98

  > find("id-data.U2.names.**", "py")
  {'id-data.U2.names.devicename': 'U2IV',
   'id-data.U2.names.key': 98,
   'id-data.U2.names.name': 'U2',
   'id-data.U2.names.prefix': 'idcp98'}

  > find("id-data.U2.names.**", "csv")
  id-data.U2.names.devicename;U2IV
  id-data.U2.names.prefix;idcp98
  id-data.U2.names.name;U2
  id-data.U2.names.key;98

  > find("id-data.*.names.key")
  id-data.U125/1.names.key : 96
  id-data.U125/2.names.key : 3
  id-data.U139.names.key   : 110
  id-data.U2.names.key     : 98
  id-data.U3.names.key     : 97
  id-data.U4.names.key     : 95
  id-data.U41.names.key    : 12
  id-data.U48.names.key    : 80
  id-data.U49/1.names.key  : 7
  id-data.U49/2.names.key  : 15
  id-data.UE112.names.key  : 13
  id-data.UE46.names.key   : 10
  id-data.UE49.names.key   : 8
  id-data.UE52.names.key   : 9
  id-data.UE56/1.names.key : 11
  id-data.UE56/2.names.key : 5
  id-data.UE56R.names.key  : 81
  id-data.Ubonsai.names.key: 99

txt.find()
::::::::::

This command returns the text that `find()`_ prints to the console as a string.
For an explanation of parameters look at the description of `find()`_.

Here is an example::

  > print txt.find("id-data.U2.names.**")
  id-data.U2.names.devicename: U2IV
  id-data.U2.names.key       : 98
  id-data.U2.names.name      : U2
  id-data.U2.names.prefix    : idcp98

fun.find()
::::::::::

The function fun.find is used to search the store for a given pattern. It
returns a list of pairs, each pair consisting of a matching path together with
the data. It usually uses the global StructuredDataContainer 
":ref:`fun.SDC <SDpyshell-basic-function>`". The command takes the following
parameters:

- *pattern*: If this parameter is given, it must be a match pattern. Only data
  that matches this pattern is printed. Note that your pattern usually should
  end with ".**" in order get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *show_links*: If this parameter is True, all links in the path are marked
  with a '*' character. See also `Marking links`_. The default for this
  parameter is False.
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here is an example::

  > pprint.pprint(fun.find("id-data.U2.names.**"))
  [('id-data.U2.names.devicename', 'U2IV'),
   ('id-data.U2.names.prefix', 'idcp98'),
   ('id-data.U2.names.name', 'U2'),
   ('id-data.U2.names.key', 98)]

ifind
#####

ifind()
:::::::

This interactive command is similar to the command `find()`_ with the exception
that the pattern is an "i-pattern".  An "i-pattern" is a list of space
separated sub-strings. All strings that contain all of these sub-strings in any
order (compared case insensitive) match.  This match is applied on all paths of
the StructuredDataContainer. The command usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The
command takes the following parameters:

- *pattern*: This specifies the i-pattern. 
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "csv", "aligned", "raw", "hidelinks", "marklinks". In aligned
  format paths and values are printed separated by a colon ":" where the colons
  are aligned in the same column making the output better readable. The default
  for this parameter is "aligned:hidelinks".
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  > ifind("U2 park")
  id-data.U2.referencing.h_park_position: 0
  id-data.U2.referencing.v_park_position: 150

  > ifind("U2 v park")
  id-data.U2.referencing.v_park_position: 150

txt.ifind()
:::::::::::

This command returns the text that `ifind()`_ prints to the console as a
string. For an explanation of parameters look at the description of `ifind()`_.

Here is an example::

  > print txt.ifind("U2 v park")
  id-data.U2.referencing.v_park_position: 150

fun.ifind()
:::::::::::

The command fun.ifind is similar to the command `find()`_ with the exception
that the pattern is an "i-pattern".  An "i-pattern" is a list of space
separated sub-strings. All strings that contain all of these sub-strings in any
order (compared case insensitive) match. This match is applied on all paths of
the StructuredDataContainer. The function returns a list of pairs, each pair
consisting of a matching path together with the data.  It usually uses the
global StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The
command takes the following parameters:

- *pattern*: This specifies the i-pattern. 
- *show_links*: If this parameter is True, all links in the path are marked
  with a '*' character. See also `Marking links`_. The default for this
  parameter is False.
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

rxfind
######

rxfind()
::::::::

This interactive command is similar to the command find with the exception that
the pattern is a regular expression. This regular expression is matched against
all paths of the StructuredDataContainer. The command usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The
command takes the following parameters:

- *regexp*: This specifies the regular expression. See the python documentation
  for `regular expression syntax <http://docs.python.org/library/re.html>`_.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "csv", "aligned", "raw", "hidelinks", "marklinks". In aligned
  format paths and values are printed separated by a colon ":" where the colons
  are aligned in the same column making the output better readable. The default
  for this parameter is "aligned:hidelinks".
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  > rxfind(r'.*U2.*park')
  id-data.U2.referencing.h_park_position: 0
  id-data.U2.referencing.v_park_position: 150

  > rxfind(r'.*U2.*[vh]_axl')
  id-data.U2.interface.h_axle_scheme: 1342
  id-data.U2.physical.v_axles       : 2

txt.rxfind()
::::::::::::

This command returns the text that `rxfind()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`rxfind()`_.

Here is an example::

  > print txt.rxfind(r'.*U2.*park')
  id-data.U2.referencing.h_park_position: 0
  id-data.U2.referencing.v_park_position: 150

fun.rxfind()
::::::::::::

The command fun.rxfind is similar to the command `fun.find()`_ with the
exception that the pattern is a regular expression. This regular expression is
matched against all paths of the StructuredDataContainer. The function returns
a list of pairs, each pair consisting of a matching path together with the
data. The function usually uses the global StructuredDataContainer
":ref:`fun.SDC <SDpyshell-basic-function>`".  The command takes the following
parameters:

- *regexp*: This specifies the regular expression. See the python documentation
  for `regular expression syntax <http://docs.python.org/library/re.html>`_.
- *show_links*: If this parameter is True, all links in the path are marked
  with a '*' character. See also `Marking links`_. The default for this
  parameter is False.
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

findval
#######

findval()
:::::::::

This interactive command is used to search the store for a given value. It
lists all paths together with the values that match the given value. It usually
uses the global StructuredDataContainer ":ref:`fun.SDC
<SDpyshell-basic-function>`". The command takes the following parameters:

- *value*: This specifies the value to look for. 
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "csv", "aligned", "raw", "hidelinks", "marklinks". In aligned
  format paths and values are printed separated by a colon ":" where the colons
  are aligned in the same column making the output better readable. The default
  for this parameter is "aligned:hidelinks".
- *pattern*: If this parameter is given, it must be a match pattern. Only data
  that matches this pattern is examined. Note that only if your pattern ends
  with ".**" you get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here is an example::

  > findval(10)
  id-data.U2.config.h_ref_velocity              : 10
  id-data.U4.config.h_ref_velocity              : 10
  id-data.U48.config.coil_number                : 10
  id-data.U48.feedback.cc_tables                : 10
  id-data.UE112.config.h_ref_velocity           : 10
  id-data.UE46.global.id-key                    : 10
  id-data.UE46.names.key                        : 10
  id-data.UE49.config.h_ref_velocity            : 10
  id-metadata.parameter-info.undulator.order_key: 10

  > findval(10, pattern="*.*.config.**")
  id-data.U2.config.h_ref_velocity   : 10
  id-data.U4.config.h_ref_velocity   : 10
  id-data.U48.config.coil_number     : 10
  id-data.UE112.config.h_ref_velocity: 10
  id-data.UE49.config.h_ref_velocity : 10


txt.findval()
:::::::::::::

This command returns the text that `findval()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`findval()`_.

Here is an example::

  > print txt.findval(10)
  id-data.U2.config.h_ref_velocity              : 10
  id-data.U4.config.h_ref_velocity              : 10
  id-data.U48.config.coil_number                : 10
  id-data.U48.feedback.cc_tables                : 10
  id-data.UE112.config.h_ref_velocity           : 10
  id-data.UE46.global.id-key                    : 10
  id-data.UE46.names.key                        : 10
  id-data.UE49.config.h_ref_velocity            : 10
  id-metadata.parameter-info.undulator.order_key: 10

fun.findval()
:::::::::::::

The command find is used to search the store for a given value. It returns a
list of pairs, each pair consisting of a path together with the matching data.
It usually uses the global StructuredDataContainer 
":ref:`fun.SDC <SDpyshell-basic-function>`". The command takes the following
parameters:

- *value*: This specifies the value to look for. 
- *show_links*: If this parameter is True, all links in the path are marked
  with a '*' character. See also `Marking links`_. The default for this
  parameter is False.
- *pattern*: If this parameter is given, it must be a match pattern. Only data
  that matches this pattern is examined. Note that your pattern usually should
  end with ".**" in order get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

ifindval
########

ifindval()
::::::::::

This interactive command is used to search the store for a value given by an
"i-pattern".  An "i-pattern" is a list of space separated sub-strings. All
strings that contain all of these sub-strings in any order (compared case
insensitive) match.  The command lists all paths together with the values whose
string representation matches the given i-pattern. It usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The
command takes the following parameters:

- *val_pattern*: This specifies the i-pattern. 
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "csv", "aligned", "raw", "hidelinks", "marklinks". In aligned
  format paths and values are printed separated by a colon ":" where the colons
  are aligned in the same column making the output better readable. The default
  for this parameter is "aligned:hidelinks".
- *pattern*: If this parameter is given, it must be a match pattern. Only data
  that matches this pattern is examined. Note that your pattern usually should
  end with ".**" in order get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  > ifindval("antiparallel", pattern="id-data.**")
  id-data.U2.operation.h_mode_label_2     : antiparallel+
  id-data.U2.operation.h_mode_label_3     : antiparallel-
  id-data.UE112.operation.h_mode_label_2  : antiparallel+
  id-data.UE112.operation.h_mode_label_3  : antiparallel-
  id-data.UE46.operation.h_mode_label_1   : antiparallel
  id-data.UE49.operation.h_mode_label_2   : antiparallel+
  id-data.UE49.operation.h_mode_label_3   : antiparallel-
  id-data.UE52.operation.h_mode_label_1   : antiparallel
  id-data.Ubonsai.operation.h_mode_label_2: antiparallel+
  id-data.Ubonsai.operation.h_mode_label_3: antiparallel-

  > ifindval("antiparallel mode")
  id-metadata.parameter-info.has_AP_mode.description: antiparallel operation mode exists

txt.ifindval()
::::::::::::::

This command returns the text that `ifindval()`_ prints
to the console as a string. For an explanation of parameters look at the
description of `ifindval()`_.

Here is an example::

  > print txt.ifindval('V0 5 4')
  id-data.UE112.config.gap2cc_nflags_10  : 4,V0,H5
  id-data.UE112.config.gap2cc_nflags_20  : 14,V0,H5
  id-data.UE112.config.gap2cc_nflags_5   : 5,V0,H4
  id-data.UE49.config.gap2cc_nflags_10   : 4,V0,H5
  id-data.UE49.config.gap2cc_nflags_5    : 5,V0,H4
  id-data.UE52.config.gap2cc_nflags_10   : 4,V0,H5
  id-data.UE52.config.gap2cc_nflags_5    : 5,V0,H4
  id-data.Ubonsai.config.gap2cc_nflags_10: 4,V0,H5
  id-data.Ubonsai.config.gap2cc_nflags_5 : 5,V0,H4

fun.ifindval()
::::::::::::::

The command ifindval is used to search the store for a value given by an
"i-pattern".  An "i-pattern" is a list of space separated sub-strings. All
strings that contain all of these sub-strings in any order (compared case
insensitive) match. It returns a list of pairs, each pair consisting of a path
together with the matching data. It usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The command
takes the following parameters:

- *val_pattern*: This specifies the i-pattern. 
- *show_links*: If this parameter is True, all links in the path are marked
  with a '*' character. See also `Marking links`_. The default for this
  parameter is False.
- *pattern*: If this parameter is given, it must be a match pattern. Only data
  that matches this pattern is examined. Note that your pattern usually should
  end with ".**" in order get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

rxfindval
#########

rxfindval()
:::::::::::

This interactive command is used to search the store for a value given by a
regular expression. It lists all paths together with the values whose string
representation match the given regular expression. It usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The
command takes the following parameters:

- *val_pattern*: This specifies the regular expression. See the python documentation
  for `regular expression syntax <http://docs.python.org/library/re.html>`_.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "csv", "aligned", "raw", "hidelinks", "marklinks". In aligned
  format paths and values are printed separated by a colon ":" where the colons
  are aligned in the same column making the output better readable. The default
  for this parameter is "aligned:hidelinks".
- *pattern*: If this parameter is given, it must be a match pattern. Only data
  that matches this pattern is examined. Note that your pattern usually should
  end with ".**" in order get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here is an example::

  > rxfindval(r'0.*V0.*H')
  id-data.UE112.config.gap2cc_nflags_0  : 0,V0,H4
  id-data.UE112.config.gap2cc_nflags_6  : 0,V0,H5
  id-data.UE46.config.gap2cc_nflags_0   : 0,V0,H2
  id-data.UE46.config.gap2cc_nflags_6   : 0,V0,H3
  id-data.UE49.config.gap2cc_nflags_6   : 0,V0,H5
  id-data.UE52.config.gap2cc_nflags_0   : 0,V0,H4
  id-data.UE52.config.gap2cc_nflags_6   : 0,V0,H5
  id-data.UE56/1.config.gap2cc_nflags_0 : 0,V0,H0
  id-data.UE56/2.config.gap2cc_nflags_0 : 0,V0,H0
  id-data.UE56R.config.gap2cc_nflags_0  : 0,V0,H0
  id-data.Ubonsai.config.gap2cc_nflags_6: 0,V0,H5

  > rxfindval(r'0.*V0.*H', pattern="id-data.*.*.gap2cc_nflags_0")
  id-data.UE112.config.gap2cc_nflags_0 : 0,V0,H4
  id-data.UE46.config.gap2cc_nflags_0  : 0,V0,H2
  id-data.UE52.config.gap2cc_nflags_0  : 0,V0,H4
  id-data.UE56/1.config.gap2cc_nflags_0: 0,V0,H0
  id-data.UE56/2.config.gap2cc_nflags_0: 0,V0,H0
  id-data.UE56R.config.gap2cc_nflags_0 : 0,V0,H0

txt.rxfindval()
:::::::::::::::

This command returns the text that `rxfindval()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`rxfindval()`_.

Here is an example::

  > print txt.rxfindval(r'0.*V0.*H5')
  id-data.UE112.config.gap2cc_nflags_6  : 0,V0,H5
  id-data.UE49.config.gap2cc_nflags_6   : 0,V0,H5
  id-data.UE52.config.gap2cc_nflags_6   : 0,V0,H5
  id-data.Ubonsai.config.gap2cc_nflags_6: 0,V0,H5

fun.rxfindval()
:::::::::::::::

The command rxfindval is used to search the store for a value given by a
regular expression. It returns a list of pairs, each pair consisting of a
matching path together with the data. It usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The command
takes the following parameters:

- *val_pattern*: This specifies the regular expression. See the python documentation
  for `regular expression syntax <http://docs.python.org/library/re.html>`_.
- *show_links*: If this parameter is True, all links in the path are marked
  with a '*' character. See also `Marking links`_. The default for this
  parameter is False.
- *pattern*: If this parameter is given, it must be a match pattern. Only data
  that matches this pattern is examined. Note that your pattern usually should
  end with ".**" in order get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here is an example::

  > import pprint
  > pprint.pprint(fun.rxfindval(r'0.*V0.*H5'))
  [('id-data.UE49.config.gap2cc_nflags_6', '0,V0,H5'),
   ('id-data.UE52.config.gap2cc_nflags_6', '0,V0,H5'),
   ('id-data.Ubonsai.config.gap2cc_nflags_6', '0,V0,H5'),
   ('id-data.UE112.config.gap2cc_nflags_6', '0,V0,H5')]

.. _SDpyshell-get:

get
###

get()
:::::

This interactive command prints the value for a given pattern or list of
patterns of a StructuredDataContainer. Note that a path is just a special case
of a pattern so you can use this command to simply print a single value. It
usually uses the global StructuredDataContainer ":ref:`fun.SDC
<SDpyshell-basic-function>`". This command prints the value referenced which
may be a simple value (scalar) or a structure (collection), see also :ref:`help
<reference-StructuredData-terminology>`. If only one path matched the command
prints the single value, if more than one path matched it prints a list of
values. The command takes the following parameters:

- *pattern*: This is a path, a pattern or a list of paths or a list of
  patterns. For patterns see also 
  :ref:`patterns <reference-StructuredData-Patterns>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "raw", "hidelinks", "marklinks".  "raw" means that
  the value is simply printed without enclosing quotes or anything. The default
  is "raw:hidelinks".
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  > get("id-data.U2.names.devicename")
  U2IV

  > get("id-data.U2.names.devicename", "py")
  'U2IV'

  > get("id-data.U2.names")
  {'devicename': 'U2IV', 'prefix': 'idcp98', 'name': 'U2', 'key': 98}

  > get("id-data.U2.names", "yaml")
  devicename: U2IV
  key: 98
  name: U2
  prefix: idcp98

  > get("id-data.*.names.key")
  [96, 3, 110, 98, 97, 95, 12, 80, 7, 15, 13, 10, 8, 9, 11, 5, 81, 99]

txt.get()
:::::::::

This command returns the text that `get()`_ prints to the console as a string.
For an explanation of parameters look at the description of `get()`_.

Here is an example::

  > print txt.get("id-data.U2.names") 
  {'devicename': 'U2IV', 'prefix': 'idcp98', 'name': 'U2', 'key': 98}

fun.get()
:::::::::

The function get returns the value for a given pattern or list of patterns of a
StructuredDataContainer. Note that a path is just a special case of a pattern
so you can use this function to simply get a single value. It usually uses the
global StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". This
function returns the value referenced which may be a simple value (scalar) or a
structure (collection), see also 
:ref:`help <reference-StructuredData-terminology>`. If only one path matched
the function returns a single value, if more than one path matched it returns a
list of values. The command takes the following parameters:

- *pattern*: This is a path, a pattern or a list of paths or a list of
  patterns. For patterns see also 
  :ref:`patterns <reference-StructuredData-Patterns>`.
- *show_links*: If this parameter is True, all links in the path are marked
  with a '*' character. See also `Marking links`_. The default for this
  parameter is False.
- *paths*: This optional parameter is used to provide a list of paths. If this
  parameter is given, not the complete StructuredDataContainer is searched but
  only all paths in this list. 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  > import pprint
  > pprint.pprint(fun.get("id-data.U2.names") 
  {'devicename': 'U2IV', 'key': 98, 'name': 'U2', 'prefix': 'idcp98'}
  > pprint.pprint(fun.get(["id-data.U2.names", "id-data.U49/1.names"]))
  [{'devicename': 'U2IV', 'key': 98, 'name': 'U2', 'prefix': 'idcp98'},
   {'devicename': 'U49ID4R', 'key': 7, 'name': 'U49/1', 'prefix': 'idcp7'}]
  > pprint.pprint(fun.get("id-data.*.names.key") 
  [96, 3, 110, 98, 97, 95, 12, 80, 7, 15, 13, 10, 8, 9, 11, 5, 81, 99]

getlinks
########

getlinks()
::::::::::

This interactive command returns a list of all paths that refer to the same
object as the given path.  It usually uses the global StructuredDataContainer
":ref:`fun.SDC <SDpyshell-basic-function>`". The command takes the following
parameters:

- *path*: This specifies the path or a list of paths. See also
  :ref:`paths <reference-Paths>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "raw". The default is "yaml".
- *include*: This parameter may be used to specify a *pattern* that all
  returned paths must match. Only paths that match this pattern are returned.
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *exclude*: This parameter may be used to specify a *pattern* that all
  returned paths must not match. Only paths that do not match this pattern are
  returned. *include* and *exclude* may be combined.
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

Here are some examples::

  > getlinks("01_facility[0]")
  - 01_facility[0]
  - 03_subdomain[0].domain.facility
  - 03_subdomain[171].domain.facility
  - 03_subdomain[1].domain.facility
  - 03_subdomain[2].domain.facility
  - 03_subdomain[3].domain.facility
  - 03_subdomain[4].domain.facility
  - 03_subdomain[5].domain.facility
  - 03_subdomain[6].domain.facility
  - 03_subdomain[7].domain.facility
  - 03_subdomain[8].domain.facility

  > getlinks("01_facility[0]", exclude="03_subdomain.*.domain.facility")
  - 01_facility[0]

  > getlinks("01_facility[0]", include="*[0].*.*")
  - 03_subdomain[0].domain.facility

txt.getlinks()
::::::::::::::

This command returns the text that `getlinks()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`getlinks()`_.

Here is an example::

  > print txt.getlinks("01_facility[0]", include="*[0].*.*")
  - 03_subdomain[0].domain.facility

fun.getlinks()
::::::::::::::

This function returns a list of all paths that refer to the same object as the
given path.  It usually uses the global StructuredDataContainer 
":ref:`fun.SDC <SDpyshell-basic-function>`". The command takes the following
parameters:

- *path*: This specifies the path or a list of paths. See also
  :ref:`paths <reference-Paths>`.
- *include*: This parameter may be used to specify a *pattern* that all
  returned paths must match. Only paths that match this pattern are returned.
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *exclude*: This parameter may be used to specify a *pattern* that all
  returned paths must not match. Only paths that do not match this pattern are
  returned. *include* and *exclude* may be combined.
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

Here is an example::

  > import pprint
  > pprint.pprint(fun.getlinks("01_facility[0]"))
  ['01_facility[0]',
   '03_subdomain[0].domain.facility',
   '03_subdomain[171].domain.facility',
   '03_subdomain[1].domain.facility',
   '03_subdomain[2].domain.facility',
   '03_subdomain[3].domain.facility',
   '03_subdomain[4].domain.facility',
   '03_subdomain[5].domain.facility',
   '03_subdomain[6].domain.facility',
   '03_subdomain[7].domain.facility',
   '03_subdomain[8].domain.facility']

findlinks
#########

findlinks()
:::::::::::

This command for interactive use returns a list of lists of paths that refer to
the same object. At least one path in each sublist matches the given pattern.
It usually uses the global StructuredDataContainer ":ref:`fun.SDC
<SDpyshell-basic-function>`". The command takes the following parameters:

- *pattern*: This specifies the match pattern. Only data
  that matches this pattern is examined. Note that your pattern usually should
  end with ".**" in order get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "raw". The default is "yaml".
- *include*: This parameter may be used to specify a *pattern* that all
  returned paths must match. Only paths that match this pattern are returned.
- *exclude*: This parameter may be used to specify a *pattern* that all
  returned paths must not match. Only paths that do not match this pattern are
  returned. *include* and *exclude* may be combined.
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

Here is an example::

  > findlinks("01_facility.*")
  -   - 01_facility[0]
      - 03_subdomain[0].domain.facility
      - 03_subdomain[171].domain.facility
      - 03_subdomain[1].domain.facility
      - 03_subdomain[2].domain.facility
      - 03_subdomain[3].domain.facility
      - 03_subdomain[4].domain.facility
      - 03_subdomain[5].domain.facility
      - 03_subdomain[6].domain.facility
      - 03_subdomain[7].domain.facility
      - 03_subdomain[8].domain.facility
  -   - 01_facility[1]
      - 02_domain[23].facility
      - 03_subdomain[137].domain.facility
      - 03_subdomain[140].domain.facility
      - 03_subdomain[141].domain.facility
      - 03_subdomain[142].domain.facility
      - 03_subdomain[165].domain.facility
      - 03_subdomain[169].domain.facility
  -   - 01_facility[2]
      - 02_domain[14].facility
      - 02_domain[16].facility
      - 02_domain[18].facility
      - 03_subdomain[103].domain.facility
      - 03_subdomain[108].domain.facility
      - 03_subdomain[111].domain.facility
      - 03_subdomain[167].domain.facility
      - 03_subdomain[94].domain.facility
      - 03_subdomain[97].domain.facility
      - 03_subdomain[99].domain.facility

txt.findlinks()
:::::::::::::::

This command returns the text that `findlinks()`_ prints
to the console as a string. For an explanation of parameters look at the
description of `findlinks()`_.

fun.findlinks()
:::::::::::::::

This command returns a list of lists of paths that refer to the same object. At
least one path in each sublist matches the given pattern. It usually uses the
global StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The
command takes the following parameters:

- *pattern*: This specifies the match pattern. Only data
  that matches this pattern is examined. Note that your pattern usually should
  end with ".**" in order get all paths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *include*: This parameter may be used to specify a *pattern* that all
  returned paths must match. Only paths that match this pattern are returned.
- *exclude*: This parameter may be used to specify a *pattern* that all
  returned paths must not match. Only paths that do not match this pattern are
  returned. *include* and *exclude* may be combined.
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

Here is an example::

  > pprint.pprint(fun.findlinks("01_facility.*")
  [['01_facility[0]',
    '03_subdomain[0].domain.facility',
    '03_subdomain[171].domain.facility',
    '03_subdomain[1].domain.facility',
    '03_subdomain[2].domain.facility',
    '03_subdomain[3].domain.facility',
    '03_subdomain[4].domain.facility',
    '03_subdomain[5].domain.facility',
    '03_subdomain[6].domain.facility',
    '03_subdomain[7].domain.facility',
    '03_subdomain[8].domain.facility'],
   ['01_facility[1]',
    '02_domain[23].facility',
    '03_subdomain[137].domain.facility',
    '03_subdomain[140].domain.facility',
    '03_subdomain[141].domain.facility',
    '03_subdomain[142].domain.facility',
    '03_subdomain[165].domain.facility',
    '03_subdomain[169].domain.facility'],
   ['01_facility[2]',
    '02_domain[14].facility',
    '02_domain[16].facility',
    '02_domain[18].facility',
    '03_subdomain[103].domain.facility',
    '03_subdomain[108].domain.facility',
    '03_subdomain[111].domain.facility',
    '03_subdomain[167].domain.facility',
    '03_subdomain[94].domain.facility',
    '03_subdomain[97].domain.facility',
    '03_subdomain[99].domain.facility']]


Modifying the data
++++++++++++++++++

filter_out
##########

filter_out()
::::::::::::

This interactive command is used to filter out data in a
StructuredDataContainer.  It usually uses the global StructuredDataContainer
":ref:`fun.SDC <SDpyshell-basic-function>`".  All parts that do not match the
given pattern are removed. The command takes the following parameters:

- *pattern*: This specifies the filter pattern.  Note that in oder tp match all
  paths *starting* with that pattern you have to end the pattern with ".**".
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified. 

This function always returns the StructuredDataContainer where the data was
changed.

Here are some examples::

  filter_out("mykey1.mykey2")
  filter_out("mykey1.*")
  filter_out("mykey1.*.mykey2.*.mykey3")

txt.filter_out()
::::::::::::::::

This command is identical to `filter_out()`_ except that it doesn't print a
message to the console.

fun.filter_out()
::::::::::::::::

This command is identical to `filter_out()`_ except that it doesn't print a
message to the console.

change
######

change()
::::::::

This interactive command is used to change a single value for a specific path
or a list of paths of a StructuredDataContainer. It usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The
command takes the following parameters:

- *path*: This specifies the path or a list of paths. See also
  :ref:`paths <reference-Paths>`.
- *value*: This is the value to be set. 
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

Here are some examples::

  > get("id-data.U2.global.device_status")
  simulated
  > change("id-data.U2.global.device_status", "installed")
  > get("id-data.U2.global.device_status")
  installed

txt.change()
::::::::::::

This command is identical to `change()`_.

fun.change()
::::::::::::

This command is identical to `change()`_.

put
###

put()
:::::

This interactive command is used to change or add a single value for a specific
path or a list of paths of a StructuredDataContainer. It usually uses the
global StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". If
the path is not present in the StructuredDataContainer, missing elements are
created on the fly. The command takes the following parameters:

- *path*: This specifies the path or a list of paths. See also
  :ref:`paths <reference-Paths>`.
- *value*: This is the value to be set. 
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

Here is an example::

  > find("id-data.U2.global.**")
  id-data.U2.global.description  : U2     ,U2IV     ,idcp98,pseudo ID for A.Pohl
  id-data.U2.global.device_status: installed
  id-data.U2.global.id-key       : 98
  id-data.U2.global.instance_no  : 0
  id-data.U2.global.primary_key  : 37
  id-data.U2.global.undulator    : U2

  > put("id-data.U2.global.extra", 100)

  > find("id-data.U2.global.**")
  id-data.U2.global.description  : U2     ,U2IV     ,idcp98,pseudo ID for A.Pohl
  id-data.U2.global.device_status: installed
  id-data.U2.global.extra        : 100
  id-data.U2.global.id-key       : 98
  id-data.U2.global.instance_no  : 0
  id-data.U2.global.primary_key  : 37
  id-data.U2.global.undulator    : U2

txt.put()
:::::::::

This command is identical to `put()`_.

fun.put()
:::::::::

This command is identical to `put()`_.

delete
######

delete()
::::::::

This interactive command is used to delete a single value of a given path or a
list of paths of a StructuredDataContainer. It usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The
command takes the following parameters:

- *path*: This specifies the path or a list of paths. See also
  :ref:`paths <reference-Paths>`.
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

Here is an example::

  > find("id-data.U2.global.**")
  id-data.U2.global.description  : U2     ,U2IV     ,idcp98
  id-data.U2.global.device_status: installed
  id-data.U2.global.id-key       : 98
  id-data.U2.global.instance_no  : 0
  id-data.U2.global.primary_key  : 37
  id-data.U2.global.undulator    : U2

  > delete("id-data.U2.global.description")

  > find("id-data.U2.global.**")
  id-data.U2.global.device_status: installed
  id-data.U2.global.id-key       : 98
  id-data.U2.global.instance_no  : 0
  id-data.U2.global.primary_key  : 37
  id-data.U2.global.undulator    : U2

txt.delete()
::::::::::::

This command is identical to `delete()`_.

fun.delete()
::::::::::::

This command is identical to `delete()`_.

link
####

link()
::::::

This interactive command is used to let a path in the StructuredDataContainer
refer to the same data as another already existing path. It usually uses the
global StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The
command takes the following parameters:

- *from_path*: This specifies the path or a list of paths whose value is
  changed. The path is a list of keys joined with a dot '.'. If the keys
  contain one of the characters '.[]' these have to be prepended with a
  backslash "\\". If the path doesn't already exist it is created, even missing
  elements within a longer path are created on the fly.
- *to_path*: This specifies the path whose node is referenced. This path must
  exist in the StructuredDataStore. The path is a list of keys joined with a
  dot '.'. If the keys contain one of the characters '.[]' these have to be
  prepended with a backslash "\\". 
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

Here is an example::

  > find("id-data.U2.interface.**", "marklinks")
  id-data.U2.interface.base_panel   : opi_baseIT.adl
  id-data.U2.interface.h_axle_scheme: 1342
  id-data.U2.interface.user_panel   : opi_usrIT.adl
  > link("id-data.U2.new", "id-data.U2.interface")
  > find("id-data.U2.new.**", "marklinks")
  id-data.U2.new*.base_panel   : opi_baseIT.adl
  id-data.U2.new*.h_axle_scheme: 1342
  id-data.U2.new*.user_panel   : opi_usrIT.adl

txt.link()
::::::::::

This command is identical to `link()`_.

fun.link()
::::::::::

This command is identical to `link()`_.

Querying types
++++++++++++++

typepaths
#########

typepaths()
:::::::::::

This interactive command used to print paths of the StructuredDataTypes object.
It usually uses the global StructuredDataContainer ":ref:`fun.SDC
<SDpyshell-basic-function>`".  Only paths that match the given pattern are
printed. The command takes the following parameters:

- *pattern*: This specifies the match pattern. Only data that matches this
  pattern is examined. Note that if your pattern ends with ".**" you get
  typepaths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "csv", "raw". The default is "yaml".
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  > typepaths("id-data.*")
  - id-data.*

  > typepaths("id-data.*.*")
  - id-data.*.config
  - id-data.*.feedback
  - id-data.*.global
  - id-data.*.interface
  - id-data.*.measurement
  - id-data.*.names
  - id-data.*.network
  - id-data.*.operation
  - id-data.*.physical
  - id-data.*.referencing
  - id-data.*.version

txt.typepaths()
:::::::::::::::

This command returns the text that `typepaths()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`typepaths()`_.

Here is an example::

  > print txt.typepaths("id-data.*.version")
  - id-data.*.version

fun.typepaths()
:::::::::::::::

This function returns a list of paths of the StructuredDataTypes object that
match the given pattern. It usually uses the global StructuredDataContainer
":ref:`fun.SDC <SDpyshell-basic-function>`". The function takes the following
parameters:

- *pattern*: This specifies the match pattern. Only data that matches this
  pattern is examined. Note that if your pattern ends with ".**" you get
  typepaths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

typefind
########

typefind()
::::::::::

This interactive command used to search the StructuredDataTypes object for a
given pattern. It lists all matching paths together with the type
specification. It usually uses the global StructuredDataContainer
":ref:`fun.SDC <SDpyshell-basic-function>`".  The command takes the following
parameters:

- *pattern*: This specifies the match pattern. Only data that matches this
  pattern is examined. Note that if your pattern ends with ".**" you get
  typepaths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "csv", "aligned", "raw". In aligned format paths and values are
  printed separated by a colon ":" where the colons are aligned in the same
  column making the output better readable. The default for this parameter is
  "aligned".
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here is an example::

  > typefind("id-data.*.names.*")
  id-data.*.names.devicename: string
  id-data.*.names.key       : integer
  id-data.*.names.name      : string
  id-data.*.names.prefix    : string

txt.typefind()
::::::::::::::

This command returns the text that `typefind()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`typefind()`_.

Here is an example::

  > print txt.typefind("id-data.*.names.*")
  id-data.*.names.devicename: string
  id-data.*.names.key       : integer
  id-data.*.names.name      : string
  id-data.*.names.prefix    : string

fun.typefind()
::::::::::::::

This command is used to search the StructuredDataTypes object for a given
pattern. It returns a list of pairs, each pair consisting of a matching path
together with the type specification. It usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`".  The command
takes the following parameters:

- *pattern*: This specifies the match pattern. Only data that matches this
  pattern is examined. Note that if your pattern ends with ".**" you get
  typepaths that *start* with the pattern. 
  See also :ref:`patterns <reference-StructuredData-Patterns>`.
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

typeget
#######

typeget()
:::::::::

This interactive command prints that type declaration for a given path. It
usually uses the global StructuredDataContainer ":ref:`fun.SDC
<SDpyshell-basic-function>`". The command takes the following parameters:

- *path*: This specifies the path. See also :ref:`paths <reference-Paths>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "raw".  "raw" means that the value is simply printed without
  enclosing quotes or anything. The default is "yaml".
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  > typeget("id-data.*.names.devicename")
  string
  ...

  > typeget("id-data.*.names")
  optional_struct:
  - devicename
  - key
  - name
  - prefix

txt.typeget()
:::::::::::::

This command returns the text the `typeget()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`typeget()`_.

Here is an example::

  > print txt.typeget("id-data.*.names")
  optional_struct:
  - devicename
  - key
  - name
  - prefix

fun.typeget()
:::::::::::::

This command returns the type declaration for a given path. The type
declaration may be a scalar or a list or a map, depending on the type. It
usually uses the global StructuredDataContainer 
":ref:`fun.SDC <SDpyshell-basic-function>`". The command takes the following
parameters:

- *path*: This specifies the typepath. The path is a list of keys and wildcards
  joined with a dot '.'. If the keys contain one of the characters '.[]' these
  have to be prepended with a backslash "\\". 
- *sdc*: The source of the data. If this parameter is omitted, the data is
  taken from the global variable ":ref:`fun.SDC <SDpyshell-basic-function>`". 

Here are some examples::

  > print fun.typeget("id-data.*.names.devicename")
  string
  > print fun.typeget("id-data.*.names")
  {'optional_struct': ['devicename', 'key', 'name', 'prefix']}

Modifying types
+++++++++++++++

typeput
#######

typeput()
:::::::::

This interactive command is used to change or add a type declaration. The
command gets a path or pattern and a type declaration that may be a string or a
map. The map should be provided in python syntax but the simplified strings of
functional python may be used. The command takes the following parameters:

- *path*: This specifies the path. See also :ref:`paths <reference-Paths>`.
- *value*: This is the value to be set. See also the examples further below.
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

Here are some examples:

All values for paths matching "id-data.*.global.remark" must be strings::

  typeput("id-data.*.global.remark", "string")

All values for paths matching "id-data.*.facility" must be of type "struct"
with the fields "description", "name" and "facility::

  typeput("id-data.*.facility", {"struct" : ["description", "name", "facility"]}

Note that due to the usage of simplified strings here, the spaces around the
second colon and the space before the closing square brackets must not be
omitted.

txt.typeput()
:::::::::::::

This command is identical to `typeput()`_.

fun.typeput()
:::::::::::::

This command is identical to `typeput()`_.

typeadditem
###########

typeadditem()
:::::::::::::

This interactive command is used to add an item to a complex type in a simple
way. Types like "struct" have a list of fields attached. With this command you
can add a field to the existing list without the need to mention all the fields
that exist already as you would have to when using typeput. The command usually
uses the global StructuredDataContainer ":ref:`fun.SDC
<SDpyshell-basic-function>`".  It takes the following parameters:

- *path*: This specifies the path. See also :ref:`paths <reference-Paths>`.
- *value*: This is the string value to be added. See also the examples further
  below.
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

Here are some examples:

This is the existing type declaration::

  > typeget("id-data.*.network")
  optional_struct:
  - bootserver
  - gateway
  - ioc
  - mount_filesystem
  - ntpserver
  - sec_lswitch_hosts


Now we add a new field to the list::

  > typeadditem("id-data.*.network", "netmask")

An here we check the results::

  > typeget("id-data.*.network")
  optional_struct:
  - bootserver
  - gateway
  - ioc
  - mount_filesystem
  - netmask
  - ntpserver
  - sec_lswitch_hosts

txt.typeadditem()
:::::::::::::::::

This command is identical to `typeadditem()`_.

fun.typeadditem()
:::::::::::::::::

This command is identical to `typeadditem()`_.

typedelete
##########

typedelete()
::::::::::::

This interactive command is used to delete a type.  It usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". The
command takes the following parameters:

- *path*: This specifies the path. See also :ref:`paths <reference-Paths>`.
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

txt.typedelete()
::::::::::::::::

This command is identical to `typedelete()`_.

fun.typedelete()
::::::::::::::::

This command is identical to `typedelete()`_.

typedeleteitem
##############

typedeleteitem()
::::::::::::::::

This interactive command is used to remove an item from a complex type in a
simple way.  Types like "struct" have a list of fields attached. With this
command you can remove a field from the existing list without the need to
mention all the fields that exist already as you would have to when using
typeput. The command usually uses the global StructuredDataContainer
":ref:`fun.SDC <SDpyshell-basic-function>`".  It takes the following
parameters:

- *path*: This specifies the path. See also :ref:`paths <reference-Paths>`.
- *value*: This is the string value to be removed. See also the examples
  further below.
- *sdc*: The StructuredDataContainer that is modified. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is modified.

Here are some examples:

First we check how the type declaration for path "id-data.*.names" looks like::

  > typeget("id-data.*.names")
  optional_struct:
  - devicename
  - key
  - name
  - prefix

Now we remove the item "facility"::

  > typedeleteitem("id-data.*.names", "key")

And here we check the results::

  > typeget("id-data.*.names")
  optional_struct:
  - devicename
  - name
  - prefix

txt.typedeleteitem()
::::::::::::::::::::

This command is identical to `typedeleteitem()`_.

fun.typedeleteitem()
::::::::::::::::::::

This command is identical to `typedeleteitem()`_.

Typechecking
++++++++++++

typecheck
#########

typecheck()
:::::::::::

This interactive command is used to check the data in a StructuredDataContainer
against it's type specifications. It usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`". This
command takes no parameters.

- *sdc*: The StructuredDataContainer that is checked. If this parameter is
  omitted, the global StructuredDataContainer 
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is checked.

txt.typecheck()
:::::::::::::::

This command is identical to `typecheck()`_.

fun.typecheck()
:::::::::::::::

This command is identical to `typecheck()`_.

typematch
#########

typematch()
:::::::::::

This interactive command shows if one of the type checks matches a given path
and shows the type specification. It usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`".

The command takes the following parameters:

- *path*: This specifies the path. See also :ref:`paths <reference-Paths>`.
- *formatspec*: The format specification. Allowed format keywords here are:
  "yaml", "py", "raw". The default is "yaml".
- *sdc*: The StructuredDataContainer where the path and the matching type are
  searched. If this parameter is omitted, the global StructuredDataContainer
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is taken.

Here is an example::

  > typematch("id-data.UE56R.names.devicename")
  id-data.*.names.devicename: string

txt.typematch()
:::::::::::::::

This command returns the text that `typematch()`_ prints to the console as a
string. For an explanation of parameters look at the description of
`typematch()`_.

Here is an example::

  > print txt.typematch("id-data.UE56R.names.devicename")
  id-data.*.names.devicename: string

fun.typematch()
:::::::::::::::

The function fun.typematch returns the type declarations that match a given
path and shows the type specification. It usually uses the global
StructuredDataContainer ":ref:`fun.SDC <SDpyshell-basic-function>`".

The command takes the following parameters:

- *path*: This specifies the typepath. The path is a list of keys and wildcards
  joined with a dot '.'. If the keys contain one of the characters '.[]' these
  have to be prepended with a backslash "\\". 
- *sdc*: The StructuredDataContainer where the path and the matching type are
  searched. If this parameter is omitted, the global StructuredDataContainer
  ":ref:`fun.SDC <SDpyshell-basic-function>`" is taken.

Here are some examples::

  > print fun.typematch("id-data.UE56R.names.devicename")
  {'id-data.*.names.devicename': 'string'}

  > import pprint
  > pprint.pprint(fun.typematch("id-data.UE56R.names"))
  {'id-data.*.names': {'optional_struct': ['devicename',
                                           'key',
                                           'name',
                                           'prefix']}}

Command aliases
---------------

These are aliases for the commands described above:

- h      : help,
- r      : read,
- p      : pr,
- w      : write,
- rw     : rewrite,

Invoking SDpyshell
------------------

Here is a short overview on the SDpyshell command line options:

--version             show program's version number and exit
-h, --help            show this help message and exit
--summary             Print a summary of the function of the program.
-p COMMANDS, --precmd=COMMANDS
                      specify COMMANDS to perform before any other action
--precmdfile=FILE     specify a FILE to execute before any other action
-c COMMANDS, --cmd=COMMANDS
                      specify COMMANDS to perform
-f FILE, --file FILE  load the specified StructuredData FILE. You may add the
                      formatspec directly with a comma.
-M MODULE, --module=MODULE
                      specify a MODULE to import at make its functions
                      accessible by XMLRPC
-I DIRECTORY, --searchpath=DIRECTORY
                      specify a DIRECTORY to prepend it to the module search
                      path.
--no-locking          do not lock file accesses
--server=PORT
                      start in telnetserver mode on port PORT
--localhost           start server on 'localhost' instead of DNSDOMAINNAME.
                      In this case the server can only be contacted from
                      applications running on the same host.
--pidfile=PIDFILE     specify the PIDFILE where PID's of sub processes will
                      be stored
--kill                just kill old servers, do not start new ones.
--password            specify the password needed to log onto the server
                      interactively
--password-hash=HASH  specify the HASH of the password needed to log onto
                      the server
--gen-password-hash=HASH
                      generate a password HASH from the given string.


Precommands
+++++++++++

Precommands are commands that are executed at the start of the shell before any
other command. These commands can be given as a command line parameter
(--precmd) or they can be read from a file (--precmdfile). A typical
application is to put the command to read a StructuredData file in a file and
provide it's name with --precmdfile. Precommands are also useful when SDpyshell
is started in server mode.

Extensions
++++++++++

These are user supplied python modules that can be loaded by the SDpyshell. The
module name (the filename without ".py") is provided with the command line
option "-M". In this case the python module is loaded and it's functions are
accessible with the module name as a prefix. 

You can use command line option "-I" in order to extend the search path for
extensions which are basically python modules. Keep in mind that extensions are
also searched in all paths specified by the "PYTHONPATH" environment variable.

Here is an example:

We have a file "myext.py" with this content::

  import StructuredData.SDshelllibTxt as txt
  import StructuredData.SDshelllibFun as fun
  
  def ids():
      p= fun.paths("id-data.*")
      return fun.poppath(p, no=-1)
  
  def print_ids(formatspec="yaml"):
      print txt.format(ids(), formatspec)

Now we start SDpyshell with "-M" to load the extension and with "--precmd" to load the 
sample StructuredData file from the "samples" directory::

  SDpyshell -M myext --precmd 'r("idcp_db.cache.SDCyml")'
  > import pprint
  > pprint.pprint(myext.ids())
  ['U125/1',
   'U125/2',
   'U139',
   'U2',
   'U3',
   'U4',
   'U41',
   'U48',
   'U49/1',
   'U49/2',
   'UE112',
   'UE46',
   'UE49',
   'UE52',
   'UE56/1',
   'UE56/2',
   'UE56R',
   'Ubonsai']

  > myext.print_ids("yaml")
  - U125/1
  - U125/2
  - U139
  - U2
  - U3
  - U4
  - U41
  - U48
  - U49/1
  - U49/2
  - UE112
  - UE46
  - UE49
  - UE52
  - UE56/1
  - UE56/2
  - UE56R
  - Ubonsai

Server mode
+++++++++++

When option "-s" is provided, SDpyshell is started in server mode. It waits for
connections on the specified port. 

Note that since SDpyshell includes a complete python interpreter, unauthorized
access to your SDpyshell server may pose a security risk. Anyone who can connect
to the server can execute arbitrary python commands under your user id. This is
the reason why specifying a password is mandatory when SDpyshell is started in
server mode. If you want a server with a restricted set of commands you might
consider using SDxmlrpc.

You can simply use telnet as a client to connect to the SDpyshell server. If you
have `rlwrap <http://freecode.com/projects/rlwrap>`_ installed you can connect
with::

  rlwrap -r telnet [host] [port]

With rlwrap you have command line history and command completion. Note that for
terminating the connection you have to enter "quit" on the command line.

Server password
+++++++++++++++

For security reasons you always have to provide a password when you start
SDpyshell in server mode. The password can be entered interactively when you
start SDpyshell with the "--password" option. With "--password-hash" you can
specify a password hash on the command line, a long hexadecimal string. With
"--gen-password-hash" you can generate the hexadecimal string from a given
password. "--password-hash" is useful when the SDpyshell server is started from a
script since you can not regenerate the password from the password hash.

Process management
++++++++++++++++++

When SDpyshell is started as a server it is useful to know the process id (PID)
of the server and to be able to restart the server by killing the old one and
starting a new one. This is done with the options --pidfile and --kill combined
with -s. --pidfile is used to specify the name of a PID file, this file
contains a line with the process id (PID) of the server and the command that
was used to start the server. When SDpyshell is started in server mode and
--pidfile is provided, the process named in this file (and it's children) are
killed first. When SDpyshell is started, it's PID and command line are put to
the PID file. If you dont't want to restart an SDpyshell server but just want
to kill the old one, use --pidfile together with --kill.
