from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
import uuid


class Acteur(models.Model):
    designation = models.CharField(max_length=255)
    fonction = models.CharField(max_length=255, blank=True, default="Visiteur")
    telephone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to="profiles/", blank=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Acteur"
        verbose_name_plural = "Acteurs"

    def __str__(self):
        return self.designation


class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="utilisateur")
    telephone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to="profiles/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.user.username


class Temoignage(models.Model):
    acteur = models.ForeignKey(Acteur, on_delete=models.CASCADE, related_name="temoignages")
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"

    def __str__(self):
        return f"Témoignage de {self.acteur.designation}"


class Message(models.Model):
    acteur = models.ForeignKey(Acteur, on_delete=models.CASCADE, related_name="messages")
    sujet = models.CharField(max_length=255)
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    lecture = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.sujet


class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


class Article(models.Model):
    titre = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return f"{self.titre}"


class CategorieArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="categorie_articles")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="articles_associes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("article", "categorie")
        verbose_name = "Catégorie d'article"
        verbose_name_plural = "Catégories d'articles"

    def __str__(self):
        return f"Article {self.article.id} - {self.categorie.nom}"


class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="commentaires")
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="commentaires")
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"

    def __str__(self):
        return f"Commentaire de {self.auteur.user.username} sur {self.article.titre}"


class Lecture(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="lectures")
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="lectures", blank=True, null=True)
    date_lecture = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("article", "utilisateur")
        verbose_name = "Lecture"
        verbose_name_plural = "Lectures"

    def __str__(self):
        lecteur = self.utilisateur.user.username if self.utilisateur else "Un visiteur"
        return f"{lecteur} a lu {self.article.titre}"


class MailingList(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mailing_lists")
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    titre = models.CharField(max_length=255, blank=True)
    contenu = models.TextField(blank=True)
    fichier = models.FileField(upload_to='mailing_files/', blank=True, null=True)

    class Meta:
        verbose_name = "Liste de diffusion"
        verbose_name_plural = "Listes de diffusion"

    def __str__(self):
        return self.email
    

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_active = models.BooleanField(default=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Abonné à la newsletter"
        verbose_name_plural = "Abonnés à la newsletter"

    def __str__(self):
        return self.email
