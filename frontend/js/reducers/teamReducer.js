import { TEAM_CREATE, POKEMON_CHANGE_INDEX } from '../constants';

export const teamReducer = (state = { pokemons: null }, action) => {
  console.log('ta chegando no reducer', action);
  switch (action.type) {
    case TEAM_CREATE:
      return { ...state, pokemons: action.payload };
    case POKEMON_CHANGE_INDEX:
      return { ...state, pokemons: action.payload };
    default:
      return state;
  }
};
