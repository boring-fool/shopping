let vm = new Vue({
    el: '#app', //id选择器绑定
    delimiters : ['[[',']]'],
    data: {
		username: '',		// 用户名
		password: '', 		// 密码
		password2: '',		// 确认密码
		mobile: '',			// 手机号
		allow: '',			// 同意协议
		image_code_url:'',   //验证码
		uuid:'',
		image_code:'',

		error_name: false,
		error_password: false,
		error_password2: false,
		error_mobile: false,
		error_allow: false,
        error_image_code:false,

		error_name_message: '',		// 用户名错误提示
		error_mobile_message: '',	// 密码错误提示
		error_image_code_message:'' //验证码错误提示
	},
	mounted(){//页面加载完会被调用
        this.generate_image_code()
	},
	methods: {
	    generate_image_code(){
            this.uuid = generateUUID();
            this.image_code_url = 'image_codes/' + this.uuid +'/';
	    },
		// 校验用户名
		check_username(){
			// 准备正则表达式
			let re = /^[a-zA-Z0-9_-]{5,20}$/;
			// 正则表达式匹配用户名
			if (re.test(this.username)) {
				this.error_name = false;
			} else {
				this.error_name_message = '请输入5-20个字符的用户名';
				this.error_name = true;
			}
			//判断用户名是否重复注册
			if (this.error_name == false) {
                let url = '/usernames/' + this.username + '/count/';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count == 1) {
                            // 用户名已存在
                            this.error_name_message = '用户名已存在';
                            this.error_name = true;
                        } else {
                            // 用户名不存在
                            this.error_name = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
		},
		// 校验密码
		check_password(){
			let re = /^[0-9A-Za-z]{8,20}$/;
			if (re.test(this.password)) {
				this.error_password = false;
			} else {
				this.error_password = true;
			}
		},
		// 校验确认密码
		check_password2(){
			// 判断两次密码是否一致
			if(this.password != this.password2) {
				this.error_password2 = true;
			} else {
				this.error_password2 = false;
			}
		},
		// 校验手机号
		check_mobile(){
			let re = /^1[3-9]\d{9}$/;
			if(re.test(this.mobile)) {
				this.error_mobile = false;
			} else {
				this.error_mobile_message = '您输入的手机号格式不正确';
				this.error_mobile = true;
			}
			if(this.error_mobile==false){
			    let url = '/mobiles/' + this.mobile +'/count/';
			    axios.get(url,{
			    responseType: 'json'
			    })
			    .then(response=>{
			        if(response.data.count==1){
			        this.error_mobile_message = '手机号已注册';
			        this.error_mobile = true;
			        }
			        else{
			        this.error_mobile = false
			        }
			    }).catch(
			        error=>{console.log(error.response)}
			    )

			}

		},
		check_image_code(){
		    if (this.image_code.length!=4){
		            this.error_image_code_message='请输入正确验证码'
		            this.error_image_code=true
		    }
		    else{
		        this.error_image_code=false
		    }
		},
		// 校验是否勾选协议
		check_allow(){
			if(!this.allow) {
				this.error_allow = true;
			} else {
				this.error_allow = false;
			}
		},
		// 监听表单提交事件
		on_submit(){
			this.check_username();
			this.check_password();
			this.check_password2();
			this.check_mobile();
			this.check_allow();

			if(this.error_name == true || this.error_password == true || this.error_password2 == true
				|| this.error_mobile == true || this.error_allow == true) {
                // 禁用表单的提交
				window.event.returnValue = false;
            }
		},
	}
})