"use strict";

$(document).ready(function(){
    $('#verify').click(function(){
            if($(this).is(':checked')){
                document.getElementById("submitRegister").disabled = false;
            } else {
                document.getElementById("submitRegister").disabled = true; 
            }
        });


    $('.active_account_id').on('click',function(){
        //alert($(this).data('id'));
        $('#modalActiveCode #username_account').html($(this).data('username'));
        $('#modalActiveCode #customer_id').val($(this).data('id'));
        
        $('#modalActiveCode').modal('show');
    })

    $('#modalActiveCode #btnActiveCode').click(function(evt) {
        $.ajax({
            url: "/account/activecode",
            data: {
                code: $('#modalActiveCode #code').val(),
                customer_id: $('#modalActiveCode #customer_id').val()
            },
            type: "POST",
            beforeSend: function() {
                $('.btnConfirm').button('loading');
            },
            error: function(data) {
                $('.btnConfirm').button('reset');
            },
            success: function(data) {
                $('.btnConfirm').button('reset');
                var data = $.parseJSON(data);
                data.status == 'error' ? (
                    showNotification('top', 'right', data.message, 'danger')
                ) : (
                    showNotification('top', 'right', data.message, 'success')
                    
                   //setTimeout(function() {location.reload(true)}, 3)
                )
            }
        });

    });
});

function showNotification(from, align, msg, type) {
        /* type = ['','info','success','warning','danger','rose','primary'];*/
        var color = Math.floor((Math.random() * 6) + 1);
        $.notify({
            icon: "notifications",
            message: msg
        }, {
            type: type,
            timer: 3000,
            placement: {
                from: from,
                align: align
            }
        });
    }
$('#submitLogin').click(function(){
    $('form#frmLogin').submit();
    $('#submitLogin').hide();
})
$('#submitRegister').click(function(){
    $('form#frmRegister').submit();
    $('#submitRegister').hide();
})

$('#submitReset').click(function(){
    $('form#frmReset').submit();
    $('#submitReset').hide();
})