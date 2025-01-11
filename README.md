Using Richard! to talk to my computer.

## Installation

Create a virtual environment, activate it, install the requirements and the commands:

~~~bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install .
~~~

## Start the server

The main application runs as a service. Start the service in a separate console:

~~~bash
source venv/bin/activate
server
~~~

## Command line client

You can talk to the computer while you are doing other things on the command line.
Just preceed each request you want to make the the computer with the letter "r".
The computer's reply will be prefixed by "C:"

~~~bash
source venv/bin/activate
r <my request to the computer>
~~~

For example

~~~bash
r play some Supertramp
C: OK

r stop
C: OK

r what is 1+1
C: 2
~~~

## Development

When developing, you want to have change take effect immediately, without running `pip install i` everytime.

To start the server:

~~~bash
python3 src/server/server.py
~~~

To start a client:

~~~bash
python3 src/client/cli.py <my request to the computer>
~~~
