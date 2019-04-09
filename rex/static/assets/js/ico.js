$(function() {
    fnBuyICO();
    FnSmTransferToAccount();
    $('#checkUsername').click(function(evt) {
        var username = $('#Username').val();
        console.log(username);
        $.ajax({
            url: "/account/checkUsername",
            data: {
                'username':username
            },
            type: "POST",
            success: function(data) {
                var data = $.parseJSON(data);
                data.status == 'error' ? (
                    showNotification('top', 'right', data.message, 'danger')
                ) : (
                    showNotification('top', 'right', data.message, 'success')
                )
            }
        });

    });
     $('#Max').click(function(evt) {
        var sva_balance = $(this).data("sva");
        $('#sva_amount').val(parseFloat(sva_balance));
    });
    $('#MaxBtc').click(function(evt) {
        var btc_balance = $(this).data("btc");
        var btc_usd = $('.btc_usd').val();
        var sva_usd =  $('.sva_usd').val();
        $('#btc_amount').val(btc_balance);
        var btc_usd = (parseFloat(btc_balance)* parseFloat(btc_usd)).toFixed(2);
        var sva_quantity = (parseFloat(btc_usd) / parseFloat(sva_usd));
            sva_quantity = parseInt(sva_quantity);
        $('#sva_quantity').val(sva_quantity);
    });
    $('#sva_quantity').on("change paste keyup", function() {
            var sva_amount = $('#sva_quantity').val();
            var btc_usd = $('.btc_usd').val();
            var sva_usd =  $('.sva_usd').val();
            sva_usd = (parseFloat(sva_amount)*parseFloat(sva_usd)).toFixed(2);
            sva_btc = sva_usd/parseFloat(btc_usd);
            if (isNaN(sva_btc) ){
                $('#btc_amount').val('...');
            }else{
                sva_btc = parseFloat(sva_btc).toFixed(8);
                $('#btc_amount').val(parseFloat(sva_btc));
            }
            

    });
    $('#btc_amount').on("change paste keyup", function() {
            var btc_amount = $('#btc_amount').val();
            var btc_usd = $('.btc_usd').val();
            var sva_usd =  $('.sva_usd').val();
                btc_usd = (parseFloat(btc_amount)* parseFloat(btc_usd)).toFixed(2);
            var sva_quantity = (parseFloat(btc_usd) / parseFloat(sva_usd));
                sva_quantity = parseInt(sva_quantity).toFixed(0);
                $('#sva_quantity').val(sva_quantity);

    });
    function fnBuyICO() {
        $('#btnBuyICO').click(function(evt) {
            $.ajax({
                url: "/account/buyIco",
                data: {
                    sva_amount: $('#sva_quantity').val(),
                    password: $('#password_ico').val(),
                    btc_amount: $('#btc_amount').val(),
                    one_time_password: $('#onetime_ico').val()
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
                        $('.btc_balance').html(data.new_btc_balance),
                        $('#sva_quantity').val(0),
                         $('#btc_amount').val(0),
                        $('#password_ico').val(''),
                        $('#modalICO').hide(),
                        setTimeout(function() {
                            location.reload()
                        }, 1000)
                    )
                }
            });
        });
    }
    function FnSmTransferToAccount() {
        $('#btnTransferMember').click(function(evt) {
            $.ajax({
                url: "/account/transferAccount",
                data: {
                    sva_amount: $('#sva_amount').val(),
                    username: $('#Username').val(),
                    password: $('#password').val(),
                    one_time_password: $('#onetime_transfer').val()
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
                        $('#sva_amount').val(''),
                        $('#username').val(''),
                        $('#password').val(''),
                        $('#onetime_transfer').val('')
                    )
                }
            });
        });
    }
    $('#amount_token').on("change paste keyup", function() {
            var amount = $('#amount_token').val();
            $('#amount_token').removeClass('error')
            if (parseFloat(amount) < 10) {
                $('#amount_token').addClass('error').attr('placeholder', 'Please enter amount > 10');
                return false;
            }
            
            var rate = (parseFloat(amount) / 10).toFixed(8);
            $('#amount_coin_token').val(parseFloat(rate));


        });
    frmExchangeToken();
    function frmExchangeToken() {
        $('#btn-transfer-token').click(function(evt) {
            $.ajax({
                url: "/account/exchangeToken",
                data: {
                    amount_token: $('#amount_token').val()
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
                        $('#sva_amount').val(''),
                        $('.s_token').html(data.new_token)
                        // $('#password').val(''),
                        // $('#onetime_transfer').val('')
                    )
                }
            });
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