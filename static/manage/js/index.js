$(function () {
    var side_nav = $('.side_bar');
    $('.top_bar').on('click', function () {
        if(side_nav.css('display')==='none'){
            side_nav.css("display","block");
        }
        else {
            side_nav.css("display","none");
        }

    });
   var ref = window.location.search;
	var r = ref.split('=')[0].split('?')[1];
	$('.tbody').find(".tr").each(function(){
		var that = $(this);
		var id = that.find('#id');
		var del_button = that.find('#del_button');
		del_button.unbind().on('click',function(){
			window.location.href="delete?id="+id.text();
		});
		var name = that.find('#name_');
		var pwd = that.find('#pwd');
		var gender = that.find('#gender');
		var phone = that.find('#phone');
		var email = that.find('#email');
		/* var name = that.find('#name_ input'); */
		var update_button = that.find('#update_button');
		var c_btn = that.find('#c_btn');
		update_button.unbind().on('click',function(){
			name.html('<input type="text" id="name" value="'+name.text()+'"> ');
			pwd.html('<input type="text" id="pwd" value="'+pwd.text()+'"> ');
			var g = gender.text();

			gender.html('<select id="gender"><option value="男">男</option><option value="女">女</option></select>');
			phone.html('<input type="text" id="phone" value="'+phone.text()+'"> ');
			email.html('<input type="text" id="email" value="'+email.text()+'"> ');
			update_button.css("display","none");
			c_btn.css("display","inline");
		})
		c_btn.unbind().on('click',function(){
			console.log(name.val());
			window.location.href="update?id="+id.text()+"&name="+name.find("#name").val()+"&pwd="+pwd.find("#pwd").val()+
					"&gender="+gender.find("#gender").val()+"&phone="+phone.find("#phone").val()+
					"&email="+email.find("#email").val();
		})
	});

	$("#s_name").keydown(function(e) {
           if (e.keyCode == 13) {
           	window.location.href="search?key="+$(this).val();
           }
      });
	$(".logout").on("click",function(){
		window.location.href="login";
	})
});
function add (){
	window.location.href="add?name="+$("#add_name").val()+ "&pwd="+$("#add_pwd").val() + "&gender="+$("#add_gender").val()+
			"&phone="+$("#add_phone").val() + "&email="+$("#add_email").val();
	};
function search (){
	window.location.href="search?key="+$("#s_name").val();
	};
function logout (){
	window.location.href="login";
	};
