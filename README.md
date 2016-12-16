# bd2

**Installation:**

Ubuntu/Debian:  
1. Install Python 3.5  
2. $sudo apt-get install python3-pip python3-dev postgresql  
3. $pip3 install virtualenv  
4. $virtualenv ENV  
	Where ENV is a directory to place the new virtual environment  
5. $source ENV/bin/activate  
6. clone repo and cd into it  
7. pip3 install -r requirements.txt  


Windows:  
1. Install:  
	- Python 3.5.2 https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe  
	- PostgreSQL 9.5.5 http://www.enterprisedb.com/products-services-training/pgdownload#windows  
2. follow steps 2-7 from above  


**Configure database:**  
    * user info:  
     username: storeuser, password: password  
    * db:  
     name: store,  

Ubuntu/Debian:  
    $ sudo -u postgres createuser --no-superuser --createdb --no-createrole storeuser  
    $ sudo -u postgres createdb -O storeuser store  
    $ sudo -u postgres psql -c "alter user storeuser with encrypted password 'password';"  

    test:
    $ psql store -U storeuser  
    if you get: "psql: FATAL: Peer authentication failed for user "storeuser"" modify file /etc/postgresql/9.5/main/pg_hba.conf by changing line "local all all peer" to "local all all md5". Restart server #/etc/init.d/postgresql restart (or sudo service postgresql restart)  

Windows:  
	TODO add manual here
