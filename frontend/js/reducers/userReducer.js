import { CURRENT_USER } from '../constants';

export const userReducer = (state = { data: null }, action) => {
  switch (action.type) {
    case CURRENT_USER:
      return { ...state, data: action.payload };
    default:
      return state;
  }
};
