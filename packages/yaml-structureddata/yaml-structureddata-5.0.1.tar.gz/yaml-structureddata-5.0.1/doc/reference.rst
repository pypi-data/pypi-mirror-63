Reference
=========

StructuredData in general
-------------------------

StructuredData is the concept of organizing data in a special hierarchical data
structure. First we have to define the terms used in the following chapters.

.. _reference-StructuredData-terminology:

StructuredData terminology
++++++++++++++++++++++++++

*StructuredData*
  This is the concept of having data in a hierarchical structure. There is
  always a top :ref:`node <reference-StructuredDataStore_terminology_node>`
  which is always a 
  :ref:`collection <reference-StructuredData-terminology-collection>`.
  
*StructuredDataContainer*
  This is a StructuredData structure that contains a StructuredDataStore and
  StructuredDataTypes.

*StructuredDataStore*
  This is a StructuredData structure that holds your data.

*StructuredDataTypes*
  This is a StructuredData structure that contains type declarations for a
  StructuredDataStore.

.. _reference-StructuredDataStore_terminology_node:

*node*
  Either a 
  :ref:`collection <reference-StructuredData-terminology-collection>`
  or a
  :ref:`scalar <reference-StructuredData-terminology-scalar>`.

.. _reference-StructuredData-terminology-scalar:

*scalar*
  Either a *boolean*, *integer*, *real* or *string*. A scalar is a simple value
  with no references. It cannot be referenced and is always contained in a
  collection.

*boolean*
  This is a scalar with only two possible Values, True or False. Note that in
  SDpyshell these two values are *True* and *False* with an upper case first
  letter. In YAML however, the values are *true* and *false* (all in small
  caps).

*integer*
  An integer number. Note that the range of these numbers is not defined here.
  We require that the range is at least -2**31 to +2**31.

*real*
  A floating point number. We require floating point numbers according to the
  IEEE 754 standard.

*string*
  A sequence of characters. Unicode characters are supported.

.. _reference-StructuredData-terminology-collection:

*collection*
  Either a :ref:`map <reference-StructuredData-terminology-map>` or a
  :ref:`list <reference-StructuredData-terminology-list>`.

.. _reference-StructuredData-terminology-map:

*map*
  A data structure that maps mapkeys, which are always strings, to values which
  are always nodes. Note that each mapkey can only be present once in the map.
  Each mapkey is associated with exactly one node. However, two map keys may be
  associated with the same node.

*mapkey*
  This is a key of a map. A mapkey is always a string.

.. _reference-StructuredData-terminology-list:

*list*
  A data structure that is a sequence of nodes. Note that the elements of the
  list have the order you gave them and that two elements of the list may be
  equal.

*listindex*
  This is the index that identifies a member of a list. An listindex is always
  an integer.

*key*
  Either a mapkey or a listindex.

*keylist*
  A list of keys. A keylist is a reference to a node in a StructuredDataStore.
  It describes how to find the node when you start at the top of the
  StructuredDataStore. The first key is a identifies a node in the top
  collection. If this node is a collection, the second key identifies a node in
  this second collection. If this node is again a collection, the third key
  identifies a node in this third collection and so on until you finally reach
  the referenced node.

*path*
  This is a keylist converted to a string. Basically mapkeys are concatenated
  with dots ‘.’ while listindices are concatenated after they are enclosed in
  square brackets. A typical path may look like this “abc.def[4].ghi”. For a
  precise definition of how paths are constructed see 
  :ref:`paths <reference-Paths>`.

*pattern*
  A path that may also contain 
  :ref:`paths <reference-StructuredData-terminology-wildcard>`. By definition,
  all paths are also patterns.

.. _reference-StructuredData-terminology-wildcard:

*wildcard*
  Special keys that match whole classes of keys in a StructuredData structure.
  "*" matches any mapkey and any listindex while "**" matches one or more
  mapkey and listindex.

*reference*
  Collections are never contained in other collections, they are only
  referenced. It is possible that a collection is referenced by more than one
  other collection.

*link*
  A link is a reference to a collection that is already referenced somewhere
  else.

References and links
++++++++++++++++++++

One is tempted to see collections as containing other collections or scalars,
but this is not true in the general case. Collections contain scalars but they
actually never contain other collections, they only have *references* to them.
The difference between containing an item and just having a reference is that
in a "contains" relationship a collection can only be contained in one other
collected where in a "reference" relationship a collection may be referenced by
several other collections. "Reference" relationships even allow circles e.g. A
referencing B referencing C referencing A.

However, if a collection is referenced by only one other collection, it makes
no practical difference if we see this as a "contains" or a "reference"
relationship.

If a collection is referenced by at least two other collections, we always have
to see this as a "reference" relationship. In the context of StructuredData we
call these cases "links" and distinguish them from the ordinary cases.

When querying a StructuredData object links are not recognizable. However, if
you apply a change to a collection it makes a big difference whether this
collection is referenced at only one or more than other collection. In order to
make the work with links easier SDpyshell provides some format parameters and
functions that help you to detect links and see what other collections
reference a given collection.

Relation of Structured Data to python data structures
+++++++++++++++++++++++++++++++++++++++++++++++++++++

You may skip this section if you are not familiar with python.

Here is an overview on which terms of the StructuredData definition relate to
which python data type:

====================   ==================================
Structured Data term   python data type
====================   ==================================
map                    dict where keys are always strings
list                   list
boolean                bool
integer                int
real                   float
string                 str
collection             either dict or list
scalar                 an int, a float or a str
====================   ==================================

.. _reference-Paths:

Paths
+++++

The definition of StructuredData allows to construct a unique path for each
node. We construct a path like this:

We start at the top of the StructuredData store and move, key by key towards
the node we have selected. We collect the keys we encounter in that order in a
list. It is now obvious that this list of keys identifies the node. A path is
simply a string representation of that list of keys.

Joining a keylist to a path
:::::::::::::::::::::::::::

The rules to construct a path from a list of keys are like this:

- If the key is a list index convert it to a string and enclose it in square
  brackets, e.g index 9 becomes the string "[9]".
- If the key is a map key it must be a string. Apply 
  :ref:`escape <reference-Escape_rules>` rules to the string.
- Combine all converted keys with the "." character. 
- If the path contains the sequence ".[" replace it with "[".

Here are some examples:

==============    =======
list of keys      path
==============    =======
"A" "B"           A.B
"A.B" "C"         A\\.B.C
"A" 2 "C"         A[2].C
"A" "\*" "C"       A\\*.C
"A" ANYKEY "C"    A.\*.C
==============    =======

Note that "ANYKEY" is a special variable that represents the "*" wildcard as
it is used in *patterns*, for more information on patterns see 
:ref:`patterns <reference-StructuredData-Patterns>`.

.. _reference-Escape_rules:

Escape rules
::::::::::::

The *escape* rules ensure that any list of map keys and list indices can be represented
as a path :ref:`path <reference-Paths>` and that this list can always 
be reconstructed from the path. The rules also ensure that a path can not be confused 
with a :ref:`pattern <reference-StructuredData-Patterns>` containing wildcards.

The *escape* rules are these:

- If the key is "\*" change it to "\\\*".
- If the key is "\*\*" change it to "\\\*\*".
- If the key is "#" change it to "\\#"
- If the key starts with a sequence of "\\" followed by either "\*", "\*\*" or
  "#", prepend a "\\" character.
- Replace all occurences of "." in the key with "\\.".
- Replace all occurences of "[" in the key with "\\[".
- Replace all occurences of "]" in the key with "\\]".

Here are some examples:

=======     ===============
key         escaped key
=======     ===============
A.B         A\\.B
A.B[5]C     A\\.B\\[5\\]C
\*           \\\*
\*\*          \\\*\*
#           \\#
\\\*         \\\\\*
=======     ===============

Example
:::::::

Here is an example of StructuredData (only the StructuredDataStore) formulated
in YAML::

  item1:
      first:
      - A
      - B
      second:
      - X
      - Y
      third:
      -   m: 1
          n: 2
      -   p: 10
          q: 11
  
If you are familiar with python, this would be the same structure in python::

  { "item1" : { "first":  ["A","B"],
                "second": ["X","Y"],
                "third":  [ {"m": 1, "n":2}, {"p":10, "q":11}]
              }
  }

In the example of StructuredData shown above the following table shows some
examples of paths and the data they point to:

=================  =====================================
path               data (in python notation)
=================  =====================================
item1.first        ["A","B"]
item1.first[1]     "B"
item1.second[0]    "X"
item1.third        [ {"m": 1, "n":2}, {"p":10, "q":11}]
item1.third[0]     {"m": 1, "n":2}
item1.third[0].m   1
item1.third[0].n   2
item1.third[1].q   11
=================  =====================================

.. _reference-StructuredData-Patterns:

Patterns
++++++++

In order to select a subset from a set of paths we define *patterns*, also
called *path patterns* where it could be confused with other types of patterns.
In patterns we combine special keys with ordinary keys. So each *path* can also
be considered as a *pattern*. These are the special keys that can be used in
patterns:

========   =====================   =======================================
key name   string representation   meaning
========   =====================   =======================================
ANYKEY     \*                      matches any key
ANYKEYS    \*\*                    matches one or more keys of any value
ROOTKEY    #                       used in type patterns for the root type
========   =====================   =======================================

Patterns come in two flavours, *type patterns* and *match patterns*. For
detailed information on *type patterns* see also 
:ref:`StructuredDataTypes <reference-StructuredDataTypes>`. 

Here are the differences between both flavours:

=============   ====================   ===================
flavour         allowed special keys   usage
=============   ====================   ===================
type pattern    ROOTKEY ANYKEY         type declarations 
match pattern   ANYKEY ANYKEYS         matching paths
=============   ====================   ===================

Example
:::::::

Here are some examples for match patterns:

Assume that we have the following set of paths::

  item1
  item1.first
  item1.first.A
  item1.first.B
  item1.second
  item1.second.X
  item1.second.Y
  item1.third
  item1.third[0]
  item1.third[1]
  item1.third[0].m
  item1.third[0].n
  item1.third[1].p
  item1.third[1].q

This is what some patterns match:

+-------------------+---------------------------------------+
| wildcard-path     | paths matched                         |
+===================+=======================================+
| \*                | item1                                 |
+-------------------+---------------------------------------+
| item1.\*          | item1.first item1.second item1.third  |
+-------------------+---------------------------------------+
| item1.second.\*   | item1.second.X item1.second.Y         |
+-------------------+---------------------------------------+
| item1.\*.\*       | item1.first.A item1.first.B           |
|                   | item1.second.X item1.second.Y         |
|                   | item1.third[0] item1.third[1]         |
+-------------------+---------------------------------------+
| item1.third[1].\* | item1.third[1].p item1.third[1].q     |
+-------------------+---------------------------------------+
| item1.third.\*\*  | item1.third[0] item1.third[1]         |
|                   | item1.third[0].m item1.third[0].n     |
|                   | item1.third[1].p item1.third[1].q     |
+-------------------+---------------------------------------+
| \*.second.\*      | item1.second.X item1.second.Y         |
+-------------------+---------------------------------------+

.. _reference-StructuredDataStore:

StructuredDataStore
-------------------

A StructuredDataStore basically is StructuredData without type declarations. A
StructuredDataStore is often embedded in a StructuredDataContainer together with
:ref:`StructuredDataTypes <reference-StructuredDataTypes>`.

.. _reference-StructuredDataTypes:

StructuredDataTypes
-------------------

The concept of :ref:`paths <reference-Paths>` allows to reference any part in a
StructuredDataStore with a single string. The concept of *patterns* allows to
reference sets of paths and by this sub sets of the StructuredDataStore. For an
introduction on *patterns* see 
:ref:`patterns <reference-StructuredData-Patterns>`. Here we use a special
flavour of patterns called *type patterns*, for further details on this
see :ref:`type patterns <reference-StructuredData-Typepatterns>`.

A StructuredDataTypes structure maps patterns, which are strings, to type
declarations which are simple scalars or nodes. By this StructuredDataTypes is
itself StructuredData. 

We can now check the types of a StructuredDataStore if they are consistent
with the type declarations in StructuredDataTypes. For all paths in the
StructuredDataStore we check if we find a matching pattern in
StructuredDataTypes. If more than one patterns match, the "best" matching
pattern is selected. See also 
:ref:`matching typepatterns <reference-Typepattern-matching>` for details.

If a pattern is found, the corresponding type declaration is checked with the
node referenced by the path. We report an error for each path where the type
declaration didn't match.

Differences to programming language type declarations
+++++++++++++++++++++++++++++++++++++++++++++++++++++

In statically typed programming languages without type inference you have to
declare types for all variables and parameters and functions. With
StructuredData you can define types *partially*. It is possible to have no
type declarations for parts of the data.

.. _reference-StructuredData-Typepatterns:

Typepatterns
++++++++++++

Typepatterns are a flavour of 
:ref:`patterns <reference-StructuredData-Patterns>` that are used for type
declarations. The wildcard "**" (ANYKEYS) is not allowed here. The special path
"#" (ROOTKEY) is used to declare the type of the *top node* since the *top
node* has no path.

Here are some examples of typepatterns:

=======   =====================================================
pattern   comment
=======   =====================================================
#         matches the *top node*
\*        matches all elements of the *top node*
A         matches element "A" of the *top node*
A.B       matches element "B" of element "A" of the *top node*
=======   =====================================================

.. _reference-Typepattern-matching:

Typepattern matching
++++++++++++++++++++

During a typecheck the program tries for each path if it finds a matching
typepattern in StructuredDataTypes. In order to speed up this process not all
typepatterns are examined but only those who have the same length as the path.
For this reason "**" is not allowed in typepatterns since it would also match
longer paths. The details of the typepattern matching algorithm are important
if more than one typepattern would match the path. The algorithm determines
which of the matching typepatterns is selected for the actual typecheck.

At each stage a directly matching key in a typepattern has precedence over a
wildcard. If a matching typepattern is found, the other typepatterns are not
searched.

Here are some examples with a path, some typepatterns and an indicator which typepattern is found by the match algorithm:

+-----------+--------------+------------+
| path      | typepatterns | matched    |
+===========+==============+============+
| X.B.D     | \*.\*.D      |   X        |
|           +--------------+------------+
|           | \*.B.C       |            |
|           +--------------+------------+
|           | X.A.\*       |            |
+-----------+--------------+------------+
| X.B.D     |  X.B.\*      |            |
|           +--------------+------------+
|           |  X.B.D       |   X        |
+-----------+--------------+------------+
| X.B.D     |  X.\*.\*     |   X        |
|           +--------------+------------+
|           |  \*.B.D      |            |
+-----------+--------------+------------+

Type declarations
+++++++++++++++++

This is the list of currently known type declarations, note that we write the
type declaration in `YAML <http://www.yaml.org>`_ syntax here:

boolean
:::::::

A boolean. A scalar of type boolean has only two possible Values, True or
False. Note that in SDpyshell these two values are *True* and *False*. In YAML
however, the values or *true* and *false* (all in small caps).  This data type
is represented with the string::

  boolean

integer
:::::::

An integer number. Note that the range of these numbers is not defined here.
We assume that the range is at least -2**31 to +2**31.
This data type is represented with the string::

  integer

real
::::

A floating point number. We assume floating point numbers according to the
IEEE 754 standard.

This data type is represented with the string::

  real

string
::::::

A sequence of characters. Unicode characters are supported.

This data type is represented with the string::

  string

optional struct
:::::::::::::::

This is a map where all map keys must be elements of the list provided in the
type declaration.

This data type is represented as a map with just one key and a list as value.
Here is the representation of it in YAML, there can be an arbitrary number of
map keys::

  optional_struct:
  - map_key1
  - map_key2

open struct
:::::::::::

This is a map where all elements of the list provided in the type declaration
must be present as map keys. The map may however, have other additional keys.

This data type is represented as a map with just one key and a list as value.
Here is the representation of it in YAML, there can be an arbitrary number of
map keys::

  open_struct:
  - map_key1
  - map_key2

struct
::::::

This is a map where all elements of the list provided in the type declaration
must be present as map keys. No other keys are allowed in the map than the
elements of the list.

This data type is represented as a map with just one key and a list as value.
Here is the representation of it in YAML, there can be an arbitrary number of
map keys::

  struct:
  - map_key1
  - map_key2

typed map
:::::::::

This is a map where each value must be of the type scalar_type. scalar_type
is either "boolean", "integer", "real" or "string".

This data type is represented as a map with just one key and a string as value.
The value must be one of the strings "boolean", "integer", "real" or "string".
Here is a representation in YAML which requires that all map values must be
integers::

  typed_map: integer

map
:::

This is a map with no further restrictions (aside from that map keys must be
strings).

This data type is represented with the string::

  map

optional list
:::::::::::::

This is a list where all list elements must be elements of the list provided
in the type declaration.

This data type is represented as a map with just one key and a list as value.
Here is the representation of it in YAML, there can be an arbitrary number of
values::

  optional_list:
  - value1
  - value2

typed list
::::::::::

This is a list where each value must be of the type scalar_type. scalar_type
is either "boolean", "integer", "real" or "string".

This data type is represented as a map with just one key and a string as value.
The value must be one of the strings "boolean", "integer", "real" or "string".
Here is a representation in YAML which requires that all list elements must be
integers::

  typed_list: integer

list
::::

This is simply a list with no further restrictions.

This data type is represented with the string::

  list

.. _reference-StructuredDataContainer:

StructuredDataContainer
-----------------------

A StructuredDataContainer contains a StructuredDataStore and optionally
StructuredDataTypes. When a StructuredDataContainer is stored in a file, it is
stored in `YAML <http://www.yaml.org>`_ format. Here is an example how such a
file looks like::

  '**SDC-Metadata**':
      version: '1.0'
  '**SDC-Store**':
      key1: 1
      key2:
          A: x
          B: y
      key3:
      - 1
      - 2
      - 3
      -   float: 1.23
  '**SDC-Types**':
      '#':
          struct:
          - key1
          - key2
          - key3
      '*.key1': integer
      '*.key2':
          optional_struct:
          - A
          - B
          - C
      '*.key2.*': string
      '*.key3':
          typed_list: integer

A StructuredDataContainer consists of three parts, the *metadata*, the
*StructuredDataStore* and the *StructuredDataTypes*. 

metadata
  This is meta information on the file. Currently it only contains the version
  number of the file format. It is everything below the key
  "\*\*SDC-Metadata\*\*".

StructuredDataStore
  This is the part of the file where the data is stored. It is everything below
  the key "\*\*SDC-Store\*\*". 

StructuredDataTypes
  Here are the type declarations. Type declarations are explained in more
  detail further below in this file. For now we just remember that type
  declarations consist of paths and types. A path is a string that identifies a
  position in the store. The "#" is the root symbol, it is used to define the
  type for the topmost part of the StructuredDataStore. The "*" characters are
  wildcards, similar to the "*" used in file systems, they match any string at
  that position. Note that the store and the types may reside in two different
  files. 

