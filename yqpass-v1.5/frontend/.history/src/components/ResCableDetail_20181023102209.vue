<template lang="html">
  <div>
  	<el-row  class="container">
      	<el-row v-if="seen" class="order_menu">
      		<el-form ref="search_form" :model="search_form" label-width="80px">
       		<el-row>
       			<h2 style="font-size:22px;">搜索工单</h2>
      			<el-col :offset="3" :span="8">
					<el-form-item  label="光缆ODF" prop="ocable_odf">
						<el-input placeholder="请输入光缆ODF" v-model="search_form.ocable_odf" style="width:100%;" clearable></el-input>
					</el-form-item>
      			</el-col>
      			<el-col :push="2" :span="8">
					<el-form-item label="转接端口" prop="switch_dport">
						<el-input placeholder="请输入光缆转接设备端口" v-model="search_form.switch_dport" style="width:100%;" clearable></el-input>
					</el-form-item>
      			</el-col>	      		
			</el-row>
			<el-row>
				<el-col :offset="3" :span="8">
					<el-form-item label="光缆对应" prop="ocable_cor">
						<el-input v-model="search_form.ocable_cor" placeholder="请输入光缆对应" clearable></el-input>
					</el-form-item>
				</el-col>
				<el-col :push="2" :span="8">
					<el-form-item label="纤芯质量" prop="core_quality">
						<el-input v-model="search_form.core_quality" placeholder="请输入纤芯质量" clearable></el-input>
					</el-form-item>
				</el-col>
			</el-row>
			<el-row>
				<el-col :offset="3" :span="8">
					<el-form-item label="电路编号" prop="circuit_num">
						<el-input v-model="search_form.circuit_num" placeholder="请输入电路编号" clearable></el-input>
					</el-form-item>
				</el-col>
				<el-col :push="2" :span="8">
					<el-form-item label="占用业务" prop="occ_business">
						<el-input v-model="search_form.occ_business" placeholder="请输入占用业务" clearable></el-input>
					</el-form-item>
				</el-col>
			</el-row>  
	      	<el-row>
	      		<el-col :offset="3" :span="8">
	      			<el-form-item label="施工单号" prop="sn">
	      				<el-input v-model="search_form.sn" placeholder="请输入施工单号" clearable></el-input>
	      			</el-form-item>
	      		</el-col>
	      		<el-col :push="2" :span="8">
					<el-form-item label="纤芯信息">
						<el-col :span="11">
							<el-form-item prop="building">
								<el-input placeholder="请输入楼栋" v-model="search_form.building" style="width:100%;" clearable></el-input>
							</el-form-item>
						</el-col>
						<el-col class="line" :span="2">-</el-col>
						<el-col :span="11">
							<el-form-item prop="room">
								<el-input placeholder="请输入机房号" v-model="search_form.room" style="width:100%;" clearable></el-input>
							</el-form-item>
						</el-col>
					</el-form-item>
	      			<!-- <el-form-item label="纤芯排序" prop="coreOrder">
	      				<el-select v-model="search_form.coreOrder" placeholder="请选择排序方式" style="width:100%;">
							<el-option label="正序" name="type" value="0"></el-option>
							<el-option label="倒序" name="type" value="1"></el-option>
	      				</el-select>
	      			</el-form-item> -->
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
              <el-breadcrumb-item :to="{ path: '/1/resCable' }">光缆总表</el-breadcrumb-item>
              <el-breadcrumb-item>纤芯详情</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>
        </el-row>
        <el-row v-if="setPageSeen" class="page_menu">
        	<h2 style="font-size:22px;">页面设置</h2>
        	<el-checkbox v-model="checked_A">A端信息</el-checkbox>
        	<el-checkbox v-model="checked_sn">光缆对接（A-Z）</el-checkbox>
        	<el-checkbox v-model="checked_Z">Z端信息</el-checkbox>
        	<el-checkbox v-model="checked_core_quality">纤芯质量</el-checkbox>
        	<el-checkbox v-model="checked_occ_business">占用业务</el-checkbox>
        	<el-checkbox v-model="checked_circuit_num">电路编号</el-checkbox>
        	<el-checkbox v-model="checked_application_id">施工单号</el-checkbox>
        	<el-checkbox v-model="checked_notes">备注</el-checkbox> 
        </el-row>
        <el-row>
        	<el-col>
				<el-button style='float: right;' type="primary" size="mini" round @click="delAll">删除</el-button>
				<el-button style='float: right; margin-right:10px;' type="primary" size="mini" round @click="setPage">设置</el-button>
				<el-button style='float: right;' type="primary" size="mini" round @click="dialogFormVisible = true">新增</el-button>
			</el-col>
		</el-row>
		<el-row>
			<el-dialog title="新增纤芯" :visible.sync="dialogFormVisible" width="66%" center class="dialog" :modal-append-to-body="false">
				<el-form :model="dialog_form" class="dialogForm">
					<!-- <el-form-item label="光缆对接（A-Z）" :label-width="formLabelWidth">
						<el-input v-model="dialog_form.sn"></el-input>
					</el-form-item> -->
					<el-row>
						<!-- <el-col :span="14"> -->
							<el-form-item label="A端光缆ODF" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.ocable_odf_A" placeholder="如1.1栋负1楼ODF01-1-A1或3.1栋103机房G101-1-A1"></el-input>
							</el-form-item>
						<!-- </el-col>
						<el-col :span="8" :push="1">
							<el-form-item label="转接设备端口" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.switch_dport_A"></el-input>
							</el-form-item>
						</el-col> -->
					</el-row>
					<el-row>
						<!-- <el-col :span="14"> -->
							<el-form-item label="Z端光缆ODF" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.ocable_odf_Z" placeholder="如1.1栋负1楼ODF01-1-A1或3.1栋103机房G101-1-A1"></el-input>
							</el-form-item>
						<!-- </el-col>
						<el-col :span="8" :push="1">
							<el-form-item label="转接设备端口" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.switch_dport_Z"></el-input>
							</el-form-item>
						</el-col> -->
					</el-row>
					<el-row>
						<el-col :span="11">
							<el-form-item label="纤芯质量" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.core_quality"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="11" :push="1">
							<!-- <el-form-item label="占用业务" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.occ_business"></el-input>
							</el-form-item> -->
							<el-form-item label="备注" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.notes"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					<!-- <el-row>
						<el-col :span="11">
							<el-form-item label="电路编号" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.circuit_num"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="11" :push="1">
							<el-form-item label="施工编号" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.application_id"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					<el-form-item label="备注" :label-width="formLabelWidth">
						<el-input v-model="dialog_form.notes"></el-input>
					</el-form-item> -->
				</el-form>
				<div slot="footer" class="dialog-footer">
					<el-button @click="resetDialogForm('dialog_form')">取消</el-button>
					<el-button type="primary" @click="submitDialogForm('dialog_form')">确定</el-button>
				</div>
			</el-dialog>
        </el-row>        
        <el-row>
        	<el-table :data="tableData" v-loading="loading" ref="multipleSelection" tooltip-effect="dark" border stripe style="width:100%;margin-top:10px;" @selection-change="handleSelectionChange">
				<el-table-column type="selection" width="55" align="center"></el-table-column>
				<el-table-column label="序号" type="index" width="60" align="center"></el-table-column>
        		<el-table-column label="A端" align="center" v-if="checked_A">
        			<el-table-column label="光缆ODF" prop="ocable_odf_A" width="360" align="center">
        				<template slot-scope="scope">
        					<el-input v-show="scope.row.edit" v-model="scope.row.ocable_odf_A" placeholder="如1.1栋负1楼ODF01-1-A1或3.1栋103机房G101-1-A1"></el-input>
        					<span v-show="!scope.row.edit">{{ scope.row.ocable_odf_A }}</span>
        				</template>
        			</el-table-column>
        			<!-- <el-table-column label="转接ODF" prop="ocable_switch_A" width="240" align="center">
        				<template slot-scope="scope">
        					<el-input v-show="scope.row.edit" v-model="scope.row.ocable_switch_A"></el-input>
        					<span v-show="!scope.row.edit">{{ scope.row.ocable_switch_A }}</span>
        				</template>
        			</el-table-column> -->
        			<el-table-column label="转接设备端口" prop="switch_dport_A" width="240" align="center">
        				<template slot-scope="scope">
        					<el-input v-show="scope.row.edit" v-model="scope.row.switch_dport_A"></el-input>
        					<span v-show="!scope.row.edit">{{ scope.row.switch_dport_A }}</span>
        				</template>
        			</el-table-column>
        		</el-table-column>
        		<el-table-column label="光缆对接（A-Z）" prop="sn" width="500" align="center" v-if="checked_sn">
        		    <template slot-scope="scope">
        		    	<el-input v-show="scope.row.edit" v-model="scope.row.sn"></el-input>
        		    	<span v-show="!scope.row.edit">{{ scope.row.sn }}</span>
        		    </template>	
        		</el-table-column>
        		<el-table-column label="Z端" align="center" v-if="checked_Z">
        			<el-table-column label="光缆ODF" prop="ocable_odf_Z" width="360" align="center">
        				<template slot-scope="scope">
        					<el-input v-show="scope.row.edit" v-model="scope.row.ocable_odf_Z" placeholder="如1.1栋负1楼ODF01-1-A1或3.1栋103机房G101-1-A1"></el-input>
        					<span v-show="!scope.row.edit">{{ scope.row.ocable_odf_Z }}</span>
        				</template>
        			</el-table-column>
        			<!--<el-table-column label="转接ODF" prop="ocable_switch_Z" width="240" align="center">
        				<template slot-scope="scope">
        					<el-input v-show="scope.row.edit" v-model="scope.row.ocable_switch_Z"></el-input>
        					<span v-show="!scope.row.edit">{{ scope.row.ocable_switch_Z }}</span>
        				</template>
        			</el-table-column> -->
        			<el-table-column label="转接设备端口" prop="switch_dport_Z" width="240" align="center">
        				<template slot-scope="scope">
        					<el-input v-show="scope.row.edit" v-model="scope.row.switch_dport_Z"></el-input>
        					<span v-show="!scope.row.edit">{{ scope.row.switch_dport_Z }}</span>
        				</template>
        			</el-table-column>
        		</el-table-column>
        		<el-table-column label="纤芯质量" prop="core_quality" width="240" align="center" v-if="checked_core_quality">
        		    <template slot-scope="scope">
        		    	<el-input v-show="scope.row.edit" v-model="scope.row.core_quality"></el-input>
        		    	<span v-show="!scope.row.edit">{{ scope.row.core_quality }}</span>	
        		    </template>	
        		</el-table-column>
        		<el-table-column label="占用业务" prop="occ_business" width="240" align="center" v-if="checked_occ_business">
        		    <template slot-scope="scope">
        		    	<el-input v-show="scope.row.edit" v-model="scope.row.occ_business"></el-input>
        		    	<span v-show="!scope.row.edit">{{ scope.row.occ_business }}</span>	
        		    </template>	
        		</el-table-column>
        		<el-table-column label="电路编号" prop="circuit_num" width="240" align="center" v-if="checked_circuit_num">
        		    <template slot-scope="scope">
        		    	<el-input v-show="scope.row.edit" v-model="scope.row.circuit_num"></el-input>
        		    	<span v-show="!scope.row.edit">{{ scope.row.circuit_num }}</span>	
        		    </template>	
        		</el-table-column>
        		<el-table-column label="施工编号" prop="application_id" width="240" align="center" v-if="checked_application_id">
        		    <template slot-scope="scope">
        		    	<el-input v-show="scope.row.edit" v-model="scope.row.application_id"></el-input>
        		    	<span v-show="!scope.row.edit">{{ scope.row.application_id }}</span>	
        		    </template>	
        		</el-table-column>
        		<el-table-column label="备注" prop="notes" width="240" align="center" v-if="checked_notes">
        		    <template slot-scope="scope">
        		    	<el-input v-show="scope.row.edit" v-model="scope.row.notes"></el-input>
        		    	<span v-show="!scope.row.edit">{{ scope.row.notes }}</span>	
        		    </template>	
        		</el-table-column>
        		<!--<el-table-column label="创建人" prop="creator" width="150" align="center" v-if="checked_creator">
        		    <template slot-scope="scope">
        		    	<el-input v-show="scope.row.edit" v-model="scope.row.creator"></el-input>
        		    	<span v-show="!scope.row.edit">{{ scope.row.creator }}</span>	
        		    </template>	
        		</el-table-column>
        		<el-table-column label="创建时间" prop="gmt_created" width="150" align="center" v-if="checked_gmt_created">
        		    <template slot-scope="scope">
        		    	<el-input v-show="scope.row.edit" v-model="scope.row.gmt_created"></el-input>
        		    	<span v-show="!scope.row.edit">{{ scope.row.gmt_created }}</span>	
        		    </template>	
        		</el-table-column>
        		<el-table-column label="修改人" prop="modifier" width="150" align="center" v-if="checked_modifier">
        		    <template slot-scope="scope">
        		    	<el-input v-show="scope.row.edit" v-model="scope.row.modifier"></el-input>
        		    	<span v-show="!scope.row.edit">{{ scope.row.modifier }}</span>	
        		    </template>	
        		</el-table-column>
        		<el-table-column label="更新时间" prop="gmt_modified" width="150" align="center" v-if="checked_gmt_modified">
        		    <template slot-scope="scope">
        		    	<el-input v-show="scope.row.edit" v-model="scope.row.gmt_modified"></el-input>
        		    	<span v-show="!scope.row.edit">{{ scope.row.gmt_modified }}</span>	
        		    </template>	
        		</el-table-column> -->        		        		        		        			
  				<el-table-column label="操作" align="center" width="100" fixed="right">
	  				<template slot-scope="scope">
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
import { getCableDetailList,newCableDetail,editCableDetail,delCableDetail } from '../api/api'
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
	  cableId: this.$route.query.id,
	  dialog_form: '',
	  dialog_form_empty: {
  		ocable_odf_A: '',
      	switch_dport_A: '',
      	sn: '',
      	ocable_odf_Z: '',
      	switch_dport_Z: '',
      	core_quality: '',
      	occ_business: '',
      	circuit_num: '',
      	application_id: '',
      	notes: '',
		  },
	  dialogFormVisible: false,
	  dialogFormIndexId: '',
	  formLabelWidth: '120px',
       tableColumns: [
       { label: '标题', prop: 'title'},
       { label: '更新时间', prop: 'updateTime'}
    ],
    	seen: false,
    	setPageSeen: false,
    	checked_A: true,
    	checked_sn: true,
    	checked_Z: true,
    	checked_core_quality: true,
    	checked_occ_business: true,
    	checked_circuit_num: true,
    	checked_application_id: true,
    	checked_notes: true,
    	search_form: [
    	{
			ocable_odf: '',
			switch_dport: '',
    		building: '',
			room: '',
			ocable_cor: '',
			core_quality: '',
			circuit_num: '',
			occ_business: '',
    		sn: '',
    		coreOrder: '',
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
		paramsData["ocable_section_id"] = this.cableId;
		paramsData["ocable_odf"] = this.search_form.ocable_odf;
		paramsData["switch_dport"] = this.search_form.switch_dport;
		paramsData["building"] = this.search_form.building;
		paramsData["room"] = this.search_form.room;
		paramsData["ocable_cor"] = this.search_form.ocable_cor;
		paramsData["core_quality"] = this.search_form.core_quality;
		paramsData["circuit_num"] = this.search_form.circuit_num;
		paramsData["occ_business"] = this.search_form.occ_business;
		paramsData["sn"] = this.search_form.sn;
		paramsData["reverse"] = this.search_form.coreOrder;
		paramsData["per_page"] = this.pageSize;
		paramsData["page"] = this.pageNo;
		getCableDetailList({params : paramsData}).then((response)=> {
			console.log(response);
			if (response.data.code == 1) {
				this.loading = false;
				let list = response.data.data.value;
				this.tableData = [];
				for (var i=0; i<list.length; i++) {
					this.tableData.push({
						circuit_num: list[i].circuit_num,
						core_no: list[i].core_no,
						core_quality: list[i].core_quality,
						notes: list[i].notes,
						id: list[i].id,
						sn: list[i].sn,
						ocable_odf_A: list[i].ocable_odf_A,
						ocable_odf_Z: list[i].ocable_odf_Z,
						ocable_section_id: list[i].ocable_section_id,
						occ_business: list[i].occ_business,
						sn: list[i].sn,
						switch_dport_A: list[i].switch_dport_A,
						switch_dport_Z: list[i].switch_dport_Z
					})
				};
				console.log(this.tableData);
				this.totalCount = response.data.data.total
				console.log(this.totalCount)
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
			ocable_odf_A: '',
			switch_dport_A: '',
    		ocable_odf_Z: '',
			switch_dport_Z: '',
			ocable_cor: '',
			core_quality: '',
			circuit_num: '',
			occ_business: '',
    		sn: '',
    		coreOrder: '',
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
		this.getCableDetail();
	},  
	delAll () {
		console.log(this.multipleSelection);
		var delList = this.multipleSelection;
	},
	handleSelectionChange (val) {
		this.multipleSelection = val;
	},
	getCableDetail (id) {
		let paramsData = {};
		paramsData["ocable_section_id"] = this.cableId;
		paramsData["per_page"] = this.pageSize;
		paramsData["page"] = this.pageNo;
		getCableDetailList({params : paramsData}).then((response)=> {
			console.log(response);
			if (response.data.code == 1) {
				this.loading = false;
				let list = response.data.data.value;
				this.tableData = [];
				for (var i=0; i<list.length; i++) {
					this.tableData.push({
						circuit_num: list[i].circuit_num,
						core_no: list[i].core_no,
						core_quality: list[i].core_quality,
						notes: list[i].notes,
						id: list[i].id,
						sn: list[i].sn,
						ocable_odf_A: list[i].ocable_odf_A,
						ocable_odf_Z: list[i].ocable_odf_Z,
						ocable_section_id: list[i].ocable_section_id,
						occ_business: list[i].occ_business,
						sn: list[i].sn,
						switch_dport_A: list[i].switch_dport_A,
						switch_dport_Z: list[i].switch_dport_Z
					})
				};
				console.log(this.tableData);
				this.totalCount = response.data.data.total
				console.log(this.totalCount)
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
  		this.$nextTick(() => this.getCableDetail())
  	},
  	handleCurrentChange(val) {
  		console.log(`当前页:`+val);
  		this.pageNo = val
  		this.getCableDetail()
  	},  
	submitDialogForm(formName) {
		let paramsData = {};
		paramsData["ocable_section_id"] = this.cableId;
		paramsData["ocable_odf_A"] = this.dialog_form.ocable_odf_A;
		paramsData["ocable_odf_Z"] = this.dialog_form.ocable_odf_Z;
		paramsData["core_quality"] = this.dialog_form.core_quality;
		paramsData["notes"] = this.dialog_form.notes;
		var parmas = JSON.stringify(paramsData);
		if (this.dialog_form == this.dialog_form_empty) {
			newCableDetail(parmas).then((response)=> {
				console.log(response);
				if (response.data.code == 1) {
					this.dialogFormVisible = false;
					this.getCableDetail();
					this.$notify({
						title: '提示',
						message: '新增纤芯成功',
						type: 'success',
						duration:1500
					});		  				
				} else {
					console.log('error submit!!');
					return false;
				}
			});
		} else {
			let id = this.dialog_form.id;
			editCableDetail(id, parmas).then((response)=> {
				console.log(response);
				if (response.data.code == 1) {
					this.dialogFormVisible = false;
					this.getCableDetail();
					this.$notify({
						title: '提示',
						message: '编辑纤芯成功',
						type: 'success',
						duration:1500
					});
				} else {
					console.log('error submit!!');
					return false;
				}
			});
		}
		// this.tableData.push({
		// 	ocable_odf_A: this.dialog_form.ocable_odf_A,
		// 	switch_dport_A: this.dialog_form.switch_dport_A,
		// 	sn: this.dialog_form.sn,
		// 	ocable_odf_Z: this.dialog_form.ocable_odf_Z,
		// 	switch_dport_Z: this.dialog_form.switch_dport_Z,
		// 	core_quality: this.dialog_form.core_quality,
		// 	occ_business: this.dialog_form.occ_business,
		// 	circuit_num: this.dialog_form.circuit_num,
		// 	application_id: this.dialog_form.application_id,
		// 	notes: this.dialog_form.notes,
		// 	edit: false
		// });
		// console.log(this.tableData);
		this.dialog_form_empty = {
			ocable_odf_A: '',
			switch_dport_A: '',
			sn: '',
			ocable_odf_Z: '',
			switch_dport_Z: '',
			core_quality: '',
			occ_business: '',
			circuit_num: '',
			application_id: '',
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
  	deleteRow (index, rows) {
    	this.$confirm('是否确定删除改行数据', '提示', {
    		confirmButtonText: '确定',
    		cancelButtonText: '取消',
    		type: 'warning'
    	}).then(() => {
			rows.splice(index, 1);   		
    	}).catch(() => {

    	});
  	},
  },
  created () {
	  this.getCableDetail(this.$route.query.id);
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
  padding: 5px 10px 5px 10px;	
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
	margin: 0 !important;
	/* max-height:calc(100% - 30px);
    max-width:calc(100% - 30px); */
	display:flex;
	flex-direction:column;
	overflow:auto;
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