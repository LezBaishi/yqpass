<template lang="html">
  <div>
  	<el-row class="sidebar">
    	<el-col>
        <el-menu router default-active="2" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span>工单管理</span>
            </template>
            <el-menu-item index="/0/orderNew">新建工单</el-menu-item>
            <el-menu-item index="/0/orderUnfinished">待办工单</el-menu-item>
            <el-menu-item index="/0/orderCompleted">已办工单</el-menu-item>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span>资源管理</span>
            </template>
            <el-menu-item index="/1/resCable">光缆总表</el-menu-item>
            <el-menu-item index="/1/resCircuit">已用电路</el-menu-item>
          </el-submenu>
          
        </el-menu>
      </el-col>
    </el-row>
    <el-row class="panel-c-c">
      <el-col>
      	<router-view></router-view>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import OrderlistNew from '../components/OrderlistNew'
import OrderlistUnfinished from '../components/OrderlistUnfinished'
import OrderlistCompleted from '../components/OrderlistCompleted'
export default {
  components: {
  	OrderlistNew,
  	OrderlistUnfinished,
  	OrderlistCompleted
  },
  data () {
    return {
      
    }
  },
  methods: {

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="css" scoped>
.sidebar {
	position: fixed;
  top: 60px;
  bottom: 0px;
  left: 0px;
  width: 180px;
  border-top: 1px solid RGBA(178,184,190,1);
  z-index: 2000;
  overflow-x: scroll;
  /* height: 100%;
  width: 100%; */
  /* display: flex; */
  /* flex: 1; */
}
/* .el-menu-item {
  height: 100px;
  line-height: 50px;
  padding: 0 45px;
  min-width: 200px;
  font-size: 14px;
} */
.panel-c-c {
    /*这是列，因为已经有了列的宽度因此无需设置width*/
  background: #f1f2f7;
  position: fixed;
  top: 60px;
  bottom: 0px;
  left: 180px;
  right: 0px;
  /* width: 100%; */
  border-top: 1px solid RGBA(178,184,190,1);
  /* position: relative;
  margin-top: 80px;
  margin-left: 180px;
  margin: auto; */
  /* height: calc(100% - 60px);
  top: 0px;
  bottom: 0px; */
  /* height: 100%; */
  overflow-y: scroll;
    /*内层设置滚动*/
  padding: 10px;
}
</style>
