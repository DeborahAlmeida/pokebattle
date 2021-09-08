import { schema } from 'normalizr';

export const userSchema = new schema.Entity('user');

export const pokemonSchema = new schema.Entity('pokemon');

export const battleSchema = new schema.Entity('battle', {
  creator: userSchema,
  opponent: userSchema,
  winner: userSchema,
  teams: [{ trainer: userSchema, pokemons: [pokemonSchema] }],
});

export const battlesSchema = new schema.Array(battleSchema);
