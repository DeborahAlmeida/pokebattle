import { BATTLE_DETAIL } from '../constants';

const initialState = {
  battle: null,
};

export const battleReducer = (state = initialState, action) => {
  switch (action.type) {
    case BATTLE_DETAIL:
      return { ...state, battle: action.payload };
    default:
      return state;
  }
};
