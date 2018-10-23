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
import OrderDetailCompleted from '../components/OrderDetailCompleted'
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
          name: 'OrderNew',
      		component: OrderlistNew
      	},
      	{
          path: 'orderUnfinished',
          name: 'OrderUnfinished',
      		component: OrderlistUnfinished
      	},
      	{
          path: 'orderCompleted',
          name: 'OrderCompleted',
      		component: OrderlistCompleted
      	},
        {
          path: 'OrderDetailUnfinished',
          name: 'OrderDetailUnfinished',
          component: OrderDetailUnfinished
        },
        {
          path: 'OrderDetailCompleted',
          name: 'OrderDetailCompleted',
          component: OrderDetailCompleted
        }]
      },
      {
      	path: '1',
      	component: Resmanagement,
      	redirect: '/1/resCable',
      	children:[
      	{
          path: 'resCable',
          name: 'ResCable',
      		component: ResCable
      	},
      	{
          path: 'resCircuit',
          name: 'ResCircuit',
      		component: ResCircuit
      	},
      	{
          path: 'resCableDetail',
          name: 'ResCableDetail',
      		component: ResCableDetail
      	}]
      },
    {
      path: 'personcenter',
      name: 'Personcenter',
      component: PersonCenter,
      redirect: '/personcenter/infor',
      children: [
      {
        path: 'infor',
        name: 'Infor',
      	component: PersonInfor
      },
      {
        path: 'changepass',
        name: 'Changepass',
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

<!-- Router.beforeEach(function (to, from, next) {
  const nextRoute = ['OrderNew', 'OrderUnfinished', 'OrderCompleted', 'OrderDetailUnfinished', 'OrderDetailCompleted', 'ResCable', 'ResCircuit', 'ResCableDetail', 'Infor', 'Changepass'];
  const auth = store.state.userInfo;
  if (nextRoute.indexOf(to.name) >= 0) {
    if (!store.state.userInfo) {
      Router.push({name: 'Login'})
    }
  }
  if (to.name == 'Login') {
    if (store.state.userInfo) {
      Router.push({name: 'Layout'})
    }
  }
}) -->