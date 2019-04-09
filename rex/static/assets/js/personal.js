(function($) {

    $.getJSON("/account/count-binary", function(data) {
            $('.Network_Left').html(data.total_binary_left);
            $('.Network_Right').html(data.total_binary_right);
    });
    /*setTimeout(function(){ 
        $.getJSON("/account/calculatorBinary", function(data) {
               return true;
        });
    }, 3000);*/
    

    jQuery.fn.show_tree = function(node) {

        positon = node.iconCls.split(" ");

        var line_class = positon[1] + 'line ' + 'linefloor' + node.fl;
        var level_active = positon[0] + 'iconLevel';

        var node_class = positon[1] + '_node ' + 'nodefloor' + node.fl+ ' '+node.level+'_tresss';
        var html = '<div class=\'' + line_class + '\'></div>';

        x_p = "<div  class='customer_toolip " + positon[1] + "'>";
        x_p += "<table class='table table-bordered'><tbody><tr class='username'>";
        x_p += "<td colspan='2'> <div align='center'>" + node.username + "</div> </td></tr>";
        x_p += "<tr><td> <div align='center'>Sponsor</div> </td> <td> <div align='center'>" + node.sponsor + "</div> </td></tr>";
        
        x_p += "<tr><td> <div align='center'>Investment</div> </td> <td> <div align='center'>$" + node.totalPD + "</div> </td></tr>";
        x_p += "<tr><td> <div align='center'>Team Left</div> </td> <td> <div align='center'>$" + node.leftPD + "</div> </td></tr>";
        x_p += "<tr><td> <div align='center'>Team Right</div> </td> <td> <div align='center'>$" + node.rightPD + "</div> </td></tr>";
        x_p += "<tr><td> <div align='center'>Creation</div> </td> <td> <div align='center'>" + node.date_added + " </div> </td></tr>";
        x_p += "";
        x_p += "</tr>";

        html += !node.empty ?
            '<div class=\'' + node_class + ' ' + level_active + '\'><a data-html="true" data-toggle="tooltip" rel="tooltip" data-placement="top" data-title="<p>' + x_p + '</p>" class="binaryTree" style="display:block;"   \'><i class="fa fa- type-' + node.level + ' package-111" onclick=\'click_node("' + node.id + '")\' value=\'' + node.id + '\' aria-hidden="true"></i></a><span class="name_node">' + node.username + '</span>' :
            '<div class=\'' + node_class + '\'><a data-toggle="tooltip" data-placement="bottom" style="display:block" onclick=\'click_node_add("' + node.p_binary + '", "' + positon[1] + '")\' value=\'' + node.p_binary + '\' ><i class="fa fa-plus-square type-add"></i></a><span class="name_node">ADD TREE</span>';
        // : '<div class=\''+node_class+'\'><a data-toggle="tooltip" data-placement="bottom" style="display:block"  title=""><i class="fa fa-plus-square type-add"></i></a>';

        html += '<div id=\'' + node.id + '\' ></div>';

        html += '</div>';

        $(this).append(html);

        node.children && $.each(node.children, function(key, value) {

            $('#' + node.id).show_tree(value);

            $('[data-toggle="tooltip"]').tooltip();
        });


    };
    jQuery.fn.show_infomation = function(node) {

    };
    jQuery.fn.build_tree = function(id, method) {
        /*$.getJSON("http://0.0.0.0:8069/json_tree", function(json_data) {
            var rootnode = json_data[0];
            $('.personal-tree').html('');
            $('.personal-tree').show_tree(rootnode);
            $('.personal_contain').show_infomation(rootnode.id);
            $('#current_top').html("Goto " + rootnode.name + "\'s");
        });*/


        //$('.personal-tree').html('<img src="/static/assets/img/recycle-spinner.gif"  />');
        $.ajax({
            url: "/account/json_tree",
            dataType: 'json',
            type: "POST",
            data: {
                id_user: id
            },
            success: function(json_data) {
                var rootnode = json_data[0];
                $('.personal-tree').html('');
                $('.personal-tree').show_tree(rootnode);
                /*$('.personal_contain').show_infomation(rootnode.id);
                $('#current_top').html("Goto " + rootnode.name + "\'s");*/
            }
        });
    };
})(jQuery);

function click_node_add(p_binary, positon) {
    var link = '/account/add-tree/'+p_binary+'/'+positon;
    location.href = link;

    /*var link = '/user/new';
    if (positon == "left")
        positon = 1;
    else
        positon = 2;
    p_node = $('#uid_customer').val();
    link += '/' + positon + '/' + p_binary + '/' + p_node;
    // var link = '/user/register'+ '/' + p_binary;
    var html = `
        <div id="myModal" class="modal left fade" role="dialog">
        <div class="modal-dialog">
        <div class="modal-content">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <div class="text-center" style=" padding-top: 50px; ">
        <a href="` + link + `" target="_blank" class="btn btn-social btn-dashboard" style="margin-bottom: 5px;margin-right: 10px;">
        Register new Member
        </a>
        <button class="btn btn-social btn-dashboard btnConfirm" data-loading-text="<i class='fa fa-spinner fa-spin '></i> Processing" style="margin-bottom: 5px;" id="AddTree" data-binary="` + p_binary + `" data-position="` + positon + `">
        Add Tree
        </button>
        <input type="hidden" id="p_binaryTree" value="` + p_binary + `">
        <input type="hidden" id="positionTree" value="` + positon + `">
        </div>
        <div class="modal-footer">
        </div>
        </div>
        </div>
        </div>`;

    $('#alertTree').html(html);
    $('#myModal').modal({
        backdrop: 'static',
        keyboard: false
    });
    $('#personal').attr('style','position : absolute; width: 100%');
    chooseNode();*/

    
};


function chooseNode() {
    $('#AddTree').click(function() {
        var p_binary = $(this).data('binary');
        var position = $(this).data('position');
        $.ajax({
            url: "/account/getNewRefferal",
            data: {
                sva_amount: $('#amount_sva').val(),
                sva_address: $('#address_sva').val(),
                password: $('#password').val(),
                one_time_password: $('#onetime_sva').val()
            },
            type: "GET",
            beforeSend: function() {
                $('.btnConfirm').button('loading');
            },
            error: function(data) {
                $('.btnConfirm').button('reset');
            },
            success: function(data) {
                var data = $.parseJSON(data);
                if (data.status == 'error'){
                    showNotification('top', 'right', data.message, 'danger')
                }
                
                $('.btnConfirm').button('reset');
                if (data.status == 'success') {
                    var data_html = `
                    <div id="modalRefferal" class="modal  left fade" role="dialog">
                    <div class="modal-dialog">
                    <div class="modal-content">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                    <table id="datatables_history" class="table table-striped table-no-bordered table-hover" style="width:100%;cellspacing:0">
                    <thead>
                    <tr>
                    <th>Fullname</th>
                    <th>Username</th>
                    <th>Add Tree</th>
                    </tr>
                    </thead>
                    <tbody>
                    ` + data.refferal + `
                    </tbody>
                    </table>
                    <div class="modal-footer" style=" height: 100px; padding-bottom: 10px; ">
                    <button class="btn btn-social btn-dashboard btnConfirm" data-loading-text="<i class='fa fa-spinner fa-spin '></i> Processing" style="margin-bottom: 5px;" id="ConfrimAdd" data-binary="1120172601345" data-position="1">
                    Confirm
                    </button>
                    </div>
                    </div>
                    </div>
                    </div>`;

                    $('#dataRefferal').html(data_html);
                    $('#datatables_history').DataTable({
                        "order": [
                            [1, "desc"]
                        ],
                        "pagingType": "full_numbers",
                        "lengthMenu": [
                            [10, 25, 50, -1],
                            [10, 25, 50, "All"]
                        ],
                        autoWidth: false,
                        searching: false,
                        ordering: true,
                        responsive: true,
                        lengthChange: false,
                        destroy: true,
                        paging: true,
                        info: false

                    });
                    $('#modalRefferal').modal({
                        backdrop: 'static',
                        keyboard: false
                    });
                    addnewUser();
                }

            }
        });

    })
}

function addnewUser() {
    $('#ConfrimAdd').click(function() {
        var uid = $('input[name="choose"]:checked').val();
        var p_binary = $('#p_binaryTree').val();
        var positon = $('#positionTree').val();
        $.ajax({
            url: "/account/confrimAddTree",
            data: {
                'uid': uid,
                'p_binary': p_binary,
                'positon': positon
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
                    setTimeout(function() {
                        location.reload();
                    }, 2000)
                )

            }
        });

    })
}
$('#btnSearchTree').click(function() {
        var username = $('#search_tree').val();
        $.ajax({
            url: "/account/SearchTree",
            data: {
                'username': username,
                'uid': $('#uid_customer').val()
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
                    // showNotification('top', 'right', data.message, 'danger'),
                    click_node(data.uid)
                ) : (
                    click_node(data.uid)
                    // showNotification('top', 'right', data.message, 'success')
                )

            }
    });

})

function click_node(id) {

    jQuery(document).build_tree(id, 'getJsonBinaryTree_Admin');
    $('.tooltip').hide();
    !_.contains(window.arr_lick, id) && window.arr_lick.push(id);
}
window.arr_lick = [];

function click_back() {
    if (window.arr_lick.length === 0) {
        click_node($('#uid_customer').val());
    } else {
        window.arr_lick = _.initial(window.arr_lick);
        typeof _.last(window.arr_lick) !== 'undefined' ? click_node(_.last(window.arr_lick)) : click_node($('#uid_customer').val());
    }
}

function upto_level(id) {
    var top = jQuery('.personal-tree' + id + ' > div a').eq(0).attr('value');
    jQuery(document).build_tree(top, 'getJsonBinaryTreeUplevel');
}

function goto_bottom_left(id) {
    jQuery(document).build_tree(id, 'goBottomLeft');
}

function goto_bottom_right(id) {
    jQuery(document).build_tree(id, 'goBottomRight');
}

function goto_bottom_left_oftop(id) {
    var top = jQuery('.personal-tree' + id + ' > div a').eq(0).attr('value');
    jQuery(document).build_tree(top, 'goBottomLeft');
}

function goto_bottom_right_oftop(id) {
    var top = jQuery('.personal-tree' + id + ' > div a').eq(0).attr('value');
    jQuery(document).build_tree(top, 'goBottomRight');
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

jQuery(document).ready(function($) {
    click_node($('#uid_customer').val());
});