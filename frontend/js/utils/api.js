import axios from 'axios';

import Urls from './urls';

const baseUrl = window.location.host;

const createTeamUrl = (id) => {
  const urlTeam = Urls.team_create(id);
  const url = `http://${baseUrl}${urlTeam}`;
  return url;
};

const getFromApi = (urlApi) => {
  const url = `http://${baseUrl}${urlApi}`;
  const response = axios.get(url).then((res) => {
    return res.data;
  });
  return response;
};

const getCurrentUserData = async () => {
  const user = await getFromApi(Urls['current-user']());
  return user;
};

const getTeamData = async (id) => {
  const data = await getFromApi(Urls['battle-detail'](id));
  return data;
};

export { getFromApi, createTeamUrl, getCurrentUserData, getTeamData };
