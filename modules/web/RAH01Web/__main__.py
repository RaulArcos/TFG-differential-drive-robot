import sys
from RAH01Web.webServer import WebServerManager

if __name__ == "__main__":
    manager = WebServerManager(*tuple(sys.argv[1:]))
    