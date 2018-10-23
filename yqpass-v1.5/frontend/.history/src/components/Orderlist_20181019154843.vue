<template lang="html">
  <div>
  	<el-row class="container">
    	<el-col style="width: 180px;height: 100%;">
        <el-menu router :default-active="$route.path" theme="dark">
          <el-submenu>
            <template slot="title">工单管理</template>
            <el-menu-item index="/0/orderNew">新建工单</el-menu-item>
            <el-menu-item index="/0/orderUnfinished">待办工单</el-menu-item>
            <el-menu-item index="/0/orderCompleted">已办工单</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-col>
      <el-col class="panel-c-c">
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
.container {
	position: absolute;
  	height: 100%;
  	width: 100%;
}
.panel-c-c {
    /*这是列，因为已经有了列的宽度因此无需设置width*/
  background: #f1f2f7;
  position: relative;
  margin-top: 80px;
  margin-left: 180px;
  margin: auto;
  /* top: 0px;
  bottom: 0px; */
  height: 100%;
  overflow-y: scroll;
    /*内层设置滚动*/
  padding: 10px;
}
</style>
