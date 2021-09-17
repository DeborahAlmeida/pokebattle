import { TEAM_CREATE, GET_POKEMONS_FROM_API, POKEMON_LIST } from '../constants';

export const teamReducer = (
  state = { pokemons: null, errorMessage: null, team: null, pokemonList: null },
  action
) => {
  switch (action.type) {
    case GET_POKEMONS_FROM_API:
      return { ...state, pokemons: action.payload };
    case TEAM_CREATE:
      if (action.payload.status !== 201) {
        return { ...state, team: null, errorMessage: action.payload.data };
      }
      return { ...state, team: action.payload, errorMessage: null };
    case POKEMON_LIST:
      return { ...state, pokemonList: action.payload };
    default:
      return state;
  }
};
