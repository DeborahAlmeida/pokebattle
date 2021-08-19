import React, { useState } from 'react';

import { useParams } from 'react-router-dom';

import { apiUrls, getFromApi } from 'utils/api.js';

function Home(){
  const [battle, setBattle] = useState();

  const { id } = useParams();

  const getTeamData = async () => {
    const data = await getFromApi(apiUrls.battleDetail(id));
    setBattle(data);
    return data;
  };
  console.log(battle)
  getTeamData();
  if (!battle){
    return 'loading'
  }
  return (
    <div className="battle_container_detail">
      <h1>Battle information</h1>
      <h2 className="subtitle_detail">Creator: {battle.creator ? battle.creator.email : ''}</h2> 
      <h2 className="subtitle_detail">Opponent: {battle.opponent ? battle.opponent.email : ''}</h2>
      {battle.winner ?
        <>
        <img className="img_detail" src="https://image.flaticon.com/icons/png/512/2119/2119019.png" alt="trofeu"/>
        <h2 className="subtitle_detail">The winner is {battle.winner ? battle.winner.email : ''}</h2> 
        </> : 'nulo'}
    </div>
  );
}

export default Home;
