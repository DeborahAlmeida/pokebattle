import _ from 'lodash';
import { denormalize } from 'normalizr';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { getBattleList } from '../actions/getBattleList';
import { getCurrentUser } from '../actions/getUser';
import Urls from '../utils/urls';

function BattleList(props) {
  const { currentUser, settledBattles, onGoingBattles } = props;

  useEffect(() => {
    if (!currentUser) {
      props.getCurrentUser();
    }
    props.getBattleList();
  }, []);
  if (!(settledBattles && onGoingBattles)) {
    return (
      <div className="battle_container_detail">
        <h1>Your Battles</h1>
        {!currentUser ? (
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
      {!currentUser ? (
        <h2 className="subtitle">You need to be logged</h2>
      ) : (
        <h2 className="subtitle">Click to see more information</h2>
      )}
      <ul className="list_battle">
        <div className="settled">
          <h3>Settled battles</h3>
          {settledBattles.map((battle) => {
            return (
              <li key={battle.id} className="item">
                <Link className="battle_settled" to={Urls.battle_detail_v2(battle.id)}>
                  Battle ID {battle.id}
                </Link>
              </li>
            );
          })}
        </div>

        <div className="your_opponent">
          <h3>On goind Battles</h3>
          {onGoingBattles.map((battle) => {
            return (
              <li key={battle.id} className="item">
                <Link className="battle_ongoing" to={Urls.battle_detail_v2(battle.id)}>
                  Battle ID {battle.id}
                </Link>
              </li>
            );
          })}
        </div>
      </ul>
    </div>
  );
}

function mapStateToProps(store) {
  const currentUser = _.get(store, 'user.data', null);
  const battlesData = _.get(store, 'battle.battles', null);

  let settledBattles;
  let onGoingBattles;
  if (battlesData) {
    settledBattles = Object.values(battlesData).filter((battle) => {
      return battle.winner;
    });
    onGoingBattles = Object.values(battlesData).filter((battle) => {
      return !battle.winner;
    });
  }
  // console.log('>>>>', settledBattles, onGoingBattles);
  // if (battlesData) {
  //   battles = denormalize(
  //     _.get(battlesData, 'result', null),
  //     battlesSchema,
  //     _.get(battlesData, 'entities', null)
  //   );
  // }
  return {
    settledBattles,
    onGoingBattles,
    currentUser,
  };
}

const mapDispatchToProps = (dispatch) => {
  return {
    getCurrentUser: () => dispatch(getCurrentUser()),
    getBattleList: () => dispatch(getBattleList()),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(BattleList);
