import { selectUserById } from './selectors';

const orderTeamsByCurrentUser = (battle, user, usersEntity) => {
  console.log('>>>>>>>>>>>>>> users', usersEntity, user, battle);
  let currentUserTeam = null;
  let otherUserTeam = null;
  if (battle.teams.length === 1) {
    currentUserTeam =
      selectUserById(usersEntity, battle.teams[0].trainer) === user.email ? battle.teams[0] : null;
    otherUserTeam = currentUserTeam === null ? battle.teams[0] : null;
  } else if (battle.teams.length === 2) {
    currentUserTeam =
      selectUserById(usersEntity, battle.teams[0].trainer) === user.email
        ? battle.teams[0]
        : battle.teams[1];
    otherUserTeam = currentUserTeam === battle.teams[0] ? battle.teams[1] : battle.teams[0];
  }
  return {
    current: currentUserTeam,
    other: otherUserTeam,
  };
};

export { orderTeamsByCurrentUser };
