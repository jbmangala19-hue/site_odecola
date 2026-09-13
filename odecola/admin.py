from django.contrib import admin

from .models import (
    Acteur,
    Article,
    Categorie,
    CategorieArticle,
    Commentaire,
    Lecture,
    MailingList,
    Message,
    Temoignage,
    Utilisateur,
    NewsletterSubscription
)

class CategorieInline(admin.TabularInline):
    model = CategorieArticle
    extra = 1


class CommentaireInline(admin.TabularInline):
    model = Commentaire
    extra = 1


@admin.register(Acteur)
class ActeurAdmin(admin.ModelAdmin):
    list_display = ("designation", "fonction", "telephone", "email")
    search_fields = ("designation", "fonction", "email")
    list_filter = ("fonction",)


@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ("acteur", "contenu", "created_at")
    list_filter = ("created_at",)
    search_fields = ("acteur__designation", "contenu")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("acteur", "sujet", "lecture", "created_at")
    list_filter = ("lecture", "created_at")
    search_fields = ("acteur__designation", "sujet", "contenu")


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom", "description")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("titre", "created_at")
    search_fields = ("titre", "contenu")
    list_filter = ("created_at",)
    inlines = [CategorieInline, CommentaireInline]
    prepopulated_fields = {"slug": ("titre",)}


@admin.register(CategorieArticle)
class CategorieArticleAdmin(admin.ModelAdmin):
    list_display = ("article", "categorie")
    list_filter = ("categorie",)
    search_fields = ("article__titre", "categorie__nom")


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ("article", "auteur", "created_at")
    search_fields = ("article__titre", "auteur__username", "contenu")
    list_filter = ("created_at",)


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("article", "utilisateur", "date_lecture")
    search_fields = ("article__titre", "utilisateur__username")
    list_filter = ("date_lecture",)


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ("email", "auteur", "date", "titre")
    search_fields = ("email", "titre", "contenu", "auteur__username")
    list_filter = ("date",)


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ("user", "telephone")
    search_fields = ("telephone", "user__username")


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("email", "date_inscription", "is_active")
    search_fields = ("email",)
    list_filter = ("date_inscription", "is_active")
