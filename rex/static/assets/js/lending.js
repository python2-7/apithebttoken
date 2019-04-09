$(function() {
    FnLending();
    FnLendingRe();
    function FnLending(){
        $('#verifyLending').click(function(){
            if($(this).is(':checked')){
                document.getElementById("btnLending").disabled = false;
            } else {
                document.getElementById("btnLending").disabled = true; 
            }
        });

        $('#btnLending').click(function(evt) {
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
                    url: "/account/LendingConfirm",
                    data: {
                        usd_amount: $('#usd_amount').val()
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
                            $('.btc_balance').html(data.new_btc_balance),
                            $('.total_invest').html(data.new_total_invest),
                            $('#amount_sva').val(''),
                            $('#address_sva').val(''),
                            $('#password').val(''),
                            $('#Alert').show(),
                            setTimeout(function() {
                                location.reload(true);
                            }, 3000)
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

    function FnLendingRe(){
        $('#verifyLendingre').click(function(){
            if($(this).is(':checked')){
                document.getElementById("btnLendingRe").disabled = false;
            } else {
                document.getElementById("btnLendingRe").disabled = true; 
            }
        });

        $('#btnLendingRe').click(function(evt) {
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
                    url: "/account/LendingConfirmRe",
                    data: {
                        sva_amount: $('#sva_amount_reinvest').val(),
                        usd_amount: $('#usd_amount_reinvest').val()
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
                            $('.usd_balance').html(data.new_usd_balance),
                            $('.total_invest').html(data.new_total_invest),
                            $('#sva_amount_reinvest').val(''),
                            $('#usd_amount_reinvest').val(''),
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


    $('#AllSVA').click(function(e){
        var sva_balance = $(this).data("sva");
        var sva_usd = $('.sva_usd').val();
        var convert_usd_sva = (parseInt(sva_balance) * parseFloat(sva_usd)).toFixed(8)
        $('#usd_amount').val(parseFloat(convert_usd_sva));
        $('#sva_amount').val(parseFloat(sva_balance));
    });
    $('#Allusd_balance').click(function(e){
        var usd_balance = $(this).data("usd");
        var sva_usd = $('.sva_usd').val();
        $('#sva_amount_reinvest').val((parseInt(usd_balance)/parseFloat(sva_usd)).toFixed(8));
        $('#usd_amount_reinvest').val(parseInt(usd_balance));
    });

    $('#usd_amount_reinvest').on("change paste keyup", function() {
        var sva_usd = $('.sva_usd').val();
        var usd_balance = $('#usd_amount_reinvest').val();
        var convert_usd_sva = (parseFloat(usd_balance) / parseFloat(sva_usd)).toFixed(8)
        $('#sva_amount_reinvest').val(parseFloat(convert_usd_sva));
    });

    $('#usd_amount').on("change paste keyup", function() {
        var sva_usd = $('.sva_usd').val();
        var usd_amount = $('#usd_amount').val();
        var convert_usd_sva = (parseFloat(usd_amount) / parseFloat(sva_usd)).toFixed(8)
        $('#sva_amount').val(parseFloat(convert_usd_sva));
    });
    $('#sva_amount').on("change paste keyup", function() {
        var sva_usd = $('.sva_usd').val();
        var sva_amount = $('#sva_amount').val();
        var convert_usd_sva = (parseFloat(sva_amount) * parseFloat(sva_usd)).toFixed(8)
        $('#usd_amount').val(parseFloat(convert_usd_sva));
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


    $('#invests_trade #usd_amount').on('change',function(){
        $('#table-invests tr').css({'background' :'none'});
        $('#table-invests tr.'+$(this).val()+'').css({'background' :'#c4c9ea'});
        $('#btc_amount').val((parseFloat($(this).val())/parseFloat($('#price_usd_btc').val())).toFixed(8));
    })

})