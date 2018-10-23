<template lang="html">
  <div>
  	<el-row class="container">
      	<el-row v-if="seen" class="order_menu">
      		<el-form ref="search_form" :model="search_form" label-width="80px">
      		<!--<h2 style="font-size:20px;">搜索工单</h2>-->
       		<el-row>
       			<h2 style="font-size:22px;">搜索工单</h2>
      			<el-col :offset="3" :span="8">
      				<el-form-item label="工单编号" prop="orderNum">
      					<el-input v-model="search_form.orderNum" placeholder="请输入工单号"></el-input>
      				</el-form-item>
      			</el-col>
      			<el-col :push="2" :span="8">
      				<el-form-item label="工单日期">
      					<el-col :span="11">
      						<el-form-item prop="date1">
      							<el-date-picker type="date" placeholder="选择起始日期" v-model="search_form.date1" style="width:100%;"></el-date-picker>
      						</el-form-item>
      					</el-col>
      					<el-col class="line" :span="2">-</el-col>
      					<el-col :span="11">
      						<el-form-item prop="date2">
	      						<el-date-picker type="date" placeholder="选择结束日期" v-model="search_form.date2" style="width:100%;"></el-date-picker>
	      					</el-form-item>
      					</el-col>
      				</el-form-item>
      			</el-col>	      		
	      	</el-row>
	      	<el-row>
	      		<el-col :offset="3" :span="8">
	      			<el-form-item label="工单标题" prop="title">
	      				<el-input v-model="search_form.title" placeholder="请输入工单标题"></el-input>
	      			</el-form-item>
	      		</el-col>
	      		<el-col :push="2" :span="8">
	      			<el-form-item label="工单排序" prop="orderState">
	      				<el-select v-model="search_form.orderState" placeholder="请选择工单排序" style="width:100%;">
	      					<el-option label="正序" name="type" value="1"></el-option>
	      					<el-option label="倒序" name="type" value="0"></el-option>
	      				</el-select>
	      			</el-form-item>
	      		</el-col>
	      	</el-row>	      		
	      	<el-row>
	      		<el-form-item>
	      			<el-col :offset="4" :span="7">
						<el-button type="primary" size="medium" @click="searchOrder">搜索</el-button>
					</el-col>
	      			<el-col :span="8">					
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
              <el-breadcrumb-item :to="{ path: '/' }">工单管理</el-breadcrumb-item>
              <el-breadcrumb-item>已办工单</el-breadcrumb-item>
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
               	 <el-button type="text" @click="onBtnDetailClick(scope.$index, tableData)">详情</el-button>
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
import { getTicketList } from '../api/api'
import OrderDetailCompleted from '../components/OrderDetailCompleted'
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
			 { label: '工单号', prop: 'sn'},
			 { label: '工单标题', prop: 'title' },
       { label: '建单人', prop: 'creator'},
       { label: '建单时间', prop: 'gmt_created'},
       { label: '当前状态', prop: 'state_name'}
    ],
    	seen: false,
    	search_form: [
    	{
    		orderNum: '',
    		date1: '',
    		date2: '',
    		title: '',
    		orderState: '',
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
			this.getOrderList();
		},
  	searchOrder () {
			this.$data.seen = false;
			let paramsData = {};
			paramsData["category"] = "relation";
			paramsData["sn"] = this.search_form.orderNum;
			paramsData["title"] = this.search_form.title;
			paramsData["create_start"] = this.getDate(this.search_form.date1);
			paramsData["create_end"] = this.getDate(this.search_form.date2);
			paramsData["reverse"] = this.search_form.orderState;
			getTicketList({params : paramsData}).then((response)=> {
				if (response.data.code == 1) {
					this.loading = false;
					let list = response.data.data.value;
					console.log(list);
					this.tableData = [];
					for (var i=0; i<list.length; i++) {
						this.tableData.push({
							id: list[i].id,
							sn: list[i].sn,
							title: list[i].title,
							creator: list[i].creator,
							gmt_created: list[i].gmt_created,
							state_name: list[i].state.state_name
						})
					};
				}
			})
  	},
  	resetForm(formName) {
			// this.$refs[formName].resetFields();
			this.search_form = [
    	{
    		orderNum: '',
    		date1: '',
    		date2: '',
    		title: '',
    		orderState: '',
    	}];
		},
		getDate (value) {
		let date = new Date(value);
        let y = date.getFullYear();
        let MM = date.getMonth() + 1;
        MM = MM < 10 ? ('0' + MM) : MM;
        let d = date.getDate();
        d = d < 10 ? ('0' + d) : d;
        let h = date.getHours();
        h = h < 10 ? ('0' + h) : h;
        let m = date.getMinutes();
        m = m < 10 ? ('0' + m) : m;
        let s = date.getSeconds();
        s = s < 10 ? ('0' + s) : s;
        //return y + '-' + MM + '-' + d + ' ' + h + ':' + m + ':' + s;
        return y + '-' + MM + '-' + d
		},
		getOrderList() {
  		let paramsData = {};
			paramsData["category"] = "relation";
			paramsData["per_page"] = this.pageSize;
  		paramsData["page"] = this.pageNo;
			getTicketList({params : paramsData}).then((response)=> {
				if (response.data.code == 1) {
					this.loading = false;
					let list = response.data.data.value;
					console.log(list);
					this.tableData = [];
					for (var i=0; i<list.length; i++) {
						this.tableData.push({
							id: list[i].id,
							sn: list[i].sn,
							title: list[i].title,
							creator: list[i].creator,
							gmt_created: list[i].gmt_created,
							state_name: list[i].state.state_name
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
  		this.$nextTick(() => this.getOrderList())
  	},
  	handleCurrentChange(val) {
  		console.log(`当前页:`+val);
  		this.pageNo = val
  		this.getOrderList()
  	},
		onBtnDetailClick (index, rows) {
			let rowValue = JSON.parse(JSON.stringify(rows[index]));
			console.log(rowValue);
			this.$router.push({path: '/0/OrderDetailCompleted', query: {id: rowValue.id}})
		}
	},
	created () {
		this.getOrderList();
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
</style>
