import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { apiUrls, getFromApi } from 'utils/api.js';

function Home(props){
  const [showCreator, Creator] = useState({});

  const { id } = useParams();

  const getTeamData = async () => {
    const data = await getFromApi(apiUrls['battleDetail'](id));
    Creator({
      creator : data.creator.email,
      opponent: data.opponent.email,
      winner: data.winner
    });
    return data;
  };

  getTeamData();

  return (
    <div className="battle_container_detail">
      <h1>Battle information</h1>
      <h2 className="subtitle_detail">Creator: {showCreator.creator ? showCreator.creator : ""}</h2> 
      <h2 className="subtitle_detail">Opponent: {showCreator.opponent ? showCreator.opponent : ""}</h2>
      {showCreator.winner ?
        <>
        <img class="img_detail" src="https://image.flaticon.com/icons/png/512/2119/2119019.png" alt="trofeu"/>
        <h2 class="subtitle_detail">The winner is {showCreator.winner}</h2> 
        </> : "nulo"}
    </div>
  );
}

export default Home;
