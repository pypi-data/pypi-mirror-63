# log-viewer: log web-exposer toolkit

## What is log-viewer for? ##

**log-viewer** is just a lightweight Python package that web-exposes your log files using 
[Flask's](https://palletsprojects.com/p/flask/) interface.

## How do I get set up? ##

## Requisites ##
* [python](https://www.python.org/downloads/release/python-360/) >= 3.6 running on a 
Linux environment.

## Where to get it ##
[PyPi](https://pypi.org/) repository, execute:
```sh
pip install log-viewer
```

## Installation from sources ##
Cloning the git [repo](https://github.com/moonrollersoft/log-viewer), execute in root folder:
```sh
python setup.py install
```

## Use ##
After package installation, execute:
```sh
log-viewer
```
**log-viewer** will search log files and it will expose them within HTML native accordions in 
http://0.0.0.0:8081 (default)
 
No login is needed by default. In order to activate the login, just set user or password 
through the execution options. 

## Execution options ##
**log-viewer** execution options:
* **-a --address** Logs exposing address. Default: "0.0.0.0"
* **-p --port** Logs exposing port. Default: 8081
* **-u --user** User for login, it activates the login mode. If no password is set, the 
login mode will only check the 
provided user
* **-psw --password** Password for login, it activates the login mode. If no user is set, 
the login mode will only check 
the provided password
* **-lp --logPaths** Paths to search (recursively) the logs from (";" separated). 
Default: "/var/log/"

### Example ###

The following example will activate the login mode with custom parameters:
```sh
log-viewer -u admin -psw admin -p 8080 -lp "/var/log/django;/var/log/apt" -a "127.0.0.1"
```

## License
[MIT](LICENSE.txt)


## Dependencies
- [Flask](https://palletsprojects.com/p/flask/) >= 1*


## Contact ##
[moonrollersoft@gmail.com](mailto:moonrollersoft@gmail.com)
