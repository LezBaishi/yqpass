<template lang="html">
  <div>
    <el-row class="container">
    <el-row> 
			<el-col :span='12' class="button_nav">
				<el-button type="primary" icon="el-icon-arrow-left" size="mini" circle style='float: left;' @click="backToList"></el-button>
			</el-col>
          <el-col :offset="12" :span='12' class="breadcrumb">
            <el-breadcrumb separator="/" style='float: right;'>
              <el-breadcrumb-item :to="{ path: '/3/roleList' }">角色列表</el-breadcrumb-item>
              <el-breadcrumb-item>角色信息</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>      
    </el-row>
		  	<h2 style="font-size:22px;">角色信息</h2>
		  	<el-row class="content">
		  	<el-form ref="order_form" :model="order_form" status-icon :rules="order_rule" label-width="80px">
		  		<el-row>
		  			<el-form-item label="角色姓名" prop="name">
		  				<el-input  placeholder="请输入角色姓名" v-model="order_form.name"></el-input>
		  			</el-form-item>
		  		</el-row>
		  		<el-row>
		  			<el-form-item label="角色描述" prop="description">
		  				<el-input placeholder="请输入角色描述" v-model="order_form.description"></el-input>
		  			</el-form-item>
		  		</el-row>
		  		<el-row>
		  			<el-form-item label="创建人" prop="creator">
		  				<el-input placeholder="请输入创建人" v-model="order_form.creator"></el-input>
		  			</el-form-item>
		  		</el-row>
		  		<!-- <el-row>
		  			<el-form-item>
		  				<el-button type="primary" @click="updateUserinfo('order_form')">提交</el-button>
		  				<el-button type="primary" @click="pass">取消</el-button>
		  			</el-form-item>
		  		</el-row> -->
		  	</el-form>
  </el-row>
  </el-row>
  </div>
</template>

<script>
import { getRoleDetail } from '../api/api'
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
      	name: '',
      	description: '',
      	creator: ''
      },
      order_rule: {
      	alias: [
      		{ validator:checkAlias, trigger:'blur' },
      	],
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
	backToList () {
		this.$router.push('/3/roleList')
	},
  	getRoleinfo (id) {
		getRoleDetail(id).then((response)=> {
	  		console.log(response);
	  		var dat = response.data.data;
	  		var that = this;
	  		if (response.data.code == 1) {
	  			that.order_form = dat;
	  		}
	  	})  		
  	},
  	// updateUserinfo (formName) {
  	// 	this.$refs[formName].validate((valid) => {
  	// 		if (valid) {
	//   		var that = this;
    //     let json = {};
    //     json["csrfmiddlewaretoken"] = that.csrf_token;
    //     json["alias"] = that.order_form.alias;
    //     json["email"] = that.order_form.email;
    //     json["phone"] = that.order_form.phone;
    //     json["job_number"] = that.order_form.job_number;
    //     json["dept_id"] = that.order_form.dept_id;
    //     var params = JSON.stringify(json);
	//   		updateUserInfo(params).then((response)=> {
	//   			console.log(response)
	//   			if (response.data.code == 1) {
	//   				this.$notify({
	//   					title: '提示',
	//   					message: '修改信息成功',
	//   					type:"success",
	//   					duration: 1500
	//   				});
	//   			}
	//   		});  				
  	// 		} else {
    //         console.log('error submit!!');
    //         return false;  				
  	// 		}
  	// 	})
  	// }
  },
  created () {
  	this.getRoleinfo(this.$route.query.id);
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
