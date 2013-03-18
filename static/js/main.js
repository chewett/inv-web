
var hash = "";


$(document).ready(function() {
    var page = window.location.href.split("#")[1];

    if(page !== undefined && page !== "") {
        query(page);
    }

    setInterval("trackHash()", 50);
});

function trackHash() {
    var curHash = location.hash.split("#")[1];

    if(curHash != hash) {
        hash = curHash;
        query(curHash);
    }
}

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
    if(data.hasOwnProperty("error")) {
        hideAllSections();
        $("#errorBoxMsg").html(data.error);
        $("#errorBox").show();
        return false;
    }else{
        return true;
    }
}

function query(q) {
    document.location.hash = q;
    $.getJSON("query?q=" + q, function(data) {
        if (errorFree(data) === false) { return; }

        hideAllSections();
        $("#results").show();
        $("#resultsBody").html("");
        $("#queryString").html(q);

        for(var item in data.results) {
            $("#resultsBody").append("<tr><td>"+
                                    "<a href='#code:"+data.results[item][0]+"' onClick=\"loadPart('"+ data.results[item] + "');\">"
                                    + data.results[item][0] +"</a></td>"
                                    +"<td>"+ data.results[item][1] + "</td>" 
                                    +"<td>"+ data.results[item][2] + "</td>"
                                    +"</tr>");
        }
    });
}

function loadPart(code) {
    document.location.hash = "code:" + code;
    $.getJSON("part?q=" + code, function(data) {
        if (errorFree(data) === false) { return; }
        var i;

        //converts links in brackets to actual links
        data.description = data.description.replace(/\((http[s]?:\/\/[^\)]*)\)/gi, "<a href=\"$1\">$1</a>");

        if(data.type == "Item") {
            hideAllSections();
            $("#item").show();
            $("#item_code").attr("href", "#code:" + data.code);
            $("#item_name").attr("href", "#type:" + data.name);
            //TODO: this stops you loading other pages for some reason
            //$("#item_code").click(loadPart(data["code"]));

            for(i in data) {
                if(i == "parent") {
                    var parentLine = "<a href='#code:" + data.parent.code
                                  + "' onClick=\"loadPart('"
                                  + data.parent.code + "')\">"
                                  + data.parent.name + "</a>";
                    $("#item_parent").html(parentLine);
                }else{
                    $("#item_" + i).html(data[i]);
                }
            }
        }else if(data.type == "ItemGroup") {
            hideAllSections();
            $("#itemgroup").show();
            
            for(i in data) {
                $("#itemgroup_" + i).html(data[i]);
            }

            var parentLine;
            if(data.parent.hasOwnProperty("code")) {
                parentLine = "<a href='#code:" + data.parent.code
                              + "' onClick=\"loadPart('"
                              + data.parent.code + "')\">"
                              + data.parent.name + "</a>";
            }else{
                parentLine = data.parent.path;
            }

            $("#itemgroup_parent").html(parentLine);
            $("#itemgroup_parts_number").html(data.parts.length);
            $("#itemgroup_code").attr("href", "#code:" + data.code);
            $("#itemgroup_name").attr("href", "#type:" + data.name);
            $("#itemgroup_table").hide();

            for(i in data.parts) {
                var part = data.parts[i];
                var partLine = "<tr><td><a href='#code:"+ part.code
                                + "' onclick=\"loadPart('"+part.code+"')\">"
                                + part.code + "</a></td><td>" + part.name + "</td></tr>\n";

                $("#itemgroup_parts").append(partLine);
            }
        }
    });
}
