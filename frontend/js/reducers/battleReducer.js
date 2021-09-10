import { BATTLE_CREATE, BATTLE_DETAIL, BATTLE_LIST } from '../constants';

const initialState = {
  battle: null,
  battles: null,
  errorMessage: null,
};

export const battleReducer = (state = initialState, action) => {
  switch (action.type) {
    case BATTLE_DETAIL:
      return { ...state, battle: action.payload };
    case BATTLE_LIST:
      return { ...state, battles: action.payload };
    case BATTLE_CREATE:
      console.log('>>> no reducer', action.payload);
      return { ...state, battle: action.payload };
    default:
      return state;
  }
};
