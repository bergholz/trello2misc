
trello2todotxt
==============

trello2todotxt is both a standalone program and a todo.txt add-on that
pulls cards from Trello and converts them into todo.txt entries. It is
developed in Python3. 

Every Trello card that is not ignored is mapped to one entry in the
todo.txt file. 

1. The title of the card becomes the entry. The title also serves as
the identifier of the entry.
2. The list of the card determines the priority. If a card has been
moved in Trello, the priority is updated.
3. The board of the card determines the context. 
4. The labels of the card determine the project.
	
If on a card in Trello the priority or the due date is changed, the
changes will be reflected for the corresponding entry in todo.txt. If,
however, the title of a Trello card is changed, a new entry will be
created and the old entry will continue to exist, because the title
serves as the identifier.


Installation
------------

Download the package into some directory. Copy the trello file to your
todo.txt add-on directory. Create a soft link to the trello2todotxt.py
file in the todo.txt add-on directory.

Example:

    cd ~/opt
    mkdir trello2todotxt
    # Put trello2todotxt files there
    cd ~/opt/todo.txt/addons
    cp ~/opt/trello2todotxt/trello .
    chmod 744 trello
    ln -s ~/opt/trello2todotxt/trello2todotxt.py .
	

Configuration
-------------

The file trello2todotxt.ini contains some options for
configuration. It is divided into two sections, [todotxt] and
[trello]. 

The [todotxt]-section:

fileName - The name of your todo.txt file

The [trello]-section:

key - Your Trello application key. See Trello documentation on how to
get one.

token - Your Trello user token. See Trello documentation on how to
get one.

allCardsBoards - Names of boards, for which all cards should be
pulled. This allows you to have a personal todo board in Trello,
where all cards belong to you.

myCardsBoards - Names of boards, for which only cards assigned to you should be pulled.

ignoredLists - Names of lists that should be ignored. Useful values
include for example "Ideas", "Backlog", "Completed", "Done".

aLists - Names of lists, for which cards should be assigned priority
A. See the default settings for some inspiration here.

bLists - Names of lists, for which cards should be assigned priority
B. See the default settings for some inspiration here.

cLists - Names of lists, for which cards should be assigned priority
C. See the default settings for some inspiration here.


Usage
-----

Standalone program:

    ./trello2todotxt.py

or:

    python3 ./trello2todotxt.py

todo.txt add-on:

    todo.sh trello


