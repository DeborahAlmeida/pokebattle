import React from 'react';

function CardPokemon(props){
    const data = props.pokemon
    return (
        <div className="card_pokemon">
            <img className="img_pokemon_card" src={data.img_url}></img>
            <p>{data.name}</p>
            <div className="base_stats">
            <div className="base_stats_title">
                <p>Attack</p>
                <p>{data.attack}</p>
            </div>
            <div className="base_stats_title">
                <p>Defense</p>
                <p>{data.defense}</p>
            </div>
            <div className="base_stats_title">
                <p>HP</p>
                <p>{data.hp}</p>
            </div>
            </div>
        </div>
    );
}
export default CardPokemon;
