# My environnement (work fine):
* Server: Debian 8 with mongodb installed
* Client: Windows 10 with Python 3.6 installed


# Requirement
## MongoDBserver 3.4 (default config)
https://www.mongodb.com/download-center?jmp=nav
## Python 3.6
https://www.python.org/downloads/
## Python 3 library
- tkinter
- pymongo

	- if you not have pip yet: https://pip.pypa.io/en/stable/installing/
		- download: https://bootstrap.pypa.io/get-pip.py
		- install: run in cmd ($ python3 get-pip)
		- use: pip install <package-name>

# Installation
## MongoDB 3.4.1
### Debian 8
1. sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
2. echo "deb http://repo.mongodb.org/apt/debian jessie/mongodb-org/3.4 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
3. sudo apt-get update
4. sudo apt-get install -y mongodb-org
5. sudo service mongod start

## Python 3.x
### Debian 8 (python3 usually come with debian):
1. sudo apt-get update
2. sudo apt-get install python3
### Python package
1. pip install pymongo
2. pip install tkinter

# Usage
1. Edit file bnotebook/module/mymongodb/basedbclass.py
	change: HOST = "192.168.99.100" and PORT = 32777 to your ip and port where mongodb install (default port is 27017)
2. Go to application directory
	$ cd bnotebook
	$ python3 bnotebook-gui.py

Thank you!