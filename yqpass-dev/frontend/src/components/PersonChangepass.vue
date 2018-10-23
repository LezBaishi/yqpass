<template lang="html">
  <div>
    <el-row class="container">
    <el-row> 
          <!--<el-col :span='12' class="button_nav">
            <el-button type="primary" icon="el-icon-edit" size="mini" circle style='float: left;' @click="searchBtn"></el-button>
            <el-button type="primary" icon="el-icon-refresh" size="mini" circle style='float: left;'></el-button>           
          </el-col>-->
          <el-col :offset="12" :span='12' class="breadcrumb">
            <el-breadcrumb separator="/" style='float: right;'>
              <el-breadcrumb-item :to="{ path: '/' }">个人中心</el-breadcrumb-item>
              <el-breadcrumb-item>修改密码</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>      
    </el-row>
  	<h2 style="font-size:22px;">修改密码</h2>
  	<el-row class="content">
  	<el-form ref="order_form" :model="order_form" status-icon :rules='pass_rule' label-width="80px">
  		<el-row>
  			<el-form-item label="旧密码" prop="oldpass">
  				<el-input placeholder="请输入旧密码" type="password" v-model="order_form.oldpass"></el-input>
  			</el-form-item>
  		</el-row>
  		<el-row>
  			<el-form-item label="新密码" prop="newPass">
  				<el-input placeholder="请输入新密码" type="password" v-model="order_form.newPass"></el-input>
  			</el-form-item>
  		</el-row>
  		<el-row>
  			<el-form-item label="确认密码" prop="checkNewPass">
  				<el-input placeholder="请再次输入新密码" type="password" v-model="order_form.checkNewPass"></el-input>
  			</el-form-item>
  		</el-row>
  		<el-row>
  			<el-form-item>
  				<el-button type="primary" @click="updatePassword('order_form')">提交</el-button>
  				<el-button type="primary" @click="pass">取消</el-button>
  			</el-form-item>
  		</el-row>
  	</el-form>
  </el-row>
</el-row>
  </div>
</template>

<script>
import { changePass,getToken } from '../api/api'
export default {
  data () {
  	var checkOldpass = (rule, value, callback)=> {
  		if (!value) {
  			return callback(new Error('旧密码不能为空'));
  		} else {
  			callback();
  		}
  	};
  	var checkPass = (rule, value, callback)=> {
  		var reg = new RegExp("^[0-9]*$")
  		if (!value) {
  			return callback(new Error('新密码不能为空'));
  		} else if(value.length < 8){
  			return callback(new Error('新密码长度必须大于8位'));
  		} else if (reg.test(value)) {
  			return callback(new Error('新密码不能全为数字'));
  		} else {
  			if (this.order_form.newPass !== ''){
  				this.$refs.order_form.validateField('checkNewPass');
  			}
  			callback();
  		}
  	};
  	var checkRepeatPass = (rule,value,callback)=>{
  		if (!value){
  			return callback(new Error('请再次输入密码'));
  		}else if(value!==this.order_form.newPass){
  			return callback(new Error('两次输入的密码不一样'));
  		}else{
  			callback();
  		}
  	}  	
    return {
    	csrf_token: '',
      order_form: [
      {
      	oldpass: '',
      	newPass: '',
      	checkNewPass: '',
      }],
      pass_rule: {
      	oldpass: [
      		{ validator:checkOldpass, trigger:'blur' },
      	],
      	newPass: [
      		{ validator:checkPass, trigger:'blur' },
      	],
      	checkNewPass: [
      		{ validator:checkRepeatPass, trigger:'blur' },
      	]
      }
    }
  },
  methods: {
  	handleSubmit () {
  		this.$router.push({path: '/'})
  	},
  	toReg () {
  		this.$router.push({path: '/reg'})
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
  	}, 
  	updatePassword (formName) {
  		this.$refs[formName].validate((valid) => {
  			if (valid) {
	  		var that = this;
	  		let params = new URLSearchParams()
	  		params.append("csrfmiddlewaretoken", that.csrf_token)
	  		params.append("old_password", that.order_form.oldpass)
	  		params.append("new_password1", that.order_form.newPass)
	  		params.append("new_password2", that.order_form.checkNewPass)
	  		changePass(params).then((response)=> {
	  			console.log(response)
	  			if (response.data.code == 1) {
	  				this.$notify({
	  					title: '提示',
	  					message: '修改密码成功',
	  					type: 'success',
	  					duration:1500
	  				})
	  			}
	  		})  				
  			} else {
  				console.log('error submit!!');
  				return false;
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
  height: 100%;
  width: 100%;
}
.el-form-item {
	text-align: center;
}
.content {
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-color: #F9FAFC;
  margin: 15px auto 20px auto ;
  border: 2px solid #8492A6;
  width: 600px;
  padding: 35px 35px 15px 35px;
}
</style>
