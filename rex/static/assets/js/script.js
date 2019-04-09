var type = ['','info','success','warning','danger'];


var myapp = {
  method: function (){
    swal({
                title: 'Please choose your payment method.',
                buttonsStyling: false,
                confirmButtonClass: "btn btn-success",
                html:
                        'You can use <b>bold text</b>, ' +
                        '<a href="http://github.com">links</a> ' +
                        'and other HTML tags'
                }).then(function() {

                
                })
  },
	deposit: function(amount, profit){
        	swal({
                title: 'Please choose your payment method',
                text: ' ',
                type: 'info',
                showCancelButton: true,
                confirmButtonText: '<img class="market-logo" src="/static/assets/img/BTC.png" style=" width: 25px; "> Pay with Bitcoin',
                cancelButtonText: '<img class="market-logo" src="/static/assets/img/ETH.png" style=" width: 25px; "> Pay with Ethereum',
                confirmButtonClass: "btn btn-success",
                cancelButtonClass: "btn btn-danger",
                buttonsStyling: false
            }).then(function() {
                window.funLazyLoad.start();
              	$.ajax({
          					type: 'POST',
          					data: {'amount' : amount, 'profit' : profit},
                    url: '/account/submitdeposit',						
                    success: function(data) {
                        window.funLazyLoad.reset();
                        data = JSON.parse(data);
                        window.location.href = data.url;
                        // setTimeout(function(){ window.location.href = data.url; }, 2000);
                     
                    }
                });

            }, function(dismiss) {
                window.funLazyLoad.start();
                $.ajax({
                    type: 'POST',
                    data: {'amount' : amount, 'profit' : profit},
                    url: '/account/submitdeposit/ETH',            
                    success: function(data) {
                        window.funLazyLoad.reset();
                        data = JSON.parse(data);
                        window.location.href = data.url;
                        // setTimeout(function(){ window.location.href = data.url; }, 2000);
                     
                    }
                });
            })
    },

    withdrawal: function(withdrawal){
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
                    $('form#fromWithdraw').submit();
                  swal({
                    title: 'Deleted!',
                    text: '.',
                    type: 'success',
                    confirmButtonClass: "btn btn-success",
                    buttonsStyling: false
                  }).catch(swal.noop);
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

        
    }
}

$('#avatar_input').change(function() {
  $('#btn_update_avatar').show();
});
$('#btn_update_avatar').click(function(){
    $('form#frmAvatar').submit();
})