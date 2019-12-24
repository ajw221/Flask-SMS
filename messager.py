### app.py imports ###
from flask import Flask, request, render_template
from twilio.rest import Client
### app.py imports ###
### db.py imports  ###
from peewee import SqliteDatabase, Model, CharField, DateTimeField
from datetime import datetime
import pytz
### db.py imports  ###

app = Flask(__name__)                                         # Flask App
db = SqliteDatabase('texts.db')                               # Database 

### Time Column Formatting START ### db.py
EST = pytz.timezone('US/Eastern')                             # Set timezone
t = datetime.now(EST)                                         # Set datetime
current_time = t.strftime("%#I:%M:%S%p").lower()              # Time Format
current_date = t.strftime("%B %#d, %Y")                       # Date Format
full_date = "{} at {} EST".format(current_date, current_time) # Full Format
### Time Column Formatting END   ### db.py

### Twilio Keys ### app.py
account_sid = "AC7996640d6e1f1f1ae10567f28915bbd3"            # accSID
auth_token = "d4b71e7955aa9939f53b47606f3f0281"               # authTok
client = Client(account_sid, auth_token)                      # creation
### Twilio Keys ### app.py

### HTML Routes ### app.py
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    number = request.form['phone']
    message = request.form['message']
    client.messages.create(
        to=str(number),
        from_="+15105737099",
        body=str(message)
    )
    Text.create(phone_number=str(number),sms_message=str(message)).save()
    sent = "Your message:'{}' has been sent to {} on {}.".format(message, number, full_date)
    return """{} <br> {}""".format(render_template("index.html"), sent)
### HTML Routes ### app.py

### db table    ### db.py
class Text(Model):
    phone_number = CharField(max_length=50)
    sms_message = CharField(max_length=255)
    time_received = DateTimeField(default=full_date)

    class Meta:
        database = db
### db table    ### db.py

### db creation ### db.py
if __name__ == '__main__':
    db.connect()
    db.create_tables([Text], safe=True)
### db creation ### db.py

app.run(debug=True, port=5000, host='127.0.0.1')