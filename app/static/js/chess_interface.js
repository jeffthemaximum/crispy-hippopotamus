$(document).ready(function(){
    board = new ChessBoard('board', cfg);
    game = new Chess();
});

var onDrop = function(source, target, piece, newPos, oldPos, orientation) {

	var move = game.move({
		from: source,
		to: target,
		promotion: 'q' //not sure if I need this..
	});

	if (move == null) {
		return 'snapback'
	} else {
		usr_move = source + target
		//post move data to python
		//$.post( "/postmethod/", {javascript_data: usr_move});
		//get usr_move from js to python
		$.get("/getmethod/<" + usr_move + ">")

		console.log("gnumove: " + usr_move);
		
		$.get("/getpythondata", function(data){

			var cpu_move = $.parseJSON(data)
			console.log(cpu_move)
			board.move(cpu_move)
			var cpuMoveFrom = cpu_move.substring(0,2)
			var cpuMoveTo = cpu_move.substring(3,5)
			game.move({
				from: cpuMoveFrom,
				to: cpuMoveTo,
				promotion: 'q' //not sure if I need this..
			});
		})
	}
};

// do not pick up pieces if the game is over
// only pick up pieces for White
var onDragStart = function(source, piece, position, orientation) {
	if (game.in_checkmate() === true || game.in_draw() === true || piece.search(/^b/) !== -1) {
		return false;
	}
};


var cfg = {
	onDragStart: onDragStart,
	draggable: true,
	dropOffBoard: 'snapback',
	position: 'start',
	onDrop: onDrop
};