from django.db import models
from djchoices import DjangoChoices, ChoiceItem

from usuario.models import Usuario


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


class Emprestimo(models.Model):
    # Choices
    class Status(DjangoChoices):
        Aberto = ChoiceItem('AB')
        Fechado = ChoiceItem('FE')
        Atrasado = ChoiceItem('AT')


    # Campos
    usuario = models.ForeignKey(Usuario, related_name='emprestimos')
    exemplar = models.ForeignKey(Exemplar)

    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True)

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.Aberto)

    class Meta:
        db_table = 'emprestimo'