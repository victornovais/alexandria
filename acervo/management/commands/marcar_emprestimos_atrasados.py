# -*- coding:utf-8 -*-
from django.core.management import BaseCommand
from acervo.models import Emprestimo


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Rodaremos esse script 1x ao dia para marcar como 'Atrasado' os Empréstimos
        # que ultrapassarem a data de devolução
        Emprestimo.objects.marcar_emprestimos_em_atraso()