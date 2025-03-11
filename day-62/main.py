import csv
import os
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms import validators
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv

load_dotenv('keys.env')
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
Bootstrap(app)

csv_file = 'cafe-data.csv'
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[validators.DataRequired()])
    location = StringField(label='Cafe Location on google Maps (URL)', validators=[validators.DataRequired(), validators.URL()])
    opening_time = StringField(label='Opening Time e.g 8AM', validators=[validators.DataRequired()])
    closing_time = StringField(label='Closing Time e.g 5:30AM', validators=[validators.DataRequired()])
    coffee_rating = SelectField(label='Coffee Rating', choices=[('✘','✘'),('☕', '☕'), ('☕☕', '☕☕'), ('☕☕☕', '☕☕☕'), ('☕☕☕☕', '☕☕☕☕'), ('☕☕☕☕☕', '☕☕☕☕☕')],
                                validators=[validators.DataRequired()])
    wifi_strength = SelectField(label='Wi-Fi strength Rating', choices=[('✘','✘'),('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'), ('💪💪💪💪', '💪💪💪💪')],
                                validators=[validators.DataRequired()])
    power = SelectField(label='Power Socket Availability',choices=[('✘', '✘'), ('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌')],
                        validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        data = [
            form.cafe.data,
            form.location.data,
            form.opening_time.data,
            form.closing_time.data,
            form.coffee_rating.data,
            form.wifi_strength.data,
            form.power.data,
        ]
        with open(csv_file, mode='a+', newline='', encoding='utf-8') as file:
            file.seek(0, os.SEEK_END)
            if file.tell() > 0:
                file.seek(file.tell() - 1)
                if file.read(1) != "\n":
                    file.write('\n')
            writer = csv.writer(file)
            writer.writerow(data)
        return redirect(url_for('cafes'))
    print(form.errors)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open(csv_file, newline='', encoding='utf-8') as file:
        csv_data = csv.reader(file, delimiter=',')
        list_of_rows = [row for row in csv_data]
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
