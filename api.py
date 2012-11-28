from bottle import Bottle, run, request, static_file
import urllib2
import sys, os, json

sys.path.append(os.path.join(os.path.dirname(__file__), "tools", "python", "inventory"))
import query, inventory

app = Bottle()
inv = inventory.Inventory("inventory").root
PATH = os.path.dirname(os.path.abspath(__file__))

def partToJson(part):

    if part.__class__.__name__ == "Item":
        partInfo = {
            "type"          : "Item",
            "code"          : part.code,
            "condition"     : part.condition,
            "description"   : part.description,
            "labelled"      : str(part.labelled),
            "name"          : part.name,
            "path"          : part.path,
            "value"         : part.value,
            "parent"        : {"code":part.parent.code, "name" : part.parent.name}
        }

    elif part.__class__.__name__ == "ItemGroup":
        partInfo = {
            "type"          : "ItemGroup",
            "code"          : part.code,
            "description"   : part.description,
            "name"          : part.name,
            "path"          : part.path
        }


    return json.dumps(partInfo)

@app.route("/query")
def _query():
    q = request.query.q
    q = urllib2.unquote(q)
    matches = query.query(q, inv)

    results =  [[part.code, part.name, part.path] for part in matches]
    return json.dumps({"results": results})

@app.route("/part")
def _part():
    q = request.query.q
    q = urllib2.unquote(q)
    matches = list(query.query("code:" + q, inv))

    if len(matches) > 1:
        return json.dumps({"error" : "Part code " + q + " apparently has multiple items associated"})
    elif len(matches) == 0:
        return json.dumps({"error" : "Cannot find item with part code " + q})

    item = matches[0]
    return partToJson(item)

@app.route("/index.html")
def indexPage():
    return open(PATH + "/index.html").read()

if __name__ == "__main__":
    run(app=app, port=8080)
