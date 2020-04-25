(function(cropper,undefined){"use strict";var canvas;var context;var image;var restoreImage;var currentDimens={};var cropping=false;var colors={white:"#ffffff",black:"#000000",overlay:"rgba(0, 0, 0, 0.6)"};var overlay;function draw(){context.clearRect(0,0,canvas.width,canvas.height);if(image===undefined){return;}
var dimens=currentDimens;context.drawImage(image,0,0,dimens.width,dimens.height);if(cropping){drawOverlay();var x=overlay.x+overlay.width-5,y=overlay.y+overlay.height-5,w=overlay.resizerSide,h=overlay.resizerSide;context.save();context.fillStyle=colors.black;context.strokeStyle=colors.white;context.fillRect(x,y,w,h);context.strokeRect(x,y,w,h);context.restore();}}
function drawOverlay(){context.save();context.fillStyle=colors.overlay;context.beginPath();context.moveTo(0,0);context.lineTo(overlay.x,overlay.y);context.lineTo(overlay.x+overlay.width,overlay.y);context.lineTo(canvas.width,0);context.moveTo(canvas.width,0);context.lineTo(overlay.x+overlay.width,overlay.y);context.lineTo(overlay.x+overlay.width,overlay.y+overlay.height);context.lineTo(canvas.width,canvas.height);context.moveTo(canvas.width,canvas.height);context.lineTo(overlay.x+overlay.width,overlay.y+overlay.height);context.lineTo(overlay.x,overlay.y+overlay.height);context.lineTo(0,canvas.height);context.moveTo(0,canvas.height);context.lineTo(overlay.x,overlay.y+overlay.height);context.lineTo(overlay.x,overlay.y);context.lineTo(0,0);context.fill();context.restore();}
function setRatio(ratio){overlay.ratioXY=ratio;overlay.height=Math.floor(overlay.width*ratio);}
function getScaledImageDimensions(width,height){var factor=1;if((canvas.width-width)<(canvas.height-height)){factor=canvas.width/width;}else{factor=canvas.height/height;}
var dimens={width:Math.floor(width*factor),height:Math.floor(height*factor),factor:factor};return dimens;}
function isInOverlay(x,y){return x>overlay.x&&x<(overlay.x+overlay.width)&&y>overlay.y&&y<(overlay.y+overlay.height);}
function isInHandle(x,y){return x>(overlay.x+overlay.width-overlay.resizerSide)&&x<(overlay.x+overlay.width+overlay.resizerSide)&&y>(overlay.y+overlay.height-overlay.resizerSide)&&y<(overlay.y+overlay.height+overlay.resizerSide);}
var drag={type:"",inProgress:false,originalOverlayX:0,originalOverlayY:0,originalX:0,originalY:0,originalOverlayWidth:0,originalOverlayHeight:0};function addEventListeners(){canvas.onmousedown=function(event){var coords=canvas.getMouseCoords(event);var x=coords.x;var y=coords.y;if(isInOverlay(x,y)){drag.type="moveOverlay";drag.inProgress=true;drag.originalOverlayX=x-overlay.x;drag.originalOverlayY=y-overlay.y;}
if(isInHandle(x,y)){drag.type="resizeOverlay";drag.inProgress=true;drag.originalX=x;drag.originalY=y;drag.originalOverlayWidth=overlay.width;drag.originalOverlayHeight=overlay.height;}};canvas.onmouseup=function(event){drag.inProgress=false;};canvas.onmouseout=function(event){drag.inProgress=false;};canvas.onmousemove=function(event){var coords=canvas.getMouseCoords(event);var x=coords.x;var y=coords.y;if(isInHandle(x,y)||(drag.inProgress&&drag.type==="resizeOverlay")){canvas.style.cursor='nwse-resize'}else if(isInOverlay(x,y)){canvas.style.cursor='move'}else{canvas.style.cursor='auto'}
if(!drag.inProgress){return;}
if(drag.type==="moveOverlay"){overlay.x=x-drag.originalOverlayX;overlay.y=y-drag.originalOverlayY;var xMax=canvas.width-overlay.width;var yMax=canvas.height-overlay.height;if(overlay.x<0){overlay.x=0;}else if(overlay.x>xMax){overlay.x=xMax;}
if(overlay.y<0){overlay.y=0;}else if(overlay.y>yMax){overlay.y=yMax;}
draw();}else if(drag.type==="resizeOverlay"){overlay.width=drag.originalOverlayWidth+(x-drag.originalX);if(overlay.width<10){overlay.width=10;}
if(overlay.x+overlay.width>canvas.width){overlay.width=canvas.width-overlay.x;}
overlay.height=overlay.width*overlay.ratioXY;if(overlay.y+overlay.height>canvas.height){overlay.height=canvas.height-overlay.y;overlay.width=overlay.height/overlay.ratioXY;}
draw();}};}
function cropImage(entire){if(image===undefined){return false;}
if(!cropping){entire=true;}
var x=0;var y=0;var width=image.width;var height=image.height;if(!entire){var factor=currentDimens.factor;x=Math.floor(overlay.x/factor);y=Math.floor(overlay.y/factor);width=Math.floor(overlay.width/factor);height=Math.floor(overlay.height/factor);if(x<0){x=0;}
if(x>image.width){x=image.width;}
if(y<0){y=0;}
if(y>image.height){y=image.height;}
if(x+width>image.width){width=image.width-x;}
if(y+height>image.height){height=image.height-y;}}
var cropCanvas=document.createElement("canvas");cropCanvas.setAttribute("width",width);cropCanvas.setAttribute("height",height);var cropContext=cropCanvas.getContext("2d");cropContext.drawImage(image,x,y,width,height,0,0,width,height);return cropCanvas;}
function dataUrlToBlob(dataURI){var byteString=atob(dataURI.split(',')[1]);var mimeString=dataURI.split(',')[0].split(':')[1].split(';')[0];var ab=new ArrayBuffer(byteString.length);var ia=new Uint8Array(ab);for(var i=0;i<byteString.length;i++){ia[i]=byteString.charCodeAt(i);}
return new Blob([ia],{type:mimeString});}
cropper.showImage=function(src){cropping=false;image=new Image();image.onload=function(){currentDimens=getScaledImageDimensions(image.width,image.height);draw();};image.src=src;};cropper.startCropping=function(){if(image===undefined){return false;}
restoreImage=new Image();restoreImage.src=image.src;cropping=true;draw();return true;};cropper.getCroppedImageSrc=function(){if(image){var cropCanvas=cropImage(!cropping);var url=cropCanvas.toDataURL("png");if(cropping){cropper.showImage(url);}
cropping=false;return url;}else{return false;}};cropper.getCroppedImageBlob=function(type){if(image){var cropCanvas=cropImage(!cropping);var url=cropCanvas.toDataURL(type||"png");if(cropping){cropper.showImage(url);}
cropping=false;return dataUrlToBlob(url);}else{return false;}};cropper.start=function(newCanvas,ratio){canvas=newCanvas;if(!canvas.getContext){return;}
context=canvas.getContext("2d");overlay={x:50,y:50,width:100,height:100,resizerSide:10,ratioXY:1}
if(ratio){setRatio(ratio);}
addEventListeners();};cropper.restore=function(){if(restoreImage===undefined){return false;}
cropping=false;cropper.showImage(restoreImage.src);return true;};HTMLCanvasElement.prototype.getMouseCoords=function(event){var totalOffsetX=0;var totalOffsetY=0;var canvasX=0;var canvasY=0;var currentElement=this;do{totalOffsetX+=currentElement.offsetLeft;totalOffsetY+=currentElement.offsetTop;}
while(currentElement=currentElement.offsetParent)
canvasX=event.pageX-totalOffsetX;canvasY=event.pageY-totalOffsetY;return{x:canvasX,y:canvasY}}}(window.cropper=window.cropper||{}));