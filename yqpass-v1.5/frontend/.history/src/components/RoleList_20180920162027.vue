<template lang="html">
  <div>
  	<el-row class="container">
      	<el-row v-if="seen" class="order_menu">
      		<el-form ref="search_form" :model="search_form" label-width="80px">
       		<el-row>
       			<h2 style="font-size:22px;">搜索角色</h2>
      			<el-col :offset="3" :span="16">
      				<el-form-item label="角色名称" prop="roleName">
      					<el-input v-model="search_form.roleName" placeholder="请输入角色名称" clearable></el-input>
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
              <el-breadcrumb-item :to="{ path: '/3/roleList' }">用户管理</el-breadcrumb-item>
              <el-breadcrumb-item>角色列表</el-breadcrumb-item>
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
import RoleListDetail from '../components/RoleListDetail'
import { getRoleList,deleteRole } from '../api/api'
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
			// { label: '工单号', prop: 'sn'},
			// { label: '工单标题', prop: 'title' },
			// { label: '建单人', prop: 'creator'},
			// { label: '建单时间', prop: 'gmt_created'},
			// { label: '当前状态', prop: 'state_name'}
		],
    	seen: false,
    	search_form: [
    	{
    		roleName: '',
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
		// this.getOrderList();
	},
  	searchOrder () {
		// this.$data.seen = false;
		// let paramsData = {};
		// paramsData["category"] = "duty";
		// paramsData["sn"] = this.search_form.roleName;
		// paramsData["title"] = this.search_form.title;
		// if (!this.search_form.date1 == '') {
		// 	paramsData["create_start"] = this.getDate(this.search_form.date1);
		// }
		// if (!this.search_form.date2 == '') {
		// 	paramsData["create_end"] = this.getDate(this.search_form.date2);
		// }
		// paramsData["reverse"] = this.search_form.orderState;
		// paramsData["per_page"] = this.pageSize;
		// paramsData["page"] = this.pageNo;
		// getTicketList({params : paramsData}).then((response)=> {
		// 	if (response.data.code == 1) {
		// 		this.loading = false;
		// 		let list = response.data.data.value;
		// 		console.log(list);
		// 		this.tableData = [];
		// 		for (var i=0; i<list.length; i++) {
		// 			this.tableData.push({
		// 				id: list[i].id,
		// 				sn: list[i].sn,
		// 				title: list[i].title,
		// 				creator: list[i].creator,
		// 				gmt_created: list[i].gmt_created,
		// 				state_name: list[i].state.state_name
		// 			})
		// 		};
		// 	}
		// })			
  	},
  	resetForm(formName) {
		this.search_form = [
    	{
    		roleName: ''
    	}];
	},
	getRoleInfoList() {
		let paramsData = {};
		paramsData["per_page"] = this.pageSize;
		paramsData["page"] = this.pageNo;
		getRoleList({params : paramsData}).then((response)=> {
			console.log(response);
			// if (response.data.code == 1)	{
			// 	this.loading = false;
			// 	let list = response.data.data.value;
			// 	console.log(list);
			// 	this.tableData = [];
			// 	for (var i=0; i<list.length; i++) {
			// 		this.tableData.push({
			// 			id: list[i].id,
			// 			sn: list[i].sn,
			// 			title: list[i].title,
			// 			creator: list[i].creator,
			// 			gmt_created: list[i].gmt_created,
			// 			state_name: list[i].state.state_name
			// 		})
			// 	};
			// 	console.log(this.tableData);
			// 	this.totalCount = response.data.data.total
			// 	console.log(this.totalCount)
			// 	this.totalPage = Math.ceil(response.data.data.total/this.pageSize)
			// console.log(this.totalPage)
			// if (this.totalPage > 1) {
			// 	this.paginationShow = true;
			// }
			// }			
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
		// this.$router.push({path: '/0/OrderDetailUnfinished', query: {id: rowValue.id}})
	}
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
