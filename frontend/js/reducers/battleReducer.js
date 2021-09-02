import { BATTLE_DETAIL, BATTLE_LIST } from '../constants';

const initialState = {
  battle: null,
  battles: null,
};

export const battleReducer = (state = initialState, action) => {
  switch (action.type) {
    case BATTLE_DETAIL:
      return { ...state, battle: action.payload };
    case BATTLE_LIST:
      return { ...state, battles: action.payload };
    default:
      return state;
  }
};

// const battles = new schema.Entity('');
