
trello2misc
===========

trello2misc is both a standalone program and a todo.txt add-on that pulls cards
from Trello and converts them into various outputs. It is developed in Python3.
Currently, two output modes are supported: stdout and todotxt.

stdout mode
-----------

Every Trello card that is not ignored is mapped to one line and print to the
console.

1. The title of the card becomes the entry. The title also serves as
the identifier of the entry.
2. The list of the card serves as the line prefix.
3. The board of the card is ignored.
4. The labels of the card are added in curly braces at the end of the line.

todotxt mode
------------

Every Trello card that is not ignored is mapped to one entry in the
todo.txt file. 

1. The title of the card becomes the entry. The title also serves as
the identifier of the entry.
2. The list of the card determines the priority. If a card has been
moved in Trello, the priority is updated.
3. The board of the card determines the context. 
4. The labels of the card determine the project.
	
If on a card in Trello the priority or the due date is changed, the changes will
be reflected for the corresponding entry in todo.txt. If, however, the title of
a Trello card is changed, a new entry will be created and the old entry will
continue to exist, because the title serves as the identifier.


Installation
------------

Download the package into some directory. Copy the template.ini file to
trello2misc.ini and adapt it to your needs. Copy the trello file to your
todo.txt add-on directory. Create a soft link to the trello2misc.py file in the
todo.txt add-on directory.

Example (assuming you have a ~/opt-directory for your local software):

    cd ~/opt
    mkdir trello2misc
    cd trello2misc
    # Put trello2misc files there
    cp ./template.ini -/trello2misc.ini
    # Adapt trello2misc.ini to your needs
    cd ~/opt/todo.txt/addons
    cp ~/opt/trello2misc/trello .
    chmod 744 trello
    ln -s ~/opt/trello2misc/trello2misc.py .
	

Configuration
-------------

The file trello2misc.ini contains some options for configuration. It is divided
into two sections, [todotxt] and [trello].

The [todotxt]-section:

fileName - The name of your todo.txt file

The [trello]-section:

key - The trello2misc application key.

token - Your Trello user token. See Trello documentation on how to
get one (http://trello.com/docs/gettingstarted/).

allCardsBoards - Names of boards, for which all cards should be
pulled. This allows you to have a personal todo board in Trello,
where all cards belong to you.

myCardsBoards - Names of boards, for which only cards assigned to you should be
pulled.

ignoredLists - Names of lists that should be ignored. Useful values include for
example "Ideas", "Backlog", "Completed", "Done". See the default settings for
some more inspiration.

aLists - Names of lists, for which cards should be assigned priority A. See the
default settings for some inspiration here. 

bLists - Names of lists, for which cards should be assigned priority B. See the
default settings for some inspiration here.

cLists - Names of lists, for which cards should be assigned priority C. See the
default settings for some inspiration here.


Usage
-----

Standalone program:

    ./trello2misc.py [stdout|todotxt|usage]?

or:

    python3 ./trello2misc.py [stdout|todotxt|usage]?

todo.txt add-on:

    todo.sh trello

