"""
A sample Hello World server.
"""
import os

from flaskr import create_app

app = create_app()

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=False, port=server_port, host='0.0.0.0')
