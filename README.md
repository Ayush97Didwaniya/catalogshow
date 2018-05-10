# ItemCatalog
This project provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Generate clientId and Secret for Google Authentication
* Go to [console.developers.google.com](https://console.developers.google.com)
* create a project
* set the OAth consent screen details
* set Authorized JavaScript origins to [http://localhost:8000]http://localhost:8000
* save and Download Json file
* rename it with client_secret.json and put it into catalog folder(after clone the project)

## steps to run the program
* clone the project
* Install Vagrant and VirtualBox
* This will give you the Sqlite database and support software needed for this project
* open git bash in the folder where is vagrant file is already there
* Launch the Vagrant VM (vagrant up) here
* vagrant ssh
* add client Id in /catalog/templates/login.html
* Run your application within the VM (python /catalog/catalog.py)
* The project will run on [localhost:8000](localhost:8000)

## Editional Info
* Here I am providing my database file with dummy data.
* you can crete Your Own.
