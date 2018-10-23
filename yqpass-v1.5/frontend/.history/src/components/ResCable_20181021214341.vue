<template lang="html">
  <div>
  	<el-row class="container">
      	<el-row v-if="seen" class="order_menu">
      		<el-form ref="search_form" :model="search_form" label-width="80px">
       		<el-row>
       			<h2 style="font-size:22px;">搜索光缆</h2>
      			<el-col :offset="3" :span="8">
					<el-form-item label="A端信息">
						<el-col :span="11">
							<el-form-item prop="building_A">
								<el-input placeholder="请输入A端楼栋" v-model="search_form.building_A" style="width:100%;"></el-input>
							</el-form-item>
						</el-col>
						<el-col class="line" :span="2">-</el-col>
						<el-col :span="11">
							<el-form-item prop="room_A">
								<el-input placeholder="请输入A端机房号" v-model="search_form.room_A" style="width:100%;"></el-input>
							</el-form-item>
						</el-col>
					</el-form-item>
      			</el-col>
      			<el-col :push="2" :span="8">
      				<el-form-item label="Z端信息">
      					<el-col :span="11">
      						<el-form-item prop="building_Z">
	      						<el-input placeholder="请输入Z端楼栋" v-model="search_form.building_Z" style="width:100%;"></el-input>
	      					</el-form-item>
      					</el-col>
      					<el-col class="line" :span="2">-</el-col>
      					<el-col :span="11">
      						<el-form-item prop="room_Z">
	      						<el-input placeholder="请输入Z端机房号" v-model="search_form.room_Z" style="width:100%;"></el-input>
	      					</el-form-item>
      					</el-col>
      				</el-form-item>
      			</el-col>	      		
	      	</el-row>
	      	<el-row>
	      		<el-col :offset="3" :span="8">
	      			<el-form-item label="光缆名称" prop="ocable_name">
	      				<el-input v-model="search_form.ocable_name" placeholder="请输入光缆名称"></el-input>
	      			</el-form-item>
	      		</el-col>
	      		<el-col :push="2" :span="8">
	      			<el-form-item label="光缆排序" prop="cableOrder">
	      				<el-select v-model="search_form.cableOrder" placeholder="请选择排序方式" style="width:100%;">
							<el-option label="正序" name="type" value="0"></el-option>
							<el-option label="倒序" name="type" value="1"></el-option>
	      				</el-select>
	      			</el-form-item>
	      		</el-col>
	      	</el-row>	      		
	      	<el-row>
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
			<el-dialog title="新增光缆段" :visible.sync="dialogFormVisible" width="66%" center class="dialog" :modal-append-to-body="false">
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
					<el-row>
						<el-col :span="11">
							<el-form-item label="纤芯数" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.core_num"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="11" :push="1">
							<el-form-item label="光缆长度" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.ocable_length" placeholder="单位：皮长公里"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					<!-- <el-form-item label="光缆名称" :label-width="formLabelWidth">
						<el-input v-model="dialog_form.ocable_name"></el-input>
					</el-form-item>
					<el-row>
						<el-col :span="11">
							<el-form-item label="纤芯数" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.core_num"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="11" :push="1">
							<el-form-item label="已用纤芯数" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.used_core_num"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					<el-row>
						<el-col :span="11">
							<el-form-item label="纤芯利用率" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.core_occ"  placeholder="等于已用纤芯数/纤芯数"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="11" :push="1">
							<el-form-item label="剩余纤芯数" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.ocable_length"  placeholder="等于纤芯数-已用纤芯数"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					<el-row>
						<el-col :span="11">
							<el-form-item label="光缆长度" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.ocable_length"  placeholder="单位：皮长公里"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="11" :push="1">
							<el-form-item label="芯公里" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.core_kilo"  placeholder="等于纤芯数*光缆长度"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					<el-row>
						<el-col :span="11">
							<el-form-item label="使用芯公里" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.used_core_kilo"  placeholder="等于已用纤芯数*光缆长度"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="11" :push="1">
							<el-form-item label="纤芯使用率" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.core_usage"  placeholder="等于使用芯公里/芯公里"></el-input>
							</el-form-item>
						</el-col>
					</el-row> -->
					<el-row>
						<el-col :span="12">
							<el-form-item label="光缆类型" :label-width="formLabelWidth">
									<el-select  v-model="dialog_form.ocable_type" placeholder="请选择">
										<el-option v-for="item in ocable_type_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
									</el-select>
							</el-form-item>	
						</el-col>
						<el-col :span="12">
							<el-form-item label="光缆等级" :label-width="formLabelWidth">
									<el-select  v-model="dialog_form.ocable_level" placeholder="请选择">
										<el-option v-for="item in ocable_level_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
									</el-select>
							</el-form-item>	
						</el-col>
					</el-row>
					<el-row>
						<el-col :span="12">
							<el-form-item label="光纤型号" :label-width="formLabelWidth">
									<el-select  v-model="dialog_form.ofiber_type" placeholder="请选择">
										<el-option v-for="item in ofiber_type_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
									</el-select>
							</el-form-item>	
						</el-col>
					</el-row>
					<el-form-item label="备注" :label-width="formLabelWidth">
						<el-input v-model="dialog_form.notes"></el-input>
					</el-form-item>
				</el-form>
				<div slot="footer" class="dialog-footer">
					<el-button @click="resetDialogForm('dialog_form')">取消</el-button>
					<el-button type="primary" @click="submitDialogForm('dialog_form')">确定</el-button>
				</div>
			</el-dialog>
        </el-row>
        <el-row>
          	<el-table :data="tableData"  v-loading="loading" ref="multipleSelection" tooltip-effect="dark" border stripe style="width:100%;margin-top:10px;" @selection-change="handleSelectionChange">
				<el-table-column type="selection" width="55" align="center"></el-table-column>  
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
          				<el-select v-show="scope.row.edit" v-model="scope.row.ocable_type" placeholder="请选择">
          					<el-option v-for="item in ocable_type_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
          				</el-select>
          				<span v-show="!scope.row.edit">{{ scope.row.ocable_type }}</span>
          			</template>
          		</el-table-column>	       
          		<el-table-column label="光缆等级" width="240" align="center" v-if="checked_ocable_level">
          			<template slot-scope="scope">
          				<el-select v-show="scope.row.edit" v-model="scope.row.ocable_level" placeholder="请选择">
          					<el-option v-for="item in ocable_level_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
          				</el-select>
          				<span v-show="!scope.row.edit">{{ scope.row.ocable_level }}</span>
          			</template>
          		</el-table-column>
          		<el-table-column label="光纤型号" width="110" align="center" v-if="checked_ofiber_type">
          			<template slot-scope="scope">
          				<el-select v-show="scope.row.edit" v-model="scope.row.ofiber_type" placeholder="请选择">
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
	  			<el-table-column label="操作" width="140" align="center" fixed="right">
	  				<template slot-scope="scope">
	  					<el-button type="primary" circle size="mini" @click="detailView(scope.$index, tableData)" icon="el-icon-view"></el-button>
	  					<el-button :type="scope.row.edit?'success':'primary'" @click='editDialogForm(scope.$index, tableData)' circle size="mini" icon="el-icon-edit"></el-button> 
	  					<el-button type="danger" circle size="mini" @click="deleteRow(scope.$index, tableData)" icon="el-icon-delete"></el-button>	  					
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
import ResCableDetail from '../components/ResCableDetail'
import { getCableList,getBuildingRoomList } from '../api/api'
export default {
  data () {
    return {
	  tableData: [],
	  multipleSelection: [],
	  loading: true,
	  pageNo: 1,
	  totalPage: 0,
      totalCount: 0,
	  pageCount: 10,
      paginationShow: false,
	  pageSize: 10,
	  pageSizeList: [5, 10, 15, 20],
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
		dialogFormIndexId: '',
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
    		building_A: '',
			room_A: '',
			building_Z: '',
    		room_Z: '',
    		ocable_name: '',
    		cableOrder: ''
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
        ocable_type_option: [{
      		value: '单模',
      		label: '单模'
      	},{
      		value: '多模',
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
		this.$data.seen = false;
		let paramsData = {};
		paramsData["building_A"] = this.search_form.building_A;
		paramsData["room_A"] = this.search_form.room_A;
		paramsData["building_Z"] = this.search_form.building_Z;
		paramsData["room_Z"] = this.search_form.room_Z;
		paramsData["ocable_name"] = this.search_form.ocable_name;
		paramsData["reverse"] = this.search_form.cableOrder;
		paramsData["per_page"] = this.pageSize;
		paramsData["page"] = this.pageNo;  
		console.log(paramsData);
		getCableList({params: paramsData}).then((response)=>{
			console.log(response);
			if (response.data.code == 1) {
				this.loading = false;
				let list = response.data.data.value;
				this.tableData = [];
				for (var i=0; i<list.length; i++) {
					this.tableData.push({
						id: list[i].id,
						building_A: list[i].building_A,
						building_Z: list[i].building_Z,
						core_kilo: list[i].core_kilo,
						core_num: list[i].core_num,
						core_occ: list[i].core_occ,
						core_usage: list[i].core_usage,
						name_A: list[i].name_A,
						name_Z: list[i].name_Z,
						notes: list[i].notes,
						ocable_length: list[i].ocable_length,
						ocable_level: list[i].ocable_level,
						ocable_name: list[i].ocable_name,
						ocable_type: list[i].ocable_type,
						ofiber_type: list[i].ofiber_type,
						room_A: list[i].room_A,
						room_Z: list[i].room_Z,
						unused_core_num: list[i].unused_core_num,
						used_core_kilo: list[i].used_core_kilo,
						used_core_num: list[i].used_core_num
					});
				}
			console.log(this.tableData);
			this.totalCount = response.data.data.total;
			this.totalPage = Math.ceil(response.data.data.total/this.pageSize)
			if (this.totalPage > 1) {
				this.paginationShow = true;
			}
			}
		})
  	},
  	resetForm (formName) {
		  // this.$refs[formName].resetFields();
		this.search_form = [
    	{
    		building_A: '',
			room_A: '',
			building_Z: '',
    		room_Z: '',
    		ocable_name: '',
    		cableOrder: ''
    	}];
  	},
  	setPage () {
  		if (this.$data.setPageSeen == false){
  			this.$data.setPageSeen = true;
  		}else {
  			this.$data.setPageSeen = false;
  		}
	},
	refreshBtn () {
		this.getocableList();
	},
	getocableList () {
		let paramsData = {};
		paramsData["per_page"] = this.pageSize;
		paramsData["page"] = this.pageNo;
		getCableList({params: paramsData}).then((response)=>{
			console.log(response);
			if (response.data.code == 1) {
				this.loading = false;
				let list = response.data.data.value;
				console.log(list);
				this.tableData = [];
				for (var i=0; i<list.length; i++) {
					this.tableData.push({
						id: list[i].id,
						building_A: list[i].building_A,
						building_Z: list[i].building_Z,
						core_kilo: list[i].core_kilo,
						core_num: list[i].core_num,
						core_occ: list[i].core_occ,
						core_usage: list[i].core_usage,
						name_A: list[i].name_A,
						name_Z: list[i].name_Z,
						notes: list[i].notes,
						ocable_length: list[i].ocable_length,
						ocable_level: list[i].ocable_level,
						ocable_name: list[i].ocable_name,
						ocable_type: list[i].ocable_type,
						ofiber_type: list[i].ofiber_type,
						room_A: list[i].room_A,
						room_Z: list[i].room_Z,
						unused_core_num: list[i].unused_core_num,
						used_core_kilo: list[i].used_core_kilo,
						used_core_num: list[i].used_core_num
					});
				}
			console.log(this.tableData);
			this.totalCount = response.data.data.total;
			this.totalPage = Math.ceil(response.data.data.total/this.pageSize)
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
  		this.$nextTick(() => this.getocableList())
  	},
  	handleCurrentChange(val) {
  		console.log(`当前页:`+val);
  		this.pageNo = val
  		this.getocableList()
  	}, 
	get_buildingData () {
		this.allRoom = [];
		for (var i=1; i<12; i++) {
			let paramsData = {};
			paramsData["page"] = i;
			getBuildingRoomList({params : paramsData}).then((response)=> {
				// console.log(response);
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
	get_machineBuilding: function (building) {
		let room_list = this.allRoom;
		// console.log(room_list);
		let temRoom = [];
		for (var i=0; i<room_list.length; i++) {
			// console.log(room_list[i]);
			if (building == room_list[i].building){
  				temRoom.push({key: room_list[i].id, label: room_list[i].label, value: room_list[i].label})
  			}
		};
  		console.log(temRoom)
  		this.machineRoom_option = temRoom;
	},
	get_machineRoom:function (room) {
		console.log(room);
	},
	submitDialogForm(formName) {
		this.dialogFormVisible = false;
		this.tableData.push({
			building_A: this.dialog_form.building_A,
			room_A: this.dialog_form.room_A,
			name_A: this.dialog_form.name_A,
			building_Z: this.dialog_form.building_Z,
			room_Z: this.dialog_form.room_Z,
			name_Z: this.dialog_form.name_Z,
			ocable_name: this.dialog_form.ocable_name,
			core_num: this.dialog_form.core_num,
			used_core_num: this.dialog_form.used_core_num,
			core_occ: this.dialog_form.core_occ,
			unused_core_num: this.dialog_form.unused_core_num,
			ocable_length: this.dialog_form.ocable_length,
			core_kilo: this.dialog_form.core_kilo,
			used_core_kilo: this.dialog_form.used_core_kilo,
			core_usage: this.dialog_form.core_usage,
			ocable_type: this.dialog_form.ocable_type,
			ocable_level: this.dialog_form.ocable_level,
			ofiber_type: this.dialog_form.ofiber_type,
			notes: this.dialog_form.notes,
			edit: false
		});
		console.log(this.tableData);
		this.dialog_form = {
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
  		};
	},
	resetDialogForm(formName) {
		this.dialogFormVisible = false;
	},
	editDialogForm (index, rows) {
		this.dialogFormIndexId = index;
		console.log(this.tableData[index]);
		this.dialogFormVisible = true;
		this.dialog_form = this.tableData[index];
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
		let rowValue = JSON.parse(JSON.stringify(rows[index]));
  		this.$router.push({path: '/1/resCableDetail', query: {id: rowValue.id}});
  	}
  },
  created () {
	  this.getocableList();
	  this.get_buildingData();
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