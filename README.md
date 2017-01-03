# bd2

## Installation:

### Ubuntu/Debian:  
1. Install Python 3.5, PostgreSQL and virtualenv:

 ```bash
$ sudo apt-get install python3-pip python3-dev postgresql  
$ pip3 install virtualenv
```
2. Create new virtual environment and enter it:

 ```bash
$ virtualenv ENV  
  #Where ENV is a directory to place the new virtual environment  
$ source ENV/bin/activate  
```
3. clone repo and cd into it and type in shell:

 ```bash
$ pip3 install -r requirements.txt
```


### Windows:  
1. Install
 * Python 3.5.2 https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe  
  **During installation please select pip installation and adding Python to $PATH**
 * PostgreSQL 9.5.5 http://www.enterprisedb.com/products-services-training/pgdownload#windows
1. **Add Postgresql\version\bin and Python installation directory to $PATH if they are not added**
3. Open Command Prompt and type:

 ```bash
> pip install virtualenv
> virtualenv ENV
  #Where ENV is a directory to place the new virtual environment
> call ENV\Scripts\activate.bat
```
4. clone repo, cd into it ant type in cmd:

 ```bash
> pip install -r requirements.txt
```


## Configure database:
* user info:  
   username: storeuser 
   password: password
* db:  
   name: store,


### Ubuntu/Debian:  

 ```bash
$ sudo -u postgres createuser --no-superuser --createdb --no-createrole storeuser  
$ sudo -u postgres createdb -O storeuser store  
$ sudo -u postgres psql -c "alter user storeuser with encrypted password 'password';"  
```
#### TEST:

 ```bash
$ psql store -U storeuser
```
If you get: "psql: FATAL: Peer authentication failed for user "storeuser"",  
modify file **/etc/postgresql/9.5/main/pg_hba.conf** by changing line "local all all peer" to "local all all md5".  
Restart server #/etc/init.d/postgresql restart (or sudo service postgresql restart)  

### Windows:

 ```bash
> createuser -U postgres --no-superuser --createdb --no-createrole storeuser
> createdb -U postgres -O storeuser store
> psql -U postgres -c "alter user storeuser with encrypted password 'password';"
```


## Prepare database and run server:  

Prepare db: (should be done once and before first server start)  
 
 ```bash
$ python sklep/manage.py migrate
```

Run server:

 ```bash
$ python sklep/manage.py runserver localhost:8000
```
Site is now visible at localhost:8000 (or 127.0.0.1:8000)  
