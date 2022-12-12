# Introduction to Python iRODS Client (PRC) and VSC-PRC tools

*Prerequisites:*  
- *A KU Leuven account (u- or b-account) to access the KU Leuven iRODS zones*  
- *Basic knowledge of Python*    

This training introduces you to the basics of using the iRODS client API implemented in Python. The Python iRODS Client (PRC) is a programming client of iRODS. The main goal of PRC is to offer researchers means to manage their data in Python. Currently supported operations with PRC are varied and powerful enough to interact with iRODS without requiring any other tools.

## Goal of this training

You will learn how to use the PRC to interact with the KU Leuven iRODS infrastructure.
The following functionalities will be covered:

- Uploading and downloading data
- Uploading and downloading data collections
- Working with file-like objects
- Adding and editing metadata
- Managing permissions for data objects and collections
- Querying for data using user-defined metadata

## Configuration of the iRODS connection

We will use the environment file of iRODS to have a secure and longer session in PRC. 

### Using PRC on a Linux Machine

If you are using a Linux machine (including VMs and WSL2) you first need to connect to the KU Leuven iRODS portal (https://{yourZone}.irods.icts.kuleuven.be) and follow relevant instructions there:

- Copy the snippet on the section 'iCommands Client on Linux' of the KU Leuven iRODS portal.

- Open your terminal, paste and execute the copied snippet.

This way you will have created a temporary password that will expire 7 days later; once this password is expired, you will need to repeat the whole procedure to be able reconnect to iRODS.

You can initiate an iRODS session in a secure way with the PRC by using the code snippet below in your Python script or interactive session.

```py
import os
import ssl
from irods.session import iRODSSession

try:
    env_file = os.environ['IRODS_ENVIRONMENT_FILE']
except KeyError:
    env_file = os.path.expanduser('~/.irods/irods_environment.json')

ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None)
ssl_settings = {'ssl_context': ssl_context}
with iRODSSession(irods_env_file=env_file, **ssl_settings) as session:
    [your code here]
```

In an interactive session, for example, to follow the examples shown in this document, you might want to replace the `with` statement above with:

```py
session = iRODSSession(irods_env_file=env_file, **ssl_settings)
```

And at the end of your session clean up with:

```py
session.cleanup()
```

### Using PRC on a Windows Machine

If you are using a pure Windows machine (no available Linux OS via VMs and WSL2), there are two options that you can follow.

The first option:

- Copy the snippet on the section 'Python Client on Windows' of the KU Leuven iRODS portal.

    - If you want to use a conda environment, open your 'Anaconda Prompt', paste and execute the copied snippet.

    - If you want to use a non-conda installed python release, then open your 'Windows PowerShell', paste and execute the copied snippet.

The second option:

1. Download the [https://rdmrepo-proxy.icts.kuleuven.be/artifactory/coz-p-foz-generic-public/iinit.exe](iinit.exe) file; you will find this file &mdash; with a green iRODS icon &mdash; in your 'Downloads' folder.
    
2. Copy the 'iinit.exe' file in 'Downloads' and paste it inside a folder on your Windows PC that doesn't require administrator rights

3. Double click `iinit.exe` and enter your 'Zone' name in the pop-up terminal screen.

4. Once you type your zone name correctly, hit the enter button: you will be forwarded to your default screen to be notified that 'You have successfully authenticated' in addition to some information. The popped-up terminal will disappear in 8 seconds.

This way you will have created a temporary password that will expire 60 hours later; once this password is expired, you will need to repeat whole procedure (either all steps in the first option or only execute `iinit.exe` again) to be able reconnect to iRODS.

You don't have to follow all these steps every time: after you download `iinit.exe`, you can use it when you need to renew your password.

After you are authenticated to iRODS, you can initiate an iRODS session in a secure way with the PRC by using the code snippet below.

```py
import os, os.path
from irods.session import iRODSSession
env_file = os.getenv('IRODS_ENVIRONMENT_FILE', os.path.expanduser('~/.irods/irods_environment.json'))
with iRODSSession(irods_env_file=env_file) as session:
    [your code here]
```

We recommend you to use the second option, since it seems more user-friendly and fault tolerant.

## How to work with the PRC

As a best practice we recommend you to work with a virtual environment. There are several ways to create a virtual environment: you can choose any of them besides what we offered &mdash; conda &mdash; in the Quick Start Guide.

To be able to call Python code during the training and the exercises, you can choose one of the ways below:

- Make python scripts by using your favourite editor (vi, nano,...)
    - Execute them with `python3 <filename>` or
    - Add the shebang line in your script file to make it file executable (chmod +x) and execute it with `./filename`.
- Work interactively
    - With the default Python interpreter or
    - With IPython, a command shell for interactive programming in Python. (IPython is not installed by default, so you might need to install it using pip: e.g: `pip install --user ipython`).

**Note1:** The shebang line in any script determines the script's ability to be executed like a standalone executable without typing 'python' beforehand in the terminal.
In other words, the shebang line specifies exactly how to run a script. You can put `#!/usr/bin/env python3` as a first line in your PRC script file.

**Note2:** You can use the python builtin `dir()` function to know about all available attributes and methods for a given object. For instance, `[x for x in dir(coll) if not x.startswith('__') ]` gives you the methods of the 'coll' instance.

## Working with Collections

You can connect to a specific iRODS collection with `session.collections.get("/path/to/collection")`; this could be your home collection, project collection or any other sub-collection. After you instantiate the collection you prefer, you can see some basic information about it. The `subcollections` and `data_objects` attributes return lists of the sub-collections and data objects of this instantiated collection. Methods that will be discussed below allow you to create, move and remove the collection as well.

Let's retrieve our existing home collection:

```py
>>> coll = session.collections.get("/yourZone/home/userName")
```

The `path` attribute shows where the collection is stored, which is the same as the path given to access the collection.

```py
>>> coll.path
'/yourZone/home/userName'
```

You can see the subcollections and data objects of your instantiated collection as lists returned by the `subcollections` and `data_objects` attributes.

```py
>>> for col in coll.subcollections:
>>>   print(col)
<iRODSCollection 10010 b'subcol1'>
<iRODSCollection 10012 b'subcol2'>
```

```py
>>> for obj in coll.data_objects:
>>>   print(obj)
<iRODSDataObject 10022 file1.txt>
<iRODSDataObject 10023 file2.txt>
```

You can also use the `walk()` method to generate a collection tree and thus see all content of a requested collection:

```py
>>> for item in coll.walk():
>>>   print(item)
(<iRODSCollection 10001 B'userName'>, [<iRODSCollection 10010 b'subcol1'>, <iRODSCollection 10012 b'subcol2'>], [<iRODSDataObject 10022 file1.txt>, <iRODSDataObject 10023 file2.txt>])
(<iRODSCollection 10001 B'subcol1'>, [<iRODSCollection 10014 b'subsubcol1'>], [<iRODSDataObject 10031 subfile1.txt>])
(<iRODSCollection 10001 B'subcol2'>, [], [])
```

A new collection can be created by specifying its absolute iRODS path:

```py
>>> session.collections.create("/yourZone/home/userName/newCollection")
<iRODSCollection 10180 b'newCollection'>
```

**Note3:** If a collection you want to create already exists, `session.collections.create()` doesn't do anything: neither complains nor overwrites the existing collection.

## Working with Data Objects

PRC allows you to achieve pretty much any data object related operations, such as creating, deleting, uploading, downloading, copying and moving data objects. This is done via various methods of the `session.data_objects` object.

You can create a new data object with `session.data_objects.create()`:

```py
>>> obj = session.data_objects.create("/yourZone/home/userName/test.txt")
>>> obj
<iRODSDataObject 20223 test.txt>
```

The `put()` and `get()` methods allow you to upload data objects to iRODS or download them.

```py
>>> session.data_objects.get("/yourZone/home/userName/test.txt", "downloaded.txt")
<iRODSDataObject 20223 test.txt>
```

```py
>>> session.data_objects.put("downloaded.txt", "/yourZone/home/userName/uploaded.txt")
coll.data_objects[-1]
<iRODSDataObject 20233 uploaded.txt>
```

**Note4:** Data object transfers using `put()` and `get()` spawn a number of threads in order to optimize performance for file sizes larger than a default threshold value of 32 Megabytes. In other word, you are transferring in parallell if your transfer is bigger than 32 Megabytes.

If you want to completely delete a data object you can use the `unlink()` method. Unless you provide the argument `force=True`, you are only moving the data object to the trash collection.

```py
>>> session.data_objects.unlink("/yourZone/home/userName/uploaded.txt", force=True)
```

Copying a data object from one collection to another can be done with the `copy()` method:

```py
>>> session.data_objects.copy("/yourZone/home/userName/test.txt", "/yourZone/home/userName/test1/test.txt")
```

For any python object having a `__dict__` attribute, you can use the builtin `vars()` function to see useful information about the object.

```py
>>> b = session.data_objects.get("/yourZone/home/userName/test1/test.txt", "/yourLocalPath/test.txt")
>>> vars(b)
{'manager': <irods.manager.data_object_manager.DataObjectManager object at 0x7f534659ef10>,
'collection': <iRODSCollection 10183 b'test1'>,
'id': 10198,
'collection_id': 10183,
'name': 'test.txt',
'replica_number': 0,
'version': None,
'type': 'generic',
'size': 25,
'resource_name': 'netapp',
'path': '/yourZone/home/userName/test1/test.txt',
'owner_name': 'userName',
'owner_zone': 'yourZone',
'replica_status': '1',
'status': None,
'checksum': None,
'expiry': '00000000000',
'map_id': 0,
'comments': None,
'create_time': datetime.datetime(2021, 10, 20, 20, 39, 45),
'modify_time': datetime.datetime(2021, 10, 20, 20, 59),
'resc_hier': 'default;netapp',
'resc_id': '10014',
'replicas': [<irods.data_object.iRODSReplica netapp>],
'_meta': None}
```

### Getting and Setting Permissions

<!-- Maybe this should be in a common section or at the end of the "Working with collections" section, since it applies to both types of items -->

Via `session.permissions` and the `iRODSAccess` class, the PRC makes it possible to work with ACLs (Access Control Lists). You can list given permissions on a collection or on a data object as well as adding, modifying and removing ACLs.

Let's now create a new collection:

```py
>>> perm = session.collections.create("/yourZone/home/userName/permission")
>>> perm.path
'/yourZone/home/userName/permission'
```

You can list given permissions for a collection by providing it to `session.permissions.get()`:

```py
>>> acl_coll = session.permissions.get(perm)[0]
>>> acl_coll
<iRODSAccess own /yourZone/home/userName/permission userName yourZone>
```

In order to add or modify ACLs, you need to create an instance of the `iRODSAccess` class, which you should import first. When initializing an `iRODSAccess` object, you provide first the ACL ("own", "read" or "write") followed by the path to the data object or collection, the user or group, and finally the zone. Then this object is provided to `session.permissions.set()`.

```py
>>> from irods.access import iRODSAccess
>>> acl_dataObj = iRODSAccess("own", "/yourZone/home/userName/test.txt", "user2", "yourZone")
>>> session.permissions.set(acl_dataObj)
>>> data_obj = session.data_objects.get("/yourZone/home/userName/test.txt")
>>> acl_dataObj = session.permissions.get(data_obj)[0]
>>> acl_dataObj
<iRODSAccess own /yourZone/home/userName/test.txt user2 yourZone>
```

### Reading and Writing Files

Data objects in the PRC are represented by the `iRODSDataObject` class, which can be instantiated with the `.get()` and `.create()` methods of `session.data_objects`:

```py
>>> obj = session.data_objects.get("/yourZone/home/userName/test.txt")
```

This class has an `.open()` method that enables operations typically performed on files, such as reading and writing.
For example, let's write something in `obj`:

```py
>>> with obj.open('r+') as f:
...     f.write(b'Hello\nWorld\n')
```

And now let's read its contents.

```py
>>> with obj.open('r+') as f:
...     content = f.read()
>>> print(content)
b'Hello\nWorld\n'
```

### Computing and Retrieving Checksums

An object can be associated with a checksum, which is used to verify data integrity. In other words, you can compare the checksums of two data objects or a data object and a local file to make sure that the files are identical.

The `chksum()` method retrieves the checksum of an object if it is already in the iCAT catalogue, otherwise computes it and stores it.

```py
>>> obj.chksum()
'sha2:1j7C8s/wkIVp7pYG9ndGKhU2fjqW+6BNG+vz+fSDPYM='
```

If a checksum already was associated to a data object, you can use the `checksum` attribute to see it. It won't be available if you only just set it with the `chksum()` method.

```py
>>> obj.checksum
'sha2:1j7C8s/wkIVp7pYG9ndGKhU2fjqW+6BNG+vz+fSDPYM='
```

## Working with metadata

iRODS offers the possibility to add metadata to iRODS objects (collections, data objects, users or resources) in the form of tuples or triples of Attributes, Values and (optionally) Units, also called AVUs. The metadata of an object is represented by its `metadata` attribute, which you can manipulate in order to add, modify and remove metadata.

The list of all the metadata associated to a given data object can be retrieved via the `items()` method. This still works even if there is no metadata yet: it just returns an empty list.

```py
obj.metadata.items()
[]
```

AVUs can be added via the `add()` method, providing the attribute name, value and, optionally, unit. It is allowed to associate more than one value to an attribute of an object. Let's add AVUs to `obj`: 

```py
>>> obj.metadata.add('key1', 'value1', 'unit1')
>>> obj.metadata.add('key1', 'value2')
>>> obj.metadata.add('key2', 'value3', 'unit3')
>>> obj.metadata.add('key2', 'value3')
>>> obj.metadata.add('key3', 'value4')
>>> obj.metadata.items()
[<iRODSMeta 10220 key1 value1 unit1>,
<iRODSMeta 10221 key1 value2 None>,
<iRODSMeta 10222 key2 value3 unit3,
<iRODSMeta 10223 key2 value3 None>,
<iRODSMeta 10224 key3 value4 None>]
```

As you can see from the output, each AVU is represented by an `iRODSMeta` object. We can instantiate the class with `iRODSMeta(name, value[, unit])` after importing it from `irods.meta`. This is useful if we want to assign the same AVU to several objects or, for example, replace all the AVUs of `obj` with the same attribute name so they all have the same value and units. This can be done by subsetting `obj.metadata` with the name of the attribute, as shown below.

```py
>>> from irods.meta import iRODSMeta
>>> new_meta = iRODSMeta('key1','value5','unit2')
>>> new_meta
<iRODSMeta None key2 value5 unit2>
>>> new_meta.name
'key1'
>>> obj.metadata[new_meta.name] = new_meta
>>> obj.metadata.items()
[<iRODSMeta 10222 key2 value3 None>,
<iRODSMeta 10223 key2 value3 unit3,
<iRODSMeta 10224 key3 value4 None>,
<iRODSMeta 10226 key1 value5 units2>]
```

It is possible to get all metadata with a given attribute name via the `get_all()` method. 

```py
>>> obj.metadata.get_all('key2')
[<iRODSMeta 10222 key2 value3 None>, <iRODSMeta 10223 key2 value3 unit3>]
```

In order to remove an AVU, we can call the `remove()` method: we use the same arguments as in `add()`:

```py
>>> obj.metadata.remove('key1', 'value5', 'units2')
>>> obj.metadata.items()
[<iRODSMeta 10222 key2 value3 None>, <iRODSMeta 10223 key2 value3 unit3>, <iRODSMeta 10224 key3 value4 None>]
```

In order to remove all the existing metadata of an object at once, you can use `remove_all()` method:

```py
>>> obj.metadata.remove_all()
>>> obj.metadata.items()
[]
```

### Atomic operations on metadata

The PRC allows you to add and remove metadata in sequence with a single operation, i.e., a single call to the server. The `apply_atomic_operations()` method takes a series of `AVUOperation` objects as arguments and implements them in the order given. To the `AVUOperation()` call we specify the kind of operation ("remove" or "add") and the AVU involved as an `iRODSMeta` object. Therefore, we need to import both the `iRODSMeta` class (already imported above) and `AVUOperation`.

Let's remove and add some AVUs in one single call.

```py
>>> from irods.meta import AVUOperation
>>> obj.metadata.apply_atomic_operations( AVUOperation(operation='remove', avu=iRODSMeta('attr1','val1','unit1')),
...                                       AVUOperation(operation='add', avu=iRODSMeta('attr3','val3')),
...                                       AVUOperation(operation='add', avu=iRODSMeta('attr2','val2','unit2')),
...                                       AVUOperation(operation='remove', avu=iRODSMeta('attr2','val2','unit2')) )
>>> obj.metadata.items()
[<iRODSMeta 10229 attr3 val3 None>]
```

As you may have noticed, a "remove" operation will be ignored if the AVU provided does not exist as metadata of the target object yet.

This is particularly useful if you want to apply a pre-built list of `AVUOperation`s with Python's `*args` syntax. For example, below we can implement this technique in order to remove all AVUs with the "attr2" attribute name:

```py
>>> obj.metadata.apply_atomic_operations(AVUOperation(operation='add', avu=iRODSMeta('attr1','val1')),
...                                      AVUOperation(operation='add', avu=iRODSMeta('attr2','val2','unit2')),
...                                      AVUOperation(operation='add', avu=iRODSMeta('attr2','val3','unit2')) )
>>> obj.metadata.items()
[<iRODSMeta 10226 attr2 val3 unit2>, <iRODSMeta 10228 attr2 val2 unit2>, <iRODSMeta 10230 attr1 val1 None>]
>>> avus_on_object = obj.metadata.items()
>>> obj.metadata.apply_atomic_operations( *[AVUOperation(operation='remove', avu=i) for i in avus_on_object if i.name == 'attr2'] )
>>> obj.metadata.items()
[]
```

It is also possible to read metadata from a JSON file and apply them with `apply_atomic_operations()`. The code below opens "metadata_example.json", which is stored as a dictionary with attribute names as keys and values as values, and adds them via this technique.

```py
>>> import json
>>> with open("your/path/to/metadata_example.json") as jsonFile:
...    jsonObject = json.load(jsonFile)
...    avus = [item for item in jsonObject.items()]
...    obj.metadata.apply_atomic_operations(*[AVUOperation(operation='add', avu=iRODSMeta(str(meta[0]), str(meta[1]))) for meta in avus])
>>> obj.metadata.items()
[<iRODSMeta 11883 reviewerID A30TL5EWN6DFXT None>,
 <iRODSMeta 11884 asin 120401325X None>,
 <iRODSMeta 11886 helpful [0, 0] None>,
 <iRODSMeta 11887 reviewText They look good. None>,
 <iRODSMeta 11888 overall 4.0 None>,
 <iRODSMeta 11889 summary Looks Good None>,
 <iRODSMeta 11890 unixReviewTime 1400630400 None>,
 <iRODSMeta 11892 reviewerName Kaan None>,
 <iRODSMeta 11893 reviewTime 25.11.2021 None>]
```

## How to make queries

Different attributes of your objects, including the metadata, can be used to perform queries on your research data. This can be done with `session.query()` and a number of PRC classes imported from the `irods.models` module.

Class | Information about | Useful attributes
---- | ------ | ----------
`Collection` | A collection | `name`, `owner_name`, `id` ...
`DataObject` | A data object | `name`, `path`, `size`, `owner_name`, `id` ...
`CollectionMeta` | The metadata of a collection | `name`, `value`, `units`, ...
`DataObjectMeta` | The metadata of a data object | `name`, `value`, `units`, ...

The `session.query()` calls takes as argument the different kinds of information you want to be able to extract, such as `Collection.name` for the *path* of a collection or `Collection` to have all the collection's information available (not its metadata, though). Its output is a generator of results from which we can extract these different columns.

```py
>>> from irods.models import Collection, DataObject
>>> query = session.query(Collection.name, DataObject.name, DataObject.size)
>>> for result in query:
...     print(f'{result[Collection.name]}/{result[DataObject.name]} size={result[DataObject.size]}')
...
/yourZone/home/userName/1GB.bin size=0
/yourZone/home/userName/test.txt size=18
/yourZone/home/userName/test1/test.txt size=25
/yourZone/home/userName/test12/test.py size=545
/yourZone/home/userName/test2/test.txt size=25
/yourZone/home/userName/training/test.tar size=81920
/yourZone/home/userName/training/test1.txt size=28
/yourZone/home/userName/training/test1/alice1.txt size=74703
/yourZone/trash/home/userName/test.txt size=18
/yourZone/trash/home/userName/test.txt.2170015135 size=18
/yourZone/trash/home/userName/test1.txt size=12
```

An important feature when querying is to be able to filter the results based on some criteria. For this purpose we also have to import the `Criterion` class from the `irods.column` module. We then create criteria by instantiating the `Criterion` class with an operator (such as "=" or "like") and the elements under comparison, and provide them to the `filter()` method of the results.

For example, `Criterion('=', CollectionMeta.name, 'type')` below will filter the results that have an AVU with "type" as the attribute name; the subsequent call `Criterion('like', CollectionMeta.value, 'train%')` will further filter the results that have an AVU with the attribute value starting with "train". Notice that the classes used in the `Criterion()` instances do not need to be used in the `query()` call.

```py
>>> from irods.column import Criterion
>>> from irods.models import Collection, CollectionMeta

>>> results = session.query(Collection, CollectionMeta).filter( \
... Criterion('=', CollectionMeta.name, 'type')).filter( \
... Criterion('like', CollectionMeta.value, 'train%'))
>>> for item in results:
...     print(item[Collection.name], item[CollectionMeta.name], item[CollectionMeta.value], item[CollectionMeta.units])
...
/yourZone/home/userName/training type training iRODS
```

Other SQL-like functions are also available as methods of the results generator, such as `count()` and `sum()`, which also take the column classes discussed above as arguments.
For instance, the code below queries the data size and number of data objects you are owner of. It first initiates a query that will extract the `DataObject.owner_name` column, uses `count(DataObject.id)` to count the number of unique data objects, and finishes by computing the sum of the `DataObject.size` column. `print(query.execute())` will print a table with the results.

```py
>>> query = session.query(DataObject.owner_name).count(DataObject.id).sum(DataObject.size)
>>> print(query.execute())
+--------------+-----------+-----------+
| D_OWNER_NAME | D_DATA_ID | DATA_SIZE |
+--------------+-----------+-----------+
| userName     | 11        | 157312    |
+--------------+-----------+-----------+
```

**Note5:** There is a small discrepancy between some of the attributes used in queries and outside of them. First, `Collection.name` will return the *path* to a collection (`Collection.path` does not exist). Given a collection `col`, this is the same as printing `col.path`. In contrast, `col.name` will print the name of the collection, e.g. if `col.path` is "/yourZone/home/userName/training", `col.name` is "training". Second, `DataObject.path` will return the location where the data object is *physically stored*, whereas `obj.path` will return the path of the parent collection followed by `obj.name`. Therefore, in order to obtain the path to a data object via a query, you should **not** extract `DataObject.path` but `Collection.name + '/' + DataObject.name`.

#  Exercises

Let's do the exercises below! 


Before starting the exercises, please clone the [git repository](https://github.com/kuleuven/iRODS-User-Training) of this training.
You will find files for the exercises in the 'data' directory.

### Exercise 1: uploading data

Make a script that does the following:

- Make a collection in your home called 'molecules'  
Tip: if you already had this folder from another training session, you can remove it via the command line with `irm -r molecules` or from Python with `os.rmdir(os.getcwd() + "molecules")`.
- Upload all files from the molecules directory
- Add the AVU 'kind: organic' to any organic molecules.
- Add the AVU 'kind: inorganic' to any inorganic molecules.  
Tip: organic molecules are the ones which have carbon (C) atoms inside of them.  
Feel free to take a look inside of the files.


<details>
    <summary>Solution</summary>

Step by step:

<details>
    <summary>Starting an iRODS session</summary>
    
```py    
import os
import ssl
from irods.session import iRODSSession
try:
    env_file = os.environ['IRODS_ENVIRONMENT_FILE']
except KeyError:
    env_file = os.path.expanduser('~/.irods/irods_environment.json')

ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None)
ssl_settings = {'ssl_context': ssl_context}

# Creating a session
with iRODSSession(irods_env_file=env_file, **ssl_settings) as session:
```    

</details>

<details>
    <summary>Creating a collection</summary>
    
```py
    collection = session.collections.create("/zone/home/username/molecules")
```    

</details>

<details>
    <summary>Uploading the files</summary>
    
```py    
    # Listing the files
    # This can be hardcoded, but with the os module, 
    # we can also do this automatically.
    directory = "/path/to/the/molecules/directory"
    files = os.listdir(directory)
```  

```py 
    # uploading files
    for filename in files:
        source = directory + "/" + filename
        destination = collection.path + "/" + filename
        session.data_objects.put(source, destination)
```

</details>


<details>
    <summary>Adding metadata</summary>
    
```py    
    # adding metadata to organic molecules
    organic_molecules = ["c6h6.xyz", "ch2och2.xyz", "ch3cooh.xyz", "isobutene.xyz"]
    attribute = "kind"
    value = "organic"
    for molecule in organic_molecules:
        obj = session.data_objects.get(collection.path + "/" + molecule)
        obj.metadata.add(attribute, value)



    # adding metadata to inorganic molecules
    inorganic_molecules = ["alcl3.xyz","no2.xyz","sih4.xyz"]
    # the variable 'attribute' is still set to 'kind'
    value = "inorganic"
    for molecule in inorganic_molecules:
        obj = session.data_objects.get(collection.path + "/" + molecule)
        obj.metadata.add(attribute, value)
```    

</details>

</details>



### Exercise 2: stage in/stage out

Make a script that does the following:
- Make a local folder with the name 'molecules'  
- Download all molecule files from iRODS to the local molecules folder
- Count the total amount of hydrogen atoms in these files
- Write the result to a file called 'hydrogen_count.txt'
- Upload hydrogen_count.txt to the 'molecules' collection in iRODS


<details>
    <summary>Solution</summary>

The amount of hydrogen atoms is 26.    

Step by step:

<details>
    <summary>Starting an iRODS session</summary>
    
```py    
import os
import ssl
from irods.session import iRODSSession
try:
    env_file = os.environ['IRODS_ENVIRONMENT_FILE']
except KeyError:
    env_file = os.path.expanduser('~/.irods/irods_environment.json')

ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None)
ssl_settings = {'ssl_context': ssl_context}

# Creating a session
with iRODSSession(irods_env_file=env_file, **ssl_settings) as session:
```    

</details>

<details>
    <summary>Making a local directory for the files</summary>
    
```py
    current_directory = os.getcwd()
    os.makedirs(current_directory + "/molecules")    
```    

</details>

<details>
    <summary>Downloading the files</summary>
    
```py 
    collection = session.collections.get("/zone/home/username/molecules")
        for data_object in collection.data_objects:
            session.data_objects.get(data_object.path, './molecules')
```    

</details> 

<details>
    <summary>Counting the hydrogen atoms and writing the result to a file</summary>
    
```py    
    # Counting hydrogen atoms
    hydrogen_count=0
    for i in os.listdir("./molecules"):
        with open("./molecules/"+i, "r") as file:
            for character in file.read():
                if character == "H":
                    hydrogen_count += 1
    
    # Write hydrogen count to a file
    with open("hydrogen_count.txt", 'w') as file:
        file.write(str(hydrogen_count))
```    

</details>

<details>
    <summary>Uploading the result to iRODS</summary>
    
```py    
    # Upload results to iRODS
    session.data_objects.put("hydrogen_count.txt", "/zone/home/username/molecules/hydrogen_count.txt")
```    

</details>

</details>

### Exercise 3: searching files based on metadata

Adapt your script from the previous exercise:  
instead of downloading all data objects, make a query that
lists the data objects with the AVU 'kind: organic', and downloads these.  
The rest of the script can stay the same.

Which number of hydrogen atoms do you get now? 

<details>
<summary>Solution</summary>

Add the following import statements to your script, 
for example at the beginning:

```py
from irods.column import Criterion
from irods.models import DataObject, DataObjectMeta, Collection
```

Then, replace the following part 

```py 
    collection = session.collections.get("/zone/home/username/molecules")
        for data_object in collection.data_objects:
            session.data_objects.get(data_object.path, './molecules')
```    

with this:

```py
    # Executing the query
    results = session.query(Collection.name, DataObject.name).filter( \
        Criterion("=", DataObjectMeta.name, "kind")).filter( \
        Criterion("=", DataObjectMeta.value, "organic"))

    # Downloading the files        
    for result in results:
        dataobject_path = result[Collection.name] + "/" + result[DataObject.name]
        session.data_objects.get(dataobject_path, './molecules')
``` 

The hydrogen count should now be 22.


</details>