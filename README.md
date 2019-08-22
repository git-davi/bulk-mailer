# bulk-mailer

This is a simple, light and fast implementation of a bulk mailer for sending html emails.\
A simple use case scenario could be a newsletter subscription.\
\
The GUI is minimal.

> ***This project is old, I've written it a long time ago and I will not support it.***
> _Sorry for bad code_

## Dependecies

- python3
- pandas
- tkinter
- sqlite3

## How to use it

Just run the ```main.py``` script.\
From the front page you can browse the file system for the mail corpus.\
\
The mail will be sent to every subscribed mail inside the db.\
You can stop the program and the state of the current bulk send will be "consistent" (you wouldn't have to resend the mail to every subscriber).\
After each successfull bulk send you should ```reset subs count``` to continue sending new mails.

> To upload new subscribers you can do it from an ```.xls``` , ```.json``` ,```.txt``` file.

Last but not least important, inside the ```server.srv``` file you should place your smtp server.


## If you want to increase speed

Go to ```mail.py``` and change the **N_THREADS** or **DB_BUFFER** value.\
I would suggest to use **N_THREADS** equal to the number of logic cores of you cpu.\
If you increase the **DB_BUFFER** the consistency of the bulk state will be weaker but the speed will benefit.\
\
**Note** : the sqlite3 provides thread safe access to the db.

## Error handling

- ***exit value 0*** : all went fine
- ***exit value 1*** : some parameters are missing
- ***exit value 2*** : failed login
- ***exit value 3*** : error wrong format file uploaded <--------- removed
- ***exit value 4*** : error while sending email