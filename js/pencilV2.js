

// The mousemove event handler.
var started = false;
var pictureWidth = 28;
var pictureHeigth = 28;
init();

function init () {
  canvas = document.getElementById("imageView");
  context = canvas.getContext("2d");
  context.lineJoin = "round";
  context.fillStyle = "Black";
  setLineWidth(10);
  tool = new tool_pencil();
  
  // Attach the mousedown, mousemove and mouseup event listeners.
  canvas.addEventListener('mousedown', ev_canvas, false);
  canvas.addEventListener('mousemove', ev_canvas, false);
  canvas.addEventListener('mouseup',   ev_canvas, false);

  // Add eventhandler for the buttons
  $("#clear").click(clearCanvas);
  $("#send").click(createPostRequest);

  $.ajax({
  type: 'GET',
  url: 'http://neural-net.herokuapp.com/list-nets',
  contentType: 'application/json',
  crossDomain: true,
  success: createOptions,
  error: printError
  });
}

// This painting tool works like a drawing pencil which tracks the mouse
// movements.
function tool_pencil () {
  var tool = this;
  this.started = false;

  // This is called when you start holding down the mouse button.
  // This starts the pencil drawing.
  this.mousedown = function (ev) {
      context.beginPath();
      context.moveTo(ev._x, ev._y);
      tool.started = true;
  };

  // This function is called every time you move the mouse. Obviously, it only
  // draws if the tool.started state is set to true (when you are holding down
  // the mouse button).
  this.mousemove = function (ev) {
    if (tool.started) {
      context.lineTo(ev._x, ev._y);
      context.stroke();
    }
  };

  // This is called when you release the mouse button.
  this.mouseup = function (ev) {
    if (tool.started) {
      tool.mousemove(ev);
      tool.started = false;
    }
  };
}
// The general-purpose event handler. This function just determines the mouse
// position relative to the canvas element.
function ev_canvas (ev) {
  
  if (ev.layerX || ev.layerX == 0) { // Firefox
    ev._x = ev.layerX;
    ev._y = ev.layerY;
  } else if (ev.offsetX || ev.offsetX == 0) { // Opera
    ev._x = ev.offsetX;
    ev._y = ev.offsetY;
  }

  // Call the event handler of the tool.
  var func = tool[ev.type];
  if (func) {
    func(ev);
  }
}

function clearCanvas(){
  canvas.width = canvas.width;
  setLineWidth(10);
}

function setLineWidth(width){
  context.lineWidth = width;
}

function createPostRequest(){
  var imageData = context.getImageData(0,0,10,10);
  placeholderCanvas = document.getElementById("resizedImage");
  context2 = placeholderCanvas.getContext("2d");
  var img = new Image();
  img.src = canvas.toDataURL("image/png");
  img.onload = function() {
       context2.drawImage(img, 0, 0, pictureWidth, pictureHeigth);
    };
  //aparently getImageData cant read the canvas right after the image was drawn onto it, therefor the timeout  
  window.setTimeout(fillArray,50);
}
function fillArray(){ 
  var imageData = context2.getImageData(0,0,pictureWidth,pictureHeigth);  
  var pixelArray = new Array(pictureWidth*pictureHeigth);
   //every pixel is described by the red, blue , green and alpha value, therfore the length is divided by 4 
  var arrayLength = imageData.data.length / 4;
  for (var i=0;i < arrayLength;i++){
    pixelArray[i] = imageData.data[i*4 + 3] / 255; //moving  the alpha value
  } 
  
  var jsonArray = JSON.stringify({"pattern":pixelArray,"net-id":$("#netList option:selected").text()});

  $.ajax({
    type: 'POST',
    url: 'http://neural-net.herokuapp.com/recognize-pattern',
    contentType: 'application/json',
    crossDomain: true,
    data: jsonArray, 
    dataType: 'json',
    success: printResult,
    error: printError
  });  

  //clear the placeholder canvas
  placeholderCanvas.width = placeholderCanvas.width;   
}

function printResult(data,b,c){
  if (data.success == 1){
    var htmlString = "<div class=\"col-lg-3\"><h3>Result</h3><p class=\"bigandfat\">"+data.result+"</p></div>"; 
    htmlString += "<div class=\"col-lg-3\"><h3>Distribution</h3><table class=\"table table-striped\"><tr><th>Number</th><th>Output</tr>";
    for (var i=0;i<data.distribution.length;i++){
      var prob = data.distribution[i];
      if (prob < 0.001){
        htmlString += "<tr><td>"+i+"</td><td><0.001</td></tr>";
      }else{
        htmlString += "<tr><td>"+i+"</td><td>"+prob+"</td></tr>";
      }
    }
    htmlString += "</table></div>";
    $("#result").html(htmlString);
  }
}
function printError(a,b,error){
  window.alert("Something went wrong. Pease try again.");
}

function createOptions(data,x,y){
  var htmlString2 = "";
  $.each(data.nets,function(key,value){
    htmlString2 += "<option>"+key+"<option>";
  });
  $("#netList").html(htmlString2);

  createNetInfo(data);
}

function createNetInfo(data){
  var htmlString3 = "<table class=\"table table-striped\"><tr><th>Net ID</th><th>Epoches</th><th>Lmbda</th><th>ETA</th><th>Number of Layers</th><th>Mini Batch Size</th></tr>";
  $.each(data.nets,function(key,value){
    var netObj = data.nets[key];
    htmlString3 += "<tr><td>"+key+"</td>";
    htmlString3 +=  "<td>"+data.nets[key].epochs+"</td>";
    htmlString3 +=  "<td>"+data.nets[key].lmbda+"</td>";
    htmlString3 +=  "<td>"+data.nets[key].eta+"</td>";
    htmlString3 +=  "<td>"+data.nets[key].layers.length+"</td>";
    htmlString3 +=  "<td>"+data.nets[key].mini_batch_size+"</td></tr>";
  })
  htmlString3 += "</table>";
  $("#netInfos").html(htmlString3);
}