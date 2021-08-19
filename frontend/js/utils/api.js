import axios from "axios";

const baseUrl = window.location.host;

const apiUrls = {
    battleDetail: (id) => (`api/battle/${id}`)
}

const getFromApi = (urlApi) => {
    const url = `http://${baseUrl}/${urlApi}`
    const response = axios.get(url)
      .then(res => {
        return res.data
      })
    return response
}

export { apiUrls, getFromApi };