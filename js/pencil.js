

// The mousemove event handler.
var started = false;
var lineSize = 0;
init();

function init () {
  canvas = document.getElementById('imageView');
  context = canvas.getContext("2d");
  context.lineJoin = "round";
  
  // Attach the mousemove event handler.
  canvas.addEventListener('mousemove', ev_mousemove, false);
  //document.getElementById('clear').addEventListener('click',clearCanvas(),false);
}

function ev_mousemove (ev) {
  var x, y;
  lineSize = document.getElementById("linestyle").value;
  context.lineWidth = lineSize;
  // Get the mouse position relative to the canvas element.
  if (ev.layerX || ev.layerX == 0) { // Firefox
    x = ev.layerX;
    y = ev.layerY;
  } else if (ev.offsetX || ev.offsetX == 0) { // Opera
    x = ev.offsetX;
    y = ev.offsetY;
  }

  // The event handler works like a drawing pencil which tracks the mouse
  // movements. We start drawing a path made up of lines.
  if (!started) {
    context.beginPath();
    context.moveTo(x, y);
    started = true;
  } else {
    context.lineTo(x, y);
    context.stroke();
  }
}

function clearCanvas(){
  canvas.width = canvas.width;
}
