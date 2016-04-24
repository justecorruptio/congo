function human_coord_to_pos(coord){
    var pos = [0, 0];
    pos[0] = 19 - parseInt(coord.substr(1));
    var x = coord.charCodeAt(0) - 65;
    if(x > 26){
        x -= 32;
    }
    if(x > 7){
        x--;
    }
    pos[1] = x;
    return pos;
}

function pos_to_sgf(pos){
    return String.fromCharCode(97 + (pos[1])) +
        String.fromCharCode(97 + (pos[0]));
}

function get_tonari(board, i, j){
    var rows = board.length;
    var cols = board[0].length;
    var tonari = []
    if(i > 0) tonari.push([i - 1, j]);
    if(j > 0) tonari.push([i, j - 1]);
    if(i < rows - 1) tonari.push([i + 1, j]);
    if(j < cols - 1) tonari.push([i, j + 1]);
    return tonari;
}

function has_libs(board, i, j, marks){
    var rows = board.length;
    var cols = board[0].length;
    var color = board[i][j];
    var other;
    if(marks[i * cols + j]){
        return 0;
    }
    marks[i * cols + j] = 1;
    var libs = 0;
    var tonari = get_tonari(board, i, j);
    for(var n = 0; n < tonari.length; n++){
        var t_i = tonari[n][0];
        var t_j = tonari[n][1];
        other = board[t_i][t_j];
        libs |= other?other == color?
            has_libs(board, t_i, t_j, marks):0:1;
    }
    return libs;
}

function remove_marks(board, marks){
    var rows = board.length;
    var cols = board[0].length;
    var count = 0;
    for(var i = 0; i < rows; i++){
        for(var j = 0; j < cols; j++){
            if(marks[i * cols + j]){
                board[i][j] = 0;
                count ++;
            }
        }
    }
    return count;
}

function play_move(board, color, pos){
    var a = pos[0];
    var b = pos[1];
    var rows = board.length;
    var cols = board[0].length;
    if(board[a][b]){
        return 0;
    }
    board[a][b] = color;
    var marks;
    var tonari = get_tonari(board, a, b);
    var kills = 0;
    for(var n = 0; n < tonari.length; n++){
        var t_i = tonari[n][0];
        var t_j = tonari[n][1];
        if(board[t_i][t_j] + color == 3){
            marks = new Array(rows * cols);
            if(!has_libs(board, t_i, t_j, marks)){
                kills += remove_marks(board, marks);
            }
        }
    }
    marks = new Array(rows * cols);
    if(!has_libs(board, a, b, marks) && !kills) {
        board[a][b] = 0;
        return 0;
    }
    return 1;
}
