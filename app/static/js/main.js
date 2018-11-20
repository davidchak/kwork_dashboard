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