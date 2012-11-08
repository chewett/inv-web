from bottle import Bottle, run, request
import urllib2
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools', 'python', 'inventory'))
import query, inventory

app = Bottle()
inv = inventory.Inventory("inventory").root

@app.route("/query")
def _query():
	q = request.query.q
	q = urllib2.unquote(q)
	matches = query.query(q, inv)
	
	return str({"results":[part.code for part in matches]})
	
	
if __name__ == "__main__":
	run(app=app, port=8080)
