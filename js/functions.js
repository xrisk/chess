function getID(){
	//Extracts the ID from the URL
	var ID = window.location.href;
	//Check for trailing slash
	if (ID.slice(-1) == '/') {
		ID = ID.substring(0, ID.length - 1);
	}
	return ID.substring(ID.lastIndexOf('/')+1);
}







function errorOut(msg){
	//Errors out and displays a message
	alert('ERROR: '+msg);
}