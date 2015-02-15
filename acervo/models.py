from django.db import models


class Livro(models.Model):
    isbn = models.IntegerField('ISBN', primary_key=True)
    nome = models.CharField('Nome', max_length=255)
    editora = models.CharField('Editora', max_length=127, null=True, blank=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        db_table = 'livro'


class Exemplar(models.Model):
    livro = models.ForeignKey('Livro')
