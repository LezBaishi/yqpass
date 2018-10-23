<template lang="html">
  <div>
  	<el-row class="container">
  	<el-col :span="4">
        <el-menu router :default-active="$route.path" theme="dark" @open="handleOpen" @close="handleClose">
          <el-submenu>
            <template slot="title">个人中心</template>
            <el-menu-item index="/personcenter/infor">个人信息</el-menu-item>
            <el-menu-item index="/personcenter/changepass">修改密码</el-menu-item>
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
