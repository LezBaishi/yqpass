<template lang="html"> 
  <div>
    <el-row class="container">
    <el-row> 
          <!-- <el-col :span='12' class="button_nav">
            <el-button type="primary" icon="el-icon-edit" size="mini" circle style='float: left;' @click="searchBtn"></el-button>
            <el-button type="primary" icon="el-icon-refresh" size="mini" circle style='float: left;'></el-button>           
          </el-col> -->
          <el-col :offset="12" :span='12' class="breadcrumb">
            <el-breadcrumb separator="/" style='float: right;'>
              <el-breadcrumb-item :to="{ path: '/' }">工单管理</el-breadcrumb-item>
              <el-breadcrumb-item>新建工单</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>      
    </el-row>
  	<h3 style="font-size:20px;">中国移动南方基地园区内部单模光缆纤芯申请单</h3>
  	<el-row class="header">
  	<el-form ref="orderMain_form" :model="orderMain_form" label-width="80px">
  		<el-row style="margin-bottom:15px;">
  			<el-col :span="12" text-align="left">
  				<p v-model="orderNum" style="font-size:14px;float: left;font-weight:bold;">申请施工单号：{{ orderNum }}</p>
  			</el-col>
  			<el-col :span="12" text-align="right">
  				<p style="font-size:14px;float: right;font-weight:bold;">申请时间：{{ applyDate | formatDate }}</p>
  			</el-col>
  		</el-row>
  		<el-row>
  			<el-col :span="11">  			
	  			<el-form-item label="* 项目名称">
	  				<el-input placeholder="请输入项目名称" v-model="orderMain_form.project_name"></el-input>
	  			</el-form-item>
  			</el-col>			
  			<el-col :span="11" :push="2">  			
	  			<el-form-item label="开通时间">
	  			  <el-date-picker type="date" placeholder="选择开通日期" value-format="yyyy-MM-dd" v-model="orderMain_form.date" style="width:100%;"></el-date-picker>	
	  			</el-form-item>
  			</el-col>
  		</el-row>
  		<el-row>
	  		<el-col :span="7">  			
		  		<el-form-item label="* 移动人员">
		  			<el-input placeholder="请填写姓名" v-model="orderMain_form.CMer_name"></el-input>
		  		</el-form-item>
	  		</el-col>
	  		<el-col :span="7" :offset="1">  			
		  		<el-form-item label="* 电话">
		  			<el-input placeholder="请填写手机号" v-model="orderMain_form.CMer_phone"></el-input>
		  		</el-form-item>
	  		</el-col>  
	  		<el-col :span="7" :offset="1">  			
		  		<el-form-item label="* 邮箱">
		  			<el-input placeholder="请填写邮箱" v-model="orderMain_form.CMer_email"></el-input>
		 			</el-form-item>
	  		</el-col>	
	  	</el-row>  			
		<el-row>			  			
	  		<el-col :span="7">  			
		  		<el-form-item label="* 配合人员">
		  			<el-input placeholder="请填写姓名" v-model="orderMain_form.CPer_name"></el-input>
				</el-form-item>
	  		</el-col>
	  		<el-col :span="7" :offset="1">  			
		  		<el-form-item label="* 电话">
		  			<el-input placeholder="请填写手机号" v-model="orderMain_form.CPer_phone"></el-input>
		  		</el-form-item>
	  		</el-col>  
	  		<el-col :span="7" :offset="1">  			
		  		<el-form-item label="* 邮箱">
		  			<el-input placeholder="请填写邮箱" v-model="orderMain_form.CPer_email"></el-input>
		  		</el-form-item>
	  		</el-col> 	  							
  		</el-row>  		
  	</el-form>
  </el-row>
  <el-row class="content">
  	<div class="button" style="width:3%;float:right;">
  		<p><el-button class="el-icon-plus" size="mini" @click.prevent="addRow()"></el-button></p>
  		<p><el-button class="el-icon-minus" size="mini" @click.prevent="delData()"></el-button></p>
  	</div>
  	<div class="table">
  		<el-table :data="order_form" ref="table" tooltip-effect="dark" border stripe style="width:95%" @selection-change='selectRow'>
  		<!-- <el-table v-for='(list, index) in lists' :key='list.id'> -->
  			<el-table-column type="selection" width="45" align="center"></el-table-column>
  			<el-table-column label="序号" type="index" width="60" align="center"></el-table-column>
  			<el-table-column label="业务系统" align="center" width="240">
  				<template slot-scope="scope">
	  				<el-input placeholder="如南方基地信息支撑平台" v-model="order_form.businessSystem"></el-input>
  				</template>
  			</el-table-column>
  			<el-table-column label="A端设备移动维护部门">
  				<el-table-column label="部门名称" width="140">
  					<template slot-scope="scope">
  						<el-input placeholder="如XX中心" v-model="order_form.ACM_department"></el-input>
	  				</template>
  				</el-table-column>
  				<el-table-column label="移动负责人" width="96">
  					<template slot-scope="scope">
  						<el-input v-model="order_form.ACM_header"></el-input>
  					</template>	
  				</el-table-column>
  				<el-table-column label="联系方式" width="140">
  					<template slot-scope="scope">
	  					<el-input v-model="order_form.ACM_headerMobile"></el-input>
  					</template>
  				</el-table-column>  				
  			</el-table-column>
  			<el-table-column label="A端设备维护合作单位">
  				<el-table-column label="单位名称" width="140">
  					<template slot-scope="scope">
	  					<el-input placeholder="如XX公司" v-model="order_form.ACP_department"></el-input>
	  				</template>
  				</el-table-column>
  				<el-table-column label="负责人" width="96">
  					<template slot-scope="scope">
  						<el-input v-model="order_form.ACP_header"></el-input>
  					</template>
  				</el-table-column>
  				<el-table-column label="联系方式" width="140">
  					<template slot-scope="scope">
	  					<el-input v-model="order_form.ACP_headerMobile"></el-input>
  					</template>
  				</el-table-column>
  			</el-table-column>
  			<el-table-column label="A端业务设备所在楼栋机房">
  				<el-table-column label="机楼" width="110">
  					<template slot-scope="scope">
  						<el-select v-model="order_form.A_machineBuilding" placeholder="请选择机房" v-on:change="get_machineBuilding($event)">
  							<el-option v-for="item in machineBuilding_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
  						</el-select>  						
  					</template>
  				</el-table-column>
  				<el-table-column label="机房" width="110">
  					<template slot-scope="scope">
  						<el-select v-model="order_form.A_machineRoom" placeholder="请选择机房" v-on:change="get_machineRoom($event)">
  							<el-option v-for="item in machineRoom_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
  						</el-select>
	  				</template>	
  				</el-table-column>
  			</el-table-column>
  			<el-table-column label="A端业务设备位置（填写具体机架号）" width="150">
  				<template slot-scope="scope">
	  				<el-input placeholder="如A02架" v-model="order_form.A_machineRack"></el-input>
  				</template>
  			</el-table-column>  			
  			<el-table-column label="A端业务设备/网元名称" width="240">
  				<template slot-scope="scope">
	  				<el-input placeholder="如S9303交换机或核心交换机" v-model="order_form.A_deviceName"></el-input>
  				</template>
  			</el-table-column>
  			<el-table-column label="A端业务设备端口" width="240">
  				<template slot-scope="scope">
  					<el-input placeholder="如POS 1/1/0或交换机端口-1" v-model="order_form.A_devicePort"></el-input>
  				</template>
  			</el-table-column>
  			<el-table-column label="A端设备端口类型" width="110">
  				<template slot-scope="scope">
  					<el-select v-model="order_form.A_portType" placeholder="请选择">
	  					<el-option v-for="item in portType_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
	  				</el-select>
  				</template>
  			</el-table-column>
  			<el-table-column label="Z端设备移动维护部门">
  				<el-table-column label="部门名称" width="140">
  					<template slot-scope="scope">
	  					<el-input placeholder="如XX中心" v-model="order_form.ZCM_department"></el-input>
  					</template>
  				</el-table-column>
  				<el-table-column label="负责人" width="96">
  					<template slot-scope="scope">
	  					<el-input v-model="order_form.ZCM_header"></el-input>
  					</template>
  				</el-table-column>
  				<el-table-column label="联系方式" width="140">
  					<template slot-scope="scope">
	  					<el-input v-model="order_form.ZCM_headerMobile"></el-input>
  					</template>
  				</el-table-column>  				
  			</el-table-column>
  			<el-table-column label="Z端设备维护合作单位">
  				<el-table-column label="单位名称" width="140">
  					<template slot-scope="scope">
	  					<el-input placeholder="如XX公司" v-model="order_form.ZCP_department"></el-input>
  					</template>
  				</el-table-column>
  				<el-table-column label="负责人" width="96">
  					<template slot-scope="scope">
	  					<el-input v-model="order_form.ZCP_header"></el-input>
  					</template>
  				</el-table-column>
  				<el-table-column label="联系方式" width="140">
  					<template slot-scope="scope">
	  					<el-input v-model="order_form.ZCP_headerMobile"></el-input>
  					</template>
  				</el-table-column>
  			</el-table-column>
  			<el-table-column label="Z端业务设备所在楼栋机房">
  				<el-table-column label="机楼" width="110">
  					<template slot-scope="scope">
  						<el-select v-model="order_form.A_machineBuilding" placeholder="请选择机房" v-on:change="get_machineBuilding($event)">
  							<el-option v-for="item in machineBuilding_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
  						</el-select>  						
  					</template>
  				</el-table-column>
  				<el-table-column label="机房" width="110">
  					<template slot-scope="scope">
  						<el-select v-model="order_form.A_machineRoom" placeholder="请选择机房" v-on:change="get_machineRoom($event)">
  							<el-option v-for="item in machineRoom_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
  						</el-select>
	  				</template>	
  				</el-table-column>
  			</el-table-column>  			
  			<el-table-column label="Z端业务设备位置（填写具体机架号）" width="150">
  				<template slot-scope="scope">
	  				<el-input placeholder="如A02架" v-model="order_form.A_machineRack"></el-input>
  				</template>
  			</el-table-column> 
  			<el-table-column label="Z端业务设备/网元名称" width="240">
  				<template slot-scope="scope">
	  				<el-input placeholder="如S9303交换机或核心交换机" v-model="order_form.A_deviceName"></el-input>
  				</template>
  			</el-table-column>
  			<el-table-column label="Z端业务设备端口" width="240">
  				<template slot-scope="scope">
  					<el-input placeholder="如POS 1/1/0或交换机端口-1" v-model="order_form.A_devicePort"></el-input>
  				</template>
  			</el-table-column>  			
  			<el-table-column label="Z端设备端口类型" width="110">
  				<template slot-scope="scope">
  					<el-select v-model="order_form.A_portType" placeholder="请选择">
	  					<el-option v-for="item in portType_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
	  				</el-select>
  				</template>
  			</el-table-column>
  			<el-table-column label="需求带宽" width="110">
				<template slot-scope="scope">
					<el-select v-model="order_form.bandwidth">
						<el-option v-for="item in bandwidth_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
	  				</el-select>
	  			</template>
  			</el-table-column>
  			<el-table-column label="链路主备关系" width="110">
  				<template slot-scope="scope">
  					<el-select v-model="order_form.linkRelations" placeholder="请选择">
	  					<el-option v-for="item in link_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
	  				</el-select>
  				</template>
  			</el-table-column> 			  			  			
  		</el-table>
  	</div>
  </el-row>
  <el-row class="footer">
  	<el-row>
  		<el-button type="primary" icon="el-icon-warning" @click="readIns">填单说明</el-button>
  		<el-button type="primary" icon="el-icon-success">提交工单</el-button>
  	</el-row>
  	<el-row class="instructions" style="text-align:left" v-if="ins_seen">
  		<p>注：南方基地园区传输网络定位为园区企业网，提供已有传输资源的、不出园区的、内部系统互联的<span style="color:red">单模光缆传输</span>，解决园区内部业务互联的传输需求。不承载广州本地网、无线网络、客户专线等出园区的业务及其延伸段。园区和机楼内如需2M/45M等小颗粒传输，由业务部门连同主设备一起采购相关转换器件，通过单模光缆传输。<br>
  		<br>1、园区内业务网与传输网以ODF为分工界面：
  		<br>（1）业务网设备系统到业务侧ODF的跳纤和标签制作（设备成端），以及机房内设备互联、机房间的多模纤芯的互联，由业务部门负责施工和维护。
  		<br><u>如业务侧没有业务侧成端架位，其业务设备连接到传输侧ODF架位的布线和标签工作由业务侧完成并负责维护。</u>
  		<br>（2）园区内部传输网资源（如机房A的ODF到机房B的ODF间的单模光缆）由南方基地网管支撑中心设备维护室负责分配和维护。传输设备到传输侧ODF的跳线和标签制作，由南基网络支撑中心设备维护室负责施工和维护。
  		<br><u>机房间单模光缆由网管支撑中心设备维护室维护，不含多模光缆。<span style="color:red;">如要使用多模光缆，由业务需求部门建设和维护。</span></u>
  		<br>2、<span style="color:red;">标*为必填信息，如填写不完整，一律退回，拖延的时间由申请部门负责。</span>套传输链路（一收一发）对应1行。请详细填写，以便顺利施工和日后维护，要求见批注。在<span style="color:red;">有资源的情况下</span>，在提交准确<span style="color:red;">完整的</span>申请单后，<span style="color:red;">约十个工作日跳通传输</span>。【请预留足够时间提前申请】
  		<br>3、园区内传输24小时报障电话：<span style="color:red;">14715008880</span>/13609076903 <span style="color:red;">只有通过本施工单正式向传输专业申请的纤芯资源才能纳入维护范畴。另请需求部门在完成业务侧成端跳纤到ODF施工后在ODF端口处做好标签记录。</span>
	  	</p>
  	</el-row>
  </el-row>
  </el-row>
  </div>
</template>

<script>
// import Header from '../components/header'
export default {
  data () {
    return {
   	  orderNum: '20180804-0001',
      applyDate: new Date().getTime(),
      orderMain_form: [{
      	project_name: '',
      	date: '',
      	CMer_name: '',
      	CMer_phone: '',
      	CMer_email: '',
      	CPer_name: '',
      	CPer_phone: '',
      	CPer_email: ''
      }],
      order_form: [
      {      	
      	businessSystem: '',
      	ACM_department: '',
      	ACM_header: '',
      	ACM_headerMobile: '',
      	ACP_department: '',
      	ACP_header: '',
      	ACP_headerMobile: '',
      	A_machineBuilding: '',
      	A_machineRoom: '',
      	A_machineRack: '',
      	A_deviceName: '',
      	A_devicePort: '',
      	A_portType: '',
      	A_odfRack: '',
      	ZCM_department: '',
      	ZCM_header: '',
      	ZCM_headerMobile: '',
      	ZCP_department: '',
      	ZCP_header: '',
      	ZCP_headerMobile: '',
      	Z_machineBuilding: '',
      	Z_machineRoom: '',
      	Z_machineRack: '',
      	Z_deviceName: '',
      	Z_devicePort: '',
      	Z_portType:'',
      	Z_odfRack: '',
      	bandwidth: '',
      	linkRelations: ''
      }],
      order_form_empty: [
      {      	
      	businessSystem: '',
      	ACM_department: '',
      	ACM_header: '',
      	ACM_headerMobile: '',
      	ACP_department: '',
      	ACP_header: '',
      	ACP_headerMobile: '',
      	A_machineBuilding: '',
      	A_machineRoom: '',
      	A_machineRack: '',
      	A_deviceName: '',
      	A_devicePort: '',
      	A_portType: '',
      	A_odfRack: '',
      	ZCM_department: '',
      	ZCM_header: '',
      	ZCM_headerMobile: '',
      	ZCP_department: '',
      	ZCP_header: '',
      	ZCP_headerMobile: '',
      	Z_machineBuilding: '',
      	Z_machineRoom: '',
      	Z_machineRack: '',
      	Z_deviceName: '',
      	Z_devicePort: '',
      	Z_portType:'',
      	Z_odfRack: '',
      	bandwidth: '',
      	linkRelations: ''
      }],
      order_form_lists: [],
      newAddFormId: 1,
      portType_option: [{
      		value: 'single',
      		label: '单模'
      	},{
      		value: 'more',
      		label: '多模'
      	}],
      link_option: [{
      		value: 'main',
      		label: '主用'
      	},{
      		value: 'spare',
      		label: '备用'
      	}], 
      bandwidth_option: [{
      	value: '155M',
      	label: '155M'
      },{
      	value: '1GE',
      	label: '1GE'
      },{
      	value: '2.5GE',
      	label: '2.5GE'
      },{
      	value: '10GE',
      	label: '10GE'
      },{
      	value: '40GE',
      	label: '40GE'
      },{
      	value: '100GE',
      	label: '100GE'
      }],   
      machineBuilding_option: [{
      		value: '3.1栋',
      		label: '3.1栋'
      },{
      		value: '2.3栋',
      		label: '2.3栋'
      }],  	
      machineRoom_option: [],
      selectlistRow: [],
      ins_seen: true
    }
  },
  filters: {
      formatDate: function (value) {
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
      }
    },
  methods: {
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
  	selectRow (val) {
  		this.selectlistRow = val
  	},
	addRow () {
		
  		var list = {
  		businessSystem: '',
      	ACM_department: '',
      	ACM_header: '',
      	ACM_headerMobile: '',
      	ACP_department: '',
      	ACP_header: '',
      	ACP_headerMobile: '',
      	A_machineBuilding: '',
      	A_machineRoom: '',
      	A_machineRack: '',
      	A_deviceName: '',
      	A_devicePort: '',
      	A_portType: '',
      	A_odfRack: '',
      	ZCM_department: '',
      	ZCM_header: '',
      	ZCM_headerMobile: '',
      	ZCP_department: '',
      	ZCP_header: '',
      	ZCP_headerMobile: '',
      	Z_machineBuilding: '',
      	Z_machineRoom: '',
      	Z_machineRack: '',
      	Z_deviceName: '',
      	Z_devicePort: '',
      	Z_portType:'',
      	Z_odfRack: '',
      	bandwidth: '',
      	linkRelations: ''
  		}
  		 this.order_form.unshift(list)
  		/* this.lists.push(this.order_form);
  		this.order_form = Object.assign({}, this.order_form_empty); */
  	},
  	/*
  	addRow () {
  		this.lists.push({
  			id: this.newAddFormId++,
  			A_machineBuilding: this.order_form.A_machineBuilding,
  			A_machineRoom: this.order_form.A_machineRoom,
  			A_machineRack: this.order_form.A_machineRack,
	      	A_deviceName: this.order_form.A_deviceName,
	      	A_devicePort: this.order_form.A_devicePort,
	      	A_portType: this.order_form.A_portType,
	      	A_odfRack: this.order_form.A_odfRack,
	      	ZCM_department: this.order_form.ZCM_department,
	      	ZCM_header: this.order_form.ZCM_header,
	      	ZCM_headerMobile: this.order_form.ZCM_headerMobile,
	      	ZCP_department: this.order_form.ZCM_department,
	      	ZCP_header: this.order_form.ZCP_header,
	      	ZCP_headerMobile: this.order_form.ZCP_headerMobile,
	      	Z_machineBuilding: this.order_form.Z_machineBuilding,
	      	Z_machineRoom: this.order_form.Z_machineRoom,
	      	Z_machineRack: this.order_form.Z_machineRack,
	      	Z_deviceName: this.order_form.Z_deviceName,
	      	Z_devicePort: this.order_form.Z_devicePort,
	      	Z_portType: this.order_form.Z_portType,
	      	Z_odfRack: this.order_form.Z_odfRack,
	      	bandwidth: this.order_form.bandwidth,
	      	linkRelations: this.order_form.linkRelations
	  		})
  		this.order_form.A_machineBuilding='',
  		this.order_form.A_machineRoom='',
  		this.order_form.A_machineRack='',
	    this.order_form.A_deviceName='',
	    this.order_form.A_devicePort='',
	    this.order_form.A_portType='',
	    this.order_form.A_odfRack='',
	    this.order_form.ZCM_department='',
	    this.order_form.ZCM_header='',
	    this.order_form.ZCM_headerMobile='',
	    this.order_form.ZCM_department='',
	    this.order_form.ZCP_header='',
	    this.order_form.ZCP_headerMobile='',
	    this.order_form.Z_machineBuilding='',
	    this.order_form.Z_machineRoom='',
	    this.order_form.Z_machineRack='',
	    this.order_form.Z_deviceName='',
	    this.order_form.Z_devicePort='',
	    this.order_form.Z_portType='',
	    this.order_form.Z_odfRack='',
	    this.order_form.bandwidth='',
	    this.order_form.linkRelations=''  		
  	}, */
  	delData () {
  		let val = this.selectlistRow
  		val.forEach(val => {
        this.order_form.splice(val, 1)          
  		})

  		this.$ref.order_form.clearSelection()
  	},
  	handleSubmit () {
  		this.$router.push({path: '/'})
  	},
  	toReg () {
  		this.$router.push({path: '/reg'})
  	},
  	readIns () {
  		if (this.$data.ins_seen == false){
  			this.$data.ins_seen = true;
  			console.log(this.dateFormatter(this.$data.applyDate))
  		}else {
  			this.$data.ins_seen = false;
  		}  		
  	}
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
.header {
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-color: #F9FAFC;
  margin: 20px 15px 20px 15px ;
  border: 2px solid #8492A6;
  padding: 10px 35px 15px 35px;	
}
.content {
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-color: #F9FAFC;
  margin: 20px 15px 20px 15px ;
  border: 2px solid #8492A6;
  padding: 10px 20px 10px 20px;
}
.instructions {
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-color: #F9FAFC;
  margin: 10px 15px 10px 15px ;
  border: 2px solid #8492A6;
  padding: 5px 20px 5px 20px;
  opacity: 0.8;	  
}
</style>
