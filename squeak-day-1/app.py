from flask import Flask, render_template, request

app = Flask(__name__, static_path='/static')



@app.route('/')
def index():
	numbers = [0,1,2,3,4,5]
	return render_template('index.html',numbers = numbers)

@app.route('/results', methods=['POST'])
def results():
	numbers = [0,1,2,3,4,5]
	return render_template('static/results.html',
		numbers = numbers)

if __name__ == '__main__':
	app.run(debug=True)