import { BATTLE_LIST } from '../constants';

export const battleListReducer = (state = {}, action) => {
  switch (action.type) {
    case BATTLE_LIST:
      return { ...state, battleList: action.payload };
    default:
      return state;
  }
};
