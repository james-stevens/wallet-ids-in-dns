#! /usr/bin/python3
# (c) Copyright 2019-2022, James Stevens ... see LICENSE for details
# Alternative license arrangements possible, contact me for more information

import syslog
import flask

import wallet


application = flask.Flask("ICO/Rest/api")

syslogFacility = syslog.LOG_LOCAL6
syslog.openlog(logoption=syslog.LOG_PID, facility=syslogFacility)


def abort(err_no, message):
    response = flask.jsonify({'error': message})
    response.status_code = err_no
    return response


@application.route('/ico/v1/api', methods=['GET'])
def get_wallet():
    local_servers = flask.request.args.get("servers")
    wallet_name = flask.request.args.get("name")
    if wallet_name is None:
        return abort(400,"No wallet name given")

    try:
        my_wallet = wallet.Wallet(wallet_name, local_servers=local_servers)
        if my_wallet.wallet_id is not None:
            return flask.jsonify(my_wallet.wallet_id)
        else:
            return abort(400,f"ERROR: No wallet named '{args.wallet}' could be found")
    except ValueError as err:  # pylint: disable=broad-except
        return abort(400,f"ERROR: {str(err)}")



@application.route("/ico/v1")
@application.route("/ico")
def hello():
    return flask.jsonify({"version":1,"hello":"world"})


if __name__ == "__main__":
    application.run()
