import argparse
import sys

from log_viewer.api import app
import log_viewer.settings as st


def run_flask(host, port):
    app.run(host, port)


def main():
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(description="Log viewer.")
    parser.add_argument("-lp", "--logPaths", type=str, required=False, default=st.DEFAULT_LOG_PATH, dest='paths',
                        help='";" separated paths to recursively search log files for.')
    parser.add_argument("-a", "--address", type=str, required=False, default=st.DEFAULT_HOST, dest='address',
                        help="Host address to expose the logs.")
    parser.add_argument("-p", "--port", type=int, required=False, default=st.DEFAULT_PORT, dest='port',
                        help="Port to expose the logs.")
    parser.add_argument("-u", "--user", type=str, required=False, default=st.DEFAULT_USER, dest='user', help="User")
    parser.add_argument("-psw", "--password", type=str, required=False, default=st.DEFAULT_PASSWORD, dest='password',
                        help="Password")
    args = parser.parse_args(args)
    app.config['LOG_PATHS'] = args.paths.split(";")
    app.config['USER'] = args.user
    app.config['PASSWORD'] = args.password
    run_flask(args.address, args.port)


if __name__ == '__main__':
    main()
