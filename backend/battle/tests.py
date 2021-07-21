from django.test import TestCase, Client
from model_bakery import baker
from users.models import User
from battle.models import Battle

'''
class ListBattlesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.battle = baker.make('battle.Battle')
        self.user = User.objects.create(email='deborah.mendonca@vinta.com.br', password='admin')
        self.user.set_password('admin')
        self.user.save()
    
    def test_login_user_can_acess_battle_list(self):
        # import ipdb; ipdb.set_trace()
        self.client.login(username=self.user.email, password='admin')
        response = self.client.get('/battle/list/')
        self.assertEqual(response.status_code, 200)
    
    def test_data_returns_battle_ids(self):
        self.client.login(username=self.user.email, password='admin')
        battles = baker.make('battle.Battle', creator=self.user, _quantity=2)
        response = self.client.get('/battle/list/')
        response_qs = response.context_data.get('battle_list')
        self.assertCountEqual(battles, response_qs)
'''

class BattleCreateViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.creator = User.objects.create(email='deborah.mendonca@vinta.com.br', password='admin')
        self.creator.set_password('admin')
        self.creator.save()
        self.opponent = baker.make('users.User')
    
    def test_create_battle_successfully(self):
        battle_data = {
            "creator": self.creator,
            "opponent": self.opponent,
        }
        self.client.login(username=self.creator.email, password='admin')
        response = self.client.post('/battle/', battle_data)
        import ipdb; ipdb.set_trace()
        # response.context_data.view.refresh_from_db()
        battle = Battle.objects.all()
        self.assertEqual(battle, True)
