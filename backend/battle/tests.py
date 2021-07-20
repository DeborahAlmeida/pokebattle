from django.test import TestCase
from battle.battles.battle import validate_sum_pokemons


class PokemonsSumTest(TestCase):
    def test_sum(self):
        pokemons = ['bulbasaur', 'pikachu', 'pidgeot']
        sum = validate_sum_pokemons(pokemons)
        self.assertTrue(sum)

    def test_sum_invalid(self):
        pokemons = ['sawsbuck', 'arcanine', 'goodra']
        sum = validate_sum_pokemons(pokemons)
        self.assertFalse(sum)
