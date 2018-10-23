<template lang="html">
  <div>
  	<el-row class="container">
      	<el-row v-if="seen" class="order_menu">
      		<el-form ref="search_form" :model="search_form" label-width="80px">
       		<el-row>
       			<h2 style="font-size:22px;">搜索用户</h2>
      			<el-col :offset="3" :span="8">
      				<el-form-item label="用户名" prop="userName">
      					<el-input v-model="search_form.userName" placeholder="请输入用户名" clearable></el-input>
      				</el-form-item>
      			</el-col>
      			<el-col :push="2" :span="8">
      				<el-form-item label="用户邮箱" prop="userEmail">
      					<el-input v-model="search_form.userEmail" placeholder="请输入用户邮箱" clearable></el-input>
      				</el-form-item>
      			</el-col>	      		
	      	</el-row>
	      	<el-row>
	      		<el-col :offset="3" :span="8">
	      			<el-form-item label="用户别名" prop="userAlias">
	      				<el-input v-model="search_form.userAlias" placeholder="请输入用户别名" clearable></el-input>
	      			</el-form-item>
	      		</el-col>
	      		<el-col :push="2" :span="8">
	      			<el-form-item label="用户类型" prop="userCate">
	      				<el-select v-model="search_form.userCate" placeholder="请选择用户类型" style="width:100%;">
	      					<el-option label="所有用户" name="type" value="all"></el-option>
							<el-option label="一般用户" name="type" value="general"></el-option>
							<el-option label="管理用户" name="type" value="admin"></el-option>
	      				</el-select>
	      			</el-form-item>
	      		</el-col>
	      	</el-row>	      		
	      	<el-row justify="space-around">
	      		<el-form-item>
	      			<el-col :push="9" :span="2">
						<el-button type="primary" size="medium" @click="searchOrder">搜索</el-button>
					</el-col>
					<el-col :push="9" :span="2">
						<el-button type="" size="medium" @click="resetForm('search_form')">重置</el-button>
					</el-col>
				</el-form-item>
	      	</el-row>
	      </el-form>
      	</el-row>      	
        <el-row>
          <el-col :span='12' class="button_nav">
          	<el-button type="primary" icon="el-icon-search" size="mini" circle style='float: left;' @click="searchBtn"></el-button>
           	<el-button type="primary" icon="el-icon-refresh" size="mini" circle style='float: left;' @click="refreshBtn"></el-button>        	  
          </el-col>
          <el-col :span='12' class="breadcrumb">
            <el-breadcrumb separator="/" style='float: right;'>
              <el-breadcrumb-item :to="{ path: '/' }">用户管理</el-breadcrumb-item>
              <el-breadcrumb-item>用户列表</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>
        </el-row>
        <el-row>
        	<el-table :data="tableData" v-loading="loading">
  				<template v-for="column in tableColumns">
	  			<el-table-column header-align="center"
	  				:label="column.label"
	  				:prop="column.prop">
	  			</el-table-column>
  				</template>
  			<el-table-column
            	label="操作"
            	prop="" header-align="center">
            	<template slot-scope="scope">
					<el-button type="primary" size="small" @click="onBtnDetailClick(scope.$index, tableData)">详情</el-button>
					<el-button type="danger" size="small" @click="onBtnDeleteClick(scope.$index, tableData)">删除</el-button>
            	</template>
       		 </el-table-column>
  			</el-table>
		</el-row>
		<el-row>
			<el-pagination class="pageView" v-if="paginationShow" background @size-change="handleSizeChange" @current-change="handleCurrentChange" :page-sizes="pageSizeList" :page-size="pageSize" layout="total,sizes,prev,pager,next" :page-count="pageCount" :total="totalCount">
			</el-pagination>
		</el-row>
    </el-row>
  </div>
</template>

<script>
// import OrderDetailUnfinished from '../components/OrderDetailUnfinished'
import { getUserList } from '../api/api'
export default {
  data () {
    return {
		tableData: [],
		loading: true,
		pageNo: 1,
		totalPage: 0,
		totalCount: 0,
		pageCount: 10,
		paginationShow: false,
		pageSize: 10,
		pageSizeList: [5, 10, 15, 20],
		tableColumns: [
			{ label: '用户名', prop: 'username'},
			{ label: '用户别名', prop: 'alias' },
			{ label: '用户邮箱', prop: 'email'},
			{ label: '是否激活状态', prop: 'active'},
			{ label: '是否为管理员', prop: 'admin'}
		],
    	seen: false,
    	search_form: [
    	{
    		userName: '',
    		userEmail: '',
    		userAlias: '',
    		userCate: '',
    	}]
    }
  },
  methods: {
  	searchBtn () {
  		if (this.$data.seen == false){
  			this.$data.seen = true;
  		}else {
  			this.$data.seen = false;
  		}
	},
	refreshBtn () {
		this.getUserAllList();
	},
  	searchOrder () {
		this.$data.seen = false;
		let paramsData = {};
		paramsData["username"] = this.search_form.userName;
		paramsData["email"] = this.search_form.userEmail;
		paramsData["alias"] = this.search_form.userAlias;
		paramsData["category"] = this.search_form.userCate;
		paramsData["per_page"] = this.pageSize;
		paramsData["page"] = this.pageNo;
		getUserList({params : paramsData}).then((response)=> {
			console.log(response)
			if (response.data.code == 1) {
				this.loading = false;
				let list = response.data.data.value;
				console.log(list);
				this.tableData = [];
				for (var i=0; i<list.length; i++) {
					this.tableData.push({
						username: list[i].username,
						alias: list[i].alias,
						email: list[i].email,
						active: list[i].active,
						admin: list[i].admin,
						id: list[i].id
					})
				};
			}
		})			
  	},
  	resetForm(formName) {
		this.search_form = [
    	{
    		userName: '',
    		userEmail: '',
    		userAlias: '',
    		userCate: '',
    	}];
	},
	getUserAllList() {
		let paramsData = {};
		paramsData["category"] = "all";
		paramsData["per_page"] = this.pageSize;
		paramsData["page"] = this.pageNo;
		getUserList({params : paramsData}).then((response)=> {
			console.log(response);
			if (response.data.code == 1)	{
				this.loading = false;
				let list = response.data.data.value;
				console.log(list);
				this.tableData = [];
				for (var i=0; i<list.length; i++) {
					this.tableData.push({
						username: list[i].username,
						alias: list[i].alias,
						email: list[i].email,
						active: list[i].active,
						admin: list[i].admin,
						id: list[i].id
					}),
					this.tableData[i].active==true?this.tableData[i].active='激活':this.tableData[i].active='未激活';
					this.tableData[i].admin==true?this.tableData[i].admin='管理员':this.tableData[i].admin='普通用户';
				};
				console.log(this.tableData);
				this.totalCount = response.data.data.total
				console.log(this.totalCount)
				this.totalPage = Math.ceil(response.data.data.total/this.pageSize)
			console.log(this.totalPage)
			if (this.totalPage > 1) {
				this.paginationShow = true;
			}
			}			
		})
	},
	handleSizeChange(val) {
  		console.log('每页' + val + '条');
  		var pageSize = `${val}`
  		this.pageSize = parseInt(pageSize)
  		this.$nextTick(() => this.getUserAllList())
  	},
  	handleCurrentChange(val) {
  		console.log(`当前页:`+val);
  		this.pageNo = val
  		this.getUserAllList()
  	},
	onBtnDetailClick (index, rows) {
		let rowValue = JSON.parse(JSON.stringify(rows[index]));
		console.log(rowValue);
		// this.$router.push({path: '/0/OrderDetailUnfinished', query: {id: rowValue.id}})
	}
  },
  created () {
	this.getUserAllList();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="css" scoped>
.container {
  height: 100%;
  width: 100%;
}
.breadcrumb {
  margin-bottom: 10px;
}
.button_nav {
  margin-bottom: 10px;
}
.order_menu {
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-color: #F9FAFC;
  margin: 10px auto 10px auto ;
  border: 2px solid #8492A6;
  padding: 0px 10px 0px 10px;	
}
.pageView {
	height: 30px;
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;
}
</style>
