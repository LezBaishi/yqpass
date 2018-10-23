<template lang="html">
  <div>
  	<el-row class="container">
  	<el-col :span="3">
        <el-menu router :default-active="$route.path" theme="dark">
          <el-submenu>
            <template slot="title">用户管理</template>
            <el-menu-item index="/3/userList">用户列表</el-menu-item>
            <el-menu-item index="/3/roleList">角色列表</el-menu-item>
            <el-menu-item index="/3/deptList">部门列表</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-col>
      <el-col :span="21" class="panel-c-c">
      	<router-view></router-view>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import UserList from '../components/UserList'
import RoleList from '../components/RoleList'
import DeptList from '../components/DeptList'
export default {
  components: {
  	UserList,
  	RoleList,
  	DeptList
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
.panel-c-c {
    /*这是列，因为已经有了列的宽度因此无需设置width*/
  background: #f1f2f7;
  position: absolute;
  right: 0px;
  top: 0px;
  bottom: 0px;
  height: 100%;
  overflow-y: scroll;
    /*内层设置滚动*/
  padding: 10px;
}
</style>
