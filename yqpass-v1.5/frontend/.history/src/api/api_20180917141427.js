import axios from 'axios'

let host = 'api';

//获取CSRF TOKEN
export const getToken = () => {
	return axios.get(`${host}/accounts/get_token/`)
}

//登录
export const login = params => {
	return axios.post(`${host}/accounts/login/`, params, {headers: {'Content-Type': 'application/json'}})
}

//注册
export const register = params => {
	return axios.post(`${host}/accounts/register/`, params)
}

//注销
export const logout = () => {
	return axios.get(`${host}/accounts/logout/`)
}

//获取用户信息
export const getUserDetail = () => {
	return axios.get(`${host}/accounts/account_change/`)
}

//修改用户信息
export const updateUserInfo = params => {
	return axios.post(`${host}/accounts/account_change/`, params)
}

//修改密码
export const changePass = params => {
	return axios.post(`${host}/accounts/password_change/`, params)
}

//获取工单列表
export const getTicketList = params => {
	return axios.get(`${host}/tickets/`, params)
}

//新建工单
export const postTicketList = params => {
	return axios.post(`${host}/tickets/`, params)
}

//获取工作流初始状态
export const getWorkflowInitState = () => {
	return axios.get(`${host}/workflow/1/init_state/`)
}

//获取工单详情
export const getTicketDetail = (id) => {
	return axios.get(`${host}/tickets/`+id)
}

//处理工单
export const dealTicket = (id,params) => {
	return axios.post(`${host}/tickets/`+id+`/`, params)
}

//获取工单流转记录
export const getTicketFlowlogs = (id,params) => {
	return axios.get(`${host}/tickets/`+id+`/flowlogs/`, params)
}