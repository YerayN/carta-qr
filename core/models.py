from django.db import models


class Usuario(models.Model):
    """
    Usuario propio del sistema.
    Relaciona 1:1 con Negocio.
    (Podemos decidir más adelante si extender directamente `User`
    o mantenerlo separado. Aquí uso un modelo propio simple.)
    """

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=150)

    def __str__(self):
        return self.username


class Negocio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.nombre


class Carta(models.Model):
    nombre = models.CharField(max_length=200)
    qr_url = models.CharField(max_length=255, blank=True, null=True)
    negocio = models.ForeignKey(
        Negocio, on_delete=models.CASCADE, related_name="cartas"
    )

    def __str__(self):
        return f"{self.nombre} ({self.negocio.nombre})"


class Categoria(models.Model):
    carta = models.ForeignKey(
        Carta, on_delete=models.CASCADE, related_name="categorias"
    )

    def __str__(self):
        return f"Categoría {self.id} de {self.carta.nombre}"


class CategoriaTraduccion(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="traducciones"
    )
    idioma = models.CharField(max_length=10)
    nombre = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["categoria", "idioma"], name="unique_categoria_idioma"
            )
        ]

    def __str__(self):
        return f"{self.nombre} ({self.idioma})"


class Plato(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="platos"
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.CharField(max_length=255, blank=True, null=True)
    alergenos = models.ManyToManyField("Alergeno", through="PlatoAlergeno")

    def __str__(self):
        return f"Plato {self.id} (Categoría {self.categoria_id})"


class PlatoTraduccion(models.Model):
    plato = models.ForeignKey(
        Plato, on_delete=models.CASCADE, related_name="traducciones"
    )
    idioma = models.CharField(max_length=10)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    historia = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["plato", "idioma"], name="unique_plato_idioma"
            )
        ]

    def __str__(self):
        return f"{self.nombre} ({self.idioma})"


class Alergeno(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre


class PlatoAlergeno(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    alergeno = models.ForeignKey(Alergeno, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("plato", "alergeno")

    def __str__(self):
        return f"{self.plato} - {self.alergeno}"
