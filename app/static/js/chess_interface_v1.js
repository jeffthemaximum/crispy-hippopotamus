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

		console.log("usrmove: " + usr_move);
		console.log("New position: " + game.fen());
		console.log("Old position: " + ChessBoard.objToFen(oldPos));
		console.log("Orientation: " + orientation);
		var whiteScoreData = comparePieceCount()['whiteScore'];
		var blackScoreData = comparePieceCount()['blackScore'];
		console.log("white score: " + whiteScoreData);
		console.log("black score: " + blackScoreData);

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
			console.log("cpumove: " + cpu_move);
			console.log("New position: " + game.fen());
			console.log("Old position: " + ChessBoard.objToFen(newPos));
			console.log("Orientation: " + orientation);
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

function isLetter(str) {
  return str.length === 1 && str.match(/[a-z]/i);
}

function pieceCount(fenStr) {
    var pieceCount = new Array();
    pieceCount = {
        'r': 0,
        'n': 0,
        'b': 0,
        'q': 0,
        'k': 0,
        'p': 0,
        'R': 0,
        'N': 0,
        'B': 0,
        'Q': 0,
        'K': 0,
        'P': 0
    };
    for (var i = 0; i < fenStr.length; i++){
        if (isLetter(fenStr[i])) {
            pieceCount[fenStr[i]] += 1
        }
    }
    return pieceCount;
}

function comparePieceCount(){
    var oldFenPieces = pieceCount(oldFen);
    var newFenPieces = pieceCount(newFen);
    var whiteScore = 0;
    var blackScore = 0;
    // standard point values https://en.wikipedia.org/wiki/Chess_piece_relative_value
    var pointValues = {
        'p': 1,
        'k': 3,
        'b': 3,
        'r': 5,
        'q': 9
    }
    for(key in oldFenPieces){
        if (oldFenPieces[key] != newFenPieces[key]){
            var difference = newFenPieces[key] - oldFenPieces[key];
            console.log("piece: " + key + " old count: " + oldFenPieces[key] + " new count: " + newFenPieces[key])
            //if piece is lowercase it's a black piece
            if (key == key.toLowerCase()) {
                blackScore += pointValues[key];
            } else if (key == key.toUpperCase()) {
                key = key.toLowerCase();
                whiteScore += pointValues[key];
            }
        }
    }
    return {'whiteScore': whiteScore, 'blackScore': blackScore}
}
