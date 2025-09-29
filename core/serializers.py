# core/serializers.py
from rest_framework import serializers
from core import models as core_models

# ---- Usuario (custom o auth) ----
try:
    UserModel = core_models.Usuario
except AttributeError:
    from django.contrib.auth import get_user_model

    UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["id", "date_joined", "last_login"]


# ---- Alergeno ----
class AlergenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Alergeno
        fields = "__all__"


# ---- Traducciones ----
class CategoriaTraduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.CategoriaTraduccion
        fields = "__all__"


class PlatoTraduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.PlatoTraduccion
        fields = "__all__"


# ---- Entidades base ----
class NegocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Negocio
        fields = "__all__"


class CartaSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Carta
        fields = "__all__"


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Categoria
        fields = "__all__"


class PlatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Plato
        fields = "__all__"


# ---- Tabla intermedia (si decides exponerla) ----
class PlatoAlergenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.PlatoAlergeno
        fields = "__all__"


# ---- Serializers "Detail" (solo lectura, con anidados) ----
class PlatoDetailSerializer(PlatoSerializer):
    alergenos = serializers.SerializerMethodField()
    traducciones = PlatoTraduccionSerializer(
        source="platotraduccion_set",
        many=True,
        read_only=True,
    )

    class Meta(PlatoSerializer.Meta):
        fields = "__all__"

    def get_alergenos(self, obj):
        # Si el M2M se llama "alergenos", úsalo; si no, caemos a la through.
        if hasattr(obj, "alergenos"):
            queryset = obj.alergenos.all()
        else:
            queryset = core_models.Alergeno.objects.filter(platoalergeno__plato=obj)
        return AlergenoSerializer(queryset, many=True, context=self.context).data


class CategoriaDetailSerializer(CategoriaSerializer):
    platos = PlatoDetailSerializer(
        source="plato_set",
        many=True,
        read_only=True,
    )
    traducciones = CategoriaTraduccionSerializer(
        source="categoriatraduccion_set",
        many=True,
        read_only=True,
    )

    class Meta(CategoriaSerializer.Meta):
        fields = "__all__"


class CartaDetailSerializer(CartaSerializer):
    categorias = CategoriaDetailSerializer(
        source="categoria_set",
        many=True,
        read_only=True,
    )

    class Meta(CartaSerializer.Meta):
        fields = "__all__"


class NegocioDetailSerializer(NegocioSerializer):
    cartas = CartaDetailSerializer(
        source="carta_set",
        many=True,
        read_only=True,
    )

    class Meta(NegocioSerializer.Meta):
        fields = "__all__"
