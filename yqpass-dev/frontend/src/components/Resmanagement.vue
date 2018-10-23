<template lang="html">
  <div>
  	<el-row  class="container">
  	<el-col :span="4">
        <el-menu router :default-active="$route.path" theme="dark">
          <el-submenu>
            <template slot="title">资源管理</template>
            <el-menu-item index="/1/resCable">光缆总表</el-menu-item>
            <el-menu-item index="/1/resCircuit">已用电路</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-col>
      <el-col :span="20" class="panel-c-c">
      	<router-view></router-view>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import ResCable from '../components/ResCable'
import ResCircuit from '../components/ResCircuit'
export default {
  components: {
  	ResCable,
  	ResCircuit
  },  
  data () {
    return {
      
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
  	}
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="css" scoped>
.container {
	position: absolute;
  	height: 100%;
  	width: 100%;
}
.breadcrumb {
  margin-bottom: 10px;
}
.button_nav {
  margin-bottom: 10px;
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