$(function() {
    
    FunctionAmountTransfer();
    FnSmTransfer();
    function FunctionAmountTransfer() {
        $('#amount_transfer').on("change paste keyup", function() {
            var sva_usd = $('.sva_usd').val();
            var amount = $('#amount_transfer').val();

            if (isNaN(amount)) {
                $('#amount_transfer').val('0');
                $('#amount_transfer').val('0');
                $('#amount_transfer').addClass('error').attr('placeholder', 'Please enter is number!');
                return false;
            } else {
                $('#amount_transfer').removeClass('error').attr('placeholder', 'Amount');
            }
            if (parseFloat(amount) < 1) {
                $('#amount_transfer').addClass('error').attr('placeholder', 'Please enter amount > 100');
                return false;
            }
            var rate = (parseFloat(amount) / parseFloat(sva_usd)).toFixed(8);
            $('#amount_coin_transfer').val(parseFloat(rate));


        });
    }


    function FnSmTransfer() {
        $('#btn-transfer').click(function(evt) {
            $.ajax({
                url: "/account/transferusd",
                data: {
                    amount: $('#amount_transfer').val()
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
                        $('.usd_balance').html(data.new_usd_balance),
                        $('#amount_coin_transfer').val(''),
                        $('#amount_transfer').val('')
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

    /*Buy XVG*/
    $('#frmBuyXVG #amount_xvg').on('input propertychange', function() {
       var price_xvg = $('#frmBuyXVG #price_xvg_btc').val();   
       $('#frmBuyXVG #amount_btc').val((parseFloat(price_xvg) * parseFloat($('#frmBuyXVG #amount_xvg').val())).toFixed(8));
    });


    $('#frmBuyXVG #btnbuyxvg').click(function(evt) {
        $.ajax({
            url: "/account/submitbuyxvg",
            data: {
                amount: $('#frmBuyXVG #amount_xvg').val()
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
                    $('.xvg_balance').html(data.new_xvg_balance),
                    $('.btc_balance').html(data.new_btc_balance),

                    $('#frmBuyXVG #amount_xvg').val(''),
                    $('#frmBuyXVG #amount_btc').val('')
                )
            }
        });
    });
    /*end Buy XVG*/

    /*Sell XVG*/
    $('#frmSellXVG #amount_xvg').on('input propertychange', function() {
       var price_xvg = $('#frmSellXVG #price_xvg_btc').val();   
       $('#frmSellXVG #amount_btc').val((parseFloat(price_xvg) * parseFloat($('#frmSellXVG #amount_xvg').val())).toFixed(8));
    });


    $('#frmSellXVG #btnsellxvg').click(function(evt) {
        $.ajax({
            url: "/account/submitsellxvg",
            data: {
                amount: $('#frmSellXVG #amount_xvg').val()
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
                    $('.xvg_balance').html(data.new_xvg_balance),
                    $('.btc_balance').html(data.new_btc_balance),

                    $('#frmSellXVG #amount_xvg').val(''),
                    $('#frmSellXVG #amount_btc').val('')
                )
            }
        });
    });
    /*end Sell XVG*/


    /*convert usd -> btc*/
    $('#ConvertUSDBTC #amount_usd').on('input propertychange', function() {
       var price_btc = $('#ConvertUSDBTC #price_usd_btc').val(); 

       $('#ConvertUSDBTC #amount_btc').val((parseFloat($('#ConvertUSDBTC #amount_usd').val())/parseFloat(price_btc)).toFixed(8));
    });

    $('#ConvertUSDBTC #btnconvertusdbtc').click(function(evt) {
        $.ajax({
            url: "/account/submitconvertusdbtc",
            data: {
                amount: $('#ConvertUSDBTC #amount_usd').val()
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
                    $('.btc_balance').html(data.new_btc_balance),

                    $('#ConvertUSDBTC #amount_usd').val(''),
                    $('#ConvertUSDBTC #amount_btc').val('')
                )
            }
        });
    });



    $('#Buycode #numbercode').on('input propertychange', function() {
       var price_btc = $('#Buycode #price_usd_btc').val();   
       $('#Buycode #amount_btc').val((parseFloat($('#Buycode #numbercode').val()*20)/parseFloat(price_btc)).toFixed(8));
    });

    $('#modalTranfers #btntransfer').click(function(evt) {
        $.ajax({
            url: "/account/transferusd",
            data: {
                amount: $('#modalTranfers #amount').val(),
                username: $('#modalTranfers #username').val(),
                password: $('#modalTranfers #password').val()
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
                    

                    $('#modalTranfers #amount').val(''),
                    $('#modalTranfers #username').val('')
                )
            }
        });
    });
    /*end convert usd -> btc*/

    $('#Buycode #btnBuyCode').click(function(evt) {
        $.ajax({
            url: "/account/buycode",
            data: {
                numbercode: $('#Buycode #numbercode').val()
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
                    
                    $('#Buycode #numbercode').val(''),
                   $('#Buycode #amount_btc').val(''),
                   setTimeout(function() {location.reload(true)}, 3)
                )
            }
        });
    });


    

    
})