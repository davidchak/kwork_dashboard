function add_user(){
    $('#addNewUser').on('click', function (event) {

        $.ajax({
            data: {
                name: $('#nameInput').val(),
                passwd: $('#passInput').val()
            },
            type: 'POST',
            url: '/adduser'
        })
            .done(function (data) {
                console.log(data)
                console.log(data.status)
            });

        event.preventDefault();

    });
}

function update_user_list(){
   
    $
    $.ajax({
        data: {
            name: $('#nameInput').val(),
            passwd: $('#passInput').val()
        },
        type: 'POST',
        url: '/getusers'
    })
        .done(function (data) {
            console.log(data)
            console.log(data.status)
        });

}




$(document).ready(function () {

    add_user()

});