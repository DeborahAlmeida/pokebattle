import {
  BATTLE_DETAIL_STARTED,
  BATTLE_DETAIL_SUCCESSED,
  BATTLE_DETAIL_FAILED,
  BATTLE_LIST,
} from '../constants';

const initialState = {
  battle: null,
  battles: null,
  loading: false,
  error: null,
};

export const battleReducer = (state = initialState, action) => {
  switch (action.type) {
    case BATTLE_DETAIL_STARTED:
      return { ...state, loading: true };
    case BATTLE_DETAIL_SUCCESSED:
      return { ...state, loading: false, battle: action.payload };
    case BATTLE_DETAIL_FAILED:
      return { ...state, loading: false, err: action.error };
    case BATTLE_LIST:
      return { ...state, battles: action.payload };
    default:
      return state;
  }
};
