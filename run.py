from app import app

def run_app():
	app.run(host="0.0.0.0")


if __name__ == '__main__':
	from waitress import serve
	serve(app, host='0.0.0.0', port=80)
	# app.run(host="0.0.0.0")