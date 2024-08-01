import random

import factory

from fast_zero_projeto_final.models.contas import Conta
from fast_zero_projeto_final.models.livros import Livro
from fast_zero_projeto_final.models.romancistas import Romancista
from fast_zero_projeto_final.sanitize import sanitize_nome


class ContaFactory(factory.Factory):
    class Meta:
        model = Conta

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    senha = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class RomancistaFactory(factory.Factory):
    class Meta:
        model = Romancista

    nome = factory.Faker('name')
    conta_id = 1

    @factory.post_generation
    def sanitize_nome(obj, create, extracted, **kwargs):
        if extracted:
            obj.nome = extracted
        else:
            obj.nome = sanitize_nome(obj.nome)


class LivroFactory(factory.Factory):
    class Meta:
        model = Livro

    titulo = factory.Faker('sentence', nb_words=4)
    ano = 1950 + random.randint(0, 75)
    romancista_id = 1
    conta_id = 1

    @factory.post_generation
    def sanitize_titulo(obj, create, extracted, **kwargs):
        if extracted:
            obj.titulo = extracted
        else:
            obj.titulo = sanitize_nome(obj.titulo)
