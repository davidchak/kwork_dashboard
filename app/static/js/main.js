function del_user(id) {
    $.ajax({
        data: {
            id: id
        },
        type: 'POST',
        url: '/del_user'
    }).done(
        function (data) {
            if (data.status === 'success') {
                row_id = $('#row_' + id)
                row_id.remove()
            } else {
                alert('Ошибка удаления пользователя!')
            }
        }
    )
}

function del_parser(id) {
    $.ajax({
        data: {
            id: id
        },
        type: 'POST',
        url: '/del_parser'
    }).done(
        function (data) {
            if (data.status === 'success') {
                row_id = $('#row_'+id)
                row_id.remove()
            } else {
                alert('Ошибка удаления парсера!')
            }
        }
    )
}

function get_last_data() {
    $.get({
        url: '/api/v1.0/get_last/10',
        dataType: 'json'
    }).done(
        function (data) {
            line = $('#dc_result')
            line.empty()
            
            for (let row in data) {
                for (let i in data[row]){
                    console.log(data[row][i])
                    line.append('<tr><td>' + data[row][i].id + '</td><td>' + data[row][i].parser_id + '</td><td>' + data[row][i].datestamp + '</td><td>' + data[row][i].json + '</td></tr>')
                }
            }
        }
    )
}


