import { getPokemonsFromApi } from 'utils/api';

import { TEAM_CREATE } from '../constants';
import { changeIndex } from '../utils/pokemons';

function createTeamAction(data) {
  return (dispatch) =>
    getPokemonsFromApi(data).then((response) => {
      return dispatch({ type: TEAM_CREATE, payload: response });
    });
}

function changePokemonsIndex(data) {
  console.log('ta chegando na aciton', data);
  const pokemonsNewIndex = changeIndex(data);
  return (dispatch) => dispatch({ type: TEAM_CREATE, payload: pokemonsNewIndex });
}
export { createTeamAction, changePokemonsIndex };
