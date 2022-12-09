# iCommands for KU Leuven Users

*Prerequisites:*  
- *A Linux client environment - a linux based operation system and terminal*  
- *A KU Leuven account (u- or b-account) to access the KU Leuven iRODS zones*  
- *Basic knowledge of command line (Bash) is useful*  

This tutorial introduces iCommands, which give users a command-line interface to iRODS, and shows you how to perform simple data management tasks with them.

## Goal of the Training

The aim of the training is to explain the following topics by using the command line tool-iCommands:
- [uploading](#data-upload)/[downloading](#data-download) data
- [adding metadata to data objects/collections](#create-avus-triples)
- [querying based on metadata](#queries-for-data)
- [deleting data objects/collections](#unix-like-icommands-basics)
- [synchronization of data](#data-synchronization)
- [assigning ACLs to data objects/collections](#access-control-and-data-sharing)

## Categorizing iCommands

As a command line user interface to iRODS, more than 50 iCommands exist. However a regular user may use only a few of them for his/her daily needs. We can categorize them in the following groups:

- [Informative iCommands](#informative-icommands)
- [Unix-like iCommands](#unix-like-icommands-basics)
- [Functional iCommands](#functional-icommands)
- [Metadata related iCommands](#metadata)
- Administrative iCommands

### Configuration of the iRODS connection

Connect to the KU Leuven iRODS portal (https://{YOURZONE}.irods.icts.kuleuven.be) and follow the instructions of the section iRODS Linux Client.

You will then start an iRODS session that will last 7 days.
After 7 days the created temporary password will expire and you will need to repeat this procedure to reconnect to iRODS.

### Informative iCommands

These commands help us find and understand some useful information. We may not need these commands directly when we work with data, but they can offer useful information in other circumstances. Typically we don’t use these commands very often.

The command that will print out all commands with their explanation is:

```sh
ihelp
```

To get help on a specific command, such as `iuserinfo`:
`ihelp iuserinfo` or `iuserinfo -h`

If you would like to know the setting details you can execute the following command:

```sh
ienv
```

To get information about a user you can run the below command followed by a username.
This command will show for example to which groups a user belongs:

```sh
iuserinfo u0XXXXXX
```

To be able to learn what an error code stands for, you can then use the command below followed by the number of the error:

```sh
ierror 826000
```

To connect to the server and retrieve some basic server information, for example as a simple test for connecting to the server:

```sh
imiscsvrinfo
```

### Unix like iCommands (Basics)

These commands work exactly like their Unix counterparts do, but on iRODS instead of on the local storage.

To identify the current working collection (iRODS directory) you can use the `ipwd` command. Basically this command tells you where you are in iRODS:

```sh
ipwd
# /yourZone/home/u0XXXXXX
```

Let’s create a collection in iRODS and name it “test”.

```sh
imkdir test
```

To see the content of our current collection we can use `ils`. It lists collections (directories) and data objects (files) contained in our current collection.
And we see that we have successfully created our “test” collection.

```sh
ils
# /yourZone/home/u0XXXXXX:
#  C- /yourZone/home/u0XXXXXX/test
```

`ils` shows you the contents of a collection, but not of its subcollections.   
If you want to see the contents of the current collection and all its subcollections, you can use the command `itree` instead. 

To go to the collection that you want, you would use `icd` with an absolute path or a relative path.
In other words, this is what we use to navigate around folder(s) of iRODS. Let's go inside the 'test' collection:

```sh
icd test
```

And go back up to the parent collection:

```sh
icd ..
```

To copy a data object (file) or collection (directory) to another data object or collection, we use `icp source target`.
When copying collections, we need to add the `-r` flag.
For example, if we want to copy the “test” collection that we created inside the same parent collection but with a different name “test1”:

```sh
icp -r test test1
```

To move/rename an iRODS data object or collection to another dataobject or collection we use `imv`.
Let’s move collection “test1” inside the collection “test”.

```sh
imv test1 test/
```

To remove one or more data objects or collections from iRODS space we use `irm` (again, with the `-r` for collections). However, once we execute this command the items are by default moved first to the trash collection (/yourZone/trash) unless the `-f` option is used.
Let's can remove test1 collection.

```sh
irm -r test1
```

**Note:** All the collections and data objects that are deleted move to the trash collection. They are permanently cleaned when they are older than 15 days. Alternatively, the `irmtrash` command may be used to delete data objects and collections in the trash collection instantly. 

We can create empty files with `itouch` and write them with `istream` followed by `write`:

```sh
itouch test1.txt
echo 'hello' | istream write -a test1.txt
```

In CLI shells, you can normally print the contents of a file with the `cat` command. In iRODS we can do the same with the command `istream` and the option `read`.
The following would print the contents of the file test1.txt to the terminal:

```sh
istream read test1.txt
```

### Functional iCommands

With the commands in this section, we will do functional data operations like data uploading/downloading, access control and verifying/synchronizing data.
This constitutes the **basis of data management in iRODS**.

#### Data Upload

We can store a file into iRODS with `iput local [irods]`: If the destination data object or collection (`irods`) are not provided, the current iRODS collection and the input file name are used.

To upload data into iRODS we should have a data object in our local system. For example, let's create a data file in our Linux home directory. 

```sh
nano example.txt
```

Inside the file, type the following:

```
Hi, this is an example file!
```

You can save files in the text editor *nano* with `Ctrl + o` and exit the program with `Ctrl + x`. 
With the linux command `ls` we can check that the file has been created.

We now upload the data to the iRODS.

```sh
iput -K example.txt
```

*The flag -K triggers iRODS to create a checksum and store it [in the iCAT metadata catalogue](#checking-data-integrity).*

Let’s remove the original file.

```sh
rm example.txt
```

The `ls` command will show that `example.txt` does not exist in the local directory anymore: the file is now only available on the iRODS server.

```sh
ils

# /yourZone/home/public:
#  example.txt
#  test1.txt
#  C- /yourZone/home/u0XXXXXX/test
```

As we have seen before, data can be deleted by `irm (-f) example.txt`, but we will not do it now.

#### Connection between logical and physical namespace

iRODS provides an abstraction from the physical location of the files. ` /yourZone/home/u0XXXXXX/example.txt` is the logical path which only iRODS knows.
But where is the file actually located on the server?

```sh
ils -L

/yourZone/home/u0XXXXXX/test:
  u00XXXXX          0 default;netapp           29 2021-04-27.19:41 & example.txt
    sha2:MGYDAyYBfv49YHkGxNBYQ4sZLE2dxR+yLGhvRjCH4pE=    generic    /netapp/home/u0XXXXXX/test/example.txt
```

Let’s try to understand what this means. The example.txt that we uploaded to iRODS has the logical path `/yourZone/home/u0XXXXXX/test/example.txt`. u00XXXXX is the owner of the file and the numbers after user name show the replica of files in the iRODS system.
“default:netapp” represents the storage resource name. The size of the file is 29KB. The file is stored with a time stamp and a checksum. `/netapp/home/u0XXXXXX/test/example.txt` is the physical path of the file.

#### Data Download

We can get data objects or collections from iRODS and place them either in a specific local area or the current working directory with `iget irods [local]`. Let's download data files from iRODS to our current VSC location.

```sh
iget -K example.txt example-restore.txt
```

We downloaded the data object example.txt as a new file called example-restore.txt in our linux home directory. Here the flag -K triggers iRODS to verify the checksum, like for `iput`. Checksums are used to verify [data integrity](#checking-data-integrity) upon data moving.

*To get the progress feedback we can use `-P` flag.*

**Note**: The `iput` and `iget` commands also work for directories/collections, simply use the `-r` (for recursive) flag.

#### Access control and data sharing

If we add the flag `-A` to the command `ils` we can see information about the ACL (access rights) of our data objects and, in the case of collections, an attribute named Inheritance. When this attribute is `Enabled`, all new items inside that collection will *inherit* the same access rights of the collection.

```sh
ils -r -A
# /yourZone/home/u0XXXXXX/test:
#        ACL - u0XXXXXX#yourZone:own
#        Inheritance - Disabled
#  example.txt
#        ACL - u0XXXXXX#yourZone:own
```

The possible ACLs in iRODS are "read", "write" and "own" rights. In the `ils -A` output, for each item we see 'ACL' followed by a list of users or groups and which access rights they have to that collection or data object. In this case, u0XXXXXX owns all files listed and no one else has access rights.

The command to manipulate the access rights of a collection or data object you own is `ichmod ACL user/group item`, where `ACL` is one of `own`, `write`, `read` or -- to remove all permissions -- `null`.

Let's create a new collection called 'shared', that we will share with another user.

```sh
imkdir shared
```

Let's change the access rights of 'shared'. You can choose another user or group who you want to give access:

```sh
ichmod read u0YYYYYY shared # or ichmod read public shared
```

The user u0YYYYYY can now list the collection and see the data to which he/she has the respective permission.

We can change the inheritance and place some new data in the collection so that any new item inside of 'shared' is automatically assigned the same ACL:

```sh
ichmod inherit shared
iput -K example-restore.txt shared/example1.txt
```

Only the recently added file will inherit the ACLs from the folder; old data will keep their ACLs. You can check the result with `ils -A -r shared`.

```sh
ils -A -r shared
```

#### Checking data integrity

For confirming data integrity, the checksum of a data object or a collection can be checked both in our local client and iRODS: if two items have the same checksum, they are the identical.
Let's first check the checksum of the `shared` collection in iRODS.

```sh
ichksum -r shared

# C- /yourZone/home/u0XXXXXX/test/shared:
#    example1.txt    sha2:MGYDAyYBfv49YHkGxNBYQ4sZLE2dxR+yLGhvRjCH4pE=
```

We can also check this with the `ils -L` command, but it lists much more information.

We can reproduce the same digits of the checksum with `sha256sum ${FILENAME} | awk '{print $1}' | xxd -r -p | base64`, where `${FILENAME}` is the name of your file.
For example, to check the checksum of the local counterpart of `example1.txt`:

```sh
sha256sum example-restored.txt | awk '{print $1}' | xxd -r -p | base64
# MGYDAyYBfv49YHkGxNBYQ4sZLE2dxR+yLGhvRjCH4pE=
```

This way we can confirm that this data object/file is the same and we don’t detect any error during its transmission or storage.

#### Data Synchronization

To synchronize the data between a local copy and the copy stored in iRODS or between two iRODS copies, we can use ` irsync source target`. In this case `source` and `target` can be either local files or directories, in which their path is given as is, or iRODS data objects and collections, in which case their path must be prefixed by `i:`.

For example, we can synchronize a local directory `foo1` with a `foo2` collection with:

```sh
mkdir foo1 # create directory to synchronize
irsync -r foo1 i:foo2
```

This is equivalent to `iput -r -f foo1 foo2`. The main difference is that `iput` will only transfer files that don't exist in iRODS and
`iput -f` will overwrite any files that exist in both the local directory and iRODS,
whereas `irsync` will first check the difference between the local copy and the iRODS version and transfer the difference.

With the same caveats, the command `irsync -r i:foo1 foo2` is equivalent to `iget -r -f foo1 foo2`, and `irsync -r i:foo1 i:foo2` is like `icp -r foo1 foo2`.

In sum, `irsync` compares the checksum values and file sizes of the source and target files to determine whether synchronization is needed.

#### File Bundling

To bundle and unbundle structured files such as tar files in iRODS we can use `ibun` command. The `-x` flag unbundles; the `-c` flag bundles.

A tar file containing many small files can be created with normal unix tar command on our local machine . We can then upload the tar file to the iRODS server like any other file, i.e., with `iput`. Afterwards, `ibun -x` can be used to extract/untar the uploaded tar file. The extracted subfiles and subdirectories will then be appeared as normal iRODS data objects and sub-collections.

As good practice we can tag the tar file using the `-Dtar` flag when uploading the file with `iput`. Alternatively, this 'dataType' tag can be added later with the `isysmeta` command: `isysmeta mod /path/to/tarfile.tar datatype 'tar file'`.

To illustrate, let's first create a small folder with files and tar it.

```
mkdir fortar
cd fortar
for file in one two three four; do touch $file.txt; done
cd ../
tar -chlf test.tar fortar
```

Running `ls fortar` will show its contents. Now we can send the file to iRODS and untar it with `ibun -x` into a collection called 'test_collection'.

```sh
iput -Dtar test.tar
ibun -x test.tar test_collection
```

We can also add/bundle an iRODS collection into a tar file with the `ibun -c` command.

```sh
ibun -cDtar test2.tar test_collection
```

### Metadata

Metadata, often called "data about data", is used to facilitate data discovery, search and retrieval. iRODS provides the user with the possibility to create attribute-value-unit triples attached to some data. The triples are stored in the iCAT catalogue.

Metadata attribute-value-units triples (AVUs) consist of an Attribute-Name, Attribute-Value, and optionally Attribute-Units.
They can be manipulated via the `imeta` command, followed by:

- `add` to add a new AVU;
- `ls` to list existing AVUs;
- `mod` to modify an existing AVU;
- `rm` to remove an existing AVU.

They can also be queried to find matching data, as shown [below](#queries-for-data).

For each command, `-d`, `-C`, `-R`, or `-u` must be used to specify the type of object to work with, respectively: data objects, collections, resources, or users.

#### Create AVUs triples

We can annotate a data file with `imeta add -d path 'attribute-name' 'attribute-value' ['attribute-units']`:

```sh
imeta add -d example.txt 'distance' '10' 'meter'
imeta add -d example.txt 'author' 'Tom'
```

It is possible to leave the 'unit' part out, since it is optional.

We can also annotate a collection with `imeta add -C path 'attribute-name' 'attribute-value' ['attribute-units']`:

```sh
imeta add -C shared 'training' 'irods' 'online'
```

#### List Metadata

To list metadata we run `imeta ls...`:

```sh
imeta ls -d example.txt
imeta ls -C shared
```

With `imeta ls`, we can retrieve the AVUs when given a file or collection name, but we could also retrieve the data object and collection names when given an attribute or value with [queries](#queries-for-data).

#### Queries for data

For simple queries we can use `imeta qu`. For example, we can obtain the files with "distance" as an attribute and "10" as a value with:

```sh
imeta qu -d distance = 10
```

However, we will probably be more interested in most sophisticated search. For that purpose we can use `iquest` followed by an SQL-like query. For example, we can fetch items with an attribute named "author" with:

```sh
iquest "select COLL_NAME, DATA_NAME, META_DATA_ATTR_VALUE where \
META_DATA_ATTR_NAME like 'author'"
```

We can also filter for a specific attribute values with something like:

```sh
iquest "select COLL_NAME, DATA_NAME where \
META_DATA_ATTR_NAME like 'author' and META_DATA_ATTR_VALUE like 'Tom'"
```

It is possible to use SQL wildcards such as "%" and "_", and thus find data objects containing "test" in their name as follows:

```sh
iquest "select COLL_NAME, DATA_NAME, DATA_CHECKSUM where DATA_NAME like '%test%'"
```

Previously we calculated a checksum with `ichksum`. The checksum was stored in the iCAT metadata catalogue, but we cannot fish it out with `imeta`: we need `iquest`:

```sh
iquest "select COLL_NAME, DATA_NAME, DATA_CHECKSUM where \
DATA_CHECKSUM like 'sha2:I+hXKW8cY3IZ1KZUJlFE8yPRltdSstwnONohiUr3UTo='"
```

If you are not sure of the possible attributes you could use in your search, such as "COLL_NAME", "DATA_NAME", "META_DATA_ATTR_VALUE", etc., you can query them with `iquest attrs`.

#  Exercises

Let's do the exercises below! 


Before starting the exercises, please clone the [git repository](https://github.com/kuleuven/iRODS-User-Training) of this training.
You will find files for the exercises in the 'data' directory.

**Exercise 1: uploading and organizing**


- Create two collections called 'earth_science' and 'economy'.
- Upload the file 'economy/inflation.txt' to the collection 'earth_science'.
- Wait...that doesn't make sense! Move this file to the collection 'economy'.
- Move into the 'economy' collection and check whether the file is actually there.
- Move one level back and remove the 'earth_science' collection.

Hint: in unix commands, '.' refers to the current directory, and .. to the parent directory.
The same is true in iCommands.   

<details>   
  <summary>Solution</summary>   
  Note: sometimes there are multiple solutions possible.
  These spoilers only show one way. 

  Also remember that you can use 'ils' and 'ipwd' between other commands to check where you are.


  ```
  imkdir earth_science
  imkdir economy
  
  iput data/economy/inflation.txt earth_science

  imv earth_science/inflation.txt economy
  icd economy
  ils

  icd ..
  irm -r -f earth_science
  
  ```

</details>       

  
**Exercise 2: downloading**

- Remove the file inflation.txt from your local directory.
- Download the file again from iRODS.


<details>
    <summary>Solution</summary>
    
```    
rm inflation.txt

icd economy
iget inflation.txt
```    

</details>

**Exercise 3: synchronizing data**

- Create a collection in iRODS called 'molecules'.
- Sync the local directory data/molecules with the collection 'molecules' in iRODS.
- Check whether all files have been uploaded to iRODS.
- Count how many carbon (C) atoms there are in all molecules combined.
- Create a file called 'carbon_count.txt' in the data/molecules directory, with this number as contents.
- Sync the local directory data/molecules with the collection 'molecules' again.
- Check whether the file 'carbon_count.txt' is now present in iRODS.

<details>
    <summary>Solution</summary>
    


```
imkdir molecules
cd data
irsync -r molecules i:molecules
ils molecules
```

```
echo 14 > molecules/carbon_count.txt
irsync -r molecules i:molecules
ils molecules
```


</details>

**Exercise 4: managing permissions**
- Go to data/lifescience. You will there find the files patient1.csv and anonymized.csv. 
- Make a folder called 'lifescience' in your home and upload both files to it.
- Give your group read access to the folder lifescience, recursively.
- Oh no, we forgot something! While the data in anonymized.csv is anonymized, the other file contains sensitive data!
  Remove the read permissions for the group from patient1.csv.
- Since the data in patient1.csv is sensitive, only colleagues who really need it can have access. 
  Choose one of your colleagues and give this person write access to the file.
- Check whether the permissions of both files are correctly set.
- Remove the lifescience collection


<details>
    <summary>Solution</summary>
    
```
cd data/lifescience

imkdir lifescience
iput patient1.csv lifescience
iput anonymized.csv lifescience

ichmod -r read <group> lifescience
ichmod null <group> lifescience/patient1.csv
ichmod write <colleague> lifescience/patient1.csv

ils -A lifescience
```


</details>


**Exercise 5: working with tar files via the ibun command**


- Create a tar file of your local lifescience folder.
- Upload the tar file to iRODS. Make sure it has the right data type.
- Make a collection called 'archive'.
- Unbundle the tar file in iRODS in this collection.
- Bundle the 'molecules' collection in iRODS and download it. 


<details>
    <summary>Solution</summary>
    
```
tar -cf lifescience.tar lifescience
iput -Dtar lifescience.tar
imkdir archive
ibun -x lifescience.tar archive

ibun -cDtar molecules.tar molecules
iget molecules.tar
```
</details>

**Exercise 6: working with metadata**

- Go to data/languages. you will there find the files corpus1.txt, corpus2.txt and corpus3.txt.   
  These are so called 'text corpora', featuring a set of texts in a certain language.
- Make a collection called 'languages' and upload the files to it.
- Add the following AVU's to the files:
    - Attribute 'language' and value 'dutch' to corpus1.txt
    - Attribute 'language' and value 'french' to corpus2.txt
    - Attribute 'language' and value 'latin' to corpus3.txt
- Oops, we made a mistake! Open the file corpus2.txt, and look what the language is. 
  Overwrite the current AVU with one with the correct value (tip: check the documentation of imeta with `imeta -h`).
- Execute a query which searches all files which contain Dutch text.
- Give all three files the AVU 'type:text', only using one command. 
  You can search for ways to do this in the documentation of imeta.


<details>
    <summary>Solution</summary>
    
```
cd  data/languages
```

```
imkdir languages
iput corpus1.txt languages 
iput corpus2.txt languages
iput corpus3.txt languages
```
alternatively, you could have used:

```
iput -r languages
```
Let's continue:
```
icd languages
imeta add -d corpus1.txt language dutch
imeta add -d corpus2.txt language french
imeta add -d corpus3.txt language latin
imeta mod -d corpus2.txt language french v:english
```

The query can be executed with `iquest` or `imeta qu`:

```
iquest "SELECT DATA_NAME where META_DATA_ATTR_NAME = 'language' and META_DATA_ATTR_VALUE = 'dutch'"

imeta qu -d language = dutch
```
```
imeta addw 
```

</details>

