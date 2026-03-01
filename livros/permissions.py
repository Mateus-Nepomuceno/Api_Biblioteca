from rest_framework import permissions

class DonoOuApenasLeitura(permissions.BasePermission):
    """Permissão: Qualquer um lê, mas apenas o dono do objeto pode deletar/editar."""

    def has_object_permission(self, request, view, obj):
        # Leitura liberada para qualquer um (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Escrita/Delete liberada apenas se o usuário logado for o 'dono' (obj.usuario)
        return obj.usuario == request.user