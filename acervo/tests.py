from datetime import datetime

from django.core.urlresolvers import reverse
from model_mommy import mommy
from rest_framework.test import APITestCase

from acervo.models import Livro, Exemplar, Emprestimo
from usuario.models import Usuario


class EmprestimoTest(APITestCase):
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

        self.exemplar = mommy.make(Exemplar, livro=livro1, numero=1)
        mommy.make(Exemplar, livro=livro2, numero=1)

        self.url = reverse('emprestimo-list')

    def test_usuario_pede_exemplar_emprestado(self):
        data = {'exemplar_id': self.exemplar.id}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Emprestimo.objects.count())

    def test_usuario_nao_pode_ter_mais_de_5_emprestimos_em_aberto(self):
        mommy.make(Emprestimo, 5, exemplar=self.exemplar, usuario=self.usuario, data_emprestimo=datetime.now(),
                   status=Emprestimo.Status.Aberto)
        data = {}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(5, Emprestimo.objects.count())

    def test_usuario_tem_7_dias_para_devolver_exemplar(self):
        data = {}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(201, response.status_code)
        self.assertTrue(response.data['data_devolucao'])

    def test_usuario_nao_pode_pegar_exemplar_emprestado_se_estiver_em_divida(self):
        mommy.make(Emprestimo, exemplar=self.exemplar, usuario=self.usuario, data_emprestimo=datetime.now(),
                   status=Emprestimo.Status.Atrasado)
        data = {}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(1, Emprestimo.objects.filter(status=Emprestimo.Status.Atrasado).count())
        self.assertEqual(0, Emprestimo.objects.filter(status=Emprestimo.Status.Aberto).count())