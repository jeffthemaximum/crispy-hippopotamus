var socket = io.connect('http://' + document.domain + ':' + location.port);

var updateList = function(line) {
    $('#response').prepend('<li>' + line + "</li>");
}

var updateTextArea = function(line) {
    var textBox = $("#thinking-output");
    line = line + "\\\n";
    textBox.val(line + textBox.val());
}

socket.on('echo', function(data){
    //console.log("socket: ", data.echo)
    updateList(data.echo);
    updateTextArea(data.echo);
});

socket.on('connect', function() {
    socket.emit('echo', {message: "connected"});
})
