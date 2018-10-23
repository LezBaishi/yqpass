<template lang="html">
  <div class="container">
  	<el-form class="reg_form" :model="user" status-icon :rules='rules2' ref="user" lable-position="left">
  		 <h2 class="title">重置密码</h2>
       <el-form-item prop="email">
        <el-input type="text" v-model="user.email" placeholder="电子邮箱"></el-input>
       </el-form-item>    
  		 <el-form-item style="width:100%">  		 	
  		 	<el-button class="reg_button" type="primary" style="width:40%;" @click="submitForm('user')">提交</el-button>
  		 	<el-button class="login_button" type="primary" style="width:40%;" @click="toLogin">返回</el-button>  		 
  		 </el-form-item>
  	</el-form>
  </div>
</template>

<script>
// import Header from '../components/header'
export default {
  data () {
  	var checkEmail = (rule,value,callback)=>{
  		var reg = new RegExp("^([a-zA-Z0-9_.-]+)\@(gd\.chinamobile\.com)$")
  		if (!value) {
  			return callback(new Error('邮箱不能为空'));
  		} else if (!reg.test(value)) {
  			return callback(new Error('邮箱格式不正确'));
  		} else {
  			callback();
  		}
  	}
    return {
      user: {
      	email: ''
      },
      rules2: {
      	    email: [
              { validator:checkEmail, trigger:'blur' },
            ]
      }
    }
  },
  methods: {
  	  submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$notify({
  				title: '提示',
  				message: '留意邮箱信息',
  				type: 'success',
  				duration: 1500
  			});
  			this.$router.push({path: '/login'})
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
  	toLogin () {
  		this.$router.push({path: '/login'})
  	}
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
