from flask import Flask, request
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from flask_cors import CORS

app = Flask (__name__)
CORS(app)

# conn = psycopg2.connect(database="nueva", host="alpha.tamps.cinvestav.mx", user="postgres", password="example", port="5437")
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
		response = {
			"quantity": len(res),
			"levels_roots": res,
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
			cursor.execute(f"""SELECT id, methodology_id, url, levels, extension, key FROM methodology_instance WHERE levels->>'levels' = '{levels}' AND methodology_id = {methodology_id};""")
			res = cursor.fetchall()
			response = {
				"quantity": len(res),
				"products": res
			}
			return response
	elif strict == False:
		levels = levels.replace('[', "")
		levels = levels.replace(']', '')
		levels = levels.replace('\"', '%')
		levels = levels.replace("\\", "\\\\")
		print(f"""SELECT id, methodology_id, url, levels, extension, key FROM methodology_instance WHERE levels->>'levels' ILIKE '{levels}' AND methodology_id = {methodology_id} ORDER BY levels->>'number_of_levels';""")
		with conn.cursor(cursor_factory=RealDictCursor) as cursor:
			cursor.execute(f"""SELECT id, methodology_id, url, levels, extension, key FROM methodology_instance WHERE levels->>'levels' ILIKE '{levels}' AND methodology_id = {methodology_id} ORDER BY levels->>'number_of_levels';""")
			res = cursor.fetchall()
			response = {
				"quantity": len(res),
				"products": res
			}
			return response
		# return "simón"

@app.route("/api/product")
def getProduct():
	data = request.args.get('id')
	print("DATA", "*"*50)
	print(data)
	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute("SELECT p.id, p.methodology_id, p.url, p.levels, p.extension, p.key, r.stars FROM methodology_instance as p, (SELECT avg(rating) as stars FROM ratings WHERE product_id = %s) as r WHERE p.key = %s", (data, data, ))
		res = cursor.fetchone()
		response = {
			"data": res,
		}
		return response

@app.route("/api/methodology-data")
def getMethodologyData():
	methodology_id = request.args.get('id')
	print("methodology", "*"*50)
	print(methodology_id)
	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute("SELECT * FROM methodology WHERE id = %s", (methodology_id,))
		res = cursor.fetchone()
		response = {
			"data": res,
		}
		return response

@app.route("/api/rating", methods = ['POST'])
def setRatingValue():
	data = request.json
	product_id = data.get("product_id")
	user_id = data.get("user_id")
	rating = data.get("rating")
	methodology_id = data.get("methodology_id")
	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute("INSERT INTO ratings (rating, user_id, product_id, methodology_id) VALUES (%s, %s, %s, %s)", (rating, user_id, product_id, methodology_id,))
		conn.commit()
		# cursor.execute(f"SELECT p.id, p.methodology_id, p.url, p.levels, p.extension, p.key, r.stars FROM methodology_instance as p, (SELECT avg(rating) as stars FROM ratings WHERE product_id = '{product_id}') as r WHERE p.key = '{product_id}'")
		cursor.execute("SELECT p.id, p.methodology_id, p.url, p.levels, p.extension, p.key, r.stars FROM methodology_instance as p, (SELECT avg(rating) as stars FROM ratings WHERE product_id = %s and methodology_id = %s) as r WHERE p.key = %s", (product_id, methodology_id, product_id, ))
		res = cursor.fetchall()
		print("la res", "*"*60)
		print(res)
		response = {
			"data": res
		}
		return response

@app.route("/api/rating")
def getRatings():
	methodology_id = request.args.get('id')
	print("methodology", "*"*50)
	print(methodology_id)
	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute("select avg(rating), product_id from ratings where methodology_id = %s GROUP BY product_id", (methodology_id,))
		res = cursor.fetchall()
		response = {
			"data": res,
		}
		return response

@app.route("/api/ratings/relevants")
def getRelevantRatings():
	with conn.cursor(cursor_factory=RealDictCursor) as cursor:
		# cursor.execute("select avg(rating) as stars, product_id from ratings GROUP BY product_id ORDER BY stars DESC LIMIT 15")
		cursor.execute("SELECT p.id, p.methodology_id, p.url, p.levels, p.extension, p.key, r.stars, r.product_id FROM methodology_instance as p, (SELECT avg(rating) as stars, product_id FROM ratings GROUP BY product_id ORDER BY stars DESC LIMIT 15) as r WHERE p.key = r.product_id ORDER BY r.stars DESC")
		res = cursor.fetchall()
		response = {
			"data": res,
		}
		return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
