# Metalnx Portal Client for KU Leuven Users

*Prerequisites:*  
*-A KU Leuven u-account*  

Metalnx is a graphical user interface and serves as a client to iRODS. It helps to simplify most administration, collection management, and metadata management tasks removing the need to memorize the long list of iCommands. It allows users to manage content and metadata associated with content.

You can reach the Metalnx portal by clicking on the Metalnx tab at your zone portal (https://{YOURZONE}.irods.icts.kuleuven.be).

You will be redirected to the KU Leuven authentication page where you will have to login with your u-account. After you are forwarded to the KU Leuven iRODS portal, you need to click to the Metalnx link.

<img align="center" src="img/metalnx-go.png" width="400px">

Or you can use the direct link of Metalnx (https://{YOURZONE}.irods.icts.kuleuven.be/metalnx).

The Metalnx portal is composed of two panes. The left pane is a menu with different options. The right pane provides functionalities based on the selected item in the menu.

<img align="center" src="img/metalnx_general.png" width="400px">

**Collections**: This tab allows you to browse through your collections. A collection is the logical representation of a group of data objects (files), similar to folders or directories on your normal PC. A collection can also contain subcollections. Under this tab, we can perform all data object and collection related activities:
 
- Uploading files  
- Moving files/collections  
- Copying files/collections  
- Renaming files/collections  
- Applying metadata templates (see later)  
- Downloading files  

Behind any collection or file, you can press 'View info' for the following options:

- Adding metadata to files/collections  
- Adding files/collections to favorites  
- Setting permissions  
- Getting previews of files  

This is the tab you will be using the most in Metalnx.

**Search**: This tab gives search options based on various parameters.

**Templates**: We can here create our own metadata templates or import a template from outside in a json format. These can then be applied to files or collections.

**Shared Links**: Here you can see the links to data objects and collections shared with you by other users.

**Favorites**: Here you can see your bookmarked collections and files.

**Tickets**: The ticket mechanism is another way to provide other people, including non-iRODS users, access to data objects  or collections . So, this tab allows you to see all the tickets you have created in addition to making new tickets with the ‘using ticket’ button. Because of the defined workflows for the Eximious project, it is kindly requested not to use this functionality.

**Public**: Here you can reach the public area collections. The public collection gives opportunity to share data easily with others. However, not recommended to use it for project data because all users can have access to this collection.

**Trash**: Here you can see the files and collections moved to trash bin. All the collections and data objects that are deleted moves to the trash collection and they are permanently cleaned when they are older than 15 days. You can also use ‘Empty Trash’ button to empty the trash collection completely.

Now let’s do some hands-on exercises:

**Exercise 1: data objects, folders and metadata**:

- Create a metalnx_test collection under your home directory.
- Upload a file inside the collection.
- Click on 'view info' to see some basic information about this file.
- Add one metadata AVU to the this uploaded file. (Attribute: Author, Value: your name).
- Look at the preview of your file, and try to edit the file (note: you can only edit certain file types, like .txt files).
- Rename your file to 'testfile'.
- Download testfile to your local machine.

 **Exercise 2: metadata templates**:

- Create one public metadata template with the name of “test_training” and it has to include at least two AVUs.
- Create one private metadata template with the name of your choice.
- Add the private one on your testfile.
- Add one of the public metadata templates on the metalnx_test collection.

Take a look at the metadata of your collection and your uploaded file. As you can see, we can easily manage metadata on both collections and the files in them, even if they have different metadata.

**Exercise 3: favorites and sharing**:

- Add metalnx_test collection to your favorites.
- Give “own” access permission to a friend and share this file link.
- Check your shared tab if there are any files shared with you. (If not, ask me to share with you one.)

**Exercise 4: deleting**:
- Delete your file.
- Delete metalnx_test collection.
- Go to the trash tab and look at your deleted items.
- Permanently delete the deleted file.
- Move the deleted collection metalnx_test to the public collection.

As you have seen we can do lots of data management operations easily with the Metalnx portal.
