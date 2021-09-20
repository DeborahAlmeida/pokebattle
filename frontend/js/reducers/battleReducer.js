import { BATTLE_CREATE, BATTLE_DETAIL, BATTLE_LIST } from '../constants';

const initialState = {
  battleDetail: null,
  battles: null,
  errorMessage: null,
};

export const battleReducer = (state = initialState, action) => {
  switch (action.type) {
    case BATTLE_DETAIL:
      return { ...state, battleDetail: action.payload };
    case BATTLE_LIST:
      return { ...state, battles: action.payload };
    case BATTLE_CREATE:
      if (action.payload.status !== 201) {
        return { ...state, battle: null, errorMessage: action.payload.data };
      }
      return { ...state, battle: action.payload, errorMessage: null };
    default:
      return state;
  }
};
