import { CURRENT_USER } from '../constants';

export const userReducer = (state = { user: null }, action) => {
  switch (action.type) {
    case CURRENT_USER:
      return { ...state, user: action.payload };
    default:
      return state;
  }
};
