init();

function init(){
	$.ajax({
    type: 'GET',
    url: 'http://neural-net.herokuapp.com/list-nets',
    contentType: 'application/json',
    success: createOptions,
    error: printError
  });  

	$("#createNN").click(postCreate);
}

function postCreate(){

}

function printError(a,b,error){
  window.alert("Can't connect to the neural net.");
}

function createOptions(data,x,y){
	window.alert("success!");

}