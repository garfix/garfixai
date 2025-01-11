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

