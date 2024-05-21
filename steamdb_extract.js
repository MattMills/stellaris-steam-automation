//Used to copy paste into the console to get an initial copy of historical manifests from steamDB

var myRows = [];
var $headers = $("div#manifests").find("th");
var $rows = $("div#manifests").find("tbody tr").each(function(index) {
  $cells = $(this).find("td");
  myRows[index] = {};
  $cells.each(function(cellIndex) {
    myRows[index][$($headers[cellIndex]).text()] = $(this).text().trim();
  });    
});

// Let's put this in the object like you want and convert to JSON (Note: jQuery will also do this for you on the Ajax request)
var myObj = {};
myObj.myrows = myRows;

JSON.stringify(myRows)
