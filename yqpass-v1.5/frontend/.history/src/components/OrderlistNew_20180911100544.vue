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
    <el-row>	
		<!-- <el-button type="primary" style="float:right;margin-bottom:10px;" size="mini" round @click.prevent="addRow(order_form)">新增表行</el-button> -->
		<el-button type="primary" style="float:right;margin-bottom:10px;" size="mini" round @click="dialogFormVisible = true">新增表行</el-button>  
			<el-dialog title="新增项目" :visible.sync="dialogFormVisible">
				<el-form :model="order_form_empty">
					<el-form-item label="业务系统" :label-width="formLabelWidth">
						<el-input placeholder="如南方基地信息支撑平台" v-model="order_form_empty.businessSystem"></el-input>
					</el-form-item>
					<el-row>
					<el-form-item label="A端设备移动维护部门" :label-width="formLabelWidth">
						<el-form-item label="部门名称">
							<el-input placeholder="如XX中心" v-model="order_form_empty.ACM_department" width="140"></el-input>
						</el-form-item>
						<el-input placeholder="移动负责人" v-model="order_form_empty.ACM_header" width="140"></el-input>
						<el-input placeholder="联系方式" v-model="order_form_empty.ACM_headerMobile" width="140"></el-input>
					</el-form-item>
					</el-row>
				</el-form>
			</el-dialog>	
  	</el-row>
  	<el-row>
  		<el-table :data="order_form" ref="table" tooltip-effect="dark" border stripe style="width:100%">
  			<el-table-column label="序号" type="index" width="60" align="center"></el-table-column>
  			<el-table-column label="业务系统" prop="businessSystem" align="center" width="240">
  				<template slot-scope="scope">
	  				<el-input placeholder="如南方基地信息支撑平台" v-show="scope.row.edit" v-model="scope.row.businessSystem"></el-input>
	  				<span v-show="!scope.row.edit">{{ scope.row.businessSystem }}</span>
  				</template>
  			</el-table-column>
  			<el-table-column label="A端设备移动维护部门" align="center">
  				<el-table-column label="部门名称" prop="ACM_department" width="140" align="center">
  					<template slot-scope="scope">
  						<el-input placeholder="如XX中心" v-show="scope.row.edit" v-model="scope.row.ACM_department"></el-input>
  						<span v-show="!scope.row.edit">{{ scope.row.ACM_department }}</span>
	  				</template>
  				</el-table-column>
  				<el-table-column label="移动负责人" prop="ACM_header" width="96" align="center">
  					<template slot-scope="scope">
  						<el-input v-show="scope.row.edit" v-model="scope.row.ACM_header"></el-input>
  						<span v-show="!scope.row.edit">{{ scope.row.ACM_header }}</span>
  					</template>	
  				</el-table-column>
  				<el-table-column label="联系方式" prop="ACM_headerMobile" width="140" align="center">
  					<template slot-scope="scope">
	  					<el-input v-show="scope.row.edit" v-model="scope.row.ACM_headerMobile"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.ACM_headerMobile }}</span>
  					</template>
  				</el-table-column>  				
  			</el-table-column>
  			<el-table-column label="A端设备维护合作单位" align="center">
  				<el-table-column label="单位名称" prop="ACP_department" width="140" align="center">
  					<template slot-scope="scope">
	  					<el-input placeholder="如XX公司" v-show="scope.row.edit" v-model="scope.row.ACP_department"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.ACP_department }}</span>
	  				</template>
  				</el-table-column>
  				<el-table-column label="负责人" prop="ACP_header" width="96" align="center">
  					<template slot-scope="scope">
  						<el-input v-show="scope.row.edit" v-model="scope.row.ACP_header"></el-input>
  						<span v-show="!scope.row.edit">{{ scope.row.ACP_header }}</span>
  					</template>
  				</el-table-column>
  				<el-table-column label="联系方式" prop="ACP_headerMobile" width="140" align="center">
  					<template slot-scope="scope">
	  					<el-input v-show="scope.row.edit" v-model="scope.row.ACP_headerMobile"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.ACP_headerMobile }}</span>
  					</template>
  				</el-table-column>
  			</el-table-column>
  			<el-table-column label="A端业务设备所在楼栋机房" align="center">
  				<el-table-column label="机楼" width="110" align="center">
  					<template slot-scope="scope">
  						<el-select v-show="scope.row.edit" v-model="scope.row.A_machineBuilding" placeholder="请选择机房" v-on:change="get_machineBuilding($event)">
  							<el-option v-for="item in machineBuilding_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
  						</el-select>
  						<span v-show="!scope.row.edit">{{ scope.row.A_machineBuilding }}</span>  						
  					</template>
  				</el-table-column>
  				<el-table-column label="机房" width="110" align="center">
  					<template slot-scope="scope">
  						<el-select v-show="scope.row.edit" v-model="scope.row.A_machineRoom" placeholder="请选择机房" v-on:change="get_machineRoom($event)">
  							<el-option v-for="item in machineRoom_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
  						</el-select>
  						<span v-show="!scope.row.edit">{{ scope.row.A_machineRoom }}</span>
	  				</template>	
  				</el-table-column>
  			</el-table-column>
  			<el-table-column label="A端业务设备位置（填写具体机架号）" prop="A_machineRack" width="150" align="center">
  				<template slot-scope="scope">
	  				<el-input placeholder="如A02架" v-show="scope.row.edit" v-model="scope.row.A_machineRack"></el-input>
	  				<span v-show="!scope.row.edit">{{ scope.row.A_machineRack }}</span>
  				</template>
  			</el-table-column>  			
  			<el-table-column label="A端业务设备/网元名称" prop="A_deviceName" width="240" align="center">
  				<template slot-scope="scope">
	  				<el-input placeholder="如S9303交换机或核心交换机" v-show="scope.row.edit" v-model="scope.row.A_deviceName"></el-input>
	  				<span v-show="!scope.row.edit">{{ scope.row.A_deviceName }}</span>
  				</template>
  			</el-table-column>
  			<el-table-column label="A端业务设备端口" prop="A_devicePort" width="240" align="center">
  				<template slot-scope="scope">
  					<el-input placeholder="如POS 1/1/0或交换机端口-1" v-show="scope.row.edit" v-model="scope.row.A_devicePort"></el-input>
  					<span v-show="!scope.row.edit">{{ scope.row.A_devicePort }}</span>
  				</template>
  			</el-table-column>
  			<el-table-column label="A端设备端口类型" width="110" align="center">
  				<template slot-scope="scope">
  					<el-select v-show="scope.row.edit" v-model="scope.row.A_portType" placeholder="请选择">
	  					<el-option v-for="item in portType_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
	  				</el-select>
	  				<span v-show="!scope.row.edit">{{ scope.row.A_portType }}</span>
  				</template>
  			</el-table-column>
  			<el-table-column label="Z端设备移动维护部门" align="center">
  				<el-table-column label="部门名称" prop="ZCM_department" width="140" align="center">
  					<template slot-scope="scope">
	  					<el-input placeholder="如XX中心" v-show="scope.row.edit" v-model="scope.row.ZCM_department"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.ZCM_department }}</span>
  					</template>
  				</el-table-column>
  				<el-table-column label="负责人" prop="ZCM_header" width="96" align="center">
  					<template slot-scope="scope">
	  					<el-input v-show="scope.row.edit" v-model="scope.row.ZCM_header"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.ZCM_header }}</span>
  					</template>
  				</el-table-column>
  				<el-table-column label="联系方式" prop="ZCM_headerMobile" width="140" align="center">
  					<template slot-scope="scope">
	  					<el-input v-show="scope.row.edit" v-model="scope.row.ZCM_headerMobile"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.ZCM_headerMobile }}</span>
  					</template>
  				</el-table-column>  				
  			</el-table-column>
  			<el-table-column label="Z端设备维护合作单位" align="center">
  				<el-table-column label="单位名称" prop="ZCP_department" width="140" align="center">
  					<template slot-scope="scope">
	  					<el-input placeholder="如XX公司" v-show="scope.row.edit" v-model="scope.row.ZCP_department"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.ZCP_department }}</span>
  					</template>
  				</el-table-column>
  				<el-table-column label="负责人" prop="ZCP_header" width="96" align="center">
  					<template slot-scope="scope">
	  					<el-input v-show="scope.row.edit" v-model="scope.row.ZCP_header"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.ZCP_header }}</span>
  					</template>
  				</el-table-column>
  				<el-table-column label="联系方式" prop="ZCP_headerMobile" width="140" align="center">
  					<template slot-scope="scope">
	  					<el-input v-show="scope.row.edit" v-model="scope.row.ZCP_headerMobile"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.ZCP_headerMobile }}</span>
  					</template>
  				</el-table-column>
  			</el-table-column>
  			<el-table-column label="Z端业务设备所在楼栋机房" align="center">
  				<el-table-column label="机楼" width="110" align="center">
  					<template slot-scope="scope">
  						<el-select v-show="scope.row.edit" v-model="scope.row.Z_machineBuilding" placeholder="请选择机房" v-on:change="get_machineBuilding($event)">
  							<el-option v-for="item in machineBuilding_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
  						</el-select>
  						<span v-show="!scope.row.edit">{{ scope.row.Z_machineBuilding }}</span>  						
  					</template>
  				</el-table-column>
  				<el-table-column label="机房" width="110" align="center">
  					<template slot-scope="scope">
  						<el-select v-show="scope.row.edit" v-model="scope.row.Z_machineRoom" placeholder="请选择机房" v-on:change="get_machineRoom($event)">
  							<el-option v-for="item in machineRoom_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
  						</el-select>
  						<span v-show="!scope.row.edit">{{ scope.row.Z_machineRoom }}</span>
	  				</template>	
  				</el-table-column>
  			</el-table-column>  			
  			<el-table-column label="Z端业务设备位置（填写具体机架号）" prop="Z_machineRack" width="150" align="center">
  				<template slot-scope="scope">
	  				<el-input placeholder="如A02架" v-show="scope.row.edit" v-model="scope.row.Z_machineRack"></el-input>
	  				<span v-show="!scope.row.edit">{{ scope.row.Z_machineRack }}</span>
  				</template>
  			</el-table-column> 
  			<el-table-column label="Z端业务设备/网元名称" prop="Z_deviceName" width="240" align="center">
  				<template slot-scope="scope">
	  				<el-input placeholder="如S9303交换机或核心交换机" v-show="scope.row.edit" v-model="scope.row.Z_deviceName"></el-input>
	  				<span v-show="!scope.row.edit">{{ scope.row.Z_deviceName }}</span>
  				</template>
  			</el-table-column>
  			<el-table-column label="Z端业务设备端口" prop="Z_devicePort" width="240" align="center">
  				<template slot-scope="scope">
  					<el-input placeholder="如POS 1/1/0或交换机端口-1" v-show="scope.row.edit" v-model="scope.row.Z_devicePort"></el-input>
  					<span v-show="!scope.row.edit">{{ scope.row.Z_devicePort }}</span>
  				</template>
  			</el-table-column>  			
  			<el-table-column label="Z端设备端口类型" width="110" align="center">
  				<template slot-scope="scope">
  					<el-select v-show="scope.row.edit" v-model="scope.row.Z_portType" placeholder="请选择">
	  					<el-option v-for="item in portType_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
	  				</el-select>
	  				<span v-show="!scope.row.edit">{{ scope.row.Z_portType }}</span>
  				</template>
  			</el-table-column>
  			<el-table-column label="需求带宽" width="110" align="center">
				<template slot-scope="scope">
					<el-select v-show="scope.row.edit" v-model="scope.row.bandwidth">
						<el-option v-for="item in bandwidth_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
	  				</el-select>
	  				<span v-show="!scope.row.edit">{{ scope.row.bandwidth }}</span>
	  			</template>
  			</el-table-column>
  			<el-table-column label="链路主备关系" width="110" align="center">
  				<template slot-scope="scope">
  					<el-select v-show="scope.row.edit" v-model="scope.row.linkRelations" placeholder="请选择">
	  					<el-option v-for="item in link_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
	  				</el-select>
	  				<span v-show="!scope.row.edit">{{ scope.row.linkRelations }}</span>
  				</template>
  			</el-table-column>
  			<el-table-column label="操作" align="center" width="100">
  				<template slot-scope="scope">
  					<el-button :type="scope.row.edit?'success':'primary'" @click='scope.row.edit=!scope.row.edit' circle size="mini" icon="el-icon-edit"></el-button>
  					<el-button type="danger" circle size="mini" @click="deleteRow(scope.$index, order_form)" icon="el-icon-delete"></el-button> 
  				</template>	
  			</el-table-column>			  			  			
  		</el-table>
  	</el-row>
  </el-row>
  <el-row class="footer">
  	<el-row>
  		<el-button type="primary" icon="el-icon-warning" @click="readIns">填单说明</el-button>
  		<el-button type="primary" icon="el-icon-success" @click="handleTable(order_form)">提交工单</el-button>
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
	  dialogFormVisible: false,
	  formLabelWidth: '150px',
      order_form: [],
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
      		value: '单模',
      		label: '单模'
      	},{
      		value: '多模',
      		label: '多模'
      	}],
      link_option: [{
      		value: '主用',
      		label: '主用'
      	},{
      		value: '备用',
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
	addRow (tableData, event) {		
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
      	linkRelations: '',
      	edit: true
  		}
  		tableData.push(list)
  		/* this.order_form.unshift(list)
  		this.lists.push(this.order_form);
  		this.order_form = Object.assign({}, this.order_form_empty); */
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
  	handleTable (order_form) {
  		console.log(order_form)
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
.container {

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
