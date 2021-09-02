import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';

import CardTeam from 'components/CardTeam';

import { getBattle } from '../actions/getBattle';
import { getCurrentUser } from '../actions/getUser';
import { orderTeamsByCurrentUser } from '../utils/battle-detail';
import Urls from '../utils/urls';

function BattleDetail(props) {
  const { id } = useParams();
  const { battle } = props.battle;
  const { user } = props.user;

  useEffect(() => {
    if (!user) {
      props.getCurrentUser();
    }
    props.getBattle(id);
  }, []);

  if (!battle) {
    return '';
  }
  const battleDetail = battle.entities.battle[id];
  const trainerDetail = battle.entities.user;
  const pokemonsDetail = battle.entities.pokemon;
  const { current, other } = orderTeamsByCurrentUser(battleDetail, user, trainerDetail);

  return (
    <div className="battle_container_detail">
      <h1>Battle information</h1>
      <h2 className="subtitle_detail">
        Creator: {battleDetail.creator ? trainerDetail[battleDetail.creator].email : ''}
      </h2>
      <h2 className="subtitle_detail">
        Opponent: {battleDetail.opponent ? trainerDetail[battleDetail.opponent].email : ''}
      </h2>
      {battle.winner ? (
        <>
          <img
            alt="trofeu"
            className="img_detail_winner"
            src="https://image.flaticon.com/icons/png/512/2119/2119019.png"
          />
          <h2 className="subtitle_detail">
            The winner is {battleDetail.winner ? trainerDetail[battleDetail.winner].email : ''}
          </h2>
        </>
      ) : (
        ''
      )}
      <div className="pokemons_info">
        <div>
          <p className="text_trainer">Your pokemons</p>
          {current === null ? (
            <a
              className="button_battle button_battle_detail"
              href={Urls.team_create(battleDetail.id)}
              role="button"
            >
              Create your team
            </a>
          ) : (
            <CardTeam pokemonsDetail={pokemonsDetail} pokemonsIds={current.pokemons} />
          )}
        </div>
        <div>
          <p className="text_trainer">Opposing pokemons</p>
          {other === null ? 'No pokemons' : <CardTeam pokemons={other.pokemons} />}
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
    getCurrentUser: () => dispatch(getCurrentUser()),
    getBattle: (battle) => dispatch(getBattle(battle)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
