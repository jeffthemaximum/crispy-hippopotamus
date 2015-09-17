var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('echo', function(data){
    $('#response').html('<p>'+data.echo+'</p>');
});

socket.on('cpu', function(data){
    $('#response').html('<p>'+data.cpu+'</p>');
});

function send(){
    socket.emit('send_message', {message : "hello, world"});
}
