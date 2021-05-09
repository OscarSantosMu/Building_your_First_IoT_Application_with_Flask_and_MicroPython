from flask import Flask, render_template, request
app = Flask(__name__)

coltitles = ("#","ID","Value","Physical quantity")
data_log = ()
i = 0

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
	i+=1
	return 'OK'

@app.route('/table')
def table():
	return render_template('table.html', title='Table', coltitles=coltitles, data_log=data_log)

if __name__ == '__main__':
   app.run(host='192.168.1.8', debug = True)