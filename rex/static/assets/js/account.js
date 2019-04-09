$(function() {

  function readURL(input,element,confirm) {
    var url = input.value;
    var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
    if (input.files && input.files[0]&& (ext == "png" || ext == "jpeg" || ext == "jpg")) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $(element).attr('src', e.target.result);
            $(confirm).addClass('active');
        }
        reader.readAsDataURL(input.files[0]);
    }
  }
  $('#file_1').on('change',function(){
      readURL(this,'#img_1','#confirm_1');
  })
  $('#file_2').on('change',function(){
      readURL(this,'#img_2','#confirm_2');
  })
  $('#file_3').on('change',function(){
      readURL(this,'#img_3','#confirm_3');
  })


  $('#confirm_1').on('click',function(){
    if ($( "#confirm_1" ).hasClass( "active" ))
    {
      $('#identity_1').hide();
      $('#identity_2').show();
    }
    else
    {
      return false;
    }
  })

  $('#confirm_2').on('click',function(){
    if ($( "#confirm_2" ).hasClass( "active" ))
    {
      $('#identity_2').hide();
      $('#identity_3').show();
    }
    else
    {
      return false;
    }
  })

  $('#confirm_3').on('click',function(){
    if ($( "#confirm_3" ).hasClass( "active" ))
    {
      $('#form_verify').submit();
    }
    else
    {
      return false;
    }
  })

  
})



