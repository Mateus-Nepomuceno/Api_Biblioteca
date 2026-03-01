from rest_framework import viewsets
from .models import Livro, Autor
from .serializers import LivroSerializer, AutorSerializer
from .permissions import DonoOuApenasLeitura

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [DonoOuApenasLeitura]

    