inv-web
=======

This script allows access to the Student Robotics inventory via a web interface. This allows
you to search and find information on parts in the inventory without having to set up an
inventory instance.

##Setup/Testing

To set up an instance of inv-web you need:

* Python Bottle - can be installed on fedora with yum install python-bottle
* dependencies for [sr tools](https://www.studentrobotics.org/trac/wiki/DevScripts)
* dependencies for the [inventory](https://www.studentrobotics.org/trac/wiki/Inventory)

Once inv-web has been cloned you will want to clone sr tools and the inventory into the inv-web directory. Or modify the api.py script to change the path it looks for the inventory and tools.

Bottle includes its own webserver, which can be stated with python api.py which currently sets up a webserver on port 8080 (can be changed in the api.py).

The script currently relies on two components, the api.py backend which provides json to the index.html which loads this and displays the results.
