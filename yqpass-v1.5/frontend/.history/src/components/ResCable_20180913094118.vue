<template lang="html">
  <div>
  	<el-row class="container">
      	<el-row v-if="seen" class="order_menu">
      		<el-form ref="search_form" :model="search_form" label-width="80px">
       		<el-row>
       			<h2 style="font-size:22px;">搜索光缆</h2>
      			<el-col :offset="3" :span="8">
      				<el-form-item label="光缆" prop="cable">
      					<el-input v-model="search_form.cable" placeholder="请输入光缆"></el-input>
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
              <el-breadcrumb-item :to="{ path: '/1/resCable' }">资源管理</el-breadcrumb-item>
              <el-breadcrumb-item>光缆总表</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>
        </el-row>
        <el-row v-if="setPageSeen" class="page_menu">
        	<h2 style="font-size:22px;">页面设置</h2>	
        	<el-checkbox v-model="checked_A">A端信息</el-checkbox>
        	<el-checkbox v-model="checked_Z">Z端信息</el-checkbox>
        	<el-checkbox v-model="checked_ocable_name">光缆名称</el-checkbox>
        	<el-checkbox v-model="checked_core_num">纤芯数</el-checkbox>
        	<el-checkbox v-model="checked_used_core_num">已用纤芯数</el-checkbox>
        	<el-checkbox v-model="checked_core_occ">纤芯占用率</el-checkbox>
        	<el-checkbox v-model="checked_unused_core_num">剩余纤芯数</el-checkbox>
        	<el-checkbox v-model="checked_ocable_length">光缆长度</el-checkbox>
        	<el-checkbox v-model="checked_core_kilo">芯公里</el-checkbox>
        	<el-checkbox v-model="checked_used_core_kilo">使用芯公里</el-checkbox>
        	<el-checkbox v-model="checked_core_usage">纤芯使用率</el-checkbox>
        	<el-checkbox v-model="checked_ocable_type">光缆类型</el-checkbox>
        	<el-checkbox v-model="checked_ocable_level">光缆等级</el-checkbox>
        	<el-checkbox v-model="checked_ofiber_type">光缆型号</el-checkbox>
        	<el-checkbox v-model="checked_notes">备注</el-checkbox>
        </el-row>
        <el-row>
        	<el-col :push="18" :span="1">	
				<!-- <el-button type="primary" size="mini" round @click="addRow(tableData)">新增表行</el-button> -->
				<el-button type="primary" size="mini" round @click="dialogFormVisible = true">新增表行</el-button>
        	</el-col>
        	<el-col :push="19" :span="1">
		        <el-button type="primary" size="mini" round @click="setPage">页面设置</el-button>
    		</el-col>
    		<el-col :push="20" :span="1">
	        	<el-button type="primary" size="mini" round @click="exportInfo">导出数据</el-button>
			</el-col>
			<el-dialog title="新增光缆段" :visible.sync="dialogFormVisible" width="60%" center class="dialog">
				<el-form :model="dialog_form" class="dialogForm">
					<el-form-item label="A端名称" :label-width="formLabelWidth">
						<el-input placeholder="如3.1栋101数据机房路由1-1或1.1栋1楼南塔弱电间" v-model="dialog_form.name_A"></el-input>
					</el-form-item>
					<el-row>
						<el-form-item label="A端设备所在楼栋机房" :label-width="formLabelWidth">
							<el-col :span="5">
								<el-select v-model="dialog_form.building_A" placeholder="请选择机楼" v-on:change="get_machineBuilding($event)">
									<el-option v-for="item in machineBuilding_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
								</el-select>
							</el-col>
							<el-col :span="5" :push="1">
								<el-select v-model="dialog_form.room_A" placeholder="请选择机房" v-on:change="get_machineRoom($event)">
									<el-option v-for="item in machineRoom_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
								</el-select>
							</el-col>							
						</el-form-item>
					</el-row>
					<el-form-item label="Z端名称" :label-width="formLabelWidth">
						<el-input placeholder="如3.1栋101数据机房路由1-1或1.1栋1楼南塔弱电间" v-model="dialog_form.name_Z"></el-input>
					</el-form-item>
					<el-row>
						<el-form-item label="Z端设备所在楼栋机房" :label-width="formLabelWidth">
							<el-col :span="5">
								<el-select v-model="dialog_form.building_Z" placeholder="请选择机楼" v-on:change="get_machineBuilding($event)">
									<el-option v-for="item in machineBuilding_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
								</el-select>
							</el-col>
							<el-col :span="5" :push="1">
								<el-select v-model="dialog_form.room_Z" placeholder="请选择机房" v-on:change="get_machineRoom($event)">
									<el-option v-for="item in machineRoom_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
								</el-select>
							</el-col>							
						</el-form-item>
					</el-row>
					<el-form-item label="光缆名称" :label-width="formLabelWidth">
						<el-input placeholder="如3.1栋101数据机房路由1-1或1.1栋1楼南塔弱电间" v-model="dialog_form.ocable_name"></el-input>
					</el-form-item>
					<el-row>
						<el-col :span="10">
							<el-form-item label="纤芯数" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.core_num"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="10" :push="1">
							<el-form-item label="已用纤芯数" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.used_core_num"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
				</el-form>
			</el-dialog>
        </el-row>
        <el-row>
          	<el-table :data="tableData" ref="table" tooltip-effect="dark" border stripe style="width:100%;margin-top:10px;">
          		<el-table-column label="序号" type="index" width="60" align="center"></el-table-column>
          		<el-table-column label="A端" align="center" v-if="checked_A">
          			<el-table-column label="楼栋" prop="building_A" width="110" align="center">
          				<template slot-scope="scope">
          					<el-select v-show="scope.row.edit" v-model="scope.row.building_A" placeholder="请选择楼栋" v-on:change="get_machineBuilding($event)">
          						<el-option v-for="item in machineBuilding_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
          					</el-select>
          					<span v-show="!scope.row.edit">{{ scope.row.building_A }}</span>
          				</template>
          			</el-table-column>
          			<el-table-column label="机房号" prop="room_A" width="110" align="center">
          				<template slot-scope="scope">
          					<el-select v-show="scope.row.edit" v-model="scope.row.room_A" placeholder="请选择机房" v-on:change="get_machineRoom($event)">
          						<el-option v-for="item in machineRoom_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
          					</el-select>
          					<span v-show="!scope.row.edit">{{ scope.row.room_A }}</span>
          				</template>
          			</el-table-column>
          			<el-table-column label="名称" prop="name_A" align="center" width="370">
          				<template slot-scope="scope">
          					<el-input v-show="scope.row.edit" v-model="scope.row.name_A" placeholder="如3.1栋101数据机房路由1-1或1.1栋1楼南塔弱电间"></el-input>
          					<span v-show="!scope.row.edit">{{ scope.row.name_A }}</span>
          				</template>
          			</el-table-column>
          		</el-table-column>
          		<el-table-column label="Z端" align="center" v-if="checked_Z">
          			<el-table-column label="楼栋" prop="building_Z" width="110" align="center">
          				<template slot-scope="scope">
          					<el-select v-show="scope.row.edit" v-model="scope.row.building_Z" placeholder="请选择楼栋" v-on:change="get_machineBuilding($event)">
          						<el-option v-for="item in machineBuilding_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
          					</el-select>
          					<span v-show="!scope.row.edit">{{ scope.row.building_Z }}</span>
          				</template>
          			</el-table-column>
          			<el-table-column label="机房号" prop="room_Z" width="110" align="center">
          				<template slot-scope="scope">
          					<el-select v-show="scope.row.edit" v-model="scope.row.room_Z" placeholder="请选择机房" v-on:change="get_machineRoom($event)">
          						<el-option v-for="item in machineRoom_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
          					</el-select>
          					<span v-show="!scope.row.edit">{{ scope.row.room_Z }}</span>
          				</template>
          			</el-table-column>
          			<el-table-column label="名称" prop="name_Z" align="center" width="370">
          				<template slot-scope="scope">
          					<el-input v-show="scope.row.edit" v-model="scope.row.name_Z" placeholder="如3.1栋101数据机房路由1-1或1.1栋1楼南塔弱电间"></el-input>
          					<span v-show="!scope.row.edit">{{ scope.row.name_Z }}</span>
          				</template>
          			</el-table-column>
          		</el-table-column>
          		<el-table-column label="光缆名称" width="500" align="center" v-if="checked_ocable_name">
          			<template slot-scope="scope">
          				<el-input v-show="scope.row.edit" v-model="scope.row.ocable_name"></el-input>
          				<span v-show="!scope.row.edit">{{ scope.row.ocable_name }}</span>
          			</template>
          		</el-table-column>
          		<el-table-column label="纤芯数" width="100" align="center" v-if="checked_core_num">
          			<template slot-scope="scope">
          				<el-input v-show="scope.row.edit" v-model="scope.row.core_num"></el-input>
          				<span v-show="!scope.row.edit">{{ scope.row.core_num }}</span>
          			</template>
          		</el-table-column>
          		<el-table-column label="已用纤芯数" width="100" align="center" v-if="checked_used_core_num">
          			<template slot-scope="scope">
          				<el-input v-show="scope.row.edit" v-model="scope.row.used_core_num"></el-input>
          				<span v-show="!scope.row.edit">{{ scope.row.used_core_num }}</span>
          			</template>
          		</el-table-column>
          		<el-table-column label="纤芯利用率" width="220" align="center" v-if="checked_core_occ">
          			<template slot-scope="scope">
          				<el-input v-show="scope.row.edit" v-model="scope.row.core_occ" placeholder="等于已用纤芯数/纤芯数"></el-input>
          				<span v-show="!scope.row.edit">{{ scope.row.core_occ }}</span>
          			</template>
          		</el-table-column>          		          		
          		<el-table-column label="剩余纤芯数" width="220" align="center" v-if="checked_unused_core_num">
          			<template slot-scope="scope">
          				<el-input v-show="scope.row.edit" v-model="scope.row.unused_core_num" placeholder="等于纤芯数-已用纤芯数"></el-input>
          				<span v-show="!scope.row.edit">{{ scope.row.unused_core_num }}</span>
          			</template>
          		</el-table-column> 
          		<el-table-column label="光缆长度" width="220" align="center" v-if="checked_ocable_length">
          			<template slot-scope="scope">
          				<el-input v-show="scope.row.edit" v-model="scope.row.ocable_length" placeholder="单位：皮长公里"></el-input>
          				<span v-show="!scope.row.edit">{{ scope.row.ocable_length }}</span>
          			</template>
          		</el-table-column>
          		<el-table-column label="芯公里" width="220" align="center" v-if="checked_core_kilo">
          			<template slot-scope="scope">
          				<el-input v-show="scope.row.edit" v-model="scope.row.core_kilo" placeholder="等于纤芯数*光缆长度"></el-input>
          				<span v-show="!scope.row.edit">{{ scope.row.core_kilo }}</span>
          			</template>
          		</el-table-column>
          		<el-table-column label="使用芯公里" width="220" align="center" v-if="checked_used_core_kilo">
          			<template slot-scope="scope">
          				<el-input v-show="scope.row.edit" v-model="scope.row.used_core_kilo" placeholder="等于已用纤芯数*光缆长度"></el-input>
          				<span v-show="!scope.row.edit">{{ scope.row.used_core_kilo }}</span>
          			</template>
          		</el-table-column>
          		<el-table-column label="纤芯使用率" width="220" align="center" v-if="checked_core_usage">
          			<template slot-scope="scope">
          				<el-input v-show="scope.row.edit" v-model="scope.row.core_usage" placeholder="等于使用芯公里/芯公里"></el-input>
          				<span v-show="!scope.row.edit">{{ scope.row.core_usage }}</span>
          			</template>
          		</el-table-column>
          		<el-table-column label="光缆类型" width="110" align="center" v-if="checked_ocable_type">
          			<template slot-scope="scope">
          				<el-select v-show="scope.row.edit" v-model="scope.row.ocable_type">
          					<el-option v-for="item in ocable_type_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
          				</el-select>
          				<span v-show="!scope.row.edit">{{ scope.row.ocable_type }}</span>
          			</template>
          		</el-table-column>	       
          		<el-table-column label="光缆等级" width="240" align="center" v-if="checked_ocable_level">
          			<template slot-scope="scope">
          				<el-select v-show="scope.row.edit" v-model="scope.row.ocable_level">
          					<el-option v-for="item in ocable_level_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
          				</el-select>
          				<span v-show="!scope.row.edit">{{ scope.row.ocable_level }}</span>
          			</template>
          		</el-table-column>
          		<el-table-column label="光纤型号" width="110" align="center" v-if="checked_ofiber_type">
          			<template slot-scope="scope">
          				<el-select v-show="scope.row.edit" v-model="scope.row.ofiber_type">
          					<el-option v-for="item in ofiber_type_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
          				</el-select>
          				<span v-show="!scope.row.edit">{{ scope.row.ofiber_type }}</span>
          			</template>
          		</el-table-column>
          		<el-table-column label="备注" width="220" align="center" v-if="checked_notes">
          			<template slot-scope="scope">
          				<el-input v-show="scope.row.edit" v-model="scope.row.notes"></el-input>
          				<span v-show="!scope.row.edit">{{ scope.row.notes }}</span>
          			</template>
          		</el-table-column>
	  			<el-table-column label="操作" width="140" align="center">
	  				<template slot-scope="scope">
	  					<el-button type="primary" circle size="mini" @click="detailView(scope.$index, tableData)" icon="el-icon-view"></el-button>
	  					<el-button :type="scope.row.edit?'success':'primary'" @click='scope.row.edit=!scope.row.edit' circle size="mini" icon="el-icon-edit"></el-button> 
	  					<el-button type="danger" circle size="mini" @click="deleteRow(scope.$index, tableData)" icon="el-icon-delete"></el-button>	  					
	  				</template>	  					
	  			</el-table-column>          		
          	</el-table>          		
        </el-row>
    </el-row>
  </div>
</template>

<script>
import ResCableDetail from '../components/ResCableDetail'
export default {
  data () {
    return {
	  tableData: [],
	  dialog_form: {
  		building_A: '',
      	room_A: '',
      	name_A: '',
      	building_Z: '',
      	room_Z: '',
      	name_Z: '',
      	ocable_name: '',
      	core_num: '',
      	used_core_num: '',
      	core_occ: '',
      	unused_core_num: '',
      	ocable_length: '',
      	core_kilo: '',
      	used_core_kilo: '',
      	core_usage: '',
      	ocable_type: '',
      	ocable_level: '',
      	ofiber_type: '',
      	notes: ''
  		}, 
       tableColumns: [
       { label: '标题', prop: 'title'},
       { label: '更新时间', prop: 'updateTime'}
	],
	    dialogFormVisible: false,
	    formLabelWidth: '150px',
    	seen: false,
    	setPageSeen: false,
    	checked_A: true,
    	checked_Z: true,
    	checked_ocable_name: true,
    	checked_core_num: true,
    	checked_used_core_num: true,
    	checked_core_occ: true,
    	checked_unused_core_num: true,
    	checked_ocable_length: true,
    	checked_core_kilo: true,
    	checked_used_core_kilo: true,
    	checked_core_usage: true,
    	checked_ocable_type: true,
    	checked_ocable_level: true,
    	checked_ofiber_type: true,
    	checked_notes: true,
    	search_form: [
    	{
    		cable: '',
    		date1: '',
    		date2: '',
    		endpoint: '',
    		orderState: '',
    	}],
    	machineBuilding_option: [{
      		value: '3.1栋',
      		label: '3.1栋'
      },{
      		value: '2.3栋',
      		label: '2.3栋'
      }],
        ocable_type_option: [{
      		value: 'single',
      		label: '单模'
      	},{
      		value: 'more',
      		label: '多模'
      	}],
      	ocable_level_option: [{
      		value: '干线',
      		label: '干线'
      	},{
      		value: '广州本地网',
      		label: '广州本地网'
      	},{
      		value: '南方基地园区',
      		label: '南方基地园区'
      	},{
      		value: '南方基地园区（CMNET网络成端）',
      		label: '南方基地园区（CMNET网络成端）'
      	}],
      	ofiber_type_option: [{
      		value: 'G652',
      		label: 'G652'
      	},{
      		value: 'G655',
      		label: 'G655'
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
  	resetForm (formName) {
  		this.$refs[formName].resetFields();
  	},
  	setPage () {
  		if (this.$data.setPageSeen == false){
  			this.$data.setPageSeen = true;
  		}else {
  			this.$data.setPageSeen = false;
  		}
  	},
  	get_machineBuilding: function (building) {
  		let temRoom = [];
  		let allRoom = [{
  			building: "3.1栋",
  			label: "201"
  		},{
  			building: "3.1栋",
  			label: "202"
  		},{
  			building: "2.3栋",
  			label: "201"
  		},{
  			building: "2.3栋",
  			label: "202"
  		}];
  		for (var i in allRoom){
  			if (building == allRoom[i].building){
  				temRoom.push({label: allRoom[i].label, value: allRoom[i].label})
  			}
  		}
  		console.log(temRoom)
  		this.machineRoom_option = temRoom;
  	},
  	addRow (tableData, event) {		
  		var list = {
  		building_A: '',
      	room_A: '',
      	name_A: '',
      	building_Z: '',
      	room_Z: '',
      	name_Z: '',
      	ocable_name: '',
      	core_num: '',
      	used_core_num: '',
      	core_occ: '',
      	unused_core_num: '',
      	ocable_length: '',
      	core_kilo: '',
      	used_core_kilo: '',
      	core_usage: '',
      	ocable_type: '',
      	ocable_level: '',
      	ofiber_type: '',
      	notes: '',
      	edit: true
  		}
  		tableData.push(list)
  	},
  	deleteRow (index, rows) {
    	this.$confirm('是否确定删除该行数据', '提示', {
    		confirmButtonText: '确定',
    		cancelButtonText: '取消',
    		type: 'warning'
    	}).then(() => {
			rows.splice(index, 1);   		
    	}).catch(() => {

    	});  		  		  		
  	},
  	detailView (index, rows) {
  		this.$router.push('/1/resCableDetail')
  	}
  },
  created () {
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
.page_menu {
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-color: #F9FAFC;
  margin: 10px auto 10px auto ;
  border: 2px solid #8492A6;
  padding: 0px 10px 10px 10px;	
}
.panel-c-c {
    /*这是列，因为已经有了列的宽度因此无需设置width*/
  background: #f1f2f7;
  position: absolute;
  right: 0px;
  top: 0px;
  bottom: 0px;
  height: 100%;
    /*内层设置滚动*/
  padding: 10px;
}
</style>