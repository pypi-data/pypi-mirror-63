Various ways of accessing the data
==================================

Here we show how StructuredData can be accessed with and without the usage of
SDpyshell.

Note that the examples are ordered from the simple ones that use SDpyshell down
to examples that do not use StructuredData libraries at all but just the pure
YAML libraries. All examples assume that you are in the directory "samples" and
that the file idcp_db.cache.SDCyml is present there. You can get "samples"
directory by checking out the source from the mercurial repository.

An example with SDpyshell
-------------------------

Hepyre is the same example using the SDshell::
Here is the same example using the SDshell::

  SDpyshell 
  > r("idcp_db.cache.SDCyml")
  > get("id-data.U125/1.global.id-key")
  96
  > get("id-data.U125/1.global", "py")
  {'description': 'U125/1 ,U125IV   ,idcp96,currently disabled',
   'device_status': 'test',
   'id-key': 96,
   'instance_no': 0,
   'primary_key': 29,
   'undulator': 'U125/1'}
  > get("id-data.U125/1.global", "yaml")
  description: U125/1 ,U125IV   ,idcp96,currently disabled
  device_status: test
  id-key: 96
  instance_no: 0
  primary_key: 29
  undulator: U125/1
  > find("id-data.U125/1.global.**")
  id-data.U125/1.global.description  : U125/1 ,U125IV   ,idcp96,currently disabled
  id-data.U125/1.global.device_status: test
  id-data.U125/1.global.id-key       : 96
  id-data.U125/1.global.instance_no  : 0
  id-data.U125/1.global.primary_key  : 29
  id-data.U125/1.global.undulator    : U125/1

An example using the SDshellib
------------------------------

Here is the same example using the python shell and the SDshelllib::

  python
  >>> from StructuredData.SDshelllib import *
  >>> read("idcp_db.cache.SDCyml")
  >>> get("id-data.U125/1.global.id-key")
  96
  >>> get("id-data.U125/1.global", "py")
  {'description': 'U125/1 ,U125IV   ,idcp96,currently disabled',
   'device_status': 'test',
   'id-key': 96,
   'instance_no': 0,
   'primary_key': 29,
   'undulator': 'U125/1'}
  >>> get("id-data.U125/1.global", "yaml")
  description: U125/1 ,U125IV   ,idcp96,currently disabled
  device_status: test
  id-key: 96
  instance_no: 0
  primary_key: 29
  undulator: U125/1
  >>> find("id-data.U125/1.global.**")
  id-data.U125/1.global.description  : U125/1 ,U125IV   ,idcp96,currently disabled
  id-data.U125/1.global.device_status: test
  id-data.U125/1.global.id-key       : 96
  id-data.U125/1.global.instance_no  : 0
  id-data.U125/1.global.primary_key  : 29
  id-data.U125/1.global.undulator    : U125/1

An example using StructuredData.Classes
---------------------------------------

Here is a simple example of using StructuredData in the python shell with
StructuredData.Classes::

  python
  >>> import pprint
  >>> import yaml
  >>> import StructuredData.Classes as SD
  >>> sdc= SD.StructuredDataContainer.from_yaml_file("idcp_db.cache.SDCyml")
  >>> sds= sdc.store()
  >>> sds["id-data.U125/1.global.id-key"]
  96
  >>> pprint.pprint(sds["id-data.U125/1.global"])
  {'description': 'U125/1 ,U125IV   ,idcp96,currently disabled',
   'device_status': 'test',
   'id-key': 96,
   'instance_no': 0,
   'primary_key': 29,
   'undulator': 'U125/1'}
  >>> print yaml.dump(sds["id-data.U125/1.global"], 
  ...                 indent=4, default_flow_style= False)
  description: U125/1 ,U125IV   ,idcp96,currently disabled
  device_status: test
  id-key: 96
  instance_no: 0
  primary_key: 29
  undulator: U125/1
   

An example with python and pure yaml
------------------------------------

This example uses python and just YAML::

  python
  >>> import pprint
  >>> import yaml
  >>> stream= file("idcp_db.cache.SDCyml")
  >>> container= yaml.load(stream)
  >>> store=container["**SDC-Store**"]
  >>> store["id-data"]["U125/1"]["global"]["id-key"]
  96
  >>> pprint.pprint(store["id-data"]["U125/1"]["global"])
  {'description': 'U125/1 ,U125IV   ,idcp96,currently disabled',
   'device_status': 'test',
   'id-key': 96,
   'instance_no': 0,
   'primary_key': 29,
   'undulator': 'U125/1'}
  >>> print yaml.dump(store["id-data"]["U125/1"]["global"],
  ...                 indent=4, default_flow_style= False)
  description: U125/1 ,U125IV   ,idcp96,currently disabled
  device_status: test
  id-key: 96
  instance_no: 0
  primary_key: 29
  undulator: U125/1

An example with perl and pure yaml
----------------------------------

Since perl has no interactive shell, you have to create a file "SDtest.pl" with
this content::

  use Data::Dumper;
  use YAML::XS;
  use strict;
  $YAML::Syck::ImplicitTyping = 1;
  my $container= YAML::XS::LoadFile("idcp_db.cache.SDCyml");
  my $store= $container->{"**SDC-Store**"};
  print $store->{"id-data"}{"U125/1"}{"global"}{"id-key"},"\n";
  print Dumper($store->{"id-data"}{"U125/1"}{"global"});

If you start this file with::

  perl SDtest.pl

you get this output::

  96
  $VAR1 = {
            'primary_key' => 29,
            'instance_no' => 0,
            'id-key' => 96,
            'undulator' => 'U125/1',
            'device_status' => 'test',
            'description' => 'U125/1 ,U125IV   ,idcp96,currently disabled'
          };


