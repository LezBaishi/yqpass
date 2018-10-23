import axios from 'axios'

let host = 'api';

//获取CSRF TOKEN
export const getToken = () => {
	return axios.get(`${host}/accounts/get_token/`)
}

//登录
export const login = params => {
	return axios.post(`${host}/accounts/login/`, params)
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