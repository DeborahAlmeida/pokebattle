import { combineReducers } from 'redux';

import { battleReducer } from './battleReducer';
import { userReducer } from './userReducer';

export const reducers = combineReducers({
  battle: battleReducer,
  user: userReducer,
});
