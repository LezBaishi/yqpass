// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import axios from 'axios'

import store from '../store/store'

import * as types from '../store/mutation-types';
import router from '../router'

axios.defaults.withCredentials = true

// 创建axios实例
const service = axios.create({
	 timeout: 5000, // 请求的超时时间
	 withCredentials: true // 允许携带cookie
})

// request拦截器
service.interceptors.request.use(
 config => {
 // 发送请求之前，要做的业务
 	if (config.method=='post') {
 		config.headers['Content-Type'] = application/json
 	}
 	return config
 },
 error => {
 // 错误处理代码
  
 return Promise.reject(error)
 }
)

// response拦截器
service.interceptors.response.use(
 response => {
 // 数据响应之后，要做的业务
 return response
 },
 error => {
 return Promise.reject(error)
 }
)
export default service