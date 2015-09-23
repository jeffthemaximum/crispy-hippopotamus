var orientation;

var move_board = function(game) {
    board_state = game.fen().split(" ")[0];
    board.position(board_state);
};

var onDrop = function(source, target, piece, newPos, oldPos, orientation) {

    var move = game.move({
        from: source,
        to: target,
        promotion: 'q' //not sure if I need this..
    });

    if (move === null) {
        return 'snapback';
    } else {
        //move usr piece
        usr_move = source + target;



        //save board state to db - crashed gunicorn server when running socketio worker
/*        $.getJSON('/fen_to_db', {
            fen_string: game.fen(),
            game_id: game_id,
            game_state: 'ongoing'
        }, function(data) {
            console.log(data);
        });*/



        //get usr_move from js to python
        $.get("/getmethod/<" + usr_move + ">");
        orientation = orientation;
        console.log("usrmove: " + usr_move);
        console.log("New position: " + game.fen());
        console.log("Old position: " + ChessBoard.objToFen(oldPos));
        console.log("Orientation: " + orientation);
        var secondsBefore = new Date().getTime();
        var whiteScoreData = comparePieceCount(ChessBoard.objToFen(oldPos), game.fen())['whiteScore'];
        var blackScoreData = comparePieceCount(ChessBoard.objToFen(oldPos), game.fen())['blackScore'];
        var secondsAfter = new Date().getTime();
        var functionTime = secondsAfter - secondsBefore;
        console.log("time: " + functionTime);
        console.log("white score: " + whiteScoreData);
        console.log("black score: " + blackScoreData);
        var currentUserScore = parseInt($("#user-score").text());
        $("#user-score").text(currentUserScore + whiteScoreData);

        var bloatedFunction = function(data){
            orientation = orientation;
            var cpu_move = $.parseJSON(data);
            //send();
            console.log(cpu_move);
/*          //old logic to parse AI coordinate move
            var cpuMoveFrom = cpu_move.substring(0,2);
            var cpuMoveTo = cpu_move.substring(3,5);

            //change this to accept SAN!!!!
            game.move({
                from: cpuMoveFrom,
                to: cpuMoveTo,
                promotion: 'q' //not sure if I need this..
            });*/

            //new logic to use SAN string move from AI to move in js

            //move game
            game.move(cpu_move);

            //old logic to move by coordinate, replaced by game.move(cpu_move)
            //where cpu_move is now SAN string
            //board.move(cpu_move);

            //move board
            move_board(game);

            //save game state to db
/*            $.get('/fen_to_db', {
                fen_string: game.fen(),
                game_id: game_id,
                game_state: 'ongoing'
            });*/

            console.log("cpumove: " + cpu_move);
            console.log("New position: " + game.fen());
            console.log("Old position: " + ChessBoard.objToFen(newPos));
            console.log("Orientation: " + orientation);
            var whiteScoreData = comparePieceCount(ChessBoard.objToFen(oldPos), game.fen())['whiteScore'];
            var blackScoreData = comparePieceCount(ChessBoard.objToFen(oldPos), game.fen())['blackScore'];
            console.log("white score: " + whiteScoreData);
            console.log("black score: " + blackScoreData);
            var currentCPUScore = parseInt($("#cpu-score").text());
            $("#cpu-score").text(currentCPUScore + blackScoreData);
        };

        $.get("/getpythondata", bloatedFunction);
    }
};

// do not pick up pieces if the game is over
// only pick up pieces for White
var onDragStart = function(source, piece, position, orientation) {
    if (game.in_checkmate() === true || game.in_draw() === true || piece.search(/^b/) !== -1) {
        return false;
    }
};

// update the board position after the piece snap
// for castling, en passant, pawn promotion
var onSnapEnd = function() {
    console.log("jeff: " + game.fen());
  board.position(game.fen());
};

var cfg = {
    onDragStart: onDragStart,
    draggable: true,
    dropOffBoard: 'snapback',
    position: 'start',
    onDrop: onDrop,
    onSnapEnd: onSnapEnd
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
            pieceCount[fenStr[i]] += 1;
        }
    }
    return pieceCount;
}

function comparePieceCount(oldFen, newFen){
    var whiteScore = 0;
    var blackScore = 0;
    var oldFenPieces = pieceCount(oldFen.split(" ")[0]);
    var newFenPieces = pieceCount(newFen.split(" ")[0]);
    // standard point values https://en.wikipedia.org/wiki/Chess_piece_relative_value
    var pointValues = {
        'p': 1,
        'k': 3,
        'b': 3,
        'n': 3,
        'r': 5,
        'q': 9
    };
    for(var key in oldFenPieces){
        if (oldFenPieces[key] != newFenPieces[key]){
            var difference = newFenPieces[key] - oldFenPieces[key];
            console.log("piece: " + key + " old count: " + oldFenPieces[key] + " new count: " + newFenPieces[key]);
            //if piece is lowercase it's a black piece
            if (key == key.toLowerCase()) {
                whiteScore += pointValues[key];
            } else if (key == key.toUpperCase()) {
                key = key.toLowerCase();
                blackScore += pointValues[key];
            }
        }
    }
    return {'whiteScore': whiteScore, 'blackScore': blackScore};
}

function killProc() {
    $.get("/killgame");
}

function set_viewer_config() {
    cfg = {
        draggable: false,
        position: 'start',
    };
    return cfg;
}

$(document).ready(function(){
    // check if game belongs to user
    game_id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);

    $.get("/does_user_own_game/" + game_id, function(data){
        var truth = $.parseJSON(data);
        console.log("truth: " + truth);
        if (truth === false) {
            cfg = set_viewer_config();
            setInterval(set_board_state, (5 * 1000));
        }
    });

    board = new ChessBoard('board', cfg);
    game = new Chess();

    function set_board_state() {
        $.get("/get_board_state/" + game_id, function(data){
            var board_state = $.parseJSON(data);
            board_state = board_state.split(" ")[0];
            board.position(board_state);
        });
    }

    function getGameIdPosts() {
        $('#posts_and_pages').load(document.URL +  ' #posts_and_pages');
    }

    $('a#saveAndQuit.btn.btn-default').on('click', function() {
        console.log("Save and quit clicked!");
        console.log(game.fen());
        data = {'fen_string': game.fen()};

        $.getJSON('/fen_to_db', {
            fen_string: game.fen(),
            game_state: 'done'
        }, function(data) {
            console.log(data);
        });
    });

    // catch chess-message form when submitted, send user to /chess-message/<game_id>
    $('.form').submit(function(ev) {
        ev.preventDefault(); // stop form from submitting
        //get current game_id from flask route
        var text = $('.form').find('textarea[id="body"]').val();
        //clear textarea field
        $('.form').find('textarea[id="body"]').val("");
        $.ajax({
            type : "POST",
            url : "/chess_message/" + game_id,
            data: text,
            contentType: 'application/json;charset=UTF-8',
            success: function(result) {
                console.log(result);
            }
        });

    });
    //refreshes posts at bottom of chess game every five seconds
    setInterval(getGameIdPosts, (5 * 1000));

    //kill game process when game_player leaves page
    $.get("/does_user_own_game/" + game_id, function(data){
        var truth = $.parseJSON(data);
        if (truth === true) {
            window.onbeforeunload = killProc;
        }
    });

});
