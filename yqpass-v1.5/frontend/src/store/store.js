// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'

import mutations from './mutations';
import * as actions from './actions';
import * as getters from './getters';

Vue.use(Vuex);

import cookie from '../static/js/cookie'

const userInfo = {
	name:cookie.getCookie('name')||'',
	token:cookie.getCookie('token')||''
}

const state = {
	userInfo
}

export default new Vuex.Store({
	state,
	mutations,
	actions,
	getters
});