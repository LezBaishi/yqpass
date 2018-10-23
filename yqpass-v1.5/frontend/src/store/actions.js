import * as types from './mutation-types';
// 提交mutation
function makeAction (type) {
  return ({ commit }, ...args) => commit(type, ...args);
};

export const setInfo = makeAction(types.SET_INFO);