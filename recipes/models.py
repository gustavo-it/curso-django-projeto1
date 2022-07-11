from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Um model nada mais é que uma class. Precisamos dizer que esta class herda de models.Model
    Nós criamos as colunas como sendo atributos.
    """
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField()  # Atributo slug específico para o slug
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    serving_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(
        default=False)  # definindo um valor padrão
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add gera uma data/hora automaticamente na hora da criação e esta não é alterada
    update_at = models.DateTimeField(auto_now=True)
    # auto_now gera a data/hora sempre que o elemento é atualizado. Ele só é chamado quando  o registro
    # for atualizado
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/')
    """
    Estamos utilizando o campo ImageField (para subir uma imagem).
    Este campo recebe o valor upload_to (que é o caminho para onde a imagem irá ficará salva).
    Ou seja, ficará salvo na pasta recipes > cover > pasta com o nome (ano/mes/dia).
    """
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    """
    on_delete=models.SET_NULL -> Quando a categoria for apagada eu estou dizendo para o django colocar como nulo
    caso a categoria da receita seja apagada. Além disso estou permitindo que a categoria possa
    receber o valor null.
    """
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
