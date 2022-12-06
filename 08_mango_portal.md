# ManGO portal

*Prerequisites:*  
*- a KU Leuven account*


The ManGO portal is a web interface for iRODS, developed at ICTS KU Leuven.  

## Logging in

You will receive the link of the ManGO portal during the training.  

On this page, you will be asked to choose the institute you are affiliated to:

<img align="center" src="img/mango_portal_login_institute.png" width="600px">

Choosing 'KU Leuven' will direct you to the KU Leuven login page, unless you already were logged in in another tab, in which case this step is skipped.  
On the next page, select your iRODS zone.   
You should be redirected to the main page of the ManGO portal:

<img align="center" src="img/mango_portal_main_page.png" width="600px">


## The collections tab

### Navigating

When you log in, you can see a menu on the left side of the page, with the different tabs.  
The **Collections** tab allows you to navigate and organize your data in the central pane.

<img align="center" src="img/mango_portal_collections.png" width="600px">

By default, you start in the 'home' collection. There you should see: 
- Your home collection 
- The collection of your group 
- The public collection

To navigate to a collection, you just click on it.
Just under the search bar, there is a handy breadcrumb menu, which allows you to go back to previous collections:

To create a collection, you click on the blue 'add collection' button, and specify a name.

**Note** If the 'Add collection' and 'Upload files ...' buttons are missing, that means you don't have permissions to write to the collection you are currently in. 

### Uploading and downloading files

To upload one or multiple files, click on the 'Upload files... button'.  
From here, there are two ways to upload files:
  1. Open your local file explorer, and drag file to 'Drop files here to upload'
  2. Click on 'Drop files here to upload' and browse your pc
Note that you can upload multiple files in one go. 

After this step, you will see the file as data object in your collection:   

<img align="center" src="img/mango_portal_data_object.png" width="600px">


To download a data object, click on the blue download icon on the right of it.  
It will end up in your local Downloads directory.  


### Moving, copying and renaming data

These actions are planned to be added in a later version.  


### Deleting data

To delete a collection, click on it to show that collection's page.  
You can find the red 'Delete' button in the lower left corner.   
The same method applies for data object.  

<img align="center" src="img/mango_portal_delete.png" width="600px">

Any data you delete gets sent to your 'trash' collection.    
For example, if you remove the file with path `/<zone>/home/<username>/research/results.txt`, it will end up at `/<zone>/trash/home/<username>/research/results.txt`.  
You can reach the trash collection by clickin on the 'trash' tab on the left of the screen.   
There it stays for 15 days, after which it is automatically deleted.  

If you want to recover data you deleted within this period, please contact the administrators via rdm-icts@kuleuven.be.  
In later versions, you will be able to move deleted data back to your home directory.  


## A deeper look

- File and collection properties
- Metadata (manual)
- Permissions
- Previews
- TIKA parser

## Searching 


## Metadata templates

- Creating templates
- Applying templates







# Exercises

Let's do the exercises below!


You can find the files used for the exercises in the [git repository](https://github.com/hpcleuven/KULeuven-iRODS-User-Training) of this training, in the 'data' folder.

You can download the repository as a Zip-file by clicking on the green 'code' button and selecting 'Download ZIP'.
Alternatively, you can clone the repository from the command line.

**Exercise 1: uploading and organizing**

In this exercise, you will use the file inflation.txt from data/economy.

- Create two collections called 'earth_science' and 'economy'.
- Upload inflation.txt to the collection 'earth_science'.
- You suddenly relialize that what you just did doesn't make sense. This file belongs in 'economy'! Remove the file you just uploaded.
- Move into the 'economy' collection and reupload the file there. 
- Remove the 'earth_science' collection.
- You can now also delete the 'inflation.txt' file in your local directory.



<details>
  <summary>Solution</summary>

You start this exercise in the 'collections' tab.  
Before starting, navigate to your home collection by clicking on it.  

- Use the 'Add collection' button to create the collection 'earth_science'.  
  Make the collection 'economy' in the same way.
- Click on the newly made 'earth_science' collection.
- Click on the 'upload files' button.
  You have two ways to do this:
    1. Open your local file explorer, and drag file to 'Drop files here to upload'
    2. Click on 'Drop files here to upload'   
       In the popup that opens, you can search the inflation.txt file on your local pc.
    Click on 'submit files'.
- Click on inflation.txt. 'Then, select 'delete'.  
- Move back to your home collection via the breadcrumb menu above.  
- Click on 'economy' and repeat the step of uploading inflation.txt.
- Move back to your home collection via the breadcrumb menu above. 
- Click on the 'earth_science' collection.
- Click on 'delete'. 

</details>

**Exercise 2: downloading and overwriting**

- Inspect the contents of inflation.txt by previewing it. 
- You realise there is a mistake in the uploaded data object.
  Download the file and edit it so the inflation for 2021 is 1.4%.
- Upload the new version of the file, overwriting the previous one.


<details>
  <summary>Solution</summary>

You start this exercise in the 'collections' tab.

</details>

**Exercise 3: managing permissions**

In this exercise, you will use the files patient1.csv and anonymized.csv from data/lifescience.

- Make a collection called 'lifescience' in your home and upload both files to it.  
- Give your group read access to the collection lifescience, recursively.  
- Oh no, we forgot something! While the data in anonymized.csv is anonymized, the other file contains sensitive data!  
  Remove the read permissions for the group from patient1.csv.  
- Later, your colleagues mention they need to upload some new files to the lifescience collection.  
  Give your group write access to the lifescience collection (without changing the permissions of anonymized.csv and patient1.csv)  



<details>
  <summary>Solution</summary>

You start this exercise in the 'collections' tab.

</details>

**Exercise 4: working with metadata**

In this exercise, you will use the files corpus1.txt, corpus2.txt and corpus3.txt from data/languages.

- Make a collection called 'languages' and upload the files to it.  
- Add the following AVU's to the files:  
    - Attrbute 'language' and value 'dutch' to corpus1.txt  
    - Attrbute 'language' and value 'french' to corpus2.txt  
    - Attrbute 'language' and value 'latin' to corpus3.txt  
- Oops, we made a mistake! Open the file corpus2.txt, and look what the language is.  
  Overwrite the current AVU with one with the correct value.  
- Go to the 'search' tab and search for all files with Metadata Attribute Name 'language' and Metadata Attribute Value 'latin'.  


<details>
  <summary>Solution</summary>

You start this exercise in the 'collections' tab.

</details>

**Exercise 5: metadata schemas**

In this exercise, you will use the file bird.JPG from data/biology, which depicts a nice specimen of the 'European roller'.

- Make a Metadata schema with the name 'animals'.
  This schema should contain the following:

  - A 'name' field where the user can type the name of the animal
  - A 'type' field, with the following options:
    - 'Mammal'
    - 'Bird'
    - 'Fish'
  - A 'flies' field, with the following options:
    - 'Yes'
    - 'No'
    - 'Only on weekdays'

  All fields should be required. 

- Create a collection called 'biology' and upload bird.JPG to it.
- Apply the template to bird.JPG.

<details>
  <summary>Solution</summary>


</details>


