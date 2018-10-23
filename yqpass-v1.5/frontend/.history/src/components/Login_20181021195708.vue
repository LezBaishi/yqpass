<template lang="html">
  <div class="container">
  	<el-form class="login_form" :model="user" status-icon :rules='rules2' ref="user" lable-position="left">
  		 <h2 class="title">园区资源调度系统</h2>
  		 <el-form-item prop="account">
  		 	<el-input type="text" v-model="user.account" placeholder="账号"></el-input>
  		 </el-form-item>
  		 <el-form-item prop="password">
  		 	<el-input type="password" v-model="user.password" placeholder="密码"></el-input>
  		 </el-form-item>
  		 <el-form-item style="width:100%">
  		 	<el-button class="login_button" type="primary" style="width:40%;" @click="handleSubmit('user')">登录</el-button>
  		 	<el-button class="reg_button" type="primary" style="width:40%;" @click="toReg">注册</el-button>        
  		 </el-form-item>
       <p style="font-size: 15px; text-align: right; cursor: pointer;" @click="forgetPass">忘记密码？</p>
  	</el-form>
    
  </div>
</template>

<script>
import { login, getToken } from '../api/api'
import cookie from '../static/js/cookie'
export default {
  data () {
  var checkAccount = (rule,value,callback)=>{
      if (!value) {
        return callback(new Error('账号不能为空'));
      } else {
        callback();
      }
    };
  var checkPass = (rule,value,callback)=>{
      if (!value) {
        return callback(new Error('密码不能为空'));
      } else {
        callback();
      }
    }
    return {
    	csrf_token: '',
      user: {
        account: '',
        password: ''
      },      
      rules2: {
            account: [
              { validator:checkAccount, trigger:'blur' },
            ],
            password: [
              { validator:checkPass, trigger:'blur' },
            ],
      }
    }
  },
  methods: {
  	handleSubmit (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
        	var that = this;
          let json = {};
          json["csrfmiddlewaretoken"] = that.csrf_token;
          json["username"] = that.user.account;
          json["password"] = that.user.password;
          // console.log(json)
          var params = JSON.stringify(json);
          // console.log(params)
        	login(params).then((response)=> {
        		console.log(response);
        		cookie.setCookie('name', that.user.account, 7);
        		// that.$store.dispatch('setInfo');
            console.log(this.$store.state.userInfo.name)
        		if (response.data.code == 1) {
		        	this.$notify({
		            title: '欢迎' + that.user.account,
		            message: '登录成功',
		            type: 'success',
		            duration: 1500
		          });
		        	let allCookies = document.cookie
		        	console.log(allCookies)
		          this.$router.push({path: '/'})
        		} else if (response.data.code == 0) {
        			this.$message.error({
        				message: '账号与密码不匹配，请重新输入',
        				duration: 2000
        				});
        		}
        	});             
        } else {
            console.log('error submit!!');
            return false;          
        }
      })
  	},
  	toReg () {
  		this.$router.push({path: '/reg'})
  	},
    forgetPass () {
      this.$router.push({path: '/forgetpass'})
    },
    get_token () {
  	  getToken({}).then((response)=> {
  		console.log(response);
  		if (response.data.code == 1) {
  			this.csrf_token = response.data.data
  			console.log(this.csrf_token)
  		}else{
  			return response.data.msg
  		} 		 
  	})
  	}
  },
  created () {
  	this.get_token();
  	cookie.delCookie('name');
  	this.$store.dispatch('setInfo');
    // console.log(this.$store.state.userInfo.name)
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
.login_form{
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-color: #F9FAFC;
  margin: 150px auto 20px auto ;
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
