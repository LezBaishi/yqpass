<template lang="html">
  <div class="container">
  	<el-form class="reg_form" :model="user" status-icon :rules='rules2' ref="user" lable-position="left">
  		 <h2 class="title">系统注册</h2>
  		 <el-form-item prop="account">
  		 	<el-input type="text" v-model="user.account" placeholder="用户名"></el-input>
  		 </el-form-item>  		 
  		 <el-form-item prop="email">
  		 	<el-input type="text" v-model="user.email" placeholder="电子邮箱"></el-input>
  		 </el-form-item>
  		 <el-form-item prop="phone">
  		 	<el-input type="text" v-model="user.phone" placeholder="电话号码"></el-input>
  		 </el-form-item>    
  		 <el-form-item prop="dept_id">
  		 	<el-input type="text" v-model="user.dept_id" placeholder="部门"></el-input>
  		 </el-form-item>    		 		           
         <el-form-item prop="password">        
  		 	<el-input type="password" v-model="user.password" placeholder="密码"></el-input>
  		 </el-form-item>
  		 <el-form-item prop="checkPassword">
  		 	<el-input type="password" v-model="user.checkPassword" placeholder="重复输入密码"></el-input>
  		 </el-form-item>
  		 <el-form-item style="width:100%">  		 	
  		 	<el-button class="reg_button" type="primary" style="width:40%;" @click="submitForm('user')">提交</el-button>
  		 	<el-button class="login_button" type="primary" style="width:40%;" @click="toLogin">返回</el-button>  		 	
  		 </el-form-item>
  	</el-form>
  </div>
</template>

<script>
import { register, getToken } from '../api/api'
export default {
  data () {
  	var checkAccount = (rule,value,callback)=>{
  		if (!value) {
  			return callback(new Error('账号不能为空'));
  		} else {
  			callback();
  		}
  	};
  	var checkEmail = (rule,value,callback)=> {
  		var reg = new RegExp("^([a-zA-Z0-9_.-]+)\@(gd\.chinamobile\.com)$")
  		if (!value) {
  			return callback(new Error('邮箱不能为空'));
  		} else if (!reg.test(value)) {
  			return callback(new Error('邮箱格式不正确'));
  		} else {
  			callback();
  		}
  	}; 
  	var checkPhone = (rule, value, callback)=> {
  		var reg = new RegExp("^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])[0-9]{8}$")
  		if (!value) {
  			return callback(new Error('电话号码不能为空'));
  		} else if (!reg.test(value)) {
  			return callback(new Error('电话号码格式不正确'));
  		} else {
  			callback();
  		}  		
  	};
  	var checkDept_id = (rule,value,callback)=>{
  		if (!value) {
  			return callback(new Error('部门编号不能为空'));
  		} else {
  			callback();
  		}
  	};  	                   
    var checkPass = (rule, value, callback) => {
  		var reg = new RegExp("^[0-9]*$")      	
        if (value === '') {
          callback(new Error('请输入密码'));
        } else if (value.length < 8) {
  		  callback(new Error('新密码长度必须大于8位'));
        }else if (reg.test(value)) {
  			return callback(new Error('新密码不能全为数字'));
  		} else {
          if (this.user.password !== '') {
            this.$refs.user.validateField('checkPassword');
          }
          callback();
        }
    };
  	var checkRepeatPass = (rule,value,callback)=>{
  		if(value === ''){
  			return callback(new Error('请再次输入密码'))
  		}else if(value!==this.user.password){
  			return callback(new Error('两次输入的密码不一样'))
  		} else {
  			callback();
  		}
  	}
    return { 
     	csrf_token: '',
      user: {
      	account: '',
      	email: '',
      	phone: '',
      	dept_id: '',      	
      	password: '',
      	checkPassword: ''
      },
      rules2: {
      	    account: [
              { validator:checkAccount, trigger:'blur' },
            ],  
            email: [
            	{ validator: checkEmail, trigger:'blur' },
            ], 
            phone: [
            	{ validator: checkPhone, trigger:'blur' },
            ],
            dept_id: [
            	{ validator: checkDept_id, trigger:'blur' },
            ], 
            password: [
              { validator:checkPass, trigger:'blur' },
            ],
            checkPassword:[
              { validator:checkRepeatPass, trigger:'blur' }
            ]
      }
    }
  },
  methods: {
  	  submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
          	var that = this;
            let json = {};
            json["csrfmiddlewaretoken"] = that.csrf_token;
            json["username"] = that.user.account;
            json["email"] = that.user.email;
            json["phone"] = that.user.phone;
            json["dept_id"] = that.user.dept_id;
            json["password1"] = that.user.password;
            json["password2"] = that.user.checkPassword;
            var params = JSON.stringify(json);
          	register(params).then((response)=> {
          		console.log(response);
          		if (response.data.code == 1) {
  		          	this.$notify({
    		  				title: '提示',
    		  				message: '注册成功',
    		  				type: 'success',
    		  				duration: 1500
    		  			});
      		  			this.$router.push({path: '/login'})          			
          		}
          	});
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
  	toLogin () {
  		this.$router.push({path: '/login'})
  	},
  	get_token () {
  	  getToken({}).then((response)=> {
  		console.log(response);
  		if (response.data.code == 1) {
  			this.csrf_token = response.data.data
  			console.log(this.csrf_token)
  		}else{
  			return response[msg]
  		} 		 
  	})
  	}
  },
  created () {
  	this.get_token();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="css" scoped>
.container{
  margin:0;
  background:url('../assets/back.jpg') no-repeat center;
  background-size: cover;
  min-width: 680px;
  position: absolute;
  top:0;
  bottom:0;
  left:0;
  right:0;
}
.title{
  text-align: center;
  margin: 0px auto 40px auto;
  text-align: center;
  color: #505458;
}
.reg_form{
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-color: #F9FAFC;
  margin: 80px auto 20px auto ;
  border: 2px solid #8492A6;
  width: 350px;
  padding: 35px 35px 15px 35px;
  opacity: 0.8;
}
.reg_button,.login_button{
  margin-top: 20px;
}

.el-form-item {
	text-align: center;
}
</style>
