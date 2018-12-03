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
function get_dashboard_info(){
    $.get({
        url: '/api/v1.0/dashboard/get_dashboard_info',
        dataType: 'json'
    }).done(
        function (data) {
            
            el_moderators = $('#moderators_count')
            el_parsers = $('#parsers_count')
            el_clients = $('#clients_count')
            table_users = $('#dc-users-table')
            table_users.empty()

            console.log(data)

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

                u_data = data['data']['users']

                for (let row in u_data ){
                    table_users.append("<tr id='user_row_" + u_data[row].id + "><td>" + u_data[row].id + "</td> <td>" + u_data[row].name + "</td> <td>" + u_data[row].active + "</td> <td>" + u_data[row].last_login + "</td> <td>" + u_data[row].last_logout + "</td> </tr>");
                } 

            } else {
                console.log(data['error'])
            }
            
        }
        
    )
}


function add_user(name, password, role) {
    $.ajax({
        data: {
            name: name,
            password: password,
            role: role

        },
        type: 'POST',
        url: '/api/v1.0/add_user'
    }).done(
        function (data) {
            if (data['success'] === true) {
                get_dashboard_info()
                console.log(data)
            } else {
                console.log(data['error'])
            }

        }
    )
}