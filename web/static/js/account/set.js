;
var account_set_ops = {
    init:function(){
        this.eventBind()
    },
    eventBind:function(){
        $('.wrap_account_set .save').click(function(){

            var nickname_value = $(".wrap_account_set input[name=nickname]").val();
            var mobile_value = $(".wrap_account_set input[name=mobile]").val();
            var email_value = $(".wrap_account_set input[name=email]").val();
            var login_name_value = $(".wrap_account_set input[name=login_name]").val();
            var login_pwd_value = $(".wrap_account_set input[name=login_pwd]").val();

            if (!nickname_value || nickname_value.length < 2) {
                alert('请输入符合要求的昵称')
                return false
            }
            if (!mobile_value || mobile_value.length < 11) {
                alert('请输入正确的手机号')
                return false
            }
            if (!email_value || email_value.length < 2) {
                alert('请输入正确的邮箱')
                return false
            }
            if (!login_name_value || login_name_value.length < 2) {
                alert('请输入正确的用户名')
                return false
            }
            if (!login_pwd_value || login_pwd_value.length < 6) {
                alert('密码长度不小于6位')
                return false
            }

            $.ajax({
                url:common_ops.buildUrl("/account/set"),
                type:"POST",
                data:{'nickname':nickname_value,'mobile':mobile_value,'email':email_value,'login_name':login_name_value,'login_pwd':login_pwd_value},
                dataType:'json',
                success:function(resp){
                    console.log(resp)
                    alert(resp.msg)
                    btn_target.removeClass("disabled");
                },
                error:function(error){
                    console.log(error)
                }
            })
        })
    }
}

$(document).ready(function(){
    account_set_ops.init()
})

