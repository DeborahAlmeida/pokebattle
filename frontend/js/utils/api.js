import axios from 'axios';

import Urls from './urls';

const baseUrl = window.location.host;

const getFromApi = (urlApi) => {
  const url = `http://${baseUrl}${urlApi}`;
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

export { getFromApi, getCurrentUserData, getTeamData, getBattles };
