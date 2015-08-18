if (typeof(cfg) === 'undefined') {
    var cfg = {
        draggable: false,
        position: 'start',
    };
}

$(document).ready(function(){
    board = new ChessBoard('board', cfg);
    game = new Chess();
    game_id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);

    function getGameIdPosts() {
        $('#posts_and_pages').load(document.URL +  ' #posts_and_pages');
    }

	$('a#saveAndQuit.btn.btn-default').on('click', function() {
		console.log("Save and quit clicked!");
		console.log(game.fen());
		data = {'fen_string': game.fen()}

		$.getJSON('/fen_to_db', {
			fen_string: game.fen()
		}, function(data) {
			console.log(data)
		})
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
});
