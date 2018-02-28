function pageLoad(){
    update_board()
    var tbl = document.getElementById("board");
    if (tbl != null) {
        for (var i = 0; i < tbl.rows.length; i++) {
            for (var j = 0; j < tbl.rows[i].cells.length; j++) {
                tbl.rows[i].cells[j].onclick = (function (i, j) {
                    return function () {
                        play_cell(j+(i*3))
                    };
                }(i, j));
            }
        }
    }
}




function update_board(){
var dataObject = { ACTION: "GETBOARD"};

$.ajax({ type: "POST",
         url: "",
         data: dataObject,//no need to call JSON.stringify etc... jQ does this for you
         cache: false,
         success: function(response){
            responseData = JSON.parse(response);
            board_data = responseData["BOARD"];
            console.log(board_data)
            for (i = 0; i < board_data.length; i++) {
                for (j = 0; j < board_data[i].length; j++) {
                    cell_num = j + (i*3)
                    cellID = "CELL" + cell_num
                    console.log(cellID)
                    document.getElementById(cellID).innerHTML = board_data[i][j]
                }
            }
        }
    });
}


function play_cell(cell){
player = document.querySelector('input[name="PLAYER"]:checked').value;
console.log(player)
var dataObject = { ACTION: "PLAY", CELL: cell, PLAYER: player};
$.ajax({ type: "POST",
         url: "",
         data: dataObject,//no need to call JSON.stringify etc... jQ does this for you
         cache: false,
         success: function(response){
            responseData = JSON.parse(response);
            board_data = responseData["BOARD"];
            console.log(board_data)
            for (i = 0; i < board_data.length; i++) {
                for (j = 0; j < board_data[i].length; j++) {
                    cell_num = j + (i*3)
                    cellID = "CELL" + cell_num
                    console.log(cellID)
                    document.getElementById(cellID).innerHTML = board_data[i][j]
                }
            }
        }
    });
    update_board()
}
