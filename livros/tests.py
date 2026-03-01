from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Autor, Livro

class LivroAPITestCase(APITestCase):
    """
    Testes automatizados para o recurso Livro.
    Abrange: GET, POST, PUT.
    """

    def setUp(self):
        # Criando superuser e autenticando
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        
        self.client.force_authenticate(user=self.user)

        # Criamos um dado inicial para os testes que precisam de um ID (detalhes, update, delete)
        self.autor = Autor.objects.create(
            nome="Machado de Assis",             
        )
        self.livro = Livro.objects.create(
            titulo="Livro 1",
            resumo="O livro 1 é sobre o número 1.",
            ano_pub=2026,
            usuario=self.user,
        )

        self.livro.autores.add(self.autor)
        
        # Geramos a URL dinamicamente usando o nome do router (livro-list e livro-detail)
        self.list_url = '/livros/'
        self.detail_url = f'/livros/{self.livro.id}/'

    def test_get_list(self):
        """Testa se a listagem de livros retorna 200 OK"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_livro(self):
        """Testa a criação de um novo livro (POST)"""
        data = {
            "titulo": "Livro 2",
            "resumo": "O livro 1 é sobre o número 1.",
            "ano_pub": 2025,
            "usuario": self.user.id,
            "autores": [self.autor.id]          
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Livro.objects.count(), 2)

    def test_put_livro_completo(self):
        """Testa a substituição total (PUT) - Exige todos os campos"""
        data = {
            "titulo": "Livro 2 Atualizado",
            "resumo": "O livro 2 é sobre o número 2.",
            "ano_pub": 2025,
            "usuario": self.user.id,
            "autores": [self.autor.id]             
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.livro.refresh_from_db()
        self.assertEqual(self.livro.titulo, "Livro 2 Atualizado")

class AutorAPITestCase(APITestCase):
    """
    Testes automatizados para o recurso Autor.
    Abrange: GET, POST, PUT, PATCH, DELETE, HEAD e OPTIONS.
    """

    def setUp(self):
        # Criando superuser e autenticando
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        
        self.client.force_authenticate(user=self.user)

        # Criamos um dado inicial para os testes que precisam de um ID (detalhes, update, delete)
        self.autor = Autor.objects.create(
            nome="Machado de Assis",             
        )
        # Geramos a URL dinamicamente usando o nome do router (autor-list e autor-detail)
        self.list_url = '/autores/'
        self.detail_url = f'/autores/{self.autor.id}/'

    def test_get_list(self):
        """Testa se a listagem de autores retorna 200 OK"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_autor(self):
        """Testa a criação de um novo autor (POST)"""
        data = {
            "nome": "Clarice Lispector",            
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Autor.objects.count(), 2)

    def test_put_autor_completo(self):
        """Testa a substituição total (PUT) - Exige todos os campos"""
        data = {
            "nome": "Machado de Assis Atualizado",            
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.autor.refresh_from_db()
        self.assertEqual(self.autor.nome, "Machado de Assis Atualizado")

    def test_patch_autor_parcial(self):
        """Testa a atualização parcial (PATCH) - Apenas um campo"""
        data = {"nome": "Machado Somente"}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.autor.refresh_from_db()#Recarrega os novos valores do banco
        self.assertEqual(self.autor.nome, "Machado Somente")        

    def test_delete_autor(self):
        """Testa a remoção de um autor (DELETE)"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Autor.objects.count(), 0)

    def test_head_request(self):
        """Testa o método HEAD (Deve retornar headers mas corpo vazio)"""
        response = self.client.head(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'') # Corpo deve ser binário vazio
        self.assertTrue('Allow' in response.headers)

    def test_options_request(self):
        """Testa o método OPTIONS (Metadados sobre a API)"""
        response = self.client.options(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # O OPTIONS no DRF retorna informações de renderização e parsing no corpo
        self.assertIn('actions', response.data)