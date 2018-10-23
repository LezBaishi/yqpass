<template lang="html">
  <div>
  	<el-row class="container">
      	<el-row v-if="seen" class="order_menu">
      		<el-form ref="search_form" :model="search_form" label-width="80px">
       		<el-row>
       			<h2 style="font-size:22px;">搜索工单</h2>
      			<el-col :offset="3" :span="8">
      				<el-form-item label="工单号" prop="orderNum">
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
	      			<el-form-item label="端点" prop="endpoint">
	      				<el-input v-model="search_form.endpoint" placeholder="请输入端点信息"></el-input>
	      			</el-form-item>
	      		</el-col>
	      		<el-col :push="2" :span="8">
	      			<el-form-item label="工单状态" prop="orderState">
	      				<el-select v-model="search_form.orderState" placeholder="请选择工单状态" style="width:100%;">
	      					<el-option label="代处理" name="type" value="unfinished"></el-option>
	      					<el-option label="已完成" name="type" value="completed"></el-option>
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
           	<el-button type="primary" icon="el-icon-refresh" size="mini" circle style='float: left;'></el-button>        	  
          </el-col>
          <el-col :span='12' class="breadcrumb">
            <el-breadcrumb separator="/" style='float: right;'>
              <el-breadcrumb-item :to="{ path: '/' }">工单管理</el-breadcrumb-item>
              <el-breadcrumb-item>代办工单</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>
        </el-row>
        <el-row>
        	<el-table :data="tableData">
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
    </el-row>
  </div>
</template>

<script>
import OrderlistDetail from '../components/OrderlistDetail'
import { getTicketList } from '../api/api'
export default {
  data () {
    return {
      tableData: [],
       tableColumns: [
       { label: '工单号', prop: 'sn'},
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
    		endpoint: '',
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
  	searchOrder () {
  		this.$data.seen = false
  	},
  	resetForm(formName) {
  		this.$refs[formName].resetFields();
		},
		getOrderList() {
			let paramsData = new Array();
  		paramsData["category"] = "duty";
			getTicketList({params : paramsData}).then((response)=> {	
				let list = response.data.data.value;
				console.log(list);
				for (var i=0; i<list.length; i++) {
					this.tableData.push({
						sn: list[i].sn,
						creator: list[i].creator,
						gmt_created: list[i].gmt_created,
						state_name: list[i].state.state_name
					})
				};
				console.log(this.tableData);
			})
		},
		onBtnDetailClick (index, rows) {
			console.log(rows[value]);
			let rowValue = JSON.parse(JSON.stringify(rows[index]));
			console.log(rowValue);
			// this.$router.push('/0/OrderlistDetail', query: {})
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
