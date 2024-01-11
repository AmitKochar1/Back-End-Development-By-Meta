<h1>Configuring MySQL Connection</h1>

By default, Django uses the SQLite database for storage and retrieval of the app data, as Python has built-in support for it. However, you can use any of the following databases supported by Django:

PostgreSQL

MariaDB

MySQL

Oracle

SQLite

In this Reading, you’ll learn the steps to enable a MySQL connection with a Django application.

<h2>Advantage of MySQL</h2>
The SQLite database has a lot of limitations. It is serverless and doesn't have a user management system. It is useful for smaller applications and for the development of a prototype to be upgraded eventually for databases that are scalable and support client-server architecture.

MySQL is an open-source database and has a lot of advantages over SQLite, such as scalability and authenticatio

<h2>Install MySQL</h2>
To install the MySQL server, download the installer appropriate for your operating system from 
https://www.mysql.com/downloads/m (https://www.mysql.com/downloads/)
. For Windows, use the mysql-installer-web-community-8.0.30.0.msi and follow the wizard-based installation steps.

First open a command line terminal, then start the MySQL command line client with the following command:
mysql -u root -p


You will be prompted to enter the password set at the time of installation. In the command terminal, you will get the MySQL prompt. You can now enter any SQL statement in it.

<img src='CSQLC1.png'>

Start by creating a database with the following command:

Create database mydatabase;

The show databases; command will show the list of currently available databases.  

<h2>Install MySQL DB API Driver</h2>
To interface a Python program with MySQL, ensure you have a DB API-compliant driver. There are a number of Python drivers for MySQL available. Django recommends mysqlclientto be used. Install it with pip installer.

pip3 install mysqlclient

<h2>Enable MySQL </h2>
To be able to use MySQL, the DATABASES variable in the Django project’s settings file must be properly configured. By default, it is set to the connection parameters for SQLite. Remove those statements. You have to add MySQL-specific settings in their place.

You must configure at least one database in the DATABASES variable. For the configuration of the first database, its name should be ‘default’.

The settings include the database engine, name of the database, username, and password, along with the host IP address. This defaults to the localhost 127.0.0.10 and the port defaults to 3306.

#Settings.py
DATABASES = {   
    'default': {   
        'ENGINE': 'django.db.backends.mysql',   
        'NAME': 'mydatabase',   
        'USER': 'root',   
        'PASSWORD': '',   
        'HOST': '127.0.0.1',   
        'PORT': '3306',   
        'OPTIONS': {   
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"   
        }   
    }   
} 

The other optional parameters include: 

sql_mode: The session SQL mode will be set to the given string. It defaults to 'STATIC_TRANS_TABLES' to prevent invalid or missing values from being stored in the database.

default-character-set: The character set to be used. Default is utf8.

read_default_file: MySQL configuration file to read.

init_command: Initial command to issue to the server upon connection.

<h2>Create database tables</h2>
The startprojecttemplate installs some Django apps by default. Some examples include admin, auth and sessions. 

Remember that you need to create the necessary database tables for these apps. 

Run the migrate command to use the models in these apps and build their respective table structure in the current mysql database.

python manage.py migrate 

Inside the MySQL terminal, run the following commands:

use mydatabase; 
Show tables; 

It shows all the tables created by the migration.

Instead of viewing the data in the MySQL terminal, add a MySQL extension from VS Code extension library

<h2>VS Code extension for MySQL</h2>
From the VS Code extension marketplace, search for MySQL and install the extension.

<img src='CSQLC2.png'>

MySQL appears in the explorer.

<img src='CSQLC3.png'>

Click on the + button and enter the following details:

domain name: localhost 

user:root

password=''. 

Note: Some users may encounter an error such as:
Client does not support authentication protocol requested by server; consider upgrading MySQL client

This usually indicates a user privilege issue. In such cases first run a command such as:

     ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';

Then refresh privileges by running a command such as:

     flush privileges;

Now, the localhost appears in the explorer bar.

<img src='CSQLC4.png'>

Expand the section by selecting the drop-down arrow and choose mydatabase. All the tables required for the INSTALLED_APPS will be visible.

<img src='CSQLC5.png'>

In this reading, you have explored how to connect MySQL database with Django.