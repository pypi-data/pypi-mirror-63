Pysafe is a terminal-based password manager with a very easy to use CLI.
### Features:
* Generate a unique encryption key to be used as a master password.
* Generate new passwords for new logins .
* Encrypt all saved password using the generated encryption key.
* Show all your saved logins with a click of button.
* Ready to export CSV file for an easy backup experience.
* Master reset to delete saved encryption key and all saved logins.
### How to install:
#### On mac:

Open terminal and type:

``python3 pip install pysafe``


#### On windows:
Open Powershell and type

``python3 pip install pysafe``


### How to use:

#### On mac:

Open terminal and type

``Python3 ``

``Import pysafe``

#### On Windows:
Open Powershell and type

``python3``

``import pysafe``

### General usage:
* Generate a new encryption key:
You only need to do this once. Save your encryption key somewhere safe as
 this will be used as your master password.
 
 Note: Encrypted credentials are linked to the generated encryption key
 . Avoid generating a new key with existing logins as this would result in
  losing the ability to decrypt your saved login credentials.

* Save a new login:
After generating a new key, you can enter as many login entries as you so desire
 with the ability to generate new passwords along the way, or just enter a
  password of your
  choosing. Then the program will save it for you in CSV file. The passwords
   in that CSV file will be encrypted, and can only be seen using the generated
    encryption key that we mentioned earlier.
    
*  Show saved logins:
The program will print out the saved logins using the saved encryption key
 and saved CSV file, so you can see them in plain text that you can use.
 
* Generate a new password:
This will give your the ability to generate a new password without having an
 encryption key or entering any additional information such as a website tile
  or website link. You only need to enter the length of the password and the
   program will do the rest.
   
* Delete all data:
This will be used in case you wish to have a fresh start without any
 encryption key nor CSV file.

Note: This will permently delete your Encryption key and saved logins. So
 only do that, if you know what you are doing.