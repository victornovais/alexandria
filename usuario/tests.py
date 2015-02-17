from django.core.urlresolvers import reverse
from model_mommy import mommy
from rest_framework.test import APITestCase

from acervo.models import Emprestimo, Livro, Exemplar

from usuario.models import Usuario


class UsuarioTokenTest(APITestCase):
    def setUp(self):
        self.usuario = mommy.make(Usuario, cpf='123456789', nome='Trollzinho do LOL')
        self.token = self.usuario.auth_token.key

    def test_nao_concede_token_de_acesso_a_usuario_nao_cadastrado(self):
        data = {'cpf': 'invalido'}
        response = self.client.post(reverse('login'), data)

        self.assertEqual(400, response.status_code)
        self.assertTrue(response.data['non_field_errors'])

    def test_concede_token_de_acesso_a_usuario_cadastrado(self):
        data = {'cpf': '123456789'}
        response = self.client.post(reverse('login'), data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.token, response.data['token'])


class UsuarioInfoTest(APITestCase):
    def setUp(self):
        self.nome = 'Fulano'
        self.cpf = '123456789'
        self.usuario = mommy.make(Usuario, cpf=self.cpf, nome=self.nome)

        # Adicionando token em todos os requests
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.usuario.auth_token.key)

        self.pk_args = {'pk': self.cpf}

        # Criando emprestimos para o nosso Usuario
        livro1 = mommy.make(Livro, isbn=111111, nome='O pequeno principe')
        livro2 = mommy.make(Livro, isbn=222222, nome='Maus')

        exemplar1 = mommy.make(Exemplar, livro=livro1, numero=1)
        exemplar2 = mommy.make(Exemplar, livro=livro2, numero=1)

        mommy.make(Emprestimo, exemplar=exemplar1, usuario=self.usuario, status=Emprestimo.Status.Aberto)

        mommy.make(Emprestimo, exemplar=exemplar2, usuario=self.usuario, status=Emprestimo.Status.Fechado)
        mommy.make(Emprestimo, exemplar=exemplar2, usuario=self.usuario, status=Emprestimo.Status.Aberto)

    def test_traz_nome_e_identificacao_do_usuario(self):
        response = self.client.get(reverse('usuario-detail', kwargs=self.pk_args))

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.nome, response.data['nome'])
        self.assertEqual(self.cpf, response.data['cpf'])

    # def test_exibe_status_do_usuario_na_biblioteca(self):
    #     response = self.client.get(reverse('usuario-detail', kwargs=self.pk_args))

    def test_traz_emprestimos_em_aberto_que_o_usuario_possui(self):
        response = self.client.get(reverse('usuario-detail', kwargs=self.pk_args))

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data['emprestimos']))

    def test_usuario_so_tem_acesso_a_seus_registros(self):
        outro_usuario = mommy.make(Usuario, cpf='987654321', nome='Ciclano')
        response = self.client.get(reverse('usuario-detail', kwargs={'pk': outro_usuario.pk}))

        self.assertEqual(404, response.status_code)

