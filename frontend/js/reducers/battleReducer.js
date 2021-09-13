import { BATTLE_DETAIL, BATTLE_LIST } from '../constants';

const initialState = {
  battleDetail: null,
  battles: null,
};

export const battleReducer = (state = initialState, action) => {
  switch (action.type) {
    case BATTLE_DETAIL:
      return { ...state, battleDetail: action.payload };
    case BATTLE_LIST:
      return { ...state, battles: action.payload };
    default:
      return state;
  }
};
