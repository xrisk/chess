function stateOfGame(ID, callback) {
    var req = new XMLHttpRequest();
    req.responseType = "json";
    req.onreadystatechange = function(e) {
        if (req.readyState == 4) {
            if (req.response != null) {
                var r = JSON.parse(req.response)["data"];
                if (r["joined"]["w"] && r["joined"]["b"])
                    callback(2);
                else if (r["joined"]["w"] || r["joined"]["b"])
                    callback(1);
                else
                    callback(0);
            } else {
                callback(-1);
            }
        }
    }
var url = `http://l33tchess-api.herokuapp.com/status/${ID}/`;
console.log(url);
req.open("GET", url);
req.send();
}


function createGame(ID, Color) {

	//Return 1 for success, 0 or fail
}
function joinGame(ID) {
	//Return -1 for fail
	//Return 0 for Black
	//Return 1 for White
}
function submitMove(ID, Move) {
	//Return -1 for fail
	//Return
}
