import { getPokemonsFromApi, createTeam, getPokemonList } from 'utils/api';

import { TEAM_CREATE, GET_POKEMONS_FROM_API, POKEMON_LIST } from '../constants';
import { changeIndex } from '../utils/pokemons';

function getPokemonsFromApiAction(data) {
  return (dispatch) =>
    getPokemonsFromApi(data).then((response) => {
      return dispatch({ type: GET_POKEMONS_FROM_API, payload: response });
    });
}

function changePokemonsIndex(data) {
  const pokemonsNewIndex = changeIndex(data);
  return (dispatch) => dispatch({ type: GET_POKEMONS_FROM_API, payload: pokemonsNewIndex });
}

function createTeamAction(data) {
  return (dispatch) =>
    createTeam(data).then((response) => {
      return dispatch({ type: TEAM_CREATE, payload: response });
    });
}

function getPokemonListAction() {
  return (dispatch) =>
    getPokemonList().then((response) => {
      return dispatch({ type: POKEMON_LIST, payload: response });
    });
}
export { getPokemonsFromApiAction, changePokemonsIndex, createTeamAction, getPokemonListAction };
