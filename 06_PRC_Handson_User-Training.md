# Introduction to Python iRODS Client (PRC) and VSC-PRC tools

*Prerequisites:*  
*-A KU Leuven account (u- or b-account) to access the KU Leuven iRODS zones*  
*-Basic knowledge of Python*    

This training introduces you to the basics of using the iRODS client API implemented in Python. The Python iRODS Client (PRC) is a programming client of iRODS. The main goal of PRC is to offer researchers means to manage their data in python. With the help of this client, users can manage their research data. Currently supported operations with PRC are quite various and enough to interact with iRODS without requiring any other tools.

## Goal of this training

You will learn how to use the PRC to interact with the KU Leuven iRODS infrastructure.
The following functionalities will be covered:

- Uploading and downloading data
- Uploading and downloading data collections
- Working with file-like objects
- Adding and editing metadata
- Managing persmissions for data objects and collections
- Querying for data using user defined metadata

## Configuration of the iRODS connection

We will use the environment file of iRODS to have a secure and longer session in PRC. 

### Using PRC on a Linux Machine

If you are using a Linux machine (including VMs and WSL2) you first need to connect to the KU Leuven iRODS portal (https://{yourZone}.irods.icts.kuleuven.be) and please follow relevant instructions there as you will see more explicitly here:

- Copy the snippet on the section 'iCommands Client on Linux' of the KU Leuven iRODS portal,

- Open your terminal, paste and execute the copied snippet,

- So that you will have created a temporary password that will expire 7 days later and once this password is expired, you will need to repeat whole procedure to be able reconnect to iRODS,

- You can initiate an iRODS session in a secure way with the PRC by using the code snippet below.

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

### Using PRC on a Windows Machine

If you are using a pure Windows machine (no available Linux OS via VMs and WSL2), there are two options that you can follow.

The first option:

- Copy the snippet on the section 'Python Client on Windows' of the KU Leuven iRODS portal,

- If you want to use conda environment, open your 'Anaconda Prompt', paste and execute the copied snippet,

- If you want to use non-conda installed python release, then open your 'Windows PowerShell', paste and execute the copied snippet.

The second option:

- Click the link here https://rdmrepo-proxy.icts.kuleuven.be/artifactory/coz-p-foz-generic-public/iinit.exe to download the 'iinit.exe' file,

- You will find this file -green iRODS icon- in your 'Downloads' folder. Copy the 'iinit.exe' file in 'Downloads' and paste it inside a folder on your windows pc which doesnt require an admin right,

- Double clicking `iinit.exe` will pop up an terminal screen and will ask you to enter your 'zone' name,

- Once you type your zone name correctly, hit the enter button,

- You will be forwarded to your default screen to be notified about that 'You have successfully authenticated' in addition to some information,

- So that you will have created a temporary password that will expire 7 days later and once this password is expired, you will need to repeat whole procedure to be able reconnect to iRODS,

- The popped-up terminal will disappear in 8 seconds.

- Each time you dont have to follow all steps. After you download `iinit.exe`, you can use it when you need to renew your password.

After you are authenticated to iRODS, you can initiate an iRODS session in a secure way with the PRC by using the code snippet below.

```py
import os, os.path
from irods.session import iRODSSession
env_file = os.getenv('IRODS_ENVIRONMENT_FILE', os.path.expanduser('~/.irods/irods_environment.json'))
with iRODSSession(irods_env_file=env_file) as session:
    [your code here]
```

We recommend you to use the second option since it seems more user-friendly and fault tolerant.

### How to work with the PRC

As a best practie we recommend you to work with a virtual enviroment. There are several ways to create a virtual enviroment. You can choose one of them besides what we offered - conda - in the Quick Start Guide.

To be able to call python codes during the traing and the exercises, you can choose one of the ways below:

- Make pythonscripts by using your favourite editor (vi, nano,...) and execute them with `python3 <filename>`. 
- Add the shebang line in your script file and make your file executable (chmod +x) and execute the file `./filename`.
- Alternatively, you can open the python interpreter and work interactively.
- Or you can use IPython (Interactive Python) which is a command shell for interactive programming in python. (The iPython is not installed by default, so you will need to install it using pip: e.g: pip install --user ipython)

**Note1:** The shebang line in any script determines the script's ability to be executed like a standalone executable without typing 'python' beforehand in the terminal. In other words, the shebang
line specifies exactly how to run a script. You can put this `#!/usr/bin/env python3` as a first line in your PRC script file.

**Note2:** You can use pyhton builtin `dir()` function to know about all available attributes and methods that you may use. For instance, `[ x for x in dir(col) if not x.startswith('__') ]` snippet gives you the methods of 'coll' instance.

## Working with Collections

You can connect to a specific iRODS collection, this could be your home collection, project collection or any other sub-collection. After you instantiate the collection you prefer, you can see some basic information of this collection. You can list the sub-collections and data objects of this instantiated collection. Also you can do some certain operations (cretae, move, remove etc.) with collections' methods.

You can instantiate a collection you want:

```py
>>> coll = session.collections.get("/yourZone/home/userName")
```

You can look into the information that you can acquire:

```py
>>> coll.path
/tempZone/home/rods
```

You can see the subcollections and data objects of your instantiated collection:

```py
>>> for col in coll.subcollections:
>>>   print(col)
<iRODSCollection /yourZone/home/userName/subcol1>
<iRODSCollection /yourZone/home/userName/subcol2>
```

```py
>>> for obj in coll.data_objects:
>>>   print(obj)
<iRODSDataObject /yourZone/home/userName/file1.txt>
<iRODSDataObject /yourZone/home/userName/file2.txt>
```

You can use `walk()` method to generate a collection tree. You can use this method to be able to see all content of a requested collection:

```py
>>> for item in coll.walk():
>>>   print(item)
< your collection tree >
```

You can create a new collection by specifying its absolute iRODS path:

```py
>>> coll = session.collections.create("/yourZone/home/userName/newCollection")
<iRODSCollection 10180 b'newCollection'>
```

**Note3:** If a collection you want to create already exists, the PRC doesn't do anything, neither complains nor overwrites on the existed collection. Also, you can create a collection recursively.

## Working with Data Objects

You can more or less achieve all data object related operations via the PRC. Some of these operations are creating a new data object, deleting a data object, uploading/downloading a data object, copying or moving a data object.

To create a new data object, you can use the code snippet below:

```py
>>> obj = session.data_objects.create("/yourZone/home/userName/test_data")
<iRODSDataObject /yourZone/home/userName/test_date>
```

You can upload a data object to iRODS:

```py
>>> session.data_objects.put("test.txt","/yourZone/home/userName/test.txt")
```

You can download a data object:

```py
>>> session.data_objects.get("/yourZone/home/userName/test.txt", "/yourLocalPath/test.txt")
<iRODSDataObject 10193 test.txt>
```

**Note4:** Data object transfers using put() and get() spawn a number of threads in order to optimize performance for file sizes larger than a default threshold value of 32 Megabytes. In other word, you are transferring parallelly if your transfer is bigger than 32 Megabytes.

If you want to completely delete a data object you can use the code snippet below. Unless you dont provide the keyword argument `force=True`, you in fact move the data object you want to delete to the trash colletion.

```py
>>> session.data_objects.unlink("/yourZone/home/userName/test.txt", force=True)
```

From one collection to another one you can copy a data object:

```py
>>> session.data_objects.copy("/yourZone/home/userName/test.txt", "/yourZone/home/userName/test1/test.txt")
```

For the python object having the `__dict__` attribute, you can use the builtin `vars()` function to see many useful information about the objest you instantiated.

```py
>>> b=session.data_objects.get("/yourZone/home/userName/test1/test.txt", "/yourLocalPath/test.txt")
>>> vars(b)
{'manager': <irods.manager.data_object_manager.DataObjectManager object at 0x7f534659ef10>, 'collection': <iRODSCollection 10183 b'test1'>, 'id': 10198, 'collection_id': 10183, 'name': 'test.txt', 'replica_number': 0, 'version': None, 'type': 'generic', 'size': 25, 'resource_name': 'netapp', 'path': '/yourZone/home/userName/test1/test.txt', 'owner_name': 'userName', 'owner_zone': 'yourZone', 'replica_status': '1', 'status': None, 'checksum': None, 'expiry': '00000000000', 'map_id': 0, 'comments': None, 'create_time': datetime.datetime(2021, 10, 20, 20, 39, 45), 'modify_time': datetime.datetime(2021, 10, 20, 20, 59), 'resc_hier': 'default;netapp', 'resc_id': '10014', 'replicas': [<irods.data_object.iRODSReplica netapp>], '_meta': None}
```

### Getting and Setting Permissions

The PRC make it possible to work with ACLs (Access Control Lists). You can list given permissions on a collection or on a data object. Also, adding a new ACL and modifying an existing one on a collection/data object in iRODS via the PRC is possible.

Let's now create a new collection:

```py
>>> coll = session.collections.create("/yourZone/home/userName/permission")
>>> coll.path
'/yourZone/home/userName/permission'
```

You can list given permissions for a collection:

```py
>>> acl_coll = session.permissions.get(coll)[0]
>>> acl_coll
<iRODSAccess own /yourZone/home/userName/permission u0137480 yourZone>
```

You can add a new permission or change the existing one. To be able to add/modify ACLs, you should import relevant classes:

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

The PRC provides us working with file-like objects. A file object in python is an object exposing an API having methods for performing operations typically done on files, such as read() or write(). So that we can read or write on a data object in iRODS.

You can read a data object:

```py
>>> obj = session.data_objects.get("/yourZone/home/userName/test.txt")
>>> with obj.open('r+') as f:
...     f.read()
...
b'This a test file.\n'
```

You can write on a data object:

```py
>>> obj = session.data_objects.get("/yourZone/home/userName/test1.txt")
>>> with obj.open('r+') as f:
...     f.write(b'Hello\nWorld\n')
...     for line in f:
...         print(line)
b'Hello\n'
b'World\n'
```

### Computing and Retrieving Checksums

You can associate a checksum on the object in question. Checksums are used to verify data integrity upon data moving.

By calling `chksum()` on an object you can add a cheksum, what this method does is to compute the checksum if already in the catalog, otherwise to compute and store it.

```py
>>> obj = session.data_objects.get("/yourZone/home/userName/test.txt")
>>> obj.chksum()
'sha2:1j7C8s/wkIVp7pYG9ndGKhU2fjqW+6BNG+vz+fSDPYM='
```

If a checksum already is associated to the data object at stake, then you can use `checksum` attribute to see it.

```py
>>> obj.checksum
'sha2:1j7C8s/wkIVp7pYG9ndGKhU2fjqW+6BNG+vz+fSDPYM='
```

## Working with metadata

iRODS offers a possibility to add metadata to iRODS objects (collection, data object, user, resource) in the form of tuples or triples (Attribute-Value-[Unit]), also called AVUs. You can add, manipulate and remove metadata via the PRC. 

If you check a file that no metadata attached to, then you will see an empty list. You can check all associated metadata with `items()` method:

```py
>>> obj = session.data_objects.get("/yourZone/home/userName/test.txt")
>>> print(obj.metadata.items())
[]
```

You can add metadata in an AVU format as many as you want. You can associate more than one valu to an attribute. Let's add AVUs to the `test.txt` data object:  

```py
>>> obj.metadata.add('key1', 'value1', 'unit1')
>>> obj.metadata.add('key1', 'value2')
>>> obj.metadata.add('key2', 'value3')
>>> obj.metadata.add('key2', 'value3', 'unit3')
>>> obj.metadata.add('key3', 'value4')
>>> print(obj.metadata.items())
[<iRODSMeta 10220 key1 value1 unit1>, <iRODSMeta 10221 key1 value2 None>, <iRODSMeta 10222 key2 value3 None>, <iRODSMeta 10223 key3 value4 None>]
```

You can also use Python's item indexing syntax to perform the equivalent of an `imeta set`, e.g. overwriting all AVU's with a name field of "key1" in a single update. However, we have to first import a relevant module:

```py
>>> from irods.meta import iRODSMeta
>>> new_meta = iRODSMeta('key1','value5','units2')
>>> obj.metadata[new_meta.name] = new_meta
>>> print(obj.metadata.items())
[<iRODSMeta 10222 key2 value3 None>, <iRODSMeta 10227 key2 value3 unit3, <iRODSMeta 10223 key3 value4 None>, <iRODSMeta 10226 key1 value5 units2>]
```

It is possible to get all metadata given with a unique attribute by `get_all()` method. 

```py
>>> obj.metadata.get_all('key2')
[<iRODSMeta 10222 key2 value3 None>, <iRODSMeta 10227 key2 value3 unit3>]
```

You can delete an attached metadata by `remove()` method. You should here specify the AVU you want to remove:

```py
>>> obj.metadata.remove('key1', 'value5', 'units2')
>>> obj.metadata.items()
[<iRODSMeta 10222 key2 value3 None>, <iRODSMeta 10223 key3 value4 None>, <iRODSMeta 10227 key2 value3 unit3>]
```

However, if you want to remove all existing metadata on an object at once, then you can use `remove_all()` method without an argument:

```py
>>> obj.metadata.remove_all()
>>> obj.metadata.items()
[]
```

### Atomic operations on metadata

The PRC allows a group of metadata add and remove operations to be performed transactionally, within a single call to the server. This does mean you can apply atomic operations on metadata. In onther words, you can add more than one AVU and also remove metadat at the same operation. One important thing to know is that the list of operations will be applied in the order given.

To be able to work with atomic operations, you should import relevant classes:

```py
>>> from irods.meta import iRODSMeta, AVUOperation
>>> obj.metadata.apply_atomic_operations( AVUOperation(operation='remove', avu=iRODSMeta('attr1','val1','unit1')),
...                                       AVUOperation(operation='add', avu=iRODSMeta('attr3','val3')),
...                                       AVUOperation(operation='add', avu=iRODSMeta('attr2','val2','unit2')),
...                                       AVUOperation(operation='remove', avu=iRODSMeta('attr2','val2','unit2')) )
>>> obj.metadata.items()
[<iRODSMeta 10229 attr3 val3 None>]
```

You have noticed that a "remove" operation will be ignored if the AVU value given does not exist on the target object at that point in the sequence of operations.

You can also use a pre-built list of AVUOperations using Python's f(*args_list) syntax. For example, this function uses the atomic metadata API to very quickly remove all AVUs from an object:

```py
>>> obj.metadata.apply_atomic_operations(AVUOperation(operation='add', avu=iRODSMeta('attr1','val1')), AVUOperation(operation='add', avu=iRODSMeta('attr2','val2','unit2')), )
>>> obj.metadata.items()
[<iRODSMeta 10228 attr2 val2 unit2>, <iRODSMeta 10230 attr1 val1 None>]
>>> avus_on_object = obj.metadata.items()
>>> obj.metadata.apply_atomic_operations( *[AVUOperation(operation='remove', avu=i) for i in avus_on_object] )
>>> obj.metadata.items()
[]
```

It is possible to read a json object both on your local machine and iRODS and add these keys/values as metadata to an iRODS object (file/folder).

You can read a json file on your local pc and attach these keys and values as metadata to your data object:

```py
>>> import json
>>> with open("your/path/to/metadata_example.json") as jsonFile:
...    jsonObject = json.load(jsonFile)
...    avus = [item for item in jsonObject.items()]
...    obj.metadata.apply_atomic_operations(*[AVUOperation(operation='add', avu=iRODSMeta("{}".format(str(meta[0]))
...    , "{}".format(str(meta[1])))) for meta in avus])
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

The PRC offers different query options that you can use based on your need. You may use these queries in your script to easily manage your research data.

First we will make a general query based on collection and data object classes:

```py
>>> from irods.models import Collection, DataObject
>>> query = session.query(Collection.name, DataObject.name, DataObject.size)
>>> for result in query:
...     print('{}/{} size={}'.format(result[Collection.name], result[DataObject.name], result[DataObject.size]))
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

Let's now make a query based on some criterias that we know already with the metadata assuming provided earlier. FIrst we have to import relevant sub modules. We will make our query based on collection and collection metadata. Also we will filter according to the criterias that we specify:

```py
>>> from irods.column import Criterion
>>> from irods.models import DataObject, DataObjectMeta, Collection, CollectionMeta

>>> results = session.query(Collection, CollectionMeta).filter( \
... Criterion('=', CollectionMeta.name, 'type')).filter( \
... Criterion('like', CollectionMeta.value, 'train%'))
>>> for item in results:
...     print(item[Collection.name], item[CollectionMeta.name], item[CollectionMeta.value], item[CollectionMeta.units])
...
/yourZone/home/userName/training type training iRODS
```

For instance, you can query the data size and and quantity of the data object you are owner of.

```py
>>> query = session.query(DataObject.owner_name).count(DataObject.id).sum(DataObject.size)
>>> print(query.execute())
+--------------+-----------+-----------+
| D_OWNER_NAME | D_DATA_ID | DATA_SIZE |
+--------------+-----------+-----------+
| userName     | 11        | 157312    |
+--------------+-----------+-----------+
```

#  Exercises

Let's do the exercises below! 


Before starting the exercises, please clone the [git repository](https://github.com/kuleuven/iRODS-User-Training) of this training.
You will find files for the exercises in the 'data' directory.

### Exercise 1: uploading data

Make a script that does the following:

- Make a collection in your home called 'molecules'  
Tip: if you already had this folder from another training session, you can remove it via the command line with `irm -r molecules`
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