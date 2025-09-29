from django.contrib import admin
from .models import (
    Usuario,
    Negocio,
    Carta,
    Categoria,
    CategoriaTraduccion,
    Plato,
    PlatoTraduccion,
    Alergeno,
    PlatoAlergeno,
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("username", "email")


@admin.register(Negocio)
class NegocioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "usuario")
    search_fields = ("nombre",)


@admin.register(Carta)
class CartaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "negocio")
    search_fields = ("nombre",)
    list_filter = ("negocio",)


class CategoriaTraduccionInline(admin.TabularInline):
    model = CategoriaTraduccion
    extra = 1


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "carta")
    list_filter = ("carta",)
    inlines = [CategoriaTraduccionInline]


class PlatoTraduccionInline(admin.TabularInline):
    model = PlatoTraduccion
    extra = 1


class PlatoAlergenoInline(admin.TabularInline):
    model = PlatoAlergeno
    extra = 1


@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ("id", "categoria", "precio")
    list_filter = ("categoria",)
    inlines = [PlatoTraduccionInline, PlatoAlergenoInline]


@admin.register(Alergeno)
class AlergenoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


# PlatoAlergeno lo mostramos como inline en Plato, no hace falta registro directo
