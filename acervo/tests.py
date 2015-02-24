from datetime import datetime, timedelta
from django.core.management import call_command

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

        self.exemplar1 = mommy.make(Exemplar, livro=livro1, numero=1)
        self.exemplar2 = mommy.make(Exemplar, livro=livro2, numero=1)

        self.list_url = reverse('emprestimo-list')
        self.detail_url = reverse('emprestimo-detail', kwargs={'pk': 1})

    def test_usuario_pede_exemplar_emprestado(self):
        data = {
            'exemplar': {
                'id': self.exemplar1.id,
            }
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Emprestimo.objects.count())

    def test_usuario_nao_pode_ter_mais_de_5_emprestimos_em_aberto(self):
        mommy.make(Emprestimo, 5, exemplar=self.exemplar1, usuario=self.usuario, data_emprestimo=datetime.now(),
                   status=Emprestimo.Status.Aberto)

        data = {
            'exemplar': {
                'id': self.exemplar2.id,
            }
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(5, Emprestimo.objects.count())

    def test_usuario_tem_7_dias_para_devolver_exemplar(self):
        data = {
            'exemplar': {
                'id': self.exemplar1.id,
            }
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(201, response.status_code)
        emprestimo = Emprestimo.objects.latest('id')
        diff = emprestimo.data_devolucao - emprestimo.data_emprestimo
        self.assertEqual(7, diff.days)

    def test_usuario_nao_pode_pegar_exemplar_emprestado_se_estiver_em_divida(self):
        mommy.make(Emprestimo, exemplar=self.exemplar1, usuario=self.usuario, data_emprestimo=datetime.now(),
                   status=Emprestimo.Status.Atrasado)
        data = {
            'exemplar': {
                'id': self.exemplar2.id,
            }
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(1, Emprestimo.objects.filter(status=Emprestimo.Status.Atrasado).count())
        self.assertEqual(0, Emprestimo.objects.filter(status=Emprestimo.Status.Aberto).count())

    def test_usuario_fecha_emprestimo(self):
        mommy.make(Emprestimo, id=1, exemplar=self.exemplar1, usuario=self.usuario, data_emprestimo=datetime.now(),
                   status=Emprestimo.Status.Aberto)

        data = {
            'status': 'FE'
        }
        self.client.put(self.detail_url, data, format='json')

        self.assertEqual(0, len(Emprestimo.objects.filter(status=Emprestimo.Status.Aberto)))
        self.assertEqual(1, len(Emprestimo.objects.filter(status=Emprestimo.Status.Fechado)))

    def test_usuario_renova_emprestimo(self):
        self.fail()

    def test_usuario_nao_pode_fechar_emprestimo_se_estiver_em_divida(self):
        mommy.make(Emprestimo, id=1, exemplar=self.exemplar1, usuario=self.usuario, data_emprestimo=datetime.now(),
                   status=Emprestimo.Status.Atrasado)

        data = {
            'status': 'FE'
        }
        response = self.client.put(self.detail_url, data, format='json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(0, len(Emprestimo.objects.filter(status=Emprestimo.Status.Fechado)))
        self.assertEqual(1, len(Emprestimo.objects.filter(status=Emprestimo.Status.Atrasado)))


class EmprestimoAtrasadoTest(APITestCase):
    def setUp(self):
        self.nome = 'Fulano'
        self.cpf = '123456789'
        self.usuario = mommy.make(Usuario, cpf=self.cpf, nome=self.nome)

        livro1 = mommy.make(Livro, isbn=111111, nome='O pequeno principe')
        exemplar1 = mommy.make(Exemplar, livro=livro1, numero=1)

        now = datetime.now()
        semana_passada = now - timedelta(7)
        ontem = now - timedelta(1)
        mommy.make(Emprestimo, 3, exemplar=exemplar1, usuario=self.usuario, data_emprestimo=semana_passada,
                   data_devolucao=ontem, status=Emprestimo.Status.Aberto)

        mommy.make(Emprestimo, 3, exemplar=exemplar1, usuario=self.usuario, data_emprestimo=semana_passada,
                   data_devolucao=ontem, status=Emprestimo.Status.Fechado)

    def test_marca_emprestimos_em_atraso(self):
        call_command('marcar_emprestimos_atrasados')

        self.assertEqual(3, len(Emprestimo.objects.filter(status=Emprestimo.Status.Atrasado)))
        self.assertEqual(3, len(Emprestimo.objects.filter(status=Emprestimo.Status.Fechado)))