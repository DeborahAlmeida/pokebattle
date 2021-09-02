import { schema } from 'normalizr';

export const user = new schema.Entity('user');

export const pokemon = new schema.Entity('pokemon');

export const battle = new schema.Entity('battle', {
  creator: user,
  opponent: user,
  winner: user,
  teams: [{ trainer: user, pokemons: [pokemon] }],
});

export const battleList = new schema.Array(battle);
