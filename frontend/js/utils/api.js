import axios from 'axios';

import Urls from './urls';

const baseUrl = window.location.host;

const createTeamUrl = (id) => {
  const url = `http://${baseUrl}/team/${id}/create/`;
  return url;
};

const getFromApi = (urlApi) => {
  const url = `http://${baseUrl}${urlApi}`;
  const response = axios.get(url).then((res) => {
    return res.data;
  });
  return response;
};

const getCurrentUserData = async (setCurrentUser) => {
  const user = await getFromApi(Urls['current-user']());
  setCurrentUser(user);
  return user;
};

const getTeamData = async (id, setBattle) => {
  const data = await getFromApi(Urls['battle-detail'](id));
  setBattle(data);
  return data;
};

export { getFromApi, createTeamUrl, getCurrentUserData, getTeamData };
