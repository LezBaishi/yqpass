import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/components/Layout'
import Login from '@/components/Login'
import Reg from '@/components/Reg'
import ForgetPass from '@/components/ForgetPass'
import PersonCenter from '@/components/PersonCenter'
import PersonInfor from '@/components/PersonInfor'
import PersonChangepass from '@/components/PersonChangepass'
import Orderlist from '../components/Orderlist'
import Resmanagement from '../components/Resmanagement'
import OrderlistUnfinished from '../components/OrderlistUnfinished'
import OrderlistNew from '../components/OrderlistNew'
import OrderDetailUnfinished from '../components/OrderDetailUnfinished'
import ResCable from '../components/ResCable'
import ResCircuit from '../components/ResCircuit'
import ResCableDetail from '../components/ResCableDetail'
import OrderlistCompleted from '../components/OrderlistCompleted'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/', 
      redirect: '/0/orderUnfinished',
      name: 'Layout',
      component: Layout,
      children: [
      {
      	path: '0',
      	component: Orderlist,
      	redirect: '/0/orderUnfinished',
      	children:[
      	{
      		path: 'orderNew',
      		component: OrderlistNew
      	},
      	{
      		path: 'orderUnfinished',
      		component: OrderlistUnfinished
      	},
      	{
      		path: 'orderCompleted',
      		component: OrderlistCompleted
      	},
        {
          path: 'OrderDetailUnfinished',
          component: OrderDetailUnfinished
        }]
      },
      {
      	path: '1',
      	component: Resmanagement,
      	redirect: '/1/resCable',
      	children:[
      	{
      		path: 'resCable',
      		component: ResCable
      	},
      	{
      		path: 'resCircuit',
      		component: ResCircuit
      	},
      	{
      		path: 'resCableDetail',
      		component: ResCableDetail
      	}]
      },
    {
      path: 'personcenter',
      component: PersonCenter,
      redirect: '/personcenter/infor',
      children: [
      {
      	path: 'infor',
      	component: PersonInfor
      },
      {
      	path: 'changepass',
      	component: PersonChangepass
      }]
    },      ]
    },
    {
      path: '/reg',
      name: 'Reg',
      component: Reg
    },
    {
      path: '/forgetpass',
      name: 'ForgetPass',
      component: ForgetPass
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})
