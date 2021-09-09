import axios from 'axios';

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
  const data = await connectToApi(Urls.api_battle_create(), battle);
  return data;
};

const connectToApi = (urlApi, battleData) => {
  const tokenCSRF = getCookie('csrftoken');

  if (tokenCSRF) {
    const battleProtocol = baseUrl === 'localhost:8000' ? baseProtocolHTTP : baseProtocolHTTPS;

    const urlBattle = `${battleProtocol}://${baseUrl}${urlApi}`;
    const data = { creator: battleData.creator, opponent: battleData.opponent };

    const response = axios
      .post(urlBattle, data, { headers: { 'X-CSRFToken': tokenCSRF } })
      .then((response) => {
        console.log(response);
        return response;
      })
      .catch((error) => {
        console.log(error);
      });
    return response;
  }
  return null;
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

export { getCurrentUserData, getTeamData, getBattles, createBattle, getCookie };
