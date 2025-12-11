import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from app_unidade_associada.models import UnidadeAssociada

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo E-mail é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('ativo', True) # Usa seu campo 'ativo'

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, nome, password, **extra_fields)

    # ----------------------------------------------------
    # OBRIGATÓRIO: Implementação para o Django Auth
    # ----------------------------------------------------
    def get_by_natural_key(self, email_):
        """Método que o Django usa para procurar o usuário durante o login."""
        return self.get(email=email_) # Procura no DB usando o e-mail

class Usuario(AbstractBaseUser, PermissionsMixin):

    id_usuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='e-mail', unique=True)  # USADO COMO LOGIN
    # senha (Já incluído pelo AbstractBaseUser)
    telefone = models.CharField(max_length=15, blank=True, null=True)

    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True, verbose_name="CPF")

    data_cadastro = models.DateField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    aprovado_coordenador = models.BooleanField(default=False, verbose_name="Aprovação Coordenador")

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_groups',  # <--- CORREÇÃO AQUI
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_permissions',  # <--- CORREÇÃO AQUI
        related_query_name='user',
    )

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    is_active = property(lambda self: self.ativo and self.aprovado_coordenador)

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.nome


# ==========================================================
# 2. COORDENADOR - Extensão de Usuario (Herança One-to-One)
# ==========================================================

class Coordenador(models.Model):
    id_usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='coordenador_profile'  # Nome para acesso reverso
    )

    formacao = models.CharField(max_length=100)

    # FK para Unidade_Associada
    id_unidade = models.ForeignKey(
        UnidadeAssociada,
        on_delete=models.PROTECT,  # Não deleta a unidade se houver coordenador
        related_name='coordenadores'
    )

    ano_vigencia = models.IntegerField()
    ativo_coordenador = models.BooleanField(default=True)

    class Meta:
        db_table = 'coordenador'  # Nome da tabela: coordenador
        # Restrição de unicidade: Uma unidade só pode ter um coordenador ativo por ano
        unique_together = ('id_unidade', 'ano_vigencia')

    def __str__(self):
        return f"Coordenador: {self.id_usuario.nome} - Unidade: {self.id_unidade.titulo}"


class Colaborador(models.Model):

    id_usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='colaborador_profile'  # Nome para acesso reverso
    )

    area_atuacao = models.CharField(max_length=100, verbose_name="Área de Atuação")
    ano_ingresso = models.IntegerField(verbose_name="Área de Ingresso")
    ano_referencia = models.IntegerField(verbose_name="Ano Referencia")

    id_unidade = models.ForeignKey(
        UnidadeAssociada,
        on_delete=models.PROTECT,  # Não deleta a unidade se houver colaborador
        related_name='colaboradores_unidade'
    )

    ativo_colaborador = models.BooleanField(default=True)

    class Meta:
        db_table = 'colaborador'
        # Um colaborador pode estar ligado a diferentes unidades em diferentes anos,
        # mas talvez só possa ter um perfil ativo em um determinado ano de referência
        unique_together = ('id_unidade', 'id_usuario')

    def __str__(self):
        return f"Colaborador: {self.id_usuario.nome} - Área: {self.area_atuacao}"