# Quick Start Guidance

A 'zone' in iRODS is an independent iRODS system consisting of various servers and clients. A zone can be dedicated to a single user group or several groups can use the same zone. Currently there are five independent zones for the KU Leuven iRODS projects. Based on your project you will be using one of these zones. Since we operate more than one zone, we have different URLs to reach those zones. Throughout this training you will see links like this: https://{YOURZONE}.irods.icts.kuleuven.be to show you these link can work with your zone name. Whenever you see YOURZONE placeholder, please use your zone name there.

You will be provided with your zone name and an URL to access to that in the training session. Also once your iRODS account is activated, you will be notified by an email about how to access to your zone.

For now, we don’t have any federated zones. However, we can federate zones in the future to facilitate data transfer between zones.

For your all questions and requests you can send an email to our service desk with a 'Data:' prefix on the title. The service desk email address is icts@kuleuven.be.

Time to time you can receive a notification email from the email address below to be informed about changes, updates or maintenances with iRODS. Please pay attention to those mails.
The mentioned mail address: 


## Prerequisites

- A KU Leuven account (u- or b-account) to access the KU Leuven iRODS zones

If you want to use iRODS' command line client (iCommands) or the python programming client (PRC), you need to have following:

- A Linux client environment - a linux based operation system and terminal
- Installed iCommands (also needed to use the PRC)
- The Python iRODS Client (PRC) and a VSC-PRC extension of it to gain functionalities some extra tools

### Installation of WSL2 (if a Linux environment is not already available)

As a windows user if you don’t already use any virtualisation system to operate Linux you can install Windows Subsystem for Linux (WSL2).

To be able to install WSL 2 on your Windows 10, you need the following:
 
- Windows 10 May 2020 (2004), Windows 10 May 2019 (1903), or Windows 10 November 2019 (1909) or later
- Hyper-V Virtualization support

Users who are using a system managed by KU Leuven should fulfill these requirements. The requirements can be checked as follows: 

To know your Windows version, type ‘winver’ on your search bar and check your version on coming screen. Anyone who cannot see 2004 should look at [this link](https://support.microsoft.com/en-us/topic/august-20-2020-kb4566116-os-builds-18362-1049-and-18363-1049-preview-c75c6a43-9c87-e412-9a9e-10a0dabac4d5).

The installation of WSL2 will consist of the following steps:
-	Enable WSL 2,
-	Enable ‘Virtual Machine Platform’,
-	Set WSL 2 as default,
-	Install a Linux distro.

We will complete all steps by using Power Shell of Windows. However you can do some of the steps by graphical screens as an option. Here you can find all steps:

-	Run Windows PowerShell as administrator,
-	Type the following to enable WSL:

`dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart`

-	To enable Virtual Machine Platform on Windows 10 (2004), execute the following command:

`dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart`

-	To set WSL 2 as default execute the command below (You might need to restart your PC):

`wsl --set-default-version 2`

-	To install your Linux distribution of choice (Ubuntu 18.04 LTS is recommended to install the following iRODS packages easily) on Windows 10, open the Microsoft Store app, search for it, and click the “Get” button.
-	The first time you launch a newly installed Linux distribution, a console window will open and you'll be asked to wait for a minute or two. 
-	You will then need to create a user account and password for your new Linux distribution. This password will give you ‘sudo’ rights when asked. 
-	If you see ‘WSLRegisterDistribution Failed with Error:’ or you may find that things don’t work as intended you should restart your system at this point.

After all these steps when you type ‘wsl’ to your Windows PowerShell, you will be directed to your Ubuntu machine mounted on your Windows’ C drive. From now on, you can execute all Linux commands. It is advised to use the home directory instead of your Windows drives. So if you type ‘cd‘ you will be forwarded to your Ubuntu home.

You can also install (optional) the Windows Terminal app, which enables multiple tabs operation, search feature, and custom themes etc.

### Installing iCommands

To be able to work with iCommands, we first need to install it if it has not been installed yet. You can check `ls /usr/bin` to find iRODS executable commands on the system. 

On a linux OS you can use a package manager to install iCommands in the terminal. Instructions for configuring via the appropriate package manager can be found at the link https://packages.irods.org/. Depending on your linux distribution and version, the installation procedure may vary. However main ones are given below.

For CentOS:

```sh
sudo yum install irods-icommands
```

For Debian/Ubuntu:

```sh
sudo apt update
sudo apt install irods-icommands
```

If the above does not work for you (e.g., no support for Ubuntu 20), you can contact placeholder@iRODSservicedesk.be.

### How to Use Miniconda on Your Linux OS with PRC (Optional)

Here you will learn how to install Miniconda from command line on Ubuntu 18.04. The whole Miniconda installation procedure needs only 3 steps, except creating and activating a conda environment which is explained later.

-	To download the latest shell script to Ubuntu 18.04, execute the following command.

```sh
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

-	To make the Miniconda installation script executable, do the following.

```sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
```

-	Run the installation script on Ubuntu 18.04 to install Miniconda.

```sh
./Miniconda3-latest-Linux-x86_64.sh
```

-	During the installation follow the instructions and give answers to questions.
-	Be sure that if you choose ‘yes’ to ‘conda init’ question at the end it will add the base environment to your.bashrc file on your Ubuntu system. But it will not hurt anything.

### Installing the Python iRODS Client (PRC)

To install with pip:

```sh
pip install python-irodsclient
```

But you can simply install it by conda using environment.yml file. Copy this file to your project directory and update the last part, 'prefix' to your conda environments. And lastly execute the command below.

```sh
conda env create --file environment.yml
```

You can activate your environment executing the command below.

```sh
conda activate prc-irods
```


## What does this training repository contain?

|Module|Description|Notes|
|----  |-----------|-----|
|02_Introduction_to_iRODS.pdf|Explains all information about iRODS in general as well as the KU Leuven iRODS architecture in particular. Also it contains some hands-on part with logging a hands-on tutorial on how to log in to the KU Leuven portal|This module is valid for users of all available zones|
|03_Metalnx_Handson_User-Training.md|Contains descriptive information about iRODS' graphical user interface client and also hands-on training|This module is mostly for the users and zones that use a portal based GUI client|
|04_WebDav_Handson.md|Explains the WebDav interface, which provides local filesytem type access to data and teaches you how to use it|This module is mostly for the users and zones that use a desktop based GUI client|
|05_iCommands_Handson_User-Training.md|Explains how to use the command line client of iRODS|This module is mostly for the users and zones that work with command line interface - terminal|
|06_PRC_Handson_User-Training.md|Explains how to use the programming client - the Python iRODS client (PRC) to iRODS|This module is mostly for the users and zones that want to interact with python|
|/img (folder)|Place for images of the tutorials||
|/molecules (folder)|Place for data objects (files)|will be used in the PRC|
|environment.yml|Contains a list of dependencies to install|for the users who want to use PRC|
|README.md|Explains the goals and structure of this training repository||


## Contribution Instructions

### Reporting an error or issue via GitHub

- Click the 'issues' tab at the top of this GitHub page to let us know about your findings or requests.

 OR

- Send an email to [placeholder@iRODSservicedesk.be](mailto:placeholder@iRODSservicedesk.be)

### Fixing and/or improving documentation via GitHub

1. [Fork](https://help.github.com/articles/fork-a-repo/) this repo to your GitHub account
2. Make edits directly to the **index.rst** file. Edits may be made to the fork the web interface to your GitHub account or [clone](https://help.github.com/articles/cloning-a-repository/) the repo to work on your local computer. For very significant changes (we suggest [making a new branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/)).
3. Commit change; if working from a local copy, push those changes to your fork in Github.
4. Submit a pull request back to the master repository; you may need to act on feedback before your request is merged.