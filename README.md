# Pizza-Time!

In README.md, include a short writeup describing your project, what’s contained in each file you created or modified, and (optionally) any other additional information the staff should know about your project. Also, include a description of your personal touch and what you chose to add to the project.

## File descriptions

### app.py

app.py is the brain of the website. Here all the necessary calculations are done and the data is configured. Further info about what this file does can be found in the comments of the file itself.

#### Personal touch
For the personal touch i made the application send a confirmation E-mail which contains a table with the shopping cart of the user.

### models.py

models.py creates the structure of the database. This is done by SQLalchemy using classes as tables. The main classes are User, Item, Order and PlacedOrder. These handle the registration and administration of the orders.

### Templates Folder

All templates extend layout.html which cotains the basic HTML structure.Templates like home.html and suc.html handle handle some basic pages. It gets more tricky with templates like order.html and shop.html. These render the menu and shopping cart based on the database. More info can be found in the comments of the respective files.

### Static Folder

The CSS file and the picture of the cute cats are found here.

## Getting Started


The first thing you do is set some environment variables

- set SECRET_KEY='\x81_h\xa0\tU\x92\xad~\x89\xd6\xce\x1a$\xd27\x12\xb9\xfe\xcc\x7f\x12'

- set EMAIL_USER=pizzawebapp69@gmail.com

- set EMAIL_PASS=#pizzapizza123

- set DATABASE_URL=postgres://dyaioefjplfbgl:9ac058be13ef339034ed763fef3d667152c3c17888eb31da720baae33f8e9cc2@ec2-54-195-247-108.eu-west-1.compute.amazonaws.com:5432/d4a4je3uute2di

Then we install the requirements

- pip3 install -r requirements.txt

Finally we run

- flask run