<template lang="html">
  <div>
  	<el-row class="container">
      	<el-row v-if="seen" class="order_menu">
      		<el-form ref="search_form" :model="search_form" label-width="80px">
       		<el-row>
       			<h2 style="font-size:22px;">搜索部门</h2>
      			<el-col :offset="3" :span="16">
      				<el-form-item label="部门名称" prop="deptName">
      					<el-input v-model="search_form.deptName" placeholder="请输入部门名称" clearable></el-input>
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
              <el-breadcrumb-item :to="{ path: '/3/deptList' }">用户管理</el-breadcrumb-item>
              <el-breadcrumb-item>部门列表</el-breadcrumb-item>
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
import DeptListDetail from '../components/DeptListDetail'
import { getDeptList,deleteDept } from '../api/api'
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
			{ label: '部门名称', prop: 'name'},
			{ label: '部门标号', prop: 'parent_dept_id' },
			{ label: '审批人', prop: 'approver'},
			{ label: '创建人', prop: 'creator'}
		],
    	seen: false,
    	search_form: [
    	{
    		deptName: ''
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
		this.getRoleInfoList();
	},
  	searchOrder () {
		this.$data.seen = false;
		let paramsData = {};
		paramsData["dept_name"] = this.search_form.deptName;
		paramsData["per_page"] = this.pageSize;
		paramsData["page"] = this.pageNo;
		getDeptList({params : paramsData}).then((response)=> {
			if (response.data.code == 1) {
				this.loading = false;
				let list = response.data.data.value;
				console.log(list);
				this.tableData = [];
				for (var i=0; i<list.length; i++) {
					this.tableData.push({
						id: list[i].id,
						name: list[i].name,
						approver: list[i].approver,						
						parent_dept_id: list[i].parent_dept_id,
						creator: list[i].creator
					})
				};
			}
		})			
  	},
  	resetForm(formName) {
		this.search_form = [
    	{
    		deptName: ''
    	}];
	},
	getRoleInfoList() {
		let paramsData = {};
		paramsData["per_page"] = this.pageSize;
		paramsData["page"] = this.pageNo;
		console.log(paramsData);
		getDeptList({params : paramsData}).then((response)=> {
			console.log(response);
			this.loading = false;
			if (response.data.code == 1)	{	
				let list = response.data.data.value;
				console.log(list);
				this.tableData = [];
				for (var i=0; i<list.length; i++) {
					this.tableData.push({
						id: list[i].id,
						name: list[i].name,
						approver: list[i].approver,						
						parent_dept_id: list[i].parent_dept_id,
						creator: list[i].creator
					})
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
  		this.$nextTick(() => this.getRoleInfoList())
  	},
  	handleCurrentChange(val) {
  		console.log(`当前页:`+val);
  		this.pageNo = val
  		this.getRoleInfoList()
  	},
	onBtnDetailClick (index, rows) {
		let rowValue = JSON.parse(JSON.stringify(rows[index]));
		console.log(rowValue);
		// this.$router.push({path: '/3/DeptListDetail', query: {id: rowValue.id}})
	},
	// onBtnDeleteClick (index, rows) {
	// 	this.$confirm('是否确定删除该部门', '提示', {
    //     confirmButtonText: '确定',
    //     cancelButtonText: '取消',
    //     type: 'warning'
    //   }).then(() => {
	// 	let rowValue = JSON.parse(JSON.stringify(rows[index]));
	// 	console.log(rowValue);
	// 	var that = this;
	// 	let json = {};
	// 	json["dept_id"] = rowValue.id;
	// 	var params = JSON.stringify(json);
	// 	deleteDept(params).then((response)=> {
	// 		if (response.data.code == 1) {
	// 			this.$notify({
	// 				title: '提示',
	// 				message: '删除成功',
	// 				type: 'success',
	// 				duration: 1500
	// 			});
	// 			this.getRoleInfoList();
	// 		}
	// 	})      
    //   }).catch(() => {

    //   });
	// }
  },
  created () {
	this.getRoleInfoList();
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
