from flask import Flask, render_template, request, json
from flask_mail import Message, Mail

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("smtp.html", url=request.url_root)


@app.route("/check", methods=["POST"])
def check():
    content = request.json
    app.config['MAIL_SERVER'] = content["mail_server"]
    app.config['MAIL_PORT'] = content["mail_port"] if content["mail_port"] else 465
    app.config['MAIL_USE_TLS'] = content["use_tls"] if content["use_tls"] else False
    app.config['MAIL_USE_SSL'] = True if not content["use_tls"] else False
    app.config['MAIL_USERNAME'] = content["mail_username"]
    app.config['MAIL_PASSWORD'] = content["mail_password"]
    app.config['MAIL_DEFAULT_SENDER'] = content["mail_sender"]
    recipient = content["from_to"]

    mail = Mail(app)

    try:
        msg = Message(
            'Test Message',
            recipients=[recipient]
        )
        msg.body = 'message attachment test'
        msg.html = render_template('mail/template.html', url=request.url_root)
        mail.send(msg)

    except Exception as e:
        return app.response_class(
            response=json.dumps({
                "success": False,
                "message": str(e)
            }),
            status=400,
            mimetype='application/json'
        )

    return app.response_class(
        response=json.dumps({
            "success": True,
        }),
        status=200,
        mimetype='application/json'
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
