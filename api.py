from bottle import Bottle, run, request, static_file
import urllib2
import sys, os
from pyparsing import ParseException

sys.path.append(os.path.join(os.path.dirname(__file__), "tools", "python", "inventory"))
import query, inventory

INVENTORY_PATH = "inventory"

app = Bottle()
inv = inventory.Inventory(INVENTORY_PATH).root
PATH = os.path.dirname(os.path.abspath(__file__))

#used to remove the "inventory" prefix,
def clean_path(path_string):
    return path_string[len(INVENTORY_PATH):]


def part_json(part):

    base_info = {
        "name"      : part.name,
        "path"      : clean_path(part.path),
        "parent"    : get_parent(part.parent)
    }
    if hasattr(part.parent, "code"):
        base_info["parent"]["code"] = part.parent.code

    if isinstance(part, inventory.Item) is True:
        part_info = {
            "type"          : "Item",
            "code"          : part.code,
            "condition"     : part.condition,
            "description"   : part.description,
            "labelled"      : str(part.labelled),
            "value"         : part.value
        }
    elif isinstance(part, inventory.ItemGroup) is True:
        part_info = {
            "type"          : "ItemGroup",
            "code"          : part.code,
            "description"   : part.description,
            "parts"         : [{"code": item_part.code, "name": item_part.name} for item_part in part.parts.values()]
        }

    part_info = dict(part_info.items() + base_info.items())

    return part_info

#should only have ItemGroup and ItemTree passed into the function
def get_parent(part):
    parent_info = {
        "type"  : "ItemTree",
        "name"  : part.name,
        "path"  : clean_path(part.path),
    }
    if isinstance(part, inventory.ItemGroup) is True:
        parent_info["type"] = "ItemGroup"
        parent_info["code"] = part.code

    return parent_info

@app.route("/query")
def _query():
    q = request.query.q
    q = urllib2.unquote(q)
    try:
        matches = query.query(q, inv)
    except ParseException:
        return {"error" : "Query string was malformed"}

    results =  [[part.code, part.name, clean_path(part.path)] for part in matches]
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
    run(app=app, host="0.0.0.0", port=8080)
