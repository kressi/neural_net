

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
  var obj={};
  obj.pattern = pixelArray;
  var jsonArray = JSON.stringify(obj);
  console.log(jsonArray);
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
  //window.location = canvas.toDataURL("image/png");   
}

function printResult(data,b,c){
  window.alert("success!");
}
function printError(a,b,error){
  window.alert(error);
}