from datetime import datetime, timedelta
from django.db import models
from djchoices import DjangoChoices, ChoiceItem


class Livro(models.Model):
    isbn = models.IntegerField('ISBN', primary_key=True)
    nome = models.CharField('Nome', max_length=255)
    editora = models.CharField('Editora', max_length=127, null=True, blank=True)

    def __unicode__(self):
        return self.nome

    def adicionar_exemplar(self):
        if self.exemplares.exists():
            ultimo_exemplar = self.exemplares.latest('id')
            numero = ultimo_exemplar.numero + 1
        else:
            numero = 1

        exemplar = Exemplar(numero=numero)
        self.exemplares.add(exemplar)

        return exemplar

    class Meta:
        db_table = 'livro'


class Exemplar(models.Model):
    livro = models.ForeignKey('Livro', related_name='exemplares')
    numero = models.IntegerField('Numero', default=1)

    class Meta:
        db_table = 'exemplar'

    def disponivel_para_emprestimo(self):
        return not self.emprestimo_set.exclude(status=Emprestimo.Status.Fechado).exists()


class EmprestimoManager(models.Manager):
    def marcar_emprestimos_em_atraso(self):
        now = datetime.now()

        return self.filter(status=Emprestimo.Status.Aberto, data_devolucao__lt=now).\
            update(status=Emprestimo.Status.Atrasado)


class Emprestimo(models.Model):
    # Choices
    class Status(DjangoChoices):
        Aberto = ChoiceItem('AB')
        Fechado = ChoiceItem('FE')
        Atrasado = ChoiceItem('AT')


    # Campos
    usuario = models.ForeignKey('usuario.Usuario', related_name='emprestimos')
    exemplar = models.ForeignKey(Exemplar)

    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True)

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.Aberto)

    objects = EmprestimoManager()

    def renovar(self):
        self.data_devolucao = datetime.now() + timedelta(8)
        self.save(update_fields=['data_devolucao'])

    class Meta:
        db_table = 'emprestimo'
        app_label = 'acervo'