<template lang="html">
  <el-row class="panel">
    <el-row class="top">
      <el-col :span='24' class="panel-top">
        <el-col style="width:180px; padding-left:20px; height: 100%;">
          <img src="../assets/logo1.png"  alt="log" class="img" />
        </el-col>
        <!-- <el-col :offset='1' :span='15'>
          <h2 style="text-align:left;color:#3399cc;">{{ msg }}</h2>
        </el-col> -->
        <el-col :span='6' class='rightbar'>
          <el-dropdown trigger="click"  placement="bottom-end" v-if="userInfo.name">
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
          </el-dropdown>            
        </el-col>        
        <!--<el-col :span='2' class='rightbar'>
           <el-button type="primary" @click.native="toHome" size="small">个人中心</el-button>
        </el-col>
        <el-col :span='2' class='rightbar'>        
           <el-button type="primary" @click.native="toLogin" size="small">退出登录</el-button>
        </el-col> -->      	
      </el-col>
    </el-row>
    <el-row class="top-nav">
      <el-col :span=10 :push="3">
          <el-tabs v-model="activeName" :stretch="true" @tab-click="handleClick" type="border-card">
          	<el-tab-pane v-for="(item, index) in label_list" :key="index" :label="item.title" :name="index">{{ item.title }}</el-tab-pane>
          </el-tabs>
      </el-col>
    </el-row>
    <el-row class="panel-center">
      <router-view></router-view>
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
      activeName: '0',
      msg: '园区传输资源调度系统',
      label_list: [
        {
          title: '工单管理',
        },
        {
          title: '资源管理',
        },
        {
          title: '资源展示',
        },
        {
          title: '用户管理',
        }
      ]
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
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.panel {
  position:absolute;
  top:0;
  bottom: 0;
  left: 0;
  right: 0;
  background:#ffffff;
}
.panel-top {
  height: 80px;
  background: #d3e5f3;
  color: #c0ccda;
  text-align: left;
  /* padding-left: 70px; */
}
.img{
   /* position: absolute; */
    height: 80px;
    /* width:35px; */
    /* top-left: 1px */
   left:0px;
   top:10px;
}
.rightbar {
  text-align: right;
  padding-right: 70px;
  line-height:60px;
}
.top-nav {
	height: 40px;
}
.panel-center {
  background: #324057;
  position: absolute;
  top: 120px;
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
.panel-c-c {
    /*这是列，因为已经有了列的宽度因此无需设置width*/
  background: #f1f2f7;
  position: absolute;
  right: 0px;
  top: 0px;
  bottom: 0px;
    /*内层设置滚动*/
  padding: 10px;
}
</style>
