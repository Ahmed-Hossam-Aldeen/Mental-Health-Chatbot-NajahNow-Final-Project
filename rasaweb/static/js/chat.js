function play() {
    var audio = document.getElementById('audio');
    audio.play(); 
}
var send = document.getElementById('send');
send.addEventListener("click", play)