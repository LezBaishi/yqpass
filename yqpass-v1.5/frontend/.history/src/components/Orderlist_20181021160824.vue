<template lang="html">
  <div>
  	<el-row class="sidebar">
    	<el-col>
          <!-- <el-menu mode="horizontal" @select="handleSelect" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
          <el-submenu style="padding-left: 20px;">
              <template slot="title">
                <i class="el-icon-location"></i>
                <span>工单管理</span>
              </template>
            <el-menu-item class="el-menu-item" style="padding-left: 40px;color: rgb(255, 255, 255);background-color: rgb(84, 92, 100);" index="/0/orderNew">新建工单</el-menu-item>
            <el-menu-item class="el-menu-item" style="padding-left: 40px;color: rgb(255, 255, 255);background-color: rgb(84, 92, 100);" index="/0/orderUnfinished">待办工单</el-menu-item>
            <el-menu-item class="el-menu-item" style="padding-left: 40px;color: rgb(255, 255, 255);background-color: rgb(84, 92, 100);" index="/0/orderCompleted">已办工单</el-menu-item>
          </el-submenu>
          <el-submenu style="padding-left: 20px;">
              <template slot="title">
                <i class="el-icon-location"></i>
                <span>工单管理</span>
              </template>
            <el-menu-item class="el-menu-item" style="padding-left: 40px;color: rgb(255, 255, 255);background-color: rgb(84, 92, 100);" index="/0/orderNew">新建工单</el-menu-item>
            <el-menu-item class="el-menu-item" style="padding-left: 40px;color: rgb(255, 255, 255);background-color: rgb(84, 92, 100);" index="/0/orderUnfinished">待办工单</el-menu-item>
            <el-menu-item class="el-menu-item" style="padding-left: 40px;color: rgb(255, 255, 255);background-color: rgb(84, 92, 100);" index="/0/orderCompleted">已办工单</el-menu-item>
          </el-submenu>
        </el-menu> -->
        <el-menu
      default-active="2"
      class="el-menu-vertical-demo"
      @open="handleOpen"
      @close="handleClose"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b">
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-location"></i>
          <span>导航一</span>
        </template>
        <el-menu-item-group>
          <template slot="title">分组一</template>
          <el-menu-item index="1-1">选项1</el-menu-item>
          <el-menu-item index="1-2">选项2</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="分组2">
          <el-menu-item index="1-3">选项3</el-menu-item>
        </el-menu-item-group>
        <el-submenu index="1-4">
          <template slot="title">选项4</template>
          <el-menu-item index="1-4-1">选项1</el-menu-item>
        </el-submenu>
      </el-submenu>
      <el-menu-item index="2">
        <i class="el-icon-menu"></i>
        <span slot="title">导航二</span>
      </el-menu-item>
      <el-menu-item index="3" disabled>
        <i class="el-icon-document"></i>
        <span slot="title">导航三</span>
      </el-menu-item>
      <el-menu-item index="4">
        <i class="el-icon-setting"></i>
        <span slot="title">导航四</span>
      </el-menu-item>
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
  width: 100%;
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
