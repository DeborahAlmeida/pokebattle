import { TEAM_CREATE, GET_POKEMONS_FROM_API } from '../constants';

export const teamReducer = (state = { pokemons: null, errorMessage: null, team: null }, action) => {
  console.log('ta chegando no reducer', action);
  switch (action.type) {
    case GET_POKEMONS_FROM_API:
      return { ...state, pokemons: action.payload };
    case TEAM_CREATE:
      if (action.payload.status !== 201) {
        return { ...state, team: null, errorMessage: action.payload.data };
      }
      return { ...state, team: action.payload, errorMessage: null };
    default:
      return state;
  }
};
