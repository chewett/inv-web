from bottle import Bottle, run, request, static_file
import urllib2
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "tools", "python", "inventory"))
import query, inventory

app = Bottle()
inv = inventory.Inventory("inventory").root
PATH = os.path.dirname(os.path.abspath(__file__))

def part_json(part):

    if isinstance(part, inventory.Item) is True:
        partInfo = {
            "type"          : "Item",
            "code"          : part.code,
            "condition"     : part.condition,
            "description"   : part.description,
            "labelled"      : str(part.labelled),
            "name"          : part.name,
            "path"          : part.path[10:],
            "value"         : part.value,
            "parent"        : {"code":part.parent.code, "name" : part.parent.name}
        }
    elif isinstance(part, inventory.ItemGroup) is True:
        partInfo = {
            "type"          : "ItemGroup",
            "code"          : part.code,
            "description"   : part.description,
            "name"          : part.name,
            "path"          : part.path[10:],
        }
        
        partInfo["children"] = list()
        for code in part.children:
            partInfo['children'].append( [code, part.children[code].name])
    elif isinstance(part, inventory.ItemTree) is True:
        partInfo = {
            "type"          : "ItemTree",
            "name"          : part.name
        }

    return partInfo

@app.route("/query")
def _query():
    q = request.query.q
    q = urllib2.unquote(q)
    matches = query.query(q, inv)

    results =  [[part.code, part.name, part.path] for part in matches]
    return {"results" : results}

@app.route("/part")
def _part():
    q = request.query.q
    q = urllib2.unquote(q)
    matches = list(query.query("code:" + q, inv))

    if len(matches) > 1:
        return {"error" : "Part code " + q + " apparently has multiple items associated"}
    elif len(matches) == 0:
        return {"error" : "Cannot find item with part code " + q}

    item = matches[0]
    return part_json(item)

@app.route("/")
@app.route("/index.html")
def indexPage():
    return static_file("index.html", root=PATH)

if __name__ == "__main__":
    run(app=app, port=8080)
