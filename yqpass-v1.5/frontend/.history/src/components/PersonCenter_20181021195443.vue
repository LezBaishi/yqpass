<template lang="html">
  <div>
  	<el-row class="sidebar">
  	<el-col>
        <el-menu router default-active="2" @open="handleOpen" @close="handleClose" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
            <el-submenu index="1">
              <template slot="title">
                <i class="el-icon-tickets"></i>
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
            <el-submenu index="3">
              <template slot="title">
                <i class="el-icon-menu"></i>
                <span>资源展示</span>
              </template>
            </el-submenu>
            <el-submenu index="4">
              <template slot="title">
                <i class="el-icon-service"></i>
                <span>用户管理</span>
              </template>
              <el-menu-item index="/3/userList">用户列表</el-menu-item>
              <el-menu-item index="/3/roleList">角色列表</el-menu-item>
              <el-menu-item index="/3/deptList">部门列表</el-menu-item>
            </el-submenu>
            <el-submenu index="5">
              <template slot="title">
                <i class="el-icon-setting"></i>
                <span>个人中心</span>
              </template>
              <el-menu-item index="/personcenter/infor">个人信息</el-menu-item>
              <el-menu-item index="/personcenter/changepass">修改密码</el-menu-item>
            </el-submenu>
          </el-menu>
        </el-col>
      </el-row>
      <el-row class="panel-c-c">
        <!-- <el-menu router :default-active="$route.path" theme="dark" @open="handleOpen" @close="handleClose">
          <el-submenu>
            <template slot="title">个人中心</template>
            <el-menu-item index="/personcenter/infor">个人信息</el-menu-item>
            <el-menu-item index="/personcenter/changepass">修改密码</el-menu-item>
          </el-submenu>
        </el-menu> -->
      <el-col>
      	<router-view></router-view>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import PersonInfor from '@/components/PersonInfor'
import PersonChangepass from '@/components/PersonChangepass'
export default {
  components: {
  	PersonInfor,
  	PersonChangepass
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
.container {
	position: absolute;
  	height: 100%;
  	width: 100%;
}
.sidebar {
	position: fixed;
  top: 60px;
  bottom: 0px;
  left: 0px;
  width: 180px;
  border-top: 1px solid RGBA(178,184,190,1);
  z-index: 2000;
  overflow-x: scroll;
}
.panel-c-c {
    /*这是列，因为已经有了列的宽度因此无需设置width*/
  background: #f1f2f7;
  position: fixed;
  top: 60px;
  bottom: 0px;
  left: 180px;
  right: 0px;
  border-top: 1px solid RGBA(178,184,190,1);
  overflow-y: scroll;
    /*内层设置滚动*/
  padding: 10px;
}
</style>
