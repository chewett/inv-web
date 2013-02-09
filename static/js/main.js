
$(document).ready(function() {
    page = window.location.href.split("#")[1];

    if(page != undefined && page != "") {
        query(page);
    }
});

function hideAllSections() {
    $("#results").hide();
    $("#itemgroup").hide();
    $("#item").hide();
    $("#errorBox").hide();
}

function findPart() {
    loadPart($("#code").val());
}

function runQuery() {
    query($("#queryBox").val());
}

function errorFree(data) {
    if("error" in data) {
        hideAllSections();
        $("#errorBoxMsg").html(data["error"]);
        $("#errorBox").show();
        return false;
    }else{
        return true;
    }
}

function query(q) {
    document.location.hash = q;
    $.getJSON("query?q=" + q, function(data) {
        if (errorFree(data) == false) return;

        hideAllSections();
        $("#results").show();
        $("#resultsBody").html("");

        $("#queryString").html(q);

        for(item in data["results"]) {
           $("#resultsBody").append("<tr><td>"+
                                    "<a href='#code:"+data["results"][item][0]+"' onClick=\"loadPart('"+ data["results"][item] + "');\">"
                                    + data["results"][item][0] +"</a></td>"
                                    +"<td>"+ data["results"][item][1] + "</td>" 
                                    +"<td>"+ data["results"][item][2] + "</td>"
                                    +"</tr>");
        }
    });
}

function loadPart(code) {
    document.location.hash = "code:" + code
    $.getJSON("part?q=" + code, function(data) {
        if (errorFree(data) == false) return;

        if(data["type"] == "Item") {
            hideAllSections();
            $("#item").show();

            for(var i in data) {
                if(i == "parent") {
                    parent_line = "<a href='#code:" + data["parent"]["code"]
                                  + "' onClick=\"loadPart('"
                                  + data["parent"]["code"] + "')\">"
                                  + data["parent"]["name"] + "</a>";
                    $("#item_parent").html(parent_line);
                }else{
                    $("#item_" + i).html(data[i]);
                }
            }
        }else if(data["type"] == "ItemGroup") {
            hideAllSections();
            $("#itemgroup").show();

            for(var i in data) {
                $("#itemgroup_" + i).html(data[i]);
            }

            $("#itemgroup_parent").html(data["parent"].path);
            $("#itemgroup_parts_number").html(data["parts"].length);

            for(var i in data["parts"]) {
                part = data["parts"][i];
                var part_line = "<a href='#code:"+ part.code
                                + "' onclick=\"loadPart('"+part.code+"')\">"
                                + part.code + "</a> - " + part.name + "<br />\n";

                $("#itemgroup_parts").append(part_line);
            }

        }
    });
}