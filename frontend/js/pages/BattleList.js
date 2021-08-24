import React, { useEffect } from 'react';
import { connect } from 'react-redux';

import { fetchBattleList } from '../actions/getBattleList';
import { setCurrentUser } from '../actions/setUser';
import Urls from '../utils/urls';

function BattleList(props) {
  useEffect(() => {
    props.setCurrentUser();
    props.fetchBattleList();
  }, []);
  const { user } = props.user;
  const { battleList } = props.battles;

  if (!battleList) {
    return (
      <div className="battle_container_detail">
        <h1>Your Battles</h1>
        {!user ? (
          <h2 className="subtitle">You need to be logged</h2>
        ) : (
          <h2 className="subtitle">There are no battle in the database.</h2>
        )}
      </div>
    );
  }
  return (
    <div className="battle_container_detail">
      <h1>Your Battles</h1>
      {!user ? (
        <h2 className="subtitle">You need to be logged</h2>
      ) : (
        <h2 className="subtitle">Click to see more information</h2>
      )}
      <ul className="list_battle">
        <div className="settled">
          <h3>Settled battles</h3>
          {battleList.map((battle) =>
            battle.winner ? (
              <li key={battle.id} className="item">
                <a className="battle_settled" href={Urls.spa_template(battle.id)}>
                  Battle ID {battle.id}
                </a>
              </li>
            ) : null
          )}
        </div>

        <div className="your_opponent">
          <h3>On goind Battles</h3>
          {battleList.map((battle) =>
            !battle.winner ? (
              <li key={battle.id} className="item">
                <a className="battle_ongoing" href={Urls.spa_template(battle.id)}>
                  Battle ID {battle.id}
                </a>
              </li>
            ) : null
          )}
        </div>
      </ul>
    </div>
  );
}

const mapStateToProps = (store) => ({
  battles: store.battleListState,
  user: store.userState,
});

const mapDispatchToProps = (dispatch) => {
  return {
    setCurrentUser: () => dispatch(setCurrentUser()),
    fetchBattleList: () => dispatch(fetchBattleList()),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(BattleList);
