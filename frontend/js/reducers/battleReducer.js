import { BATTLE_DETAIL, BATTLE_LIST } from '../constants';

const initialState = {
  battleDetail: null,
  battles: null,
  users: null,
  pokemons: null,
};

export const battleReducer = (state = initialState, action) => {
  switch (action.type) {
    case BATTLE_DETAIL:
      return {
        ...state,
        battleDetail: action.payload.entities.battle,
        users: action.payload.entities.user,
        pokemons: action.payload.entities.pokemon,
      };
    case BATTLE_LIST:
      return {
        ...state,
        battles: action.payload.entities.battle,
        users: action.payload.entities.user,
        pokemons: action.payload.entities.pokemon,
      };
    default:
      return state;
  }
};
