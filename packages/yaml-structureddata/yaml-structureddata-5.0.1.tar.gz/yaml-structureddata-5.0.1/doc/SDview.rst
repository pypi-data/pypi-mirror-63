SDview
======

Introduction
------------

SDview is a viewer and browser with a graphical user interface for
StructuredData. 

You can use this program to explore a StructuredDataContainer file as well as
performing queries in the file. 

The start screen
----------------

This is the start screen of SDview when you load the file
"idcp_db.cache.SDCyml" from the "samples" directory of the software
distribution of StructuredData:

.. image:: images/SDview-idcp_db-initialwin.png

The graphical user interface consists of the following parts:

The menu
  You use the menu to open a file or quit the program or to display the
  program's license.

The search frame
  You use the search frame when you want to search the data for paths with a
  certain name or nodes with a certain values.

The tree display frame
  This window has some controls for the tree window. The buttons here change
  the expanded or collapsed state of the displayed nodes.

The tree frame
  This is the most important part of the program. In this window the
  StructuredData is displayed as a clickable hierarchy.

The tree frame
--------------

The most important part of the GUI is the tree display at the bottom. In the
picture above you see three elements that have a small folder icon. Folder
icons represent *collections*. Collections are nodes that contain references to
other nodes, they are displayed either *expanded* or *collapsed*. 

There is a label at the right side of each icon. This label is either a *map
key*, a *list index* or a combination of one of these with a value. 

The label of the *top node*, which is not part of another collection is "#".

The two following nodes labeled "id-data" and "id-metadata" are part of the
*top node*. This means that the top node is a map that maps these strings to
the nodes. The relation can also be seen by the small connection lines.

You will notice the small "+" or "-" in a small box left to each folder icon.
This is only shown for nodes that are *collections*. The box shows the state of
the collection which is either *expanded* or *collapsed*. A "-" indicates that
the collection it is expanded meaning that all referenced nodes are shown. A
"+" indicates that it is collapsed meaning that the referenced nodes are not
shown.

You can toggle between the expanded and collapsed state by clicking on the
small "+" or "-".

If the displayed nodes do not fit on the screen, a scroll bar appears at the
right or bottom of the tree frame. You can use the mouse wheel to scroll
vertically.

The following screen shot shows the program when the nodes "id-data", "U125/1"
and "config" are expanded:

.. image:: images/SDview-idcp_db-expanded.png

Here you do not see the yellow folder icons but also while file icons. These
represent *scalars*. These are nodes that are simple values, booleans, numbers
or strings. Scalars never have references to other nodes. For this reason these
nodes can not be expanded or collapsed.

For nodes that are scalars, the node labels consist of the map key or list
index and a colon ":" followed by the value. Note that string values are
enclosed in single quotes. 

You see that the label "config" is red. The color red is used for *selected*
nodes. Whenever you click with mouse on a node it becomes selected. This
feature becomes important when you perform searches with the elements of the
*search frame*. All results of a search become selected and are then indicated
by red labels.

The tree display frame
----------------------

The tree display frame has buttons to control the expand and collapse state of
the displayed nodes.

collapse all
++++++++++++

This button collapses all nodes meaning that only the *top node* is shown.
This is how the program looks like after pressing "collapse all":

.. image:: images/SDview-small-collapse-all.png

expand all
++++++++++

This button expands all nodes meaning that all nodes are shown. Here is how the
program looks like after pressing "expand all", in this case we use the small
example from the "Introduction to StructuredData":

.. image:: images/SDview-small-expand-all.png

collapse
++++++++

This button collapses one more level. If we press "collapse" after "expand all"
in the example, the node labeled "[3]" gets collapsed. Here is the picture:

.. image:: images/SDview-small-collapse.png

expand
++++++

This button expands one more level. If we press "expand" after "collapse all"
in the example, the three nodes "key1", "key2" and "key3" are displayed. The
nodes "key2" and "key3" are collapsed, their referenced nodes are not shown.

.. image:: images/SDview-small-expand.png

The search frame
----------------

This frame has controls to perform searches in StructuredData. 

You have always to enter a string in the entry field labeled "pattern". If you
press the <Return> key or press the "search" button all nodes matching the
search will be *selected*. Their font color changes to red. You can navigate
between the results with the buttons "up" and "down". "up" goes to the nearest
previous selected (red) node, "down" goes to the nearest next selected node.
Note that if you click with the mouse in the tree frame, the selection will be
cleared. 

The search type
+++++++++++++++

The selection field after the label "type:" sets the kind of search. These
search types are defined:

pattern
:::::::

This is a StructuredData pattern. A pattern consists of map keys and indices
joined by a dot ".". Indices must be enclosed in square brackets. A square
bracket must no preceded by a dot. You can use "*" as a wildcard, meaning "any
key" and "**" as a wildcard, meaning "any key, one or more". All paths that
match the pattern get selected. Here is an example searching for "key.*":

.. image:: images/SDview-small-pattern1.png

ipattern
::::::::

This is an "ipattern". This pattern consist of several *words* separated by
spaces. A *word* can contain any character except a space. All paths that
contain *all* of the words in *any order* are selected. Here is an example
searching for paths that contain the strings "key3" and "float":

.. image:: images/SDview-small-pattern2.png

regexp
::::::

This is a perl compatible regular expression. All paths that match this
expression are shown. Here is an example that looks for all paths that start
with "key", "2" or "3" and end there:

.. image:: images/SDview-small-pattern3.png

find value
::::::::::

This looks for all nodes where the value is equal to the entered value. Note
that if you want to look for a string that could be interpreted as a number
(like "150") you have to enclose the string in double quotes. Here is an
example where we look for the value 1 (the number, not the string):

.. image:: images/SDview-small-pattern4.png

ipattern find value
:::::::::::::::::::

Here we specify the value with an ipattern (see also "ipattern" further above).
If a value is a number it is first converted to a string before the program
tries to match it with the ipattern. In this example we look for the ipattern
"1", note that 1.23 also matches, since, interpreted as a string, it contains
"1":

.. image:: images/SDview-small-pattern5.png

regexp find value
:::::::::::::::::

Here we specify the value with a regular expression. If a value is a number it
is first converted to a string before the program tries to match it with the
regular expression. Here we search for all values that start with "x" or "y":

.. image:: images/SDview-small-pattern6.png

report only leaves
++++++++++++++++++

If you look at the StructuredData hierarchy as a tree, then all nodes that are
just *scalar values* could be considered the *leafs* of the tree. This is the
meaning of this checkbutton. If it is checked, the search returns only paths
whose nodes are scalars. Here is an example to show the difference. We look for
paths that match the regular expression "key". Without "report only leaves",
all nodes are selected:

.. image:: images/SDview-small-pattern7.png

With "report only leaves", only nodes with a scalar value are selected:

.. image:: images/SDview-small-pattern8.png

result window
+++++++++++++

The selection field after the label "result window:" determines if an extra
window with search results should be shown.  We show the effect of this field
on the search of the previous example where we look for paths that match the
regular expression "key", we want only to see nodes that are scalar values:


Here are the three possible values of "result window":

no
::

No result window is created. The program looks like this:

.. image:: images/SDview-small-pattern8.png

show paths
::::::::::

In this case the program looks the same as in the picture above but and extra
window is created:

.. image:: images/SDview-small-pattern-result1.png

show paths and values
:::::::::::::::::::::

Here this extra window is created:

.. image:: images/SDview-small-pattern-result2.png

