print("Hello world")
from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_bootstrap import Bootstrap

from werkzeug.utils import secure_filename
import os
import net as neuronet

import lxml.etree as ET

app = Flask(__name__)


@app.route("/")
def hello():
    return "<html><head></head><body>Hello world!</body></html>"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)


@app.route("/data_to")
def data_to():
    some_pars = {'user': 'Ivan', 'color': 'red'}
    some_str = "Hello my dear friends!"
    some_value = 10
    return render_template('simple.html', some_str=some_str, some_value=some_value, some_pars=some_pars)

# csrf token
SECRET_KEY = 'secret'

# captcha
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcRZUkfAAAAAMC2w8n8lPX-8_dHhgAs9vaVGLGw'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcRZUkfAAAAAN-2opKl6_A1s4Ugr8ANEEPCyvpC'
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}

bootstrap = Bootstrap(app)

class NetForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    upload = FileField('Load image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    recaptcha = RecaptchaField()
    submit = SubmitField('send')

@app.route("/net", methods=["GET", "POST"])
def net():
    form = NetForm()
    filename = None
    neurodic = {}

    if form.validate_on_submit():
        filename = os.path.join('./static', secure_filename(form.upload.data.filename))
        fcount, fimage = neuronet.read_image_files(10, './static')
        decode = neuronet.getresult(fimage)
        for elem in decode:
            neurodic[elem[0][1]] = elem[0][2]
        form.upload.data.save(filename)

    return render_template('net.html', form=form, image_name=filename, neurodic=neurodic)

@app.route("/apixml", methods=["GET", "POST"])
def apixml():
    dom = ET.parse("./static/xml/file.xml")
    xslt = ET.parse("./static/xml/file.xslt")
    transform = ET.XSLT(xslt)
    newhtml = transform(dom)
    strfile = ET.tostring(newhtml)
    return strfile
