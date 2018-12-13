function add_client() {
    el = $('#input_new_client_name')[0];
    if (el.value === "" || el.value === undefined) {
        alert('Укажите имя для нового клиента!')
    }
    $.ajax({
        data: {
            name: el.value,
        },
        type: 'POST',
        url: '/dash/v1.0/add_client'
    }).done(
        function (data) {
            console.log(data)
            if (data['success'] === true) {

                table = $('#dc-clients-table')
                table.append('<tr id="client_row_'+ data['resp_data']['id'] +'"> \
                        <td class="text-center">'+ data['resp_data']['id'] +'</td> \
                        <td class="text-center">'+ data['resp_data']['name'] +'</td> \
                        <td class="text-center dc_client_status">True</td> \
                        <td class="text-center">'+ data['resp_data']['token'] +'</td> \
                        <td id="dc_client_token_expiration_'+ data['resp_data']['id'] +'" class="text-center">'+ data['resp_data']['token_expiration'] +'</td> \
                        <td class="text-center">None</td> \
                        <td class="text-center"> \
                            <div class="input-group"> \
                                <input id="input_count_'+  data['resp_data']['id'] +'" type="number" class="form-control form-control-sm" style="max-width:60px;" aria-describedby="button-addon2" />  \
                                <div class="input-group-append"> \
                                    <button class="btn btn-sm btn-outline-secondary" type="button" id="button-addon2" onclick="update_token_expiration('+ data['resp_data']['id'] +')">Продлить</button> \
                                </div> \
                            </div> \
                        </td> \
                        <td class="text-center"> \
                            <button class="btn btn-sm btn-outline-warning mr-2" onclick="activ_deactiv_client('+ data['resp_data']['id'] +')">Деактивировать</button> \
                            <button class="btn btn-sm btn-outline-danger mr-2" onclick="del_client('+ data['resp_data']['id'] +')">Удалить</button> \
                        </td> \
                    </tr >')
                el.value = ""
                update_counters()
                
            } else {
                alert(data['error'])
            }
        }
    )
}


function activ_deactiv_client(id) {
    $.ajax({
        data: {
            id: id
        },
        type: 'POST',
        url: '/dash/v1.0/activ_deactiv_client'
    }).done(
        function (data) {
            console.log(data)
            if (data['success'] === true) {

                row_id = $('#client_row_' + id)

                if (row_id.children('.dc_client_status').text() === "True") {
                    row_id.children('.dc_client_status').text("False")
                } else {
                    row_id.children('.dc_client_status').text("True")
                }

            } else {
                alert(data['error'])
            }
        }
    )
}


function del_client(id) {
    $.ajax({
        data: {
            id: id
        },
        type: 'POST',
        url: '/dash/v1.0/del_client'
    }).done(
        function (data) {
            console.log(data)
            if (data['success'] === true) {
                row_id = $('#client_row_' + id)
                row_id.remove()
                update_counters()
            } else {
                alert(data['error'])
            }
        }
    )
}


function update_token_expiration(id) {
    count = $('#input_count_' + id)[0];
    token_expiration = $('#dc_client_token_expiration_'+ id)[0];
    if (count.value === '' || count === undefined ){
        alert('Укажите количество дней для продления!')
    }
    $.ajax({
        data: {
            id: id,
            count: count.value,
        },
        type: 'POST',
        url: '/dash/v1.0/update_client_token'
    }).done(
        function (data) {
            console.log(data)
            if (data['success'] === true) {
                token_expiration.innerText = data['resp_data']['token_expiration']
                count.value = ""
            } else {
                alert(data['error'])
            }
        }
    )
}


function update_counters() {
    $.get({
        url: '/dash/v1.0/get_moderator_counters',
        dataType: 'json'
    }).done(
        function (data) {

            el_clients = $('#clients_count')

            console.log(data['data'])

            if (data['success'] === true) {

                if (el_clients[0].innerText != data['data'].clients_count) {
                    el_clients[0].innerText = data['data'].clients_count
                }

            } else {
                console.log(data['error'])
            }

        }

    )
} 
