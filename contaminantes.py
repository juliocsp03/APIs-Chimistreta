from flask import Flask, request
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from flask_cors import CORS

app = Flask (__name__)
CORS(app)

conn = psycopg2.connect(database="prueba", host="alpha.tamps.cinvestav.mx", user="postgres", password="example", port="5448")
# conn = psycopg2.connect(database="prueba", host="localhost", user="postgres", password="example", port="5448")

@app.route("/")
def index():
	return "Julio"


@app.route("/api/test")
def test():
	return "Hoy no se fía, mañana sí."


@app.route("/api/query", methods = ['POST'])
def getProducts():
	data = request.json
	estado = data.get("estado")
	anio = data.get('anio')
	iarc = data.get('iarc')
	# levels = json.dumps(levels)
	# if strict == True:
	# 	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
	# 		cursor.execute(f"""SELECT id, methodology_id, url, levels, extension, key, type FROM methodology_instance WHERE levels->>'levels' = '{levels}' AND methodology_id = {methodology_id};""")
	# 		res = cursor.fetchall()
	# 		response = {
	# 			"quantity": len(res),
	# 			"products": res
	# 		}
	# 		return response
	# elif strict == False:
	# 	levels = levels.replace('[', "")
	# 	levels = levels.replace(']', '')
	# 	levels = levels.replace('\"', '%')
	# 	levels = levels.replace("\\", "\\\\")
	# 	print(f"""SELECT id, methodology_id, url, levels, extension, key FROM methodology_instance WHERE levels->>'levels' ILIKE '{levels}' AND methodology_id = {methodology_id} ORDER BY levels->>'number_of_levels';""")
	# 	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
	# 		cursor.execute(f"""SELECT id, methodology_id, url, levels, extension, key, type FROM methodology_instance WHERE levels->>'levels' ILIKE '{levels}' AND methodology_id = {methodology_id} ORDER BY levels->>'number_of_levels';""")
	# 		res = cursor.fetchall()
	# 		response = {
	# 			"quantity": len(res),
	# 			"products": res
	# 		}
	# 		return response
		# return "simón"
	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute(f"""SELECT * FROM data WHERE estado = '{estado}' AND anio = {anio} AND iarc = '{iarc}'""")
		res = cursor.fetchall()
		response = {
			"quantity": len(res),
			"products": res
		}
		return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
