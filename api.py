from bottle import Bottle, run, request
import urllib2
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools', 'python', 'inventory'))
import query, inventory

app = Bottle()
inv = inventory.Inventory("inventory").root

def partToJson(part):
    return {'code':part.code,
            'name':part.name}

@app.route("/query")
def _query():
	q = request.query.q
	q = urllib2.unquote(q)
	matches = query.query(q, inv)
	
	return str({"results":[part.code for part in matches]})

@app.route("/part")
def _part():
    q = request.query.q
    q = urllib2.unquote(q)
    matches = list(query.query("code:" + q, inv))
    if len(matches) != 1:
        return "Part code " + q + " apparently has multiple items associated"

    item = matches[0]
    return str(partToJson(item))

if __name__ == "__main__":
	run(app=app, port=8080)
