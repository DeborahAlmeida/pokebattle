export const selectUserById = (userEntity, id) => {
  return userEntity[id].email;
};

export const selectPokemonById = (pokemonEntity, id) => {
  return pokemonEntity[id];
};
