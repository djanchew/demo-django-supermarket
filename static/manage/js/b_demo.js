// span菜单功能
$('.b_span').on('click', function () {
    $('#sidebar_toggle').click();
});

// 左侧菜单栏自动收起
$('.nav-dropdown').on('click', function () {
    // console.log($(this).attr('class'));
        $(this).siblings('li').attr('class', 'nav-item nav-dropdown')
});
// $("ul>li>a").click(function(){
//                     $(this).next("ul").toggle().closest("li").siblings("li").children("ul").hide();
//                 }).next("ul").hide();

//所有账号页面
//在模板加一个加载css和js的自定义block？

//转到修改页面，传递id
$('.mod_manager').on('click',function () {
    console.log(this.id);
    window.location.href='/account_update?id='+this.id;
});

//删除账号，传递id
$('.del_manager').on('click',function () {
    console.log(this.id);
    if(confirm("确认删除？")){
        window.location.href='/account_delete?id='+this.id;
    }
});

//供应商页面。商品信息也可以这样？还是用进货那个页面
$('.del_pro').on('click',function () {
    console.log(this.id);
    if(confirm("确认删除？")){
        window.location.href='/provider_delete?id='+this.id;
    }
});
$('.mod_pro').on('click',function () {
    // console.log(this.id);
    // console.log($(this).parent().siblings());
    $(this).parent().siblings().filter(":not('#none')").each(function () {
        $(this).html('<input class="form-control" type="text" name="'+$(this).text()+'" id="'+this.id+'" value="'+$(this).text()+'"> ')
    });
    $(this).toggle().siblings().toggle()
});
$('.mod_cancel').on('click',function () {
    $(this).toggle().siblings().toggle();
    $(this).parent().siblings().filter(":not('#none')").each(function () {
        // console.log($(this).html());
        // console.log($(this).find('.form-control').attr('name'));
        var v = $(this).find('.form-control').attr('name');
        $(this).html(v);
    });
});
$('.mod_confirm').on('click',function () {
    console.log($(this).attr('id'));
    var data = {
        id: $(this).attr('id'),
        name: $("td #mod_p_name").val(),
        phone: $("td #mod_p_phone").val(),
        address: $("td #mod_p_address").val(),
        };
        console.log(data);
        $.post('/provider_update/', data, function (text, status) {
            alert(text);
            if(text==="ok"){
                console.log("okok");
                // $(".card-body").load(location.href + " .card-body");
                window.location.href="/provider";
            }
            else{
                console.log("nono");
            }
        });
});
$("#add_p_name #add_p_phone #add_p_address").keydown(function(e) {
           if (e.keyCode == 13) {
                $(".add_pro").click();
           }
      });
$('.add_pro').on('click',function () {
    if ($('#add_p_name').val().length != 0 && $('#add_p_phone').val().length != 0 && $('#add_p_address').val().length != 0 ) {
        var data = {
            name: $("#add_p_name").val(),
            phone: $("#add_p_phone").val(),
            address: $("#add_p_address").val(),
        };
        console.log(data);
        $.post('/provider_add/', data, function (text, status) {
            alert(text);
            if(text==="ok"){
                console.log("okok");
                // $(".card-body").load(location.href + " .card-body");
                window.location.href="/provider";
            }
            else{
                console.log("nono");
            }
        });
    }
    else {
        alert("请检查输入内容！");
    }
});


// 计算人数
function counter() {
    //获取每个表格的列数
    var count_0 = 0;
    $("#auth_0 tbody").find("tr:Visible").each(function(){
        count_0++;
    });
    $("#t_0").text(count_0);
    var count_1 = 0;
    $("#auth_1 tbody").find("tr:Visible").each(function(){
        count_1++;
    });
    $("#t_1").text(count_1);
    var count_2 = 0;
    $("#auth_2 tbody").find("tr:Visible").each(function(){
        count_2++;
    });
    $("#t_2").text(count_2);
    var count_3 = 0;
    $("#auth_3 tbody").find("tr:Visible").each(function(){
        count_3++;
    });
    $("#t_3").text(count_3);
    var count_num = 0;
    $(".count_p tbody").find("#p_tr:Visible").each(function(){
        console.log(count_num);
        count_num++;
    });
    $("#p_count").text(count_num);
}
// 页面加载的时候运行一次计算
counter();

//搜索，不请求后台直接js获取
//按权限显示
$("#select_by_auth").change(function(){
  var v = $(this).val();
  if(v){
      $("#auth_"+v).css("display", "block");
      $("#auth_"+v).siblings().css("display", "none");
  }
  else {
      $("#auth_1").css("display", "block");
      $("#auth_1").siblings().css("display", "block");
  }
});
//按性别显示
$("#select_by_gender").change(function(){
    var v = $(this).val();
    console.log(v);
    $("tbody").find("tr").each(function(){
        var tdArr = $(this).children().filter("#order_flag");
        if (v === '1') {
            // $(".table tr:not('#thead')").hide().filter(":contains('男')").show(); //有bug，用下面的替代，ok
            tdArr.filter(":contains('男')").parent().show();
            tdArr.filter(":contains('女')").parent().hide();
        }
        else if (v === '0') {
            // $(".table tr:not('#thead')").hide().filter(":contains('女')").show();
            tdArr.filter(":contains('女')").parent().show();
            tdArr.filter(":contains('男')").parent().hide();
        }
        else{
            $(".table tr:not('#thead')").show();
        }
    });
    counter()
});
//按关键字搜索
$("#s_key").keydown(function(e) {
           if (e.keyCode == 13) {
                $("#search").click();
           }
      });
$("#search").on("click", function () {
    var key = $('#s_key').val();
    $("tbody").find("tr").each(function(){
        var tdArr = $(this).children();
            $(".table tr:not('#thead')").hide().filter(":contains('"+key+"')").show();
        // if (key===tdArr.eq(2).text()){
        //     $(this).css('display', '');
        // }
        // else {
        //     $(this).css('display', 'none');
        // }
    });
    counter()
});


//添加修改页面
//自动选中
var gender=$(".b_select_gender").val();
$("#s_gender").find("option").each(function () {
    if($(this).attr("value")===gender){
        $(this).attr("selected", "selected");
    }
});
var auth=$(".b_select_auth").val();
$("#s_auth").find("option").each(function () {
    if($(this).attr("value")===auth){
        $(this).attr("selected", "selected");
    }
});
//取消修改
$("#cancel").on("click", function () {
    window.location.href="/account_all"
});
//确认修改
$("#update").on("click", function () {
    var data = {
        id: $("#parse_id").text(),
        pwd: $("#pwd").val(),
        name: $("#name").val(),
        phone: $("#phone").val(),
        gender: $("#s_gender").select().val(),
        account: $("#account").val(),
        authority: $("#s_auth").select().val(),
    }
    console.log(data);
    $.post('/account_update/', data, function (text, status) {
        alert(text);
        window.location.href="/account_all";
    });
});

// 信息检查标志 [1]检查无误 [2]检查有误
var input_check = 0;

// 添加账号 输入框为空变色
$(".input_check").focus(function(){
    var curValue=$(this).val();
    if($.trim(curValue)===$(this).attr("placeholder")){
        $(this).val("");
        $(this).css({"border-color":"","color":""});
    }
});
$(".input_check").blur(function(){
    var curValue=$(this).val();
    if($.trim(curValue)===""){
        // console.log($(this).attr("placeholder"));
        $(this).val($(this).attr("placeholder"));
        $(this).css({"border-color":"red","color":"red"});
        input_check = 0;
    }
    else {
        input_check = 1;
    }
});
//添加账号检测账号是否存在
$(".input_check_ajax").focus(function(){
    var curValue=$(this).val();
    if($.trim(curValue)===$(this).attr("placeholder") || $.trim(curValue)==="账号已存在"){
        $(this).val("");
        $(this).css({"border-color":"","color":""});
    }
    else {
        $(this).css({"border-color":"","color":""});
    }
});
$(".input_check_ajax").blur(function(){
    if($(this).val()!==""){
        $.post('/account_exist/', {account: $(this).val()}, function (text, status) {
            if(text==="ok"){
                console.log("okok");
                input_check = 1;
                // window.location.href="/account_all";
            }
            else{
                $("#account").val("账号已存在");
                $("#account").css({"border-color":"red","color":"red"});
                input_check = 0;
            }
        });
    }
    else {
        $(this).val($(this).attr("placeholder"));
        $(this).css({"border-color":"red","color":"red"});
        input_check = 0;
    }
});
// 选择框无选择变色提示
$(".select_check").focus(function(){
    $(this).css({"border-color":"","color":""});
});
$(".select_check").blur(function(){
    var curValue=$(this).val();
    console.log(curValue);
    if(curValue===null){
        $(this).css({"border-color":"red","color":"red"});
        input_check = 0;
    }
});
//确认添加
$("#confirm").on("click", function () {
    if(input_check === 1) {
        var data = {
        id: $("#parse_id").text(),
        pwd: $("#pwd").val(),
        name: $("#name").val(),
        phone: $("#phone").val(),
        gender: $("#s_gender").select().val(),
        account: $("#account").val(),
        authority: $("#s_auth").select().val(),
        };
        console.log(data);
        $.post('/account_add/', data, function (text, status) {
            alert(text);
            if(text==="ok"){
                console.log("okok");
                window.location.href="/account_all";
            }
            else{
                console.log("nono");
            }
        });
    }
    else {
        alert("请检查输入内容！");
        $("#account, #pwd, #name, #phone, #s_gender, #s_auth").blur();
    }
});

//
//
// $('.editable-select').editableSelect({
//     filter: false
// });


$('.sale_btn').click(function () {
    $('.blur_bg').fadeIn();
});
$('.blur_bg button').click(function () {
    console.log($(this).val());
    if($(this).val() === '1' || $(this).val() === '2' || $(this).val() === '4' ){
        window.location.href='/sale?loc='+$(this).val();
    }
    else {
        $('.blur_bg').fadeOut();
    }
});
$('.blur_bg').click(function () {
    $(this).fadeOut();
});
