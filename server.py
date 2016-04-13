#!/usr/bin/env python2.7

"""
Liberated Webserver

    Bill Roberts - wjr2113
    Jonathan Sun - jys2124

    COMS W4111.001 - Introduction to Databases

To run locally:

    python server.py

Go to http://localhost:4111 in your browser.

A debugger such as 'pdb' may be helpful for debugging.
Read about it online.
"""

import click
from liberated import app

if __name__ == '__main__':
    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=4111, type=int)
    def serve(debug, threaded, host, port):
        """
        Run the server using:

            python server.py

        Show the help text using:

            python server.py --help

        """
        app.run(host=host, port=port, debug=debug, threaded=threaded)

    serve()
