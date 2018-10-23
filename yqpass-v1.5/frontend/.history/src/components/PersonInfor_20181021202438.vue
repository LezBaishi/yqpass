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
              <el-breadcrumb-item>个人信息</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>      
    </el-row>
		  	<h2 style="font-size:22px;">个人信息</h2>
		  	<el-row class="content">
		  	<el-form ref="order_form" :model="order_form" status-icon :rules="order_rule" label-width="80px">
		  		<!-- <el-row>
		  			<el-form-item label="用户姓名" prop="alias">
		  				<el-input  placeholder="请输入用户姓名" v-model="order_form.alias"></el-input>
		  			</el-form-item>
		  		</el-row> -->
		  		<el-row>
		  			<el-form-item label="电子邮箱" prop="email">
		  				<el-input placeholder="请输入电子邮箱" v-model="order_form.email"></el-input>
		  			</el-form-item>
		  		</el-row>
		  		<el-row>
		  			<el-form-item label="手机号码" prop="phone">
		  				<el-input placeholder="请输入手机号码" v-model="order_form.phone"></el-input>
		  			</el-form-item>
		  		</el-row>
		  		<el-row>
		  			<el-form-item label="员工编号" prop="job_number">
		  				<el-input placeholder="请输入员工编号" v-model="order_form.job_number"></el-input>
		  			</el-form-item>
		  		</el-row>
		  		<el-row>
		  			<el-form-item label="部门编号" prop="dept_id">
		  				<el-input placeholder="请输入部门编号" v-model="order_form.dept_id"></el-input>
		  			</el-form-item>
		  		</el-row>
		  		<el-row>
		  			<el-form-item>
						<el-col :push="5" :span="2">
							<el-button type="primary" @click="updateUserinfo('order_form')">提交</el-button>
						</el-col>
						<el-col :push="9" :span="2"> 
							<el-button type="primary" @click="pass">取消</el-button>
						</el-col>
		  			</el-form-item>
		  		</el-row>
		  	</el-form>
  </el-row>
  </el-row>
  </div>
</template>

<script>
import { getUserDetail,updateUserInfo,getToken } from '../api/api'
export default {
  data () {
  	var checkAlias = (rule,value,callback)=>{
  		if (!value) {
  			return callback(new Error('用户姓名不能为空'));
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
  	var checkJob_number = (rule,value,callback)=>{
  		if (!value) {
  			return callback(new Error('员工编号不能为空'));
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
    return {
    	csrf_token: '',
      order_form: {
      	// alias: '',
      	email: '',
      	phone: '',
      	job_number: '',
      	dept_id: ''
      },
      order_rule: {
      	// alias: [
      	// 	{ validator:checkAlias, trigger:'blur' },
      	// ],
      	email: [
      		{ validator:checkEmail, trigger:'blur' },
      	],
      	phone: [
      		{ validator:checkPhone, trigger:'blur' },
      	],
      	job_number: [
      		{ validator:checkJob_number, trigger:'blur' },
      	],
      	dept_id: [
      		{ validator:checkDept_id, trigger:'blur' },
      	]
      }
    }
  },
  methods: {
  	submit () {
  		this.$router.push({path: '/'})
  	},
  	toReg () {
  		this.$router.push({path: '/reg'})
  	},
  	get_token () {
  	  getToken({}).then((response)=> {
  		if (response.data.code == 1) {
  			this.csrf_token = response.data.data
  			console.log(this.csrf_token)
  		}else{
  			return response[msg]
  		} 		 
  	})
  	},
  	getUserinfo () {
	  	getUserDetail({}).then((response)=> {
	  		console.log(response);
	  		var dat = response.data.data;
	  		var that = this;
	  		if (response.data.code == 1) {
	  			that.order_form = dat;
	  		}
	  	})  		
  	},
  	updateUserinfo (formName) {
  		this.$refs[formName].validate((valid) => {
  			if (valid) {
	  		var that = this;
        let json = {};
        json["csrfmiddlewaretoken"] = that.csrf_token;
        // json["alias"] = that.order_form.alias;
        json["email"] = that.order_form.email;
        json["phone"] = that.order_form.phone;
        json["job_number"] = that.order_form.job_number;
        json["dept_id"] = that.order_form.dept_id;
        var params = JSON.stringify(json);
	  		updateUserInfo(params).then((response)=> {
	  			console.log(response)
	  			if (response.data.code == 1) {
	  				this.$notify({
	  					title: '提示',
	  					message: '修改信息成功',
	  					type:"success",
	  					duration: 1500
	  				});
	  			}
	  		});  				
  			} else {
            console.log('error submit!!');
            return false;  				
  			}
  		})

  	}
  },
  created () {
  	this.getUserinfo();
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
