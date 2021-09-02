import React from 'react';

import CardPokemon from 'components/CardPokemon';

function CardTeam(props) {
  return (
    <div className="content_card">
      {props.pokemonsIds.map((pokemon) => {
        return <CardPokemon key={pokemon} pokemon={props.pokemonsDetail[pokemon]} />;
      })}
    </div>
  );
}
export default CardTeam;
