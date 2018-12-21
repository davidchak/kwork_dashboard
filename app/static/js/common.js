function del_user(id) {
    $.ajax({
        data: {
            id: id
        },
        type: 'POST',
        url: '/dash/v1.0/del_user'
    }).done(
        function (data) {
            console.log(data)
            if (data['success'] === true) {
                row_id = $('#user_row_' + id)
                row_id.remove()
                update_counters()
            } else {
                alert(data['error'])
            }
        }
    )
}


function activ_deactiv_user(id) {
    $.ajax({
        data: {
            id: id
        },
        type: 'POST',
        url: '/dash/v1.0/activ_deactiv_user'
    }).done(
        function (data) {
            console.log(data)
            if (data['success'] === true) {

                row_id = $('#user_row_' + id)

                if (row_id.children('.dc_user_status').text() === "True") {
                    row_id.children('.dc_user_status').text("False")
                } else {
                    row_id.children('.dc_user_status').text("True")
                }

            } else {
                alert(data['error'])
            }
        }
    )
}


function add_user() {
    login = $('#input_new_user_login')[0];
    password = $('#input_new_user_password')[0];
    role = $('#select_new_user_role')[0];

    if (login.value === "" || login.value === undefined) {
        alert('Укажите логин для нового пользователя!')
    }

    if (password.value === "" || password.value === undefined) {
        alert('Укажите пароль для нового пользователя!')
    }

    $.ajax({
        data: {
            login: login.value,
            password: password.value,
            role: role.value
        },
        type: 'POST',
        url: '/dash/v1.0/add_user'
    }).done(
        function (data) {
            console.log(data)
            if (data['success'] === true) {

                table = $('#dc-users-table')
                table.append('<tr id="user_row_' + data['resp_data']['id'] + '"> \
                    <th scope="row">' + data['resp_data']['id'] + '</th> \
                    <td>'+ data['resp_data']['name'] + '</td> \
                    <td>'+ data['resp_data']['role'] + '</td> \
                    <td class="dc_user_status">True</td> \
                    <td class="text-center">None</td> \
                    <td class="text-center">None</td> \
                    <td class="text-center"> \
                        <button class="btn btn-sm btn-outline-primary mr-2" onclick="activ_deactiv_user(' + data['resp_data']['id'] + ')">Актив./Деактив.</button> \
                        <button class="del_user_btn btn btn-sm btn-outline-danger mr-2" onclick="del_user(' + data['resp_data']['id'] + ')">удалить</button> \
                    </td> \
                </tr>')
                login.value = ""
                password.value = ""
                update_counters()

            } else {
                alert(data['error'])
            }
        }
    )
}


function add_parser() {
    parser_name = $('#input_new_parser')[0];

    if (parser_name.value === "" || parser_name.value === undefined) {
        alert('Укажите имя нового парсера!')
    }

    $.ajax({
        data: {
            name: parser_name.value
        },
        type: 'POST',
        url: '/dash/v1.0/add_parser'
    }).done(
        function (data) {
            console.log(data)
            if (data['success'] === true) {

                table = $('#dc-parsers-table')
                table.append('<tr id="parser_row_' + data['resp_data']['id'] + '"> \
                        <th scope="row">' + data['resp_data']['id'] + '</th> \
                        <td ><a href="/admin_panel/parsers/' + data['resp_data']['id'] + '">' + data['resp_data']['name'] + '</td> \
                        <td class="text-center">' + data['resp_data']['token'] + '</td> \
                        <td class="text-center"> \
                            <button class="del_user_btn btn btn-sm btn-outline-danger mr-2" onclick="del_parser( ' + data['resp_data']['id'] + ' )">Удалить</button> \
                        </td> \
                    </tr >')
                parser_name.value = ""
                update_counters()

            } else {
                alert(data['error'])
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
        url: '/dash/v1.0/del_parser'
    }).done(
        function (data) {
            console.log(data)
            if (data['success'] === true) {
                row_id = $('#parser_row_' + id)
                row_id.remove()
                update_counters()
            } else {
                alert(data['error'])
            }
        }
    )
}


function update_counters() {
    $.get({
        url: '/dash/v1.0/get_admin_counters',
        dataType: 'json'
    }).done(
        function (data) {

            el_admins = $('#admins_count')
            el_moderators = $('#moderators_count')
            el_parsers = $('#parsers_count')
            el_clients = $('#clients_count')


            console.log(data['data'])

            if (data['success'] === true) {

                if (el_admins[0].innerText != data['data'].admins_count) {
                    el_admins[0].innerText = data['data'].admins_count
                }

                if (el_moderators[0].innerText != data['data'].moderators_count) {
                    el_moderators[0].innerText = data['data'].moderators_count
                }

                if (el_parsers[0].innerText != data['data'].parsers_count) {
                    el_parsers[0].innerText = data['data'].parsers_count
                }

                if (el_clients[0].innerText != data['data'].clients_count) {
                    el_clients[0].innerText = data['data'].clients_count
                }

            } else {
                console.log(data['error'])
            }

        }

    )
} 

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
                table.append('<tr id="client_row_' + data['resp_data']['id'] + '"> \
                        <td class="text-center">'+ data['resp_data']['id'] + '</td> \
                        <td class="text-center">'+ data['resp_data']['name'] + '</td> \
                        <td class="text-center dc_client_status">True</td> \
                        <td class="text-center">'+ data['resp_data']['token'] + '</td> \
                        <td id="dc_client_token_expiration_'+ data['resp_data']['id'] + '" class="text-center">' + data['resp_data']['token_expiration'] + '</td> \
                        <td class="text-center">None</td> \
                        <td class="text-center"> \
                            <div class="input-group"> \
                                <input id="input_count_'+ data['resp_data']['id'] + '" type="number" class="form-control form-control-sm" style="max-width:60px;" aria-describedby="button-addon2" />  \
                                <div class="input-group-append"> \
                                    <button class="btn btn-sm btn-outline-secondary" type="button" id="button-addon2" onclick="update_token_expiration('+ data['resp_data']['id'] + ')">Продлить</button> \
                                </div> \
                            </div> \
                        </td> \
                        <td class="text-center"> \
                            <button class="btn btn-sm btn-outline-warning mr-2" onclick="activ_deactiv_client('+ data['resp_data']['id'] + ')">Деактивировать</button> \
                            <button class="btn btn-sm btn-outline-danger mr-2" onclick="del_client('+ data['resp_data']['id'] + ')">Удалить</button> \
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
    token_expiration = $('#dc_client_token_expiration_' + id)[0];
    if (count.value === '' || count === undefined) {
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
