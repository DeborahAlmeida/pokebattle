import axios from 'axios';
import { ErrorMessage } from 'formik';
import _ from 'lodash';

import Urls from './urls';

const baseUrl = window.location.host;

const baseProtocolHTTPS = 'https';
const baseProtocolHTTP = 'http';

const getFromApi = (urlApi) => {
  const pokeProtocol = baseUrl === 'localhost:8000' ? baseProtocolHTTP : baseProtocolHTTPS;
  const url = `${pokeProtocol}://${baseUrl}${urlApi}`;
  const response = axios.get(url).then((res) => {
    return res.data;
  });
  return response;
};

const getCurrentUserData = async () => {
  const user = await getFromApi(Urls.api_current_user());
  return user;
};

const getTeamData = async (id) => {
  const data = await getFromApi(Urls.api_battle_detail(id));
  return data;
};

const getBattles = async () => {
  const data = await getFromApi(Urls.api_battle_list());
  return data;
};

const createBattle = async (battle) => {
  const battleData = {
    creator: _.get(battle, 'creator', null),
    opponent: _.get(battle, 'opponent', null),
  };
  const data = await connectToApi(Urls.api_battle_create(), battleData);
  return data;
};

const connectToApi = (urlApi, data) => {
  const tokenCSRF = getCookie('csrftoken');

  if (tokenCSRF) {
    const battleProtocol = baseUrl === 'localhost:8000' ? baseProtocolHTTP : baseProtocolHTTPS;

    const urlBattle = `${battleProtocol}://${baseUrl}${urlApi}`;

    const response = axios
      .post(urlBattle, data, { headers: { 'X-CSRFToken': tokenCSRF } })
      .then((response) => {
        return response;
      })
      .catch((error) => {
        return handleError(error);
      });
    return response;
  }
  return null;
};

const handleError = (error) => {
  const errorMessage = Object.values(error.response.data);
  if (error.response.status === 400) {
    error.response.data = { detail: errorMessage[0][0] };
  }
  if (error.response.status === 403) {
    error.response.data = { detail: 'You need to be logged' };
  }
  return error.response;
};
const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (const element of cookies) {
      const cookie = element.trim();
      if (cookie.slice(0, Math.max(0, name.length + 1)) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.slice(Math.max(0, name.length + 1)));
        break;
      }
    }
  }
  return cookieValue;
};

const getPokemonFromApi = (pokemon) => {
  const url = `https://pokeapi.co/api/v2/pokemon/${pokemon}`;
  const response = axios.get(url).then((res) => {
    const pokemonData = {
      defense: _.get(res, 'data.stats[2].base_stat', null),
      attack: _.get(res, 'data.stats[1].base_stat', null),
      hp: _.get(res, 'data.stats[0].base_stat', null),
      name: _.get(res, 'data.name', null),
      imgUrl: _.get(res, 'data.sprites.front_default', null),
      pokemonId: _.get(res, 'data.id', null),
    };
    return pokemonData;
  });
  return response;
};

const getPokemonsFromApi = async (pokemons) => {
  const pokemonsNames = Object.values(pokemons);
  const pokemon1 = await getPokemonFromApi(pokemonsNames[0]);
  const pokemon2 = await getPokemonFromApi(pokemonsNames[1]);
  const pokemon3 = await getPokemonFromApi(pokemonsNames[2]);

  return { pokemon1, pokemon2, pokemon3 };
};

const createTeam = async (team) => {
  let teamArray = team.pokemons;
  const validateObject = _.get(team, 'pokemons.pokemon3.name', null);
  if (validateObject) {
    teamArray = Object.values(team.pokemons);
  }
  const teamData = {
    battle: _.get(team, 'id', null),
    trainer: String(_.get(team, 'user.id', null)),
    pokemon_1: _.get(teamArray, '[0].name', null),
    pokemon_2: _.get(teamArray, '[1].name', null),
    pokemon_3: _.get(teamArray, '[2].name', null),
    position_pkn_1: 1,
    position_pkn_2: 2,
    position_pkn_3: 3,
  };
  const data = await connectToApi(Urls.api_team_create(), teamData);
  return data;
};

export {
  getCurrentUserData,
  getTeamData,
  getBattles,
  createBattle,
  getCookie,
  getPokemonFromApi,
  getPokemonsFromApi,
  createTeam,
};
