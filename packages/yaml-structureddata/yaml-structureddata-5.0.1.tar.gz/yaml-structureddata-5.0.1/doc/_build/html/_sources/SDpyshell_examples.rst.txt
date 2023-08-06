SDpyshell Examples
==================

All these examples use the SDpyshell and the file "idcp_db.cache.SDCyml" of the
"samples" directory that is provided with the source of the python
StructuredDataStore module. They give you an overview of the capabilities of
StructuredData. For more details see also the chapter "Reference".

Details of the SDpyshell syntax are described in the chapter "Working with the
SDpyshell", it is the same syntax as of python version 2.7.

Start the SDpyshell and read the data file
------------------------------------------

Change to the "samples" directory of the source distribution::

  cd samples

Now we start SDpyshell and read the file "idcp_db.cache.SDCyml". Note that lines beginning with ">" are commands entered at the SDpyshell prompt::

  > SDpyshell
  SDpython shell
  >>> r("idcp_db.cache.SDCyml")


Reports with get
----------------

The "get" command returns the data structure referenced by a given path. Here
we want to see everything of the group "global" for the "UE112" device and
pretty-print this as a python structure::

  >>> get("id-data.UE112.global", "py")
  {'description': 'UE112  ,UE112ID7R,idcp13',
   'device_status': 'installed',
   'id-key': 13,
   'instance_no': 0,
   'primary_key': 39,
   'undulator': 'UE112'}

We can also specify YAML as format for the result::

  >>> get("id-data.UE112.global", "yaml")
  description: UE112  ,UE112ID7R,idcp13
  device_status: installed
  id-key: 13
  instance_no: 0
  primary_key: 39
  undulator: UE112
  
get can also print simple scalar values::

  >>> get("id-data.UE112.global.device_status", "py")
  'installed'

If we don't want to have simple values printed as python literals, we can omit
the format specification ":py". In this case get uses the "raw" format, which
prints the raw values::

  >>> get("id-data.UE112.global.device_status")
  installed

If provided with a :ref:`pattern <reference-StructuredData-Patterns>` 
get returns a list if more than one path matches::

  >>> get("id-data.*.global.id-key")
  [96, 3, 110, 98, 97, 95, 12, 80, 7, 15, 13, 10, 8, 9, 11, 5, 81, 99]
  
Reports with find
-----------------

Find accepts *wildcards* in the path argument. Currently wildcard is just the
string "*". A path with optional wildcards is called a *pattern*. With this
feature we can print data for several paths with a single command. 

Here we print the "id-key" property for all devices::

  >>> find("id-data.*.global.id-key")
  id-data.U125/1.global.id-key : 96
  id-data.U125/2.global.id-key : 3
  id-data.U139.global.id-key   : 110
  id-data.U2.global.id-key     : 98
  id-data.U3.global.id-key     : 97
  id-data.U4.global.id-key     : 95
  id-data.U41.global.id-key    : 12
  id-data.U48.global.id-key    : 80
  id-data.U49/1.global.id-key  : 7
  id-data.U49/2.global.id-key  : 15
  id-data.UE112.global.id-key  : 13
  id-data.UE46.global.id-key   : 10
  id-data.UE49.global.id-key   : 8
  id-data.UE52.global.id-key   : 9
  id-data.UE56/1.global.id-key : 11
  id-data.UE56/2.global.id-key : 5
  id-data.UE56R.global.id-key  : 81
  id-data.Ubonsai.global.id-key: 99

The find command uses the "aligned" format as a default. It can also return
it's results in YAML or python. Note that find searches *all paths* in the
StructuredData to test if they match the given pattern. 

If you enter a path without wildcards, find returns the same as get would do
with the "aligned" format. However, find is much slower than get in this case
since it tests all paths where get directly uses the path provided.

Reports with rxfind
-------------------

rxfind tests all paths whether they match a regular expression. Regular
expressions are quite powerful for searching strings. Since a regular
expression may contain many special characters, we do not use *simplified
strings* here but use single quotes instead::

  >>> rxfind('.*UE56/2.*v_max')
  id-data.UE56/2.config.v_max_diff    : 0.1
  id-data.UE56/2.config.v_max_pos     : 185
  id-data.UE56/2.config.v_max_velocity: 2500

Like find, rxfind returns it's results in "aligned" format as a default.

Reports with findval
--------------------

This command looks for a given scalar in the StructuredData. Like the other
find commands it returns it's results in "aligned" format as default::

  >>> findval(20)
  id-data.U125/2.config.v_critical_pos       : 20.0
  id-data.U2.config.v_critical_pos           : 20.0
  id-data.U3.config.v_critical_pos           : 20.0
  id-data.U3.feedback.cc_tables              : 20
  id-data.U49/1.config.v_critical_pos        : 20.0
  id-data.UE112.config.coil_number           : 20
  id-data.UE56/2.feedback.cc_tables          : 20
  id-metadata.parameter-info.id-key.order_key: 20

If provided with a :ref:`pattern <reference-StructuredData-Patterns>` 
findval looks only at paths that match the given pattern::

  >>> findval(20, pattern="id-data.*.config.v_critical_pos")
  id-data.U125/2.config.v_critical_pos: 20.0
  id-data.U2.config.v_critical_pos    : 20.0
  id-data.U3.config.v_critical_pos    : 20.0
  id-data.U49/1.config.v_critical_pos : 20.0

You can now combine the results of findval from the example above with other
commands. In the following example we use the results from the query above. We
call "fun.findval" instead of "findval" and store it's results in variable "n".
We then modify the returned paths with 
":ref:`fun.substpath <SDpyshell-fun.substpath>`" and use 
":ref:`get <SDpyshell-get>`" with it's results.  In the end we get the values
of the property "devicename" for all the devices::

  >>> n=fun.findval(20, pattern="id-data.*.config.v_critical_pos")
  >>> get(fun.substpath(n, "id-data.*.names.devicename"))
  ['U49ID4R', 'U3IV', 'U2IV', 'U125ID2R']

Reports with rxfindval
----------------------

This command matches all scalar values with a given regular expression. Here is
an example::

  >>> rxfindval('.*-ppc')
  id-data.U125/2.config.target_arch : vxWorks-ppc603
  id-data.U139.config.target_arch   : vxWorks-ppc603
  id-data.U3.config.target_arch     : vxWorks-ppc603
  id-data.U41.config.target_arch    : vxWorks-ppc603
  id-data.U49/1.config.target_arch  : vxWorks-ppc603
  id-data.U49/2.config.target_arch  : vxWorks-ppc603
  id-data.UE112.config.target_arch  : vxWorks-ppc603
  id-data.UE46.config.target_arch   : vxWorks-ppc603
  id-data.UE49.config.target_arch   : vxWorks-ppc603
  id-data.UE52.config.target_arch   : vxWorks-ppc603
  id-data.UE56/1.config.target_arch : vxWorks-ppc603
  id-data.Ubonsai.config.target_arch: vxWorks-ppc603

Reports with pr
---------------

The pr command is used to print StructuredData or parts of it to the console.
Note that this is different from "print", which is the generic print command to
print any value (numbers, strings, data structures) to the console. 

pr filters it's results when a *pattern* is provided. As a default it returns
it's results in YAML format. pr usually would also print all the type
declarations. In this example we want only see the pure data, so we specify
only to print the "store" in the format specification::

  >>> pr("store", pattern="id-data.UE112.global.**")
  id-data:
      UE112:
          global:
              description: UE112  ,UE112ID7R,idcp13
              device_status: installed
              id-key: 13
              instance_no: 0
              primary_key: 39
              undulator: UE112

pr can also return it's results in csv format::

  >>> p("store:csv", pattern="id-data.UE112.global.**")
  id-data;UE112;global;description;UE112  ,UE112ID7R,idcp13
  id-data;UE112;global;device_status;installed
  id-data;UE112;global;id-key;13
  id-data;UE112;global;instance_no;0
  id-data;UE112;global;primary_key;39
  id-data;UE112;global;undulator;UE112

Changing a single value with change
-----------------------------------

This command is used to change an existing value. Here we read a value, change
it and then read it again::

  >>> get("id-data.Ubonsai.global.id-key")
  99
  >>> change("id-data.Ubonsai.global.id-key", 100)
  >>> get("id-data.Ubonsai.global.id-key")
  100

Note that for the change command, a node for the specified path must already
exist. If it doesn't, you get an error message::

  >>> change("id-data.Ubonsai.global.id-keyx", 101)
  path "id-data.Ubonsai.global.id-keyx" doesn't exist

Adding a value with put
-----------------------

The put command can create all parts of a path on the fly. It is not necessary
that all nodes for the specified path already exist.

Here is the node for path "id-data.U48.global" before the change::

  >>> get("id-data.U48.global", "py")
  {'description': 'U48    ,U48IV    ,idcp80,located in lund',
   'device_status': 'test',
   'id-key': 80,
   'instance_no': 0,
   'primary_key': 40,
   'undulator': 'U48'}

Now we add a value and create a new map on the fly::

  >>> put("id-data.U48.global.newdict.param1", 10)

This is how the node now looks like::

  >>> get("id-data.U48.global", "py")
  {'description': 'U48    ,U48IV    ,idcp80,located in lund',
   'device_status': 'test',
   'id-key': 80,
   'instance_no': 0,
   'newdict': {'param1': 10},
   'primary_key': 40,
   'undulator': 'U48'}

Working with links
------------------

For these examples we need to load another StructuredData file. We finish the
shell from the previous examples with CTRL-D and start another one::

  SDpython shell
  >>> r("NAMES.SDCyml")

In this example we use *links* at many places. The data was actually imported
from a relational database where foreign keys were replaced with links. 

An item is called a *link* when the referenced data is also referenced to at
one or more other places in StructuredData.

Here we print a single entry from the "names" list in python format::

  >>> get("names[9]", "py")
  {'description': 'Quadrupole GIS',
   'device_family': {'description': 'Geodesy', 'part_family': 'G'},
   'part_counter': '2',
   'part_index': '12',
   'part_name': 'Q',
   'part_subindex': '',
   'subdomain': {'description': 'Triplet Section 1',
                 'domain': {'description': 'Storage ring',
                            'facility': {'description': 'BESSY II Ring',
                                         'name': 'BII',
                                         'part_facility': ' '},
                            'part_domain': 'R'},
                 'part_postfix': '1',
                 'part_subdomain': 'T'}}

The map for the key "subdomain" is actually a link, but in the example above we
cannot see this (if we looked in the file "NAMES.SDCyml" we could). 

If we use find with the format "marklinks", links get a mark,
a star character at the end of a key::

  >>> find("names[9].**","marklinks")
  names[9].description                               : Quadrupole GIS
  names[9].device_family*.description                : Geodesy
  names[9].device_family*.part_family                : G
  names[9].part_counter                              : 2
  names[9].part_index                                : 12
  names[9].part_name                                 : Q
  names[9].part_subindex                             : 
  names[9].subdomain*.description                    : Triplet Section 1
  names[9].subdomain*.domain*.description            : Storage ring
  names[9].subdomain*.domain*.facility*.description  : BESSY II Ring
  names[9].subdomain*.domain*.facility*.name         : BII
  names[9].subdomain*.domain*.facility*.part_facility:  
  names[9].subdomain*.domain*.part_domain            : R
  names[9].subdomain*.part_postfix                   : 1
  names[9].subdomain*.part_subdomain                 : T

Each part of a path that has a star at the end is a link. Here we see that these paths are links:

* names[9].device_family
* names[9].subdomain
* names[9].subdomain.domain
* names[9].subdomain.domain.facility

We can also list all paths that refer to the same data for a given path with
the getlinks command.

First we show the links for the subdomain property::

  >>> getlinks("names[9].subdomain")
  - 03_subdomain[78]
  - names[9].subdomain

Here we show the links for the facility property::

  >>> getlinks("names[9].subdomain.domain.facility")
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

We can filter the results of such a query in order to see only paths that do
not match a pattern like this::

  >>> getlinks("names[9].subdomain.domain.facility", exclude="03_subdomain.*.domain.facility")
  - 01_facility[0]

Now we show how a link can be changed. In names[9] we want to assign a
different subdomain. This is done with the link command::

  >>> link("names[9].subdomain", "03_subdomain[44]")

If we print names[9] again we see that the subdomain (see the first get on
names[9] further above) has changed::

  >>> find("names[9].**", "marklinks")
  names[9].description                               : Quadrupole GIS
  names[9].device_family*.description                : Geodesy
  names[9].device_family*.part_family                : G
  names[9].part_counter                              : 2
  names[9].part_index                                : 12
  names[9].part_name                                 : Q
  names[9].part_subindex                             : 
  names[9].subdomain*.description                    : Doublet Section 2
  names[9].subdomain*.domain*.description            : Gallery/Supply Area/Infrastructure
  names[9].subdomain*.domain*.facility*.description  : BESSY II Ring
  names[9].subdomain*.domain*.facility*.name         : BII
  names[9].subdomain*.domain*.facility*.part_facility:  
  names[9].subdomain*.domain*.part_domain            : G
  names[9].subdomain*.part_postfix                   : 2
  names[9].subdomain*.part_subdomain                 : D

Working with types
------------------

The simplies action with types is to perform a typecheck of a
StructuredDataContainer file from the command line. Here is an example::

  > SDpyshell -c 'r("idcp_db.cache.SDCyml");typecheck()'
  all typechecks succeeded

We can, however, explore and change types in the interacticve shell. First we
start the shell and load the file "idcp_db.cache.SDCyml"::

  > SDpyshell 
  SDpython shell
  >>> r("idcp_db.cache.SDCyml")

We first print a certain value::

  >>> find("id-data.UE46.names.**", "aligned")
  id-data.UE46.names.devicename: UE46IT5R
  id-data.UE46.names.key       : 10
  id-data.UE46.names.name      : UE46
  id-data.UE46.names.prefix    : idcp10

We now want to know if a type is defined for this path. The typematch command
prints the matching type declaration if it finds one::

  >>> typematch("id-data.UE46.names")
  id-data.*.names:
      optional_struct:
      - devicename
      - key
      - name
      - prefix

The first line of the result is the matching pattern in the StructuredDataTypes
object. The part that follows is the type declaration.  We see that this is an
"optional_struct" meaning that this is a map where all keys must be keys of the
given list of keys but not all keys of the list must be present.

Now we want to see if there are type declarations for the members of this
"optional_struct". The typepaths command just prints the patterns without the
type declarations::

  >>> typepaths("id-data.*.names.*")
  - id-data.*.names.devicename
  - id-data.*.names.key
  - id-data.*.names.name
  - id-data.*.names.prefix

We want to see what the type declaration for path "id-data.*.names.devicename"
is::

  >>> typeget("id-data.*.names.devicename")
  string
  ...

The "..." is created by converting a simple string to YAML.

The typefind command can be used to print all types that match a pattern::

  >>> typefind("id-data.*.names.*")
  id-data.*.names.devicename: string
  id-data.*.names.key       : integer
  id-data.*.names.name      : string
  id-data.*.names.prefix    : string

Types can also be modified on the command line. We can for example remove an
item in the optional_struct::

  >>> typedeleteitem("id-data.*.names", "key")

If we verify the result we see that the item is gone::

  >>> typeget("id-data.*.names")
  optional_struct:
  - devicename
  - name
  - prefix

We can also add a new item::

  >>> typeadditem("id-data.*.names", "newkey")

We again verify the result::

  >>> typeget("id-data.*.names")
  optional_struct:
  - devicename
  - name
  - newkey
  - prefix

We can remove a complete type declaration::

  >>> typedelete("id-data.*.names.devicename")

We can add a type, even a complex one. For a *struct* for example we have to
provide a dictionary, we use *simplified strings* in this case. Note that the
space after ":" after "struct" is important. Without it SDpyshell would interpret
":[" as a string literal::

  >>> typeput("id-data.*.newnames", {"struct" : ["elm1", "elm2", "elm3" ]})

We verify the result::

  >>> typeget("id-data.*.newnames")
  struct:
  - elm1
  - elm2
  - elm3

A change of many parameters with export and re-import
-----------------------------------------------------

First we extract all parameters named "device_status" for all insertion
devices, we use the "flat" format in order to make the file more easily
editable::

  SDpyshell -c 'r("idcp_db.cache.SDCyml");w("PARAMS.TXT", "store:flat", pattern="id-data.*.global.device_status")'

The file "PARAMS.TXT" now looks like this::

  id-data.U125/1.global.device_status: test
  id-data.U125/2.global.device_status: installed
  id-data.U139.global.device_status: installed
  id-data.U2.global.device_status: simulated
  id-data.U3.global.device_status: test
  id-data.U4.global.device_status: test
  id-data.U41.global.device_status: installed
  id-data.U48.global.device_status: test
  id-data.U49/1.global.device_status: installed
  id-data.U49/2.global.device_status: installed
  id-data.UE112.global.device_status: installed
  id-data.UE46.global.device_status: installed
  id-data.UE49.global.device_status: installed
  id-data.UE52.global.device_status: installed
  id-data.UE56/1.global.device_status: installed
  id-data.UE56/2.global.device_status: installed
  id-data.UE56R.global.device_status: test
  id-data.Ubonsai.global.device_status: simulated

Now we can edit this file with a text editor or any program. In this example we
want to change all parameters that have the value "test" to the value
"installed". We do this with this perl one-liner::

  perl -pi -e 's/: test/: installed/' PARAMS.TXT

Now we want to merge these changes with the existing StructuredData file. We do
this with a single command line::

  SDpyshell -c 'r("idcp_db.cache.SDCyml"); r("PARAMS.TXT", "store:flat"); w("new.SDCyml")'

The "r" reads alls files "\*.SDCyml" in the current directory. The "sread"
command reads the file "PARAMS.TXT". It assumes a StructuredDataStore in YAML
and "flat" format. The data is merged with the StructuredData that was read
before. Already existing values are replaced with the new ones. The final
statement "w" writes the modified StructuredData to the file "new.SDCyml".

We control the changes with "diff"::

  diff idcp_db.cache.SDCyml new.SDCyml
  97c97
  <                 device_status: test
  ---
  >                 device_status: installed
  770c770
  <                 device_status: test
  ---
  >                 device_status: installed
  944c944
  <                 device_status: test
  ---
  >                 device_status: installed
  1260c1260
  <                 device_status: test
  ---
  >                 device_status: installed
  3131c3131
  <                 device_status: test
  ---
  >                 device_status: installed
  5702d5701
  < 

Converting a python structure to StructuredData
-----------------------------------------------

Let's assume that we have a file, pythonstruc.py with this content::

  { "key1": 1,
    "key2": { "A": "x",
              "B": "y"
            },
    "key3": [ 1, 2, 3, { "float": 1.23 }]
  }

We convert this directly with a single SDpyshell command line::

  SDpyshell -c 'r("pythonstruc.py", "store:py"); w("pythonstruc.SDCyml")'

The file pythonstruc.SDCyml now looks like this::

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
  '**SDC-Types**': {}


Converting a perl structure to StructuredData
---------------------------------------------

Let's assume that we have a file, perlstruc.pl with this content::

  %struc= ( "key1"=> 1,
            "key2"=> { "A"=> "x",
                       "B"=> "y"
                     },
            "key3"=> [ 1, 2, 3, { "float"=> 1.23 }]
          );

In order to convert this we first convert the perl structure to pure YAML
with this command line::
  
  perl -MYAML::XS -e 'require "perlstruc.pl";print Dump(\%struc);' > perlstruc.yml

Now we create a StructuredData file like this::
  
  SDpyshell -c 'r("perlstruc.yml", "store"); w("perlstruc.SDCyml")'

The file perlstruc.SDCyml now looks like this::

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
  '**SDC-Types**': {}


