<template lang="html">
  <div>
  	<el-row  class="container">
      	<el-row v-if="seen" class="order_menu">
      		<el-form ref="search_form" :model="search_form" label-width="80px">
       		<el-row>
       			<h2 style="font-size:22px;">搜索工单</h2>
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
              <el-breadcrumb-item :to="{ path: '/1/resCable' }">光缆总表</el-breadcrumb-item>
              <el-breadcrumb-item>纤芯详情</el-breadcrumb-item>
            </el-breadcrumb>
          </el-col>
        </el-row>
        <el-row v-if="setPageSeen" class="page_menu">
        	<h2 style="font-size:22px;">页面设置</h2>
        	<el-checkbox v-model="checked_A">A端信息</el-checkbox>
        	<el-checkbox v-model="checked_ocable_cor">光缆对接（A-Z）</el-checkbox>
        	<el-checkbox v-model="checked_Z">Z端信息</el-checkbox>
        	<el-checkbox v-model="checked_core_quality">纤芯质量</el-checkbox>
        	<el-checkbox v-model="checked_occ_business">占用业务</el-checkbox>
        	<el-checkbox v-model="checked_circuit_num">电路编号</el-checkbox>
        	<el-checkbox v-model="checked_application_id">施工单号</el-checkbox>
        	<el-checkbox v-model="checked_notes">备注</el-checkbox> 
        </el-row>
        <el-row>
        	<el-col :push="20" :span="1">
				<!-- <el-button type="primary" style='float: right;' size="mini" round @click="addRow(tableData)">新增表行</el-button> -->
				<el-button type="primary" style='float: right;' size="mini" round @click="dialogFormVisible = true">新增表行</el-button>
        	</el-col>
			<el-col :push="21" :span="1">
	        	<el-button type="primary" style='float: right;' size="mini" round @click="setPage">页面设置</el-button>
			</el-col>
			<el-dialog title="新增纤芯" :visible.sync="dialogFormVisible" width="66%" center class="dialog">
				<el-form :model="dialog_form" class="dialogForm">
					<el-form-item label="光缆对接（A-Z）" :label-width="formLabelWidth">
						<el-input v-model="dialog_form.ocable_cor"></el-input>
					</el-form-item>
					<el-row>
						<el-col :span="14">
							<el-form-item label="A端光缆ODF" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.ocable_odf_A" placeholder="如1.1栋负1楼ODF01-1-A1或3.1栋103机房G101-1-A1"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="8" :push="1">
							<el-form-item label="转接设备端口" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.switch_dport_A"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					<el-row>
						<el-col :span="14">
							<el-form-item label="Z端光缆ODF" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.ocable_odf_Z" placeholder="如1.1栋负1楼ODF01-1-A1或3.1栋103机房G101-1-A1"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="8" :push="1">
							<el-form-item label="转接设备端口" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.switch_dport_Z"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					<el-row>
						<el-col :span="11">
							<el-form-item label="纤芯质量" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.core_quality"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="11" :push="1">
							<el-form-item label="占用业务" :label-width="formLabelWidth">
								<el-input v-model="dialog_form.occ_business"></el-input>
							</el-form-item>
						</el-col>
					</el-row>
					<el-row>
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
					</el-form-item>
				</el-form>
				<div slot="footer" class="dialog-footer">
					<el-button @click="resetDialogForm('dialog_form')">取消</el-button>
					<el-button type="primary" @click="submitDialogForm('dialog_form')">确定</el-button>
				</div>
			</el-dialog>
        </el-row>        
        <el-row>
        	<el-table :data="tableData" ref="table" tooltip-effect="dark" border stripe style="width:100%;margin-top:10px;">
        		<el-table-column label="序号" type="index" width="60" align="center"></el-table-column>
        		<el-table-column label="A端" align="center" v-if="checked_A">
        			<el-table-column label="光缆ODF" prop="ocable_odf_A" width="360" align="center">
        				<template slot-scope="scope">
        					<el-input v-show="scope.row.edit" v-model="scope.row.ocable_odf_A" placeholder="如1.1栋负1楼ODF01-1-A1或3.1栋103机房G101-1-A1"></el-input>
        					<span v-show="!scope.row.ocable_odf_A">{{ scope.row.ocable_odf_A }}</span>
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
        		<el-table-column label="光缆对接（A-Z）" prop="ocable_cor" width="500" align="center" v-if="checked_ocable_cor">
        		    <template slot-scope="scope">
        		    	<el-input v-show="scope.row.edit" v-model="scope.row.ocable_cor"></el-input>
        		    	<span v-show="!scope.row.edit">{{ scope.row.ocable_cor }}</span>
        		    </template>	
        		</el-table-column>
        		<el-table-column label="Z端" align="center" v-if="checked_Z">
        			<el-table-column label="光缆ODF" prop="ocable_odf_Z" width="360" align="center">
        				<template slot-scope="scope">
        					<el-input v-show="scope.row.edit" v-model="scope.row.ocable_odf_Z" placeholder="如1.1栋负1楼ODF01-1-A1或3.1栋103机房G101-1-A1"></el-input>
        					<span v-show="!scope.row.ocable_odf_A">{{ scope.row.ocable_odf_Z }}</span>
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
export default {
  data () {
    return {
	  tableData: [],
	  dialog_form: {
  		ocable_odf_A: '',
      	switch_dport_A: '',
      	ocable_cor: '',
      	ocable_odf_Z: '',
      	switch_dport_Z: '',
      	core_quality: '',
      	occ_business: '',
      	circuit_num: '',
      	application_id: '',
      	notes: '',
		  },
	  dialogFormVisible: false,
	  formLabelWidth: '120px',
       tableColumns: [
       { label: '标题', prop: 'title'},
       { label: '更新时间', prop: 'updateTime'}
    ],
    	seen: false,
    	setPageSeen: false,
    	checked_A: true,
    	checked_ocable_cor: true,
    	checked_Z: true,
    	checked_core_quality: true,
    	checked_occ_business: true,
    	checked_circuit_num: true,
    	checked_application_id: true,
    	checked_notes: true,
    	search_form: [
    	{
    		cable: '',
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
	submitDialogForm(formName) {
		this.dialogFormVisible = false;
		this.tableData.push({
			ocable_odf_A: this.dialog_form.ocable_odf_A,
			switch_dport_A: this.dialog_form.switch_dport_A,
			ocable_cor: this.dialog_form.ocable_cor,
			ocable_odf_Z: this.dialog_form.ocable_odf_Z,
			switch_dport_Z: this.dialog_form.switch_dport_Z,
			core_quality: this.dialog_form.core_quality,
			occ_business: this.dialog_form.occ_business,
			circuit_num: this.dialog_form.circuit_num,
			application_id: this.dialog_form.application_id,
			notes: this.dialog_form.notes,
			edit: false
		});
		console.log(this.tableData);
		this.dialog_form = {
			ocable_odf_A: '',
			switch_dport_A: '',
			ocable_cor: '',
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
  	addRow (tableData, event) {		
  		var list = {
			ocable_odf_A: '',
			switch_dport_A: '',
			ocable_cor: '',
			ocable_odf_Z: '',
			switch_dport_Z: '',
			core_quality: '',
			occ_business: '',
			circuit_num: '',
			application_id: '',
			notes: '',
			edit: true
  		}
  		tableData.push(list)
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