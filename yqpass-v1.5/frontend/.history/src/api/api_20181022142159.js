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

//获取用户列表
export const getUserList = params => {
	return axios.get(`${host}/accounts/user_list/`, params)
}

//获取用户详情
export const getUserDetailInfo = (id) => {
	return axios.get(`${host}/accounts/`+id+`/user_detail/`)
}

//删除用户
export const deleteUser = params => {
	return axios.post(`${host}/accounts/user_delete/`, params)
}

//获取角色列表
export const getRoleList = params => {
	return axios.get(`${host}/accounts/role_list/`, params)
}

//获取角色详情
export const getRoleDetail = (id) => {
	return axios.get(`${host}/accounts/`+id+`/role_detail/`)
}

//删除角色
export const deleteRole = params => {
	return axios.post(`${host}/accounts/role_delete/`, params)
}

//获取部门列表
export const getDeptList = params => {
	return axios.get(`${host}/accounts/dept_list/`, params)
}

//获取部门详情
export const getDeptDetail = (id) => {
	return axios.get(`${host}/accounts/`+id+`/dept_detail/`)
}

//删除部门
export const deleteDept = params => {
	return axios.post(`${host}/accounts/dept_delete/`, params)
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

//获取工单处理步骤信息
export const getTicketFlowsteps = (id) => {
	return axios.get(`${host}/tickets/`+id+`/flowsteps/`)
}

//获取楼栋机房信息列表
export const getBuildingRoomList = params => {
	return axios.get(`${host}/resmanage/building_room/`, params)
}

//获取光缆段（视图）列表
export const getCableList = params => {
	return axios.get(`${host}/resmanage/ocable_section/`, params)
}

//获取纤芯（视图）列表
export const getCableDetailList = params => {
	return axios.get(`${host}/resmanage/ofiber_core/`, params)
}

//新建光缆段
export const newCableList = (params) => {
	return axios.post(`${host}/resmanage/ocable_section/`, params)
}

//编辑光缆段
export const editCableList = (id,params) => {
	return axios.post(`${host}/resmanage/`+id+`/ocable_section/`, params)
}

//删除光缆段
export const delCableList = (params) => {
	return axios.post(`${host}/resmanage/ocable_section/delete/`, params)
}