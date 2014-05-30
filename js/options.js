init();

function init(){

	$("#createNN").click(postCreate);
	$("#deleteNN").click(postDelete);

	$.ajax({
    type: 'GET',
    url: 'http://neural-net.herokuapp.com/list-nets',
    contentType: 'application/json',
    crossDomain: true,
    success: createOptions,
    error: printError
  });  

}

function postCreate(){

	var jsonArray = JSON.stringify({
		"net-id":$("#net-id").val()
		,"epochs":$("#epochs").val()
		,"eta":$("#eta").val()
		,"lmbda":$("#lmbda").val()
		,"layers":$("#layers").val().split(",")});

  	$.ajax({
	    type: 'POST',
	    url: 'http://neural-net.herokuapp.com/train-mnist',
	    contentType: 'application/json',
	    crossDomain: true,
	    data: jsonArray,
	    dataType: 'json',
	    success: printSuccess,	
	    error: printError
  	});	

 }

function postDelete(){
	var jsonArray = JSON.stringify({"net-id":$("#netList option:selected").text()});

  	$.ajax({
	    type: 'POST',
	    url: 'http://neural-net.herokuapp.com/delete',
	    contentType: 'application/json',
	    crossDomain: true,
	    data: jsonArray,
	    dataType: 'json',
	    success: printSuccess,	
	    error: printError
  	});	

 }

function printSuccess(data,a,b){
	if (data.success==1){
		window.alert("It worked!");
	}else{
		window.alert(data.message);
	}
}

function printError(a,b,error){
  	window.alert("Can't connect to the neural net server.");
}

function createOptions(data,x,y){
	var htmlString = "";
	$.each(data.nets,function(key,value){
		if (key.length > 0){		
			htmlString += "<option>"+key+"<option>";
		}
	});
	$("#netList").html(htmlString);
}