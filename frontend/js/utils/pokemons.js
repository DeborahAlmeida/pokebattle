import { arrayMove } from 'react-sortable-hoc';

export const changeIndex = ({ oldIndex, newIndex, pokemons }) => {
  const bla = Object.values(pokemons);
  const pokemonsOrdered = arrayMove(bla, oldIndex, newIndex);
  return pokemonsOrdered;
};
