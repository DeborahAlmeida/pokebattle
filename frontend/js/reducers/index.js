import { combineReducers } from 'redux';

import { battleListReducer } from './battleListReducer';
import { battleReducer } from './battleReducer';
import { userReducer } from './userReducer';

export const reducers = combineReducers({
  battle: battleReducer,
  user: userReducer,
  battleListState: battleListReducer,
});
