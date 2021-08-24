import { combineReducers } from 'redux';

import { battleReducer } from './battleReducer';
import { userReducer } from './userReducer';

export const Reducers = combineReducers({
  battleState: battleReducer,
  userState: userReducer,
});
