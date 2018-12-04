// function del_user(id) {
//     $.ajax({
//         data: {
//             id: id
//         },
//         type: 'POST',
//         url: '/del_user'
//     }).done(
//         function (data) {
//             if (data.status === 'success') {
//                 row_id = $('#row_' + id)
//                 row_id.remove()
//             } else {
//                 alert('Ошибка удаления пользователя!')
//             }
//         }
//     )
// }

// function del_parser(id) {
//     $.ajax({
//         data: {
//             id: id
//         },
//         type: 'POST',
//         url: '/del_parser'
//     }).done(
//         function (data) {
//             if (data.status === 'success') {
//                 row_id = $('#row_'+id)
//                 row_id.remove()
//             } else {
//                 alert('Ошибка удаления парсера!')
//             }
//         }
//     )
// }

// function get_last_data() {
//     $.get({
//         url: '/api/v1.0/get_last/10',
//         dataType: 'json'
//     }).done(
//         function (data) {
//             line = $('#dc_result')
//             line.empty()
            
//             for (let row in data) {
//                 for (let i in data[row]){
//                     console.log(data[row][i])
//                     line.append('<tr><td>' + data[row][i].id + '</td><td>' + data[row][i].parser_id + '</td><td>' + data[row][i].datestamp + '</td><td>' + data[row][i].json + '</td></tr>')
//                 }
//             }
//         }
//     )
// }

// TODO: написать функцию обновления сразу для всех
function get_admin_info(){
    $.get({
        url: '/dash/v1.0/dashboard/get_admin_info',
        dataType: 'json'
    }).done(
        function (data) {
            
            el_moderators = $('#moderators_count')
            el_parsers = $('#parsers_count')
            el_clients = $('#clients_count')
           

            console.log(data['data'])

            if (data['success'] === true) {
                
                if (el_moderators[0].innerText != data['data'].moderators_count) {

                    el_moderators[0].innerText = data['data'].moderators_count
                }

                if (el_parsers[0].innerText != data['data'].parsers_count) {

                    el_parsers[0].innerText = data['data'].parsers_count
                }

                if (el_clients[0].innerText != data['data'].clients_count) {

                    el_clients[0].innerText = data['data'].clients_count
                }

                if (data['data']['users']){
                    table_users = $('#dc-users-table')
                    table_users.empty()

                    for (var row in data['data']['users']) {
                        table_users.append("<tr id='row_id_" + data['data']['users'][row].id + "'><td>" + row + "</td> <td>" + data['data']['users'][row].name + "</td> <td>" + data['data']['users'][row].id + "</td> <td>" + data['data']['users'][row].active + "</td> <td>" + data['data']['users'][row].last_login + "</td> <td>" + data['data']['users'][row].last_logout +"</td></tr>")
                    } 
                }  
                

            } else {
                console.log(data['error'])
            }
            
        }
        
    )
}


// function add_user(name, password, role) {
//     $.ajax({
//         data: {
//             name: name,
//             password: password,
//             role: role

//         },
//         type: 'POST',
//         url: '/api/v1.0/add_user'
//     }).done(
//         function (data) {
//             if (data['success'] === true) {
//                 get_dashboard_info()
//                 console.log(data)
//             } else {
//                 console.log(data['error'])
//             }

//         }
//     )
// }



// Добавляем клиента
function add_client(name) {
    $.post({
        data: {
            name: name
        },
        type: 'POST',
        url: '/dash/v1.0/client/add_client'
    }).done(
        function (data) {
            if (data['success'] === true) {
                console.log(data)
            } else {
                console.log(data['error'])
            }
        }
    )
}


// ОБНОВЛЕНИЕ ДАННЫХ ДЛЯ СТАРНИЦЫ МОДЕРАТОРА
function get_moderator_info(){

    $.get({
        url: '/dash/v1.0/dashboard/get_moderator_info',
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
