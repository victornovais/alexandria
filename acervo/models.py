from django.db import models


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
