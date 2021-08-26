import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';

import CardTeam from 'components/CardTeam';
import { createTeamUrl } from 'utils/api';

import { fetchBattle } from '../actions/setBattle';
import { setCurrentUser } from '../actions/setUser';
import { showTeams } from '../utils/battle-detail';

function BattleDetail(props) {
  const { id } = useParams();
  useEffect(() => {
    props.setCurrentUser();
    props.fetchBattle(id);
  }, []);
  const { battle } = props.battle;
  const { user } = props.user;
  if (!battle) {
    return '';
  }
  const teams = showTeams(battle, user);

  const currentUserTeam = teams[0];
  const otherUserTeam = teams[1];

  return (
    <div className="battle_container_detail">
      <h1>Battle information</h1>
      <h2 className="subtitle_detail">Creator: {battle.creator ? battle.creator.email : ''}</h2>
      <h2 className="subtitle_detail">Opponent: {battle.opponent ? battle.opponent.email : ''}</h2>
      {battle.winner ? (
        <>
          <img
            alt="trofeu"
            className="img_detail_winner"
            src="https://image.flaticon.com/icons/png/512/2119/2119019.png"
          />
          <h2 className="subtitle_detail">
            The winner is {battle.winner ? battle.winner.email : ''}
          </h2>
        </>
      ) : (
        ''
      )}
      <div className="pokemons_info">
        <div>
          <p className="text_trainer">Your pokemons</p>
          {currentUserTeam === null ? (
            <a
              className="button_battle button_battle_detail"
              href={createTeamUrl(battle.id)}
              role="button"
            >
              Create your team
            </a>
          ) : (
            <CardTeam pokemons={currentUserTeam.pokemons} />
          )}
        </div>
        <div>
          <p className="text_trainer">Opposing pokemons</p>
          {otherUserTeam === null ? 'No pokemons' : <CardTeam pokemons={otherUserTeam.pokemons} />}
        </div>
      </div>
    </div>
  );
}

const mapStateToProps = (store) => ({
  battle: store.battle,
  user: store.user,
});

const mapDispatchToProps = (dispatch) => {
  return {
    setCurrentUser: () => dispatch(setCurrentUser()),
    fetchBattle: (battle) => dispatch(fetchBattle(battle)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
