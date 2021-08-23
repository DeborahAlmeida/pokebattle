const showTeams = (battle, user) => {
  let currentUserTeam = null;
  let otherUserTeam = null;
  if (battle.teams.length === 1) {
    currentUserTeam = battle.teams[0].trainer.email === user.email ? battle.teams[0] : null;
    otherUserTeam = currentUserTeam === null ? battle.teams[0] : null;
  } else if (battle.teams.length === 2) {
    currentUserTeam =
      battle.teams[0].trainer.email === user.email ? battle.teams[0] : battle.teams[1];
    otherUserTeam = currentUserTeam === battle.teams[0] ? battle.teams[1] : battle.teams[0];
  }
  return [currentUserTeam, otherUserTeam];
};

export { showTeams };
