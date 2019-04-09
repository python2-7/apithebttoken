$(function() {
    FnWithdraw();
    $('#btnDepositSVA').click(function(evt) {
        var sva_amount = $('#sva_amount_deposit').val();
        var sva_address = $('#sva_address').val();
        if (isNaN(sva_amount) || parseFloat(sva_amount) >= 0.01) {
            $('#qrSva').html('<img src="https://chart.googleapis.com/chart?chs=250x250&cht=qr&chl=sva:'+sva_address+'?amount='+sva_amount+'?message=SVA" alt="">')
        }
        
    });

    function FnWithdraw(){
        $('#btnSvaWithdraw').click(function(evt) {
        	swal({
                title: 'Are you sure?',
                text: '',
                type: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Yes',
                cancelButtonText: 'No',
                confirmButtonClass: "btn btn-success",
                cancelButtonClass: "btn btn-danger",
                buttonsStyling: false
            }).then(function() {
               $.ajax({
                    url: "/account/withdrawSVC",
                    data: {
                        sva_amount: $('#amount_sva').val(),
                        sva_address: $('#address_sva').val(),
                        password: $('#password').val()
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
                            showNotification('top', 'right', data.message, 'success'),
                            $('.sva_balance').html(data.new_sva_balance),
                            $('#amount_sva').val(''),
                            $('#address_sva').val(''),
                            $('#password').val(''),
                            $('#Alert').show()
                        )
                    }
                });
              
            }, function(dismiss) {
              // dismiss can be 'overlay', 'cancel', 'close', 'esc', 'timer'
              if (dismiss === 'cancel') {
                swal({
                  title: 'Cancelled',
                  text: '',
                  type: 'error',
                  confirmButtonClass: "btn btn-info",
                  buttonsStyling: false
                }).catch(swal.noop);
              }
            })
        });
    }

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


})