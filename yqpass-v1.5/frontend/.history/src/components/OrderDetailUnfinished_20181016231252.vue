<template lang="html"> 
  <div>
    <el-row class="container">
    <el-row> 
          <el-col :span='12' class="button_nav">
            <el-button type="primary" icon="el-icon-arrow-left" size="mini" circle style='float: left;' @click="backToList"></el-button>
            <!-- <el-button type="primary" icon="el-icon-refresh" size="mini" circle style='float: left;'></el-button>            -->
          </el-col>
          <el-col :span='12' class="breadcrumb">
            <el-breadcrumb separator="/" style='float: right;'>
              <el-breadcrumb-item :to="{ path: '/0/orderUnfinished' }">待办工单</el-breadcrumb-item>
              <el-breadcrumb-item>工单详情</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>      
    </el-row>
  	<h3 style="font-size:20px;">中国移动南方基地园区内部单模光缆纤芯申请单</h3>
  	<el-row class="header">
  		<el-form ref="orderMain_form" :model="orderMain_form" label-width="80px">
  		<el-row style="margin-bottom:15px;">
  			<el-col :span="12" text-align="left">
  				<p v-model="sn" style="font-size:14px;float: left;font-weight:bold;">申请施工单号：{{ orderMain_form.sn }}</p>
  			</el-col>
  			<el-col :span="12" text-align="right">
  				<p style="font-size:14px;float: right;font-weight:bold;">申请时间：{{ orderMain_form.application_date }}</p>
  			</el-col>
  		</el-row>
  		<el-row>
  			<el-col :span="11">  			
	  			<el-form-item label="项目名称" label-width="80px" class="is-required">
	  				<el-input placeholder="请输入项目名称" v-model="orderMain_form.title"></el-input>
	  			</el-form-item>
  			</el-col>			
  			<el-col :span="11" :push="2">  			
	  			<el-form-item label="预计开通时间" label-width="100px">
	  			  <el-date-picker type="date" placeholder="选择开通日期" value-format="yyyy-MM-dd" v-model="orderMain_form.open_date" style="width:100%;" readonly=true></el-date-picker>	
	  			</el-form-item>
  			</el-col>
  		</el-row>
  		<el-row>
	  		<el-col :span="7">  			
		  		<el-form-item label="移动人员" label-width="80px" class="is-required">
		  			<el-input placeholder="请填写姓名" v-model="orderMain_form.person1"></el-input>
		  		</el-form-item>
	  		</el-col>
	  		<el-col :span="7" :offset="1">  			
		  		<el-form-item label="电话" label-width="80px" class="is-required">
		  			<el-input placeholder="请填写手机号" v-model="orderMain_form.phone1"></el-input>
		  		</el-form-item>
	  		</el-col>  
	  		<el-col :span="7" :offset="1">  			
		  		<el-form-item label="邮箱" label-width="80px" class="is-required">
		  			<el-input placeholder="请填写邮箱" v-model="orderMain_form.email1"></el-input>
		 			</el-form-item>
	  		</el-col>	
	  	</el-row>  			
		<el-row>			  			
	  		<el-col :span="7">  			
		  		<el-form-item label="配合人员" label-width="80px" class="is-required">
		  			<el-input placeholder="请填写姓名" v-model="orderMain_form.person2"></el-input>
				</el-form-item>
	  		</el-col>
	  		<el-col :span="7" :offset="1">  			
		  		<el-form-item label="电话" label-width="80px" class="is-required">
		  			<el-input placeholder="请填写手机号" v-model="orderMain_form.phone2"></el-input>
		  		</el-form-item>
	  		</el-col>  
	  		<el-col :span="7" :offset="1">  			
		  		<el-form-item label="邮箱" label-width="80px" class="is-required">
		  			<el-input placeholder="请填写邮箱" v-model="orderMain_form.email2"></el-input>
		  		</el-form-item>
	  		</el-col> 	  							
		  </el-row>
		  <!-- <el-row>
			<el-form-item :label="opinion">
				<el-input placeholder="请填写处理意见" v-model="orderMain_form.opinion" v-if="deal_view"></el-input> 
			</el-form-item>
    	  </el-row>  	 -->
		</el-form>
 	</el-row>
 	<el-row class="content">
    <el-row>	
		<!-- <el-button type="primary" style="float:right;margin-bottom:10px;" size="mini" round @click.prevent="addRow(order_form)">新增表行</el-button> -->
		<el-button type="primary" style="float:left;margin-bottom:10px;" size="mini" round @click="newDialogForm('data_dialogForm')">新增表行</el-button>  
		<el-dialog title="新增申请项目" :visible.sync="dialogFormVisible" width="66%" center class="dialog">
				<el-form :model=data_dialogForm class="dialogForm">
					<el-form-item label="业务系统" :label-width="formLabelWidth">
						<el-input placeholder="如南方基地信息支撑平台" v-model="data_dialogForm.bus_sys_name" clearable></el-input>
					</el-form-item>
					<el-row>
						<el-form-item label="A端设备移动维护部门" :label-width="formLabelWidth">
							<el-col :span="8">
								<el-input placeholder="如XX中心" v-model="data_dialogForm.department1_A" clearable></el-input>
							</el-col>
							<el-col :span="7" :push="1">
								<el-input placeholder="部门负责人" v-model="data_dialogForm.person1_A" clearable></el-input>
							</el-col>
							<el-col :span="7" :push="2">
								<el-input placeholder="联系方式" v-model="data_dialogForm.phone1_A" clearable></el-input>
							</el-col>
						</el-form-item>
					</el-row>
					<el-row>
						<el-form-item label="A端设备维护合作单位" :label-width="formLabelWidth">
							<el-col :span="8">
								<el-input placeholder="如XX公司" v-model="data_dialogForm.department2_A" clearable></el-input>
							</el-col>
							<el-col :span="7" :push="1">
								<el-input placeholder="公司负责人" v-model="data_dialogForm.person2_A" clearable></el-input>
							</el-col>
							<el-col :span="7" :push="2">
								<el-input placeholder="联系方式" v-model="data_dialogForm.phone2_A" clearable></el-input>
							</el-col>
						</el-form-item>
					</el-row>
					<el-row>
						<el-col :span="8">
							<el-form-item label="A端业务设备楼栋" :label-width="formLabelWidth">							
								<el-select v-model="data_dialogForm.A_machineBuilding" placeholder="请选择" v-on:change="get_machineBuilding($event)">
									<el-option v-for="item in machineBuilding_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
								</el-select>
							</el-form-item>
						</el-col>
						<el-col :span="8" :push="2">
							<el-form-item label="机房号" label-width="120px">
								<el-select v-model="data_dialogForm.A_machineRoom" placeholder="请选择" v-on:change="get_machineRoom($event)">
									<el-option v-for="item in machineRoom_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
								</el-select>
							</el-form-item>
						</el-col>							
					</el-row>
					<el-row>
						<el-form-item label="A端业务设备位置" :label-width="formLabelWidth">
							<el-input v-model="data_dialogForm.rack_num_A" placeholder="填写具体机架号：如A02架" clearable></el-input>
						</el-form-item>
					</el-row>
					<el-row>
						<el-form-item label="A端业务设备网元名称" :label-width="formLabelWidth">
							<el-input v-model="data_dialogForm.device_name_A" placeholder="如S9303交换机或核心交换机" clearable></el-input>
						</el-form-item>	
					</el-row>
					<el-row>
						<el-col :span="14">
							<el-form-item label="A端业务设备端口" :label-width="formLabelWidth">
								<el-input v-model="data_dialogForm.port_name_A" placeholder="如POS 1/1/0或交换机端口-1" clearable></el-input>
							</el-form-item>	
						</el-col>
						<el-col :span="8" :push="1">
							<el-form-item label="端口类型" label-width="120px">
									<el-select  v-model="data_dialogForm.port_type_A" placeholder="请选择">
										<el-option v-for="item in portType_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
									</el-select>
							</el-form-item>	
						</el-col>
					</el-row>
					<div style="margin-bottom:10px;padding-top:10px;padding-left:5px;background-color:#ccffff">
						<el-row>
							<el-col :span="4">
								<el-form-item :label-width="formLabelWidth" label="路由申请">
									<el-button @click="addCable">新增</el-button>
								</el-form-item>
							</el-col>
						</el-row>
						<el-row>
							<el-form-item :label-width="formLabelWidth" v-for="(cable, index) in data_dialogForm.cables" :label="'传输系统（待分配）' + (index+1)" :key="cable.key" :prop="'cables.' + index + '.value'">
								<el-col :span="18"><el-input v-model="cable.value"></el-input></el-col>
								<el-col :span="4"><el-button @click.prevent="removeCable(cable)">删除</el-button></el-col>
							</el-form-item>
						</el-row>
					</div>
					<el-row>
						<el-col :span="14">
							<el-form-item label="Z端业务设备端口" :label-width="formLabelWidth">
								<el-input v-model="data_dialogForm.port_name_Z" placeholder="如POS 1/1/0或交换机端口-1" clearable></el-input>
							</el-form-item>	
						</el-col>
						<el-col :span="8" :push="1">
							<el-form-item label="端口类型" label-width="120px">
									<el-select  v-model="data_dialogForm.port_type_Z" placeholder="请选择">
										<el-option v-for="item in portType_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
									</el-select>
							</el-form-item>	
						</el-col>
					</el-row>
					<el-row>
						<el-form-item label="Z端业务设备网元名称" :label-width="formLabelWidth">
							<el-input v-model="data_dialogForm.device_name_Z" placeholder="如S9303交换机或核心交换机" clearable></el-input>
						</el-form-item>	
					</el-row>
					<el-row>
						<el-form-item label="Z端业务设备位置" :label-width="formLabelWidth">
							<el-input v-model="data_dialogForm.rack_num_Z" placeholder="填写具体机架号：如A02架" clearable></el-input>
						</el-form-item>
					</el-row>
					<el-row>
						<el-col :span="8">
							<el-form-item label="Z端业务设备楼栋" :label-width="formLabelWidth">
								<el-select v-model="data_dialogForm.Z_machineBuilding" placeholder="请选择" v-on:change="get_machineBuilding($event)">
									<el-option v-for="item in machineBuilding_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
								</el-select>
							</el-form-item>
						</el-col>
						<el-col :span="8" :push="2">
							<el-form-item label="机房号" label-width="120px">
								<el-select v-model="data_dialogForm.Z_machineRoom" placeholder="请选择" v-on:change="get_machineRoom($event)">
									<el-option v-for="item in machineRoom_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
								</el-select>
							</el-form-item>
						</el-col>
					</el-row>
					<el-row>
						<el-form-item label="Z端设备维护合作单位" :label-width="formLabelWidth">
							<el-col :span="8">
								<el-input placeholder="如XX公司" v-model="data_dialogForm.department2_Z" clearable></el-input>
							</el-col>
							<el-col :span="7" :push="1">
								<el-input placeholder="公司负责人" v-model="data_dialogForm.person2_Z" clearable></el-input>
							</el-col>
							<el-col :span="7" :push="2">
								<el-input placeholder="联系方式" v-model="data_dialogForm.phone2_Z" clearable></el-input>
							</el-col>
						</el-form-item>
					</el-row>
					<el-row>
						<el-form-item label="Z端设备移动维护部门" :label-width="formLabelWidth">
							<el-col :span="8">
								<el-input placeholder="如XX中心" v-model="data_dialogForm.department1_Z" clearable></el-input>
							</el-col>
							<el-col :span="7" :push="1">
								<el-input placeholder="部门负责人" v-model="data_dialogForm.person1_Z" clearable></el-input>
							</el-col>
							<el-col :span="7" :push="2">
								<el-input placeholder="联系方式" v-model="data_dialogForm.phone1_Z" clearable></el-input>
							</el-col>
						</el-form-item>
					</el-row>	
					<el-row>
						<el-col :span="8">
							<el-form-item label="需求带宽" :label-width="formLabelWidth">
									<el-select  v-model="data_dialogForm.bandwidth" placeholder="请选择">
										<el-option v-for="item in bandwidth_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
									</el-select>
							</el-form-item>	
						</el-col>
						<el-col :span="8" :push="2">
							<el-form-item label="链路主备关系" label-width="120px">
									<el-select  v-model="data_dialogForm.main_or_spare" placeholder="请选择">
										<el-option v-for="item in link_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
									</el-select>
							</el-form-item>	
						</el-col>
					</el-row>
					<el-row>
						<el-form-item label="备注" :label-width="formLabelWidth">
							<el-input placeholder="填写备注信息" v-model="data_dialogForm.notes" clearable></el-input>
						</el-form-item>
					</el-row>
				</el-form>
				<div slot="footer" class="dialog-footer">					
					<el-button @click="resetDialogForm('data_dialogForm')">取消</el-button>
					<el-button type="primary" @click="submitDialogForm('data_dialogForm')">确定</el-button>
				</div>
			</el-dialog>	
  	</el-row>
  	<el-row>
  		<el-table :data="order_form" ref="table" tooltip-effect="dark" border stripe style="width:100%">
  			<el-table-column label="序号" type="index" width="60" align="center"></el-table-column>
  			<el-table-column label="业务系统" prop="bus_sys_name" align="center" width="240">
  				<template slot-scope="scope">
	  				<el-input placeholder="如南方基地信息支撑平台" v-show="scope.row.edit" v-model="scope.row.bus_sys_name"></el-input>
	  				<span v-show="!scope.row.edit">{{ scope.row.bus_sys_name }}</span>
  				</template>
  			</el-table-column>
  			<el-table-column label="A端设备移动维护部门" align="center">
  				<el-table-column label="部门名称" prop="department1_A" width="140" align="center">
  					<template slot-scope="scope">
  						<el-input placeholder="如XX中心" v-show="scope.row.edit" v-model="scope.row.department1_A"></el-input>
  						<span v-show="!scope.row.edit">{{ scope.row.department1_A }}</span>
	  				</template>
  				</el-table-column>
  				<el-table-column label="负责人" prop="person1_A" width="96" align="center">
  					<template slot-scope="scope">
  						<el-input v-show="scope.row.edit" v-model="scope.row.person1_A"></el-input>
  						<span v-show="!scope.row.edit">{{ scope.row.person1_A }}</span>
  					</template>	
  				</el-table-column>
  				<el-table-column label="联系方式" prop="phone1_A" width="140" align="center">
  					<template slot-scope="scope">
	  					<el-input v-show="scope.row.edit" v-model="scope.row.phone1_A"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.phone1_A }}</span>
  					</template>
  				</el-table-column>  				
  			</el-table-column>
  			<el-table-column label="A端设备维护合作单位" align="center">
  				<el-table-column label="单位名称" prop="department2_A" width="140" align="center">
  					<template slot-scope="scope">
	  					<el-input placeholder="如XX公司" v-show="scope.row.edit" v-model="scope.row.department2_A"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.department2_A }}</span>
	  				</template>
  				</el-table-column>
  				<el-table-column label="负责人" prop="person2_A" width="96" align="center">
  					<template slot-scope="scope">
  						<el-input v-show="scope.row.edit" v-model="scope.row.person2_A"></el-input>
  						<span v-show="!scope.row.edit">{{ scope.row.person2_A }}</span>
  					</template>
  				</el-table-column>
  				<el-table-column label="联系方式" prop="phone2_A" width="140" align="center">
  					<template slot-scope="scope">
	  					<el-input v-show="scope.row.edit" v-model="scope.row.phone2_A"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.phone2_A }}</span>
  					</template>
  				</el-table-column>
  			</el-table-column>
			<el-table-column label="A端业务设备位置" align="center">
				<el-table-column label="机楼" width="110" align="center">
					<template slot-scope="scope">
						<el-select v-show="scope.row.edit" v-model="scope.row.A_machineBuilding" placeholder="请选择机楼" v-on:change="get_machineBuilding($event)">
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
				<el-table-column label="机架号" prop="rack_num_A" width="150" align="center">
					<template slot-scope="scope">
						<el-input placeholder="如A02架" v-show="scope.row.edit" v-model="scope.row.rack_num_A"></el-input>
						<span v-show="!scope.row.edit">{{ scope.row.rack_num_A }}</span>
					</template>
				</el-table-column>
			</el-table-column>  
			<el-table-column label="A端业务设备" align="center">  			
				<el-table-column label="网元名称" prop="device_name_A" width="240" align="center">
					<template slot-scope="scope">
						<el-input placeholder="如S9303交换机或核心交换机" v-show="scope.row.edit" v-model="scope.row.device_name_A"></el-input>
						<span v-show="!scope.row.edit">{{ scope.row.device_name_A }}</span>
					</template>
				</el-table-column>
				<el-table-column label="设备端口" prop="port_name_A" width="240" align="center">
					<template slot-scope="scope">
						<el-input placeholder="如POS 1/1/0或交换机端口-1" v-show="scope.row.edit" v-model="scope.row.port_name_A"></el-input>
						<span v-show="!scope.row.edit">{{ scope.row.port_name_A }}</span>
					</template>
				</el-table-column>
				<el-table-column label="端口类型" width="110" align="center">
					<template slot-scope="scope">
						<el-select v-show="scope.row.edit" v-model="scope.row.port_type_A" placeholder="请选择">
							<el-option v-for="item in portType_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
						</el-select>
						<span v-show="!scope.row.edit">{{ scope.row.port_type_A }}</span>
					</template>
				</el-table-column>
			</el-table-column>
			<el-table-column label="传输光缆段申请" prop="cable_list" width="600" align="center">
				<template slot-scope="scope">
					<el-input v-show="scope.row.edit" v-model="scope.row.cable_list"></el-input>
					<span v-show="!scope.row.edit">{{ scope.row.cable_list }}</span>
				</template>
			</el-table-column>
			<el-table-column label="Z端业务设备" align="center">
				<el-table-column label="端口类型" width="110" align="center">
					<template slot-scope="scope">
						<el-select v-show="scope.row.edit" v-model="scope.row.port_type_Z" placeholder="请选择">
							<el-option v-for="item in portType_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
						</el-select>
						<span v-show="!scope.row.edit">{{ scope.row.port_type_Z }}</span>
					</template>
				</el-table-column>   
				<el-table-column label="设备端口" prop="port_name_Z" width="240" align="center">
					<template slot-scope="scope">
						<el-input placeholder="如POS 1/1/0或交换机端口-1" v-show="scope.row.edit" v-model="scope.row.port_name_Z"></el-input>
						<span v-show="!scope.row.edit">{{ scope.row.port_name_Z }}</span>
					</template>
				</el-table-column>  
				<el-table-column label="网元名称" prop="device_name_Z" width="240" align="center">
					<template slot-scope="scope">
						<el-input placeholder="如S9303交换机或核心交换机" v-show="scope.row.edit" v-model="scope.row.device_name_Z"></el-input>
						<span v-show="!scope.row.edit">{{ scope.row.device_name_Z }}</span>
					</template>
				</el-table-column>							
			</el-table-column>
			<el-table-column label="Z端业务设备位置" align="center">
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
				<el-table-column label="机架号" prop="rack_num_Z" width="150" align="center">
					<template slot-scope="scope">
						<el-input placeholder="如A02架" v-show="scope.row.edit" v-model="scope.row.rack_num_Z"></el-input>
						<span v-show="!scope.row.edit">{{ scope.row.rack_num_Z }}</span>
					</template>
				</el-table-column>  
			</el-table-column>  
  			<el-table-column label="Z端设备维护合作单位" align="center">
  				<el-table-column label="单位名称" prop="department2_Z" width="140" align="center">
  					<template slot-scope="scope">
	  					<el-input placeholder="如XX公司" v-show="scope.row.edit" v-model="scope.row.department2_Z"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.department2_Z }}</span>
  					</template>
  				</el-table-column>
  				<el-table-column label="负责人" prop="person2_Z" width="96" align="center">
  					<template slot-scope="scope">
	  					<el-input v-show="scope.row.edit" v-model="scope.row.person2_Z"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.person2_Z }}</span>
  					</template>
  				</el-table-column>
  				<el-table-column label="联系方式" prop="phone2_Z" width="140" align="center">
  					<template slot-scope="scope">
	  					<el-input v-show="scope.row.edit" v-model="scope.row.phone2_Z"></el-input>
	  					<span v-show="!scope.row.edit">{{ scope.row.phone2_Z }}</span>
  					</template>
  				</el-table-column>
			</el-table-column>
			<el-table-column label="Z端设备移动维护部门" align="center">
				<el-table-column label="部门名称" prop="department1_Z" width="140" align="center">
					<template slot-scope="scope">
						<el-input placeholder="如XX中心" v-show="scope.row.edit" v-model="scope.row.department1_Z"></el-input>
						<span v-show="!scope.row.edit">{{ scope.row.department1_Z }}</span>
					</template>
				</el-table-column>
				<el-table-column label="负责人" prop="person1_Z" width="96" align="center">
					<template slot-scope="scope">
						<el-input v-show="scope.row.edit" v-model="scope.row.person1_Z"></el-input>
						<span v-show="!scope.row.edit">{{ scope.row.person1_Z }}</span>
					</template>
				</el-table-column>
				<el-table-column label="联系方式" prop="phone1_Z" width="140" align="center">
					<template slot-scope="scope">
						<el-input v-show="scope.row.edit" v-model="scope.row.phone1_Z"></el-input>
						<span v-show="!scope.row.edit">{{ scope.row.phone1_Z }}</span>
					</template>
				</el-table-column>  				
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
  					<el-select v-show="scope.row.edit" v-model="scope.row.main_or_spare" placeholder="请选择">
	  					<el-option v-for="item in link_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
	  				</el-select>
	  				<span v-show="!scope.row.edit">{{ scope.row.main_or_spare }}</span>
  				</template>
			</el-table-column>
			<el-table-column label="备注" prop="notes" width="200" align="center">
				<template slot-scope="scope">
					<el-input v-show="scope.row.edit" v-model="scope.row.notes"></el-input>
					<span v-show="!scope.row.edit">{{ scope.row.notes }}</span>
				</template>
			</el-table-column>  
  			<el-table-column label="操作" align="center" width="100" fixed="right">
  				<template slot-scope="scope">
  					<el-button :type="scope.row.edit?'success':'primary'" @click='editDialogForm(scope.$index, order_form)' circle size="mini" icon="el-icon-edit"></el-button>
  					<el-button type="danger" circle size="mini" @click="deleteRow(scope.$index, order_form)" icon="el-icon-delete"></el-button> 
  				</template>	
  			</el-table-column>			  			  			
		</el-table>
  	</el-row>
  </el-row>
  <el-row class="opinion_view" v-if="deal_view">
	<el-form ref="orderMain_form" :model="orderMain_form" label-width="80px">
		<el-form-item :label="opinion">
			<el-input placeholder="请填写处理意见" v-model="orderMain_form.opinion"></el-input> 
		</el-form-item>
	</el-form>
  </el-row>  	
  <el-row class="footer">
  	<el-row>
  		<el-button type="warning" icon="el-icon-warning" @click="readIns">工单流转记录</el-button>
		<el-button type="primary" icon="el-icon-success" v-for="(value, key) in button_list" :key="key" @click="handleData(value.transition_id)">{{ value.transition_name }}</el-button>
	</el-row>
	<el-row class="transfer_record" v-if="ins_seen">
		<el-steps :active="active" align-center finish-status="success" style="margin-top:10px;margin-bottom: 10px;">
			<el-step title="新建工单"></el-step>
			<el-step title="保存工单"></el-step>
			<el-step title="接口人审核"></el-step>
			<el-step title="脚本执行"></el-step>
			<el-step title="厂家调度执行"></el-step>
			<el-step title="需求方确认"></el-step>
			<el-step title="关闭工单"></el-step>
		</el-steps>
		<el-collapse v-model="activeNames" @change="handleChange">
			<el-collapse-item v-for="(value, key) in flowLogs" :key="key" :name="key">
				<template slot="title">
					<div>{{key+1}}、工单状态：<b>{{ value.state }}</b>&nbsp;————&nbsp;处理结果：<b>{{value.transition}}</b></div>
				</template>
				<div>工单状态：<b>{{value.state}}</b>，处理人：<b>{{value.participant}}</b>，处理结果：<b>{{value.transition}}</b>，处理意见：<b>{{value.suggestion}}</b>， 处理时间：<b>{{value.gmt_modified}}</b></div>
			</el-collapse-item>
		</el-collapse>
	</el-row>
  	<el-row class="instructions" style="text-align:left">
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
import { postTicketList,getWorkflowInitState,getTicketDetail,dealTicket,getTicketFlowlogs,getTicketFlowsteps,getBuildingRoomList } from '../api/api'
export default {
  data () {
    return {
	  applyDate: new Date().getTime(),
	  data_dialogForm: '',
      orderMain_form: [{
		sn: '',
		application_date: '',
      	title: '',
      	open_date: '',
      	person1: '',
      	phone1: '',
      	email1: '',
      	person2: '',
      	phone2: '',
		email2: '',
		opinion: ''
	  }],
	  deal_view: false,
	  opinion: '',
	  dialogFormVisible: false,
	  dialogFormIndexId: '',
	  formLabelWidth: '150px',
	  button_list: [],
	  flowLogs: [],
	  activeNames: '0',
	  order_form: [],
	//   nextId: 1,
      order_form_empty: {      	
      	bus_sys_name: '',
      	department1_A: '',
      	person1_A: '',
      	phone1_A: '',
      	department2_A: '',
      	person2_A: '',
      	phone2_A: '',
      	A_machineBuilding: '',
      	A_machineRoom: '',
      	rack_num_A: '',
      	device_name_A: '',
      	port_name_A: '',
		port_type_A: '',
		cables: [{
			value: ''
		}],   
      	department1_Z: '',
      	person1_Z: '',
      	phone1_Z: '',
      	department2_Z: '',
      	person2_Z: '',
      	phone2_Z: '',
      	Z_machineBuilding: '',
      	Z_machineRoom: '',
      	rack_num_Z: '',
      	device_name_Z: '',
      	port_name_Z: '',
      	port_type_Z:'',
      	bandwidth: '',
		main_or_spare: '',
		notes: ''
      },
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
		  value: '3.1',
		  label: '3.1'
	  },{
		  value: '2.3',
		  label: '2.3'
	  },{
		  value: '2.2',
		  label: '2.2'
	  },{
		  value: '1.3',
		  label: '1.3'
	  },{
		  value: '1.2',
		  label: '1.2'
	  },{
		  value: '1.1',
		  label: '1.1'
	  },{
		  value: '2.1',
		  label: '2.1'
	  },{
		  value: '6.1',
		  label: '6.1'
	  },{
		  value: '6.2',
		  label: '6.2'
	  },{
		  value: '4.1',
		  label: '4.1'
	  },{
		  value: '4.2',
		  label: '4.2'
	  },{
		  value: '4.3',
		  label: '4.3'
	  },{
		  value: '4.4.1',
		  label: '4.4.1'
	  },{
		  value: '4.4.2',
		  label: '4.4.2'
	  },{
		  value: '4.4.3',
		  label: '4.4.3'
	  },{
		  value: '4.5.1',
		  label: '4.5.1'
	  },{
		  value: '4.5.2',
		  label: '4.5.2'
	  },{
		  value: '4.5.3',
		  label: '4.5.3'
	  },{
		  value: '4.5.4',
		  label: '4.5.4'
	  },{
		  value: '园内',
		  label: '园内'
	  },{
		  value: '出局',
		  label: '出局'
	  }],  	
      machineRoom_option: [],
	  allRoom: [],
      selectlistRow: [],
	  active: 0,
      ins_seen: false
    }
  },
  methods: {
	get_buildingData () {
		this.allRoom = [];
		for (var i=1; i<12; i++) {
			let paramsData = {};
			paramsData["page"] = i;
			getBuildingRoomList({params : paramsData}).then((response)=> {
				console.log(response);
				if (response.data.code = 1) {
					let list = response.data.data.value;
					// console.log(list)
					for (var i=0; i<list.length; i++) {
						this.allRoom.push({
							id: list[i].id,
							building: list[i].building,
							label: list[i].room
						});	
					}
				} else {
					console.log("no data")
				}
			});
		}
	},
	et_machineBuilding: function (building) {
		let room_list = this.allRoom;
		setTimeout(console.log(room_list.length), 2000);
		// console.log(room_list.length);
		let temRoom = [];
		for (var i=0; i<room_list.length; i++) {
			// console.log(room_list[i]);
			if (building == room_list[i].building){
  				temRoom.push({label: room_list[i].label, value: room_list[i].id})
  			}
		};
  		console.log(temRoom)
  		this.machineRoom_option = temRoom;
	},
	newDialogForm(formName) {
		this.dialogFormVisible = true;
		this.data_dialogForm = this.order_form_empty;
	},
	addCable () {
		if (this.data_dialogForm == this.order_form_empty) {
			this.data_dialogForm.cables.push({
				value: ''
			});
		} else {
			let indexId = this.dialogFormIndexId;
			console.log(this.data_dialogForm);
			console.log(this.order_form[indexId].cables)
			this.data_dialogForm.cables.push({
				value: ''
			});
		}
	},
	removeCable(item) {
		var index = this.data_dialogForm.cables.indexOf(item)
        if (index !== -1) {
          this.data_dialogForm.cables.splice(index, 1)
        }
	}, 
	submitDialogForm(formName) {
		this.dialogFormVisible = false;
		if (this.data_dialogForm == this.order_form_empty) {
			var cable_data = '';
			for (var i=0; i<this.order_form_empty.cables.length; i++) {
				let data = JSON.parse(JSON.stringify(this.order_form_empty.cables[i]))
				cable_data += i === this.order_form_empty.cables.length - 1?data.value:data.value+"——"
			};
			console.log(cable_data);
			this.order_form.push({
				// field_num:this.nextId++,
				bus_sys_name:this.order_form_empty.bus_sys_name,
				department1_A:this.order_form_empty.department1_A,
				person1_A:this.order_form_empty.person1_A,
				phone1_A:this.order_form_empty.phone1_A,
				department2_A:this.order_form_empty.department2_A,
				person2_A:this.order_form_empty.person2_A,
				phone2_A:this.order_form_empty.phone2_A,
				A_machineBuilding:this.order_form_empty.A_machineBuilding,
				A_machineRoom:this.order_form_empty.A_machineRoom,
				rack_num_A:this.order_form_empty.rack_num_A,
				device_name_A:this.order_form_empty.device_name_A,
				port_name_A:this.order_form_empty.port_name_A,
				port_type_A:this.order_form_empty.port_type_A,
				cable_list:cable_data,
				department1_Z:this.order_form_empty.department1_Z,
				person1_Z:this.order_form_empty.person1_Z,
				phone1_Z:this.order_form_empty.phone1_Z,
				department2_Z:this.order_form_empty.department2_Z,
				person2_Z:this.order_form_empty.person2_Z,
				phone2_Z:this.order_form_empty.phone2_Z,
				Z_machineBuilding:this.order_form_empty.Z_machineBuilding,
				Z_machineRoom:this.order_form_empty.Z_machineRoom,
				rack_num_Z:this.order_form_empty.rack_num_Z,
				device_name_Z:this.order_form_empty.device_name_Z,
				port_name_Z:this.order_form_empty.port_name_Z,
				port_type_Z:this.order_form_empty.port_type_Z,
				bandwidth:this.order_form_empty.bandwidth,
				main_or_spare:this.order_form_empty.main_or_spare,
				notes: '',
				edit:false
			});
			console.log(this.order_form)
			this.order_form_empty = {
				bus_sys_name: '',
				department1_A: '',
				person1_A: '',
				phone1_A: '',
				department2_A: '',
				person2_A: '',
				phone2_A: '',
				A_machineBuilding: '',
				A_machineRoom: '',
				rack_num_A: '',
				device_name_A: '',
				port_name_A: '',
				port_type_A: '',
				cables: [{
					value: ''
				}], 
				department1_Z: '',
				person1_Z: '',
				phone1_Z: '',
				department2_Z: '',
				person2_Z: '',
				phone2_Z: '',
				Z_machineBuilding: '',
				Z_machineRoom: '',
				rack_num_Z: '',
				device_name_Z: '',
				port_name_Z: '',
				port_type_Z:'',
				bandwidth: '',
				main_or_spare: '',
				notes: ''
			};
		} else {
			let indexId = this.dialogFormIndexId;
			var cable_data = '';
			for (var i=0; i<this.order_form[indexId].cables.length; i++) {
				let data = JSON.parse(JSON.stringify(this.order_form[indexId].cables[i]))
				cable_data += i === this.order_form[indexId].cables.length - 1?data.value:data.value+"——"
			};
			this.order_form[indexId].cable_list = cable_data;
			console.log(this.data_dialogForm);
			this.order_form[indexId] =this.data_dialogForm;
		}
	},
	resetDialogForm(formName) {
		this.dialogFormVisible = false;
		// this.$refs[formName].resetFields();
	}, 
	backToList () {
		this.$router.push('/0/orderUnfinished')
	}, 
	selectRow (val) {
  		this.selectlistRow = val
	},
	editDialogForm (index, rows) {
		this.dialogFormIndexId = index;
		console.log(this.order_form[index]);
		this.dialogFormVisible = true;
		// var array = this.order_form[index].cable_list.split("——");
		// console.log(array);
		var list = [];
		// for (var i=0; i<array.length; i++) {
		// 	let data = array[i]
		// 	list.push({value: array[i]})
		// 	console.log(list)
		// };
		// this.order_form[index].cables = list;
		this.data_dialogForm = this.order_form[index];
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
	getOrderDetail (id) {
		getTicketFlowsteps(id).then((response)=> {	
			// console.log(response);		
			if (response.data.code == 1) {
				var list = response.data.data.value;
				// console.log(list);
				for (var i=0; i<list.length; i++) {
					// console.log(list[i])
					if (list[i].is_deal == true) {
						this.active++;
					}
				}
			}
		});
		getTicketDetail(id).then((response)=> {
			console.log(response);
			if (response.data.code == 1) {
				this.button_list = response.data.data.transition;
				// console.log(this.button_list);
				var tableList = response.data.data.field_list;
				let list = [{}];
				for (var i=0; i<tableList.length; i++) {
					list[tableList[i].field_key] = tableList[i].field_value;
				};
				let list_detail = JSON.parse(list.application_detail);
				for (var i=0; i<list_detail.length; i++) {
					// console.log(list_detail)
					this.order_form.push(list_detail[i]);
				};
				console.log(this.order_form);
				this.orderMain_form = list;
				this.orderMain_form.title = response.data.data.title;
				this.orderMain_form.application_date = response.data.data.application_date;
				this.orderMain_form.sn = response.data.data.sn;
			}else{
				return response[msg]
			}
		})
	},
	handleData (key) {
		console.log(key);
		let id = this.$route.query.id;
		var that = this;
		let json = {};
		json["sn"] = that.orderMain_form.sn;
		json["title"] = that.orderMain_form.title;
		json["application_date"] = that.orderMain_form.application_date;
		json["open_date"] = that.orderMain_form.open_date;
		json["person1"] = that.orderMain_form.person1;
		json["phone1"] = that.orderMain_form.phone1;
		json["email1"] = that.orderMain_form.email1;
		json["person2"] = that.orderMain_form.person2;
		json["phone2"] = that.orderMain_form.phone2;
		json["email2"] = that.orderMain_form.phone2;
		json["application_detail"] = that.order_form;
		if (that.deal_view == false) {
			that.deal_view = true;
			switch (key)
			{
				case 3:
					that.opinion = "提交工单";
					break;
				
				case 4:
					that.opinion = "退回工单";
					break;
				
				case 5:
					that.opinion = "通过工单";
					break;	

				case 7:
					that.opinion = "调度完成";
					break;

				case 8:
					that.opinion = "调度失败";
					break;

				case 9:
					that.opinion = "关闭工单";
					break;

				case 10:
					that.opinion = "作废工单";
					break;
			}
		}else{
			if (key == 3) {
				json["transition_id"] = key;	
				json["suggestion"] = that.orderMain_form.opinion;		
				var parmas = JSON.stringify(json);
				console.log(parmas);
				dealTicket(id,parmas).then((response)=> {
					console.log(response);
					if (response.data.code == 1) {
						this.$router.push('/0/orderUnfinished')
						this.$notify({
							title: '提示',
							message: '提交工单成功',
							type:"success",
							duration: 1500
						});
					}
				})
			};
			if (key == 4) {
				json["transition_id"] = key;
				json["suggestion"] = that.orderMain_form.opinion;
				var parmas = JSON.stringify(json);
				console.log(parmas);
				dealTicket(id,parmas).then((response)=> {
					console.log(response);
					if (response.data.code == 1) {
						this.$router.push('/0/orderUnfinished')
						this.$notify({
							title: '提示',
							message: '退回工单成功',
							type:"success",
							duration: 1500
						});
					}
				})
			};
			if (key == 5) {
				json["transition_id"] = key;
				json["suggestion"] = that.orderMain_form.opinion;
				var parmas = JSON.stringify(json);
				console.log(parmas);
				dealTicket(id,parmas).then((response)=> {
					console.log(response);
					if (response.data.code == 1) {
						this.$router.push('/0/orderUnfinished')
						this.$notify({
							title: '提示',
							message: '审批通过成功',
							type:"success",
							duration: 1500
						});
					}
				})
			};
			if (key == 7) {
				json["transition_id"] = key;
				json["suggestion"] = that.orderMain_form.opinion;
				var parmas = JSON.stringify(json);
				console.log(parmas);
				dealTicket(id,parmas).then((response)=> {
					console.log(response);
					if (response.data.code == 1) {
						this.$router.push('/0/orderUnfinished')
						this.$notify({
							title: '提示',
							message: '调度分配完成',
							type:"success",
							duration: 1500
						});
					}
				})
			};
			if (key == 8) {
				json["transition_id"] = key;
				json["suggestion"] = that.orderMain_form.opinion;
				var parmas = JSON.stringify(json);
				console.log(parmas);
				dealTicket(id,parmas).then((response)=> {
					console.log(response);
					if (response.data.code == 1) {
						this.$router.push('/0/orderUnfinished')
						this.$notify({
							title: '提示',
							message: '调度失败回退',
							type:"success",
							duration: 1500
						});
					}
				})
			};		
			if (key == 9) {
				json["transition_id"] = key;
				json["suggestion"] = that.orderMain_form.opinion;
				var parmas = JSON.stringify(json);
				console.log(parmas);
				dealTicket(id,parmas).then((response)=> {
					console.log(response);
					if (response.data.code == 1) {
						this.$router.push('/0/orderUnfinished')
						this.$notify({
							title: '提示',
							message: '关单成功',
							type:"success",
							duration: 1500
						});
					}
				})
			};				
			if (key == 10) {
				json["transition_id"] = key;
				json["suggestion"] = that.orderMain_form.opinion;
				var parmas = JSON.stringify(json);
				console.log(parmas);
				dealTicket(id,parmas).then((response)=> {
					console.log(response);
					if (response.data.code == 1) {
						this.$router.push('/0/orderUnfinished')
						this.$notify({
							title: '提示',
							message: '作废工单成功',
							type:"success",
							duration: 1500
						});
					}
				})
			};
		}	
	},  
  	handleTable (order_form) {
		console.log(this.order_form);
		var that = this;
		let json = {};
		json["workflow_id"] = 1;
		json["title"] = that.orderMain_form.title;
		json["person1"] = that.orderMain_form.person1;
		json["phone1"] = that.orderMain_form.phone1;
		json["email1"] = that.orderMain_form.email1;
		json["person2"] = that.orderMain_form.person2;
		json["phone2"] = that.orderMain_form.phone2;
		json["email2"] = that.orderMain_form.phone2;
		json["application_detail"] = that.order_form;
		var parmas = JSON.stringify(json);
		postTicketList(parmas).then((response)=> {
			console.log(response);
			if (response.data.code == 1) {
				this.$notify({
					title: '提示',
					message: '提交工单成功',
					type:"success",
					duration: 1500
				});
			}
		})
  	},
  	readIns () {
  		if (this.$data.ins_seen == false){
  			this.$data.ins_seen = true;
  			let paramsData = {};
			paramsData["per_page"] = 20;
			getTicketFlowlogs(this.$route.query.id, {params : paramsData}).then((response)=> {
				console.log(response)
				if (response.data.code == 1) {
					console.log(response.data.data.value)
					var logList = response.data.data.value;
					if (this.flowLogs == '') {
						let list = [{}];
						for (var i=logList.length-1; i>=0; i--) {
							this.flowLogs.push({
								gmt_modified: logList[i].gmt_modified,
								participant: logList[i].participant,
								suggestion: logList[i].suggestion,
								state: logList[i].state.state_name,
								transition: logList[i].transition.transition_name
							})
						}
						console.log(this.flowLogs)
					}					
				}				
			})
  		}else {
  			this.$data.ins_seen = false;
  		}  		
  	}
  },
  created () {
	this.getOrderDetail(this.$route.query.id);
	this.get_buildingData();
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
.opinion_view {
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-color: #F9FAFC;
  margin: 20px 15px 20px 15px ;
  border: 2px solid #8492A6;
  padding: 20px 35px 0px 35px;	
}
.dialogForm {	
  /* position:absolute;
  top: 50%;
  left: 50%;
  margin: 0 !important;
  transform: translate(-50%, -50%);
  max-height:calc(100% - 30px);
  max-width:calc(100% - 30px);
  display flex
  flex-direction column
  >.el-dialog__body
    overflow auto */
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-color: #F9FAFC;
  margin: 0px 10px 0px 10px ;
  border: 2px solid #8492A6;
  padding: 20px 10px 0px 10px;
  overflow:auto;
}
.dialog {
	top:5%;
	bottom: 5%;
	margin: 0 !important;
	/* max-height:calc(100% - 30px);
    max-width:calc(100% - 30px); */
	display:flex;
	flex-direction:column;
	overflow:auto;
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
.transfer_record {
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-color: #F9FAFC;
  margin: 10px 15px 10px 15px ;
  border: 2px solid #8492A6;
  padding: 5px 20px 5px 20px;
  opacity: 0.8;	
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
