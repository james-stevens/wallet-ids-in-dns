#! /usr/bin/python3
# (c) Copyright 2019-2022, James Stevens ... see LICENSE for details
# Alternative license arrangements possible, contact me for more information
""" ico wallet name to wallet id rest/api in flask """

import syslog
import flask

import wallet

application = flask.Flask("ICO/Rest/api")

syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_DAEMON)


def abort(err_no, message):
    """ return error code {err_no} with {message} """
    response = flask.jsonify({'error': message})
    response.status_code = err_no
    return response


@application.route('/ico/v1/api', methods=['GET', 'POST'])
def get_wallet():
    """ look up a wallet {name}, optional using {servers} """
    local_servers = flask.request.args.get("servers")
    wallet_name = flask.request.args.get("name")
    if wallet_name is None:
        return abort(400, "No wallet name given")

    try:
        my_wallet = wallet.Wallet(wallet_name, local_servers=local_servers)
        if my_wallet.wallet_id is not None:
            return flask.jsonify(my_wallet.wallet_id)

        return abort(400,
                     f"ERROR: No wallet named '{wallet_name}' could be found")
    except Exception as err:  # pylint: disable=broad-except
        return abort(400, f"ERROR: {str(err)}")


@application.route("/ico/v1")
@application.route("/ico")
def hello():
    """ standard hello.world fn """
    return flask.jsonify({"version": 1, "hello": "world"})


if __name__ == "__main__":
    application.run()
