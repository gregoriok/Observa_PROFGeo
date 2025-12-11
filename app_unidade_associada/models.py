import uuid
import datetime
from django.db import models

class UnidadeAssociada(models.Model):
    Id_unidade = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Nome_unidade = models.TextField(max_length=50)
    Municipio = models.TextField(max_length=255)
    Estado_UF = models.TextField(max_length=2)
    Data_insercao = models.DateTimeField(auto_created=datetime.datetime.now)
    Status = models.BooleanField()

    class Meta:
        db_table = 'unidade_associada'

    def __str__(self):
        # Retorna o nome da unidade como a representação legível do objeto
        return f"{self.Nome_unidade} - ({self.Municipio}/{self.Estado_UF})"