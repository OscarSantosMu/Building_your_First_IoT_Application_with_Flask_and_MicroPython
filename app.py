from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

coltitles = ("#","ID","Value","Physical quantity")
data_log = ()
i = 0

class SensorDataModel(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	esp32_pin_id = db.Column(db.Integer, nullable=False)
	value = db.Column(db.Integer, nullable=False)
	physical_quantity = db.Column(db.Float, nullable=False)

	def __repr__(self):
		return 'SensorDataModel(id = {}, esp32_pin_id = {}, \
				value = {}, physical_quantity = {})'.format(
				self.id, self.esp32_pin_id, self.value, self.physical_quantity)

#db.create_all()

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/receive')
def receive():
	global i
	global data_log
	esp32_pin_id = request.args.get('esp32_pin_id')
	value = request.args.get('value_1')
	physical_quantity = request.args.get('physical_quantity_1')
	tup = (i, esp32_pin_id, value, physical_quantity)
	data_log = data_log + (tup,)
	data = SensorDataModel(id = i, esp32_pin_id = esp32_pin_id, value = value, physical_quantity = physical_quantity)
	db.session.add(data)
	db.session.commit()
	i+=1
	return 'OK'

@app.route('/table')
def table():
	return render_template('table.html', title='Table', coltitles=coltitles, data_log=data_log)

if __name__ == '__main__':
   app.run(host = '192.168.1.3',debug = True)