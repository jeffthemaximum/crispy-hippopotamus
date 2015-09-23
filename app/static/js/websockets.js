var socket = io.connect('http://' + document.domain + ':' + location.port);


socket.on('echo', function(data){
    //console.log("socket: ", data.echo)
    $('#response').prepend('<li>' + data.echo + "</li>");
});

socket.on('test', function(data){
    console.log("emit tester: " + data)
})


socket.on('cpu', function(data){
    $('#response').html('<p>'+data.cpu+'</p>');
});

function send(){
    socket.emit('send_message', {message : "hello, world"});
}

socket.on('connect', function() {
    socket.emit('echo', {message: "connected"});
})
