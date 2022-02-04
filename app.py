from service import app
from service_handler import overwriteCSVData

HOSTNAME = 'localhost'
PORT_NUMBER = 3000

if __name__ == '__main__':
    # reset csv data
    overwriteCSVData()
    # run server
    app.run(host=HOSTNAME, port=PORT_NUMBER, debug=False)
