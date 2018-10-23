<template lang="html">
  <el-row class="panel">
    <el-row class="top">
      <el-col :span='24' class="panel-top">
        <el-col style="width:480px; padding-left:20px; height: 100%;align-items: flex-end;">
          <!-- <img src="../assets/logo1.png"  alt="log" class="img" /> -->
          <h3 style="color:#ffffff;">{{ msg }}</h3>
        </el-col>
        <el-col class='rightbar'>
          <el-menu mode="horizontal" @select="handleSelect" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
            <el-submenu>
              <template slot="title">{{userInfo.name}}</template>
              <el-menu-item index="1">个人中心</el-menu-item>
            </el-submenu>
            <el-menu-item index="2">退出系统</el-menu-item>
          </el-menu>  
            <!-- <el-dropdown trigger="click"  placement="bottom-end" v-if="userInfo.name">
            <span class="el-dropdown-link" v-model="name" style="cursor: pointer;font-weight:700l;font-size:15px;">
              欢迎您： {{userInfo.name}}<i class="el-icon-caret-bottom el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item @click.native="toPersonCenter">个人中心</el-dropdown-item>
              <el-dropdown-item @click.native="toLogin">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <el-dropdown trigger="click" placement="top" v-else>
            <span class="el-dropdown-link" v-model="name" style="cursor: pointer;font-weight:700l;font-size:15px;">
              您好，请先登录<i class="el-icon-caret-bottom el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item @click.native="firstLogin">前往登录</el-dropdown-item>
              <el-dropdown-item @click.native="firstRes">前往注册</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>             -->
        </el-col>     	
      </el-col>
    </el-row>
    <el-row class="sidebar">
    	<el-col>
        <el-menu unique-opened router @open="handleOpen" @close="handleClose" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
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
      <el-col>
      	<router-view></router-view>
      </el-col>
    </el-row>
  </el-row>
</template>

<script>
import Orderlist from '../components/Orderlist'
import Resmanagement from '../components/Resmanagement'
import PersonCenter from '@/components/PersonCenter'
import { logout,getUserDetail } from '../api/api'
import { mapGetters } from 'vuex';
export default {
  components: {
  	Orderlist,
  	Resmanagement,
  	PersonCenter
  },
  data () {
    return {
      msg: 'China Mobile - 园区传输资源调度管理系统',
    }
  },
  computed: {
  	...mapGetters({
  		userInfo: 'userInfo'
  	})
  },
  methods: {
    handleClick (tab, event) {
      console.log(tab, event);
      let urlStr = '/' + this.activeName;
      this.$router.push(urlStr);
    },
    toPersonCenter () {
	  	  getUserDetail({}).then((response)=> {
	  		if (response.data.code == 1) {
	  			this.$router.push({path: '/personcenter'})
	  		}else{
	  			return response.data.msg
	  		} 		 
	  	})    		
    },
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
      if (key == 1) {
        getUserDetail({}).then((response)=> {
	  		if (response.data.code == 1) {
	  			this.$router.push({path: '/personcenter'})
	  		}else{
	  			return response.data.msg
	  		} 		 
	  	})
      }
      if (key == 2) {
        this.$confirm('是否确定退出系统', '提示', {
    		confirmButtonText: '确定',
    		cancelButtonText: '取消',
    		type: 'warning'
    	}).then(() => {
		  	  logout({}).then((response)=> {
		  		console.log(response);
		  		if (response.data.code == 1) {
    				this.$router.push({path: '/login'})
		  		}else{
		  			return response.data.msg
		  		} 		 
		  	})   		
    	}).catch(() => {
    	});
      }
    },
    toLogin () {    	
    	this.$confirm('是否确定退出系统', '提示', {
    		confirmButtonText: '确定',
    		cancelButtonText: '取消',
    		type: 'warning'
    	}).then(() => {
		  	  logout({}).then((response)=> {
		  		console.log(response);
		  		if (response.data.code == 1) {
    				this.$router.push({path: '/login'})
		  		}else{
		  			return response.data.msg
		  		} 		 
		  	})   		
    	}).catch(() => {

    	});
    },
    firstLogin () {
    	this.$router.push({path: '/login'})
    },
    firstRes () {
    	this.$router.push({path: '/reg'})
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="css" scoped>
.panel {
  position:absolute;
  top:0;
  bottom: 5px;
  left: 0;
  right: 0;
  background:#545c64;
}
.panel-top {
  display: flex;
  justify-content: space-between;
  height: 60px;
  background: #545c64;
  /* color: #c0ccda; */
  text-align: left;
  /* padding-left: 70px; */
}
.img{
  height:60px;
  left:0px;
  top:0px;
}
.rightbar {
  width: 280px;
}
.top-nav {
	height: 40px;
}
.panel-center {
  background: #545c64;
  position: absolute;
  top: 60px;
  bottom: 0px;
  width: 100%;
  margin: auto 0;
    /*最外层要hidden*/
    /*这是行，绝对定位之后没有宽度因此必须设置width*/
}
.breadcrumb {
  margin-bottom: 10px;
}
.button_nav {
  margin-bottom: 10px;
}
.sidebar {
	position: fixed;
  top: 60px;
  bottom: 0px;
  left: 0px;
  width: 180px;
  border-top: 1px solid RGBA(178,184,190,1);
  /* z-index: 2000; */
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
