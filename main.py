from flask import Flask, request
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from flask_cors import CORS

app = Flask (__name__)
CORS(app)

# conn = psycopg2.connect(database="prueba", host="alpha.tamps.cinvestav.mx", user="postgres", password="example", port="5437")
conn = psycopg2.connect(database="prueba", host="localhost", user="postgres", password="example", port="5433")

@app.route("/")
def index():
	return "Julio"

@app.route("/api/levels-roots", methods = ['POST'])
def getLevelsRoots():
	data = request.json
	methodology_id = data.get("methodology_id")
	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute(f"SELECT * FROM levels_roots WHERE methodology_id = {methodology_id};")
		res = cursor.fetchall()
		# cursor.execute(f"SELECT max(level) FROM levels WHERE methodology_id = {methodology_id};")
		# total_levels = cursor.fetchone()
		# # more_levels = False
		# # if total_levels['max'] > level:
		# # 	more_levels = True
		response = {
			"quantity": len(res),
			"levels_roots": res,
			# "more_levels": more_levels
		}
		return response

@app.route("/api/levels", methods = ['POST'])
def getLevels():
	data = request.json
	level = data.get("level")
	methodology_id = data.get("methodology_id")
	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute(f"SELECT * FROM levels WHERE level = {level} AND methodology_id = {methodology_id};")
		res = cursor.fetchall()
		cursor.execute(f"SELECT max(level) FROM levels WHERE methodology_id = {methodology_id};")
		total_levels = cursor.fetchone()
		more_levels = False
		if total_levels['max'] > level:
			more_levels = True
		response = {
			"quantity": len(res),
			"levels": res,
			"more_levels": more_levels
		}
		return response

@app.route("/api/query_products", methods = ['POST'])
def getProducts():
	data = request.json
	levels = data.get("levels")
	methodology_id = data.get('methodology_id')
	strict = data.get('strict')
	levels = json.dumps(levels)
	if strict == True:
		with conn.cursor(cursor_factory=RealDictCursor) as cursor:
			cursor.execute(f"""SELECT id, methodology_id, url, levels, extension FROM methodology_instance WHERE levels->>'levels' = '{levels}' AND methodology_id = {methodology_id};""")
			res = cursor.fetchall()
			response = {
				"quantity": len(res),
				"products": res
			}
			return response
	elif strict == False:
		# print("*"*100)
		# print(levels)
		# levels = levels.replace('[', "%")
		# levels = levels.replace(']', '%')
		levels = levels.replace('[', "")
		levels = levels.replace(']', '')
		levels = levels.replace('\"', '%')
		levels = levels.replace("\\", "\\\\")
		# print(levels)
		# print("CONSULTA")
		# print(f"""SELECT id, methodology_id, url, levels, extension FROM methodology_instance WHERE levels->>'levels' LIKE '{levels}' AND methodology_id = {methodology_id};""")
		with conn.cursor(cursor_factory=RealDictCursor) as cursor:
			cursor.execute(f"""SELECT id, methodology_id, url, levels, extension FROM methodology_instance WHERE levels->>'levels' ILIKE '{levels}' AND methodology_id = {methodology_id} ORDER BY levels->>'number_of_levels';""")
			res = cursor.fetchall()
			response = {
				"quantity": len(res),
				"products": res
			}
			return response
		# return "simón"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
