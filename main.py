from flask import Flask, request
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from flask_cors import CORS

app = Flask (__name__)
CORS(app)

conn = psycopg2.connect(database="prueba", host="localhost", user="postgres", password="example", port="5432")


@app.route("/")
def index():
	return "Julio"

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
		# more_levels = json.dumps(more_levels)[0]
		# more_levels = more_levels[1
		# print("hay mas niveles: ", more_levels['max'])
		# levels = []
		# for item in res:
		# 	level_object = {
		# 		"id": item[0],
		# 		"name_level": item[1],
		# 		"level": item[2],
		# 		"methodology_id": item[3]
		# 	}
		# 	levels.append(level_object)
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
	levels = json.dumps(levels)
	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute(f"""SELECT id, methodology_id, path, levels, extension FROM methodology_instance WHERE levels->>'levels' = '{levels}' AND methodology_id = {methodology_id};""")
		res = cursor.fetchall()
		response = {
			"quantity": len(res),
			"products": res
		}
		return response
	# print("niveles: ", json.dumps(levels))
	# print(f"""SELECT id, methodology_id, path, levels, extension FROM methodology_instance WHERE levels->>'levels' = '{levels}' AND methodology_id = {methodology_id};""")
	# return data	


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)