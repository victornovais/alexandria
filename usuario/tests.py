from django.core.urlresolvers import reverse
from model_mommy import mommy
from rest_framework.test import APITestCase

from usuario.models import Usuario


class UsuarioTest(APITestCase):
    def setUp(self):
        self.usuario = mommy.make(Usuario, cpf='123456789', nome='Trollzinho do LOL')
        self.token = self.usuario.auth_token.key

    def test_nao_concede_token_de_acesso_a_usuario_nao_cadastrado(self):
        data = {'cpf': 'invalido'}
        response = self.client.post(reverse('login'), data)

        self.assertEqual(400, response.status_code)
        self.assertTrue(response.data['non_field_errors'])

    # def test_nao_concede_acesso_a_usuario_em_divida_na_biblioteca(self):
    #     self.fail()

    def test_concede_token_de_acesso_a_usuario_cadastrado(self):
        data = {'cpf': '123456789'}
        response = self.client.post(reverse('login'), data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.token, response.data['token'])
