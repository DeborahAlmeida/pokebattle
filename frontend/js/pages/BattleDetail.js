import _ from 'lodash';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams, Link } from 'react-router-dom';

import CardTeam from 'components/CardTeam';

import { getBattle } from '../actions/getBattle';
import { getCurrentUser } from '../actions/getUser';
import { orderTeamsByCurrentUser } from '../utils/battle-detail';
import { selectUserById } from '../utils/selectors';
import Urls from '../utils/urls';

function BattleDetail(props) {
  const { id } = useParams();
  const { battle, battles, currentUser, users } = props;
  useEffect(() => {
    if (!currentUser) {
      props.getCurrentUser();
    }
  }, []);

  useEffect(() => {
    if (!battles) {
      props.getBattle(id);
    }
  }, []);

  if (!battles && !battle) {
    return 'loading';
  }
  const battleDetail = battle ? battle[id] : battles[id];
  const { current, other } = orderTeamsByCurrentUser(battleDetail, currentUser, users);

  return (
    <div className="battle_container_detail">
      <h1>Battle information</h1>
      <h2 className="subtitle_detail">
        Creator: {selectUserById(users, battleDetail.creator) || ''}
      </h2>
      <h2 className="subtitle_detail">
        Opponent: {selectUserById(users, battleDetail.opponent) || ''}
      </h2>
      {battleDetail.winner ? (
        <>
          <img
            alt="trofeu"
            className="img_detail_winner"
            src="https://image.flaticon.com/icons/png/512/2119/2119019.png"
          />
          <h2 className="subtitle_detail">
            The winner is {selectUserById(users, battleDetail.winner) || ''}
          </h2>
        </>
      ) : (
        ''
      )}
      <div className="pokemons_info">
        <div>
          <p className="text_trainer">Your pokemons</p>
          {current === null ? (
            <Link className="button_battle button_battle_detail" to={Urls.team_create(id)}>
              Create your team
            </Link>
          ) : (
            <CardTeam pokemons={current.pokemons} />
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

function mapStateToProps(store) {
  const battle = _.get(store, 'battle.battleDetail', null);
  const currentUser = _.get(store, 'user.data', null);
  const battles = _.get(store, 'battle.battles', null);
  const users = _.get(store, 'battle.users', null);

  return {
    battles,
    battle,
    currentUser,
    users,
  };
}

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    getBattle: (battle) => dispatch(getBattle(battle)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
