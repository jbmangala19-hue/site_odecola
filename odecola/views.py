from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from urllib.parse import urlencode
from .models import *

# Create your views here.
def index(request):

    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        email = request.POST.get('email', '').strip()
        telephone = request.POST.get('tel', '').strip()
        sujet = request.POST.get('sujet', '').strip()
        contenu = request.POST.get('message', '').strip()

        acteur = Acteur.objects.filter(email=email).first()
        if acteur is None:
            acteur = Acteur.objects.create(
                designation=nom,
                telephone=telephone,
                email=email,
            )
        elif telephone and not acteur.telephone:
            acteur.telephone = telephone
            acteur.save(update_fields=['telephone'])

        Message.objects.create(
            acteur=acteur,
            sujet=sujet,
            contenu=contenu,
        )
        return redirect('/?message=Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.#section_5')

    else:

        articles = Article.objects.filter(is_active=True).annotate(
                nombre_commentaires=Count('commentaires', distinct=True),
                nombre_lectures=Count('lectures', distinct=True),
            ).order_by('-created_at')[:5]
        categories = Categorie.objects.order_by('nom')
        temoignages = Temoignage.objects.select_related('acteur').order_by('-created_at')[:4]

        try:
            message = request.GET.get('message', False)
        except:
            message = False

        return render(request, 'index.html', {
            'featured_articles': list(articles[:2]),
            'recent_articles': list(articles[2:]),
            'categories': categories,
            'message' : message,
            'temoignages': temoignages,
        })


def blog(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('categorie', '').strip()
    articles = Article.objects.filter(is_active=True).annotate(
        nombre_commentaires=Count('commentaires', distinct=True),
        nombre_lectures=Count('lectures', distinct=True),
    ).order_by('-created_at')

    if query:
        articles = articles.filter(
            Q(titre__icontains=query)
            | Q(contenu__icontains=query)
            | Q(categorie_articles__categorie__nom__icontains=query)
        ).distinct()

    if category_id.isdigit():
        articles = articles.filter(categorie_articles__categorie_id=int(category_id)).distinct()
    else:
        category_id = ''

    recent_articles = articles[:3]
    paginator = Paginator(articles, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    pagination_params = request.GET.copy()
    pagination_params.pop('page', None)
    categories = Categorie.objects.order_by('nom')
    return render(request, 'news.html', {
        'blog_active': 'active',
        'articles': page_obj.object_list,
        'page_obj': page_obj,
        'pagination_query': urlencode(pagination_params),
        'recent_articles': recent_articles,
        'categories': categories,
        'category_id': category_id,
        'query': query,
    })


def detail_article(request, article_slug):
    article = get_object_or_404(
        Article.objects.filter(is_active=True).annotate(
            nombre_commentaires=Count('commentaires', distinct=True),
            nombre_lectures=Count('lectures', distinct=True),
        ),
        slug=article_slug,
    )

    article_category = article.categorie_articles.select_related('categorie').first()
    article_category = article_category.categorie if article_category else None

    if request.method == 'POST':
        contenu = request.POST.get('contenu', '').strip()
        if contenu and request.user.is_authenticated:
            utilisateur = Utilisateur.objects.filter(user=request.user).first()
            if utilisateur:
                article.commentaires.create(auteur=utilisateur, contenu=contenu)
        return redirect('detail_article', article_slug=article_slug)

    if request.user.is_authenticated:
        utilisateur = Utilisateur.objects.filter(user=request.user).first()
        if utilisateur and not article.lectures.filter(utilisateur=utilisateur).exists():
            article.lectures.create(utilisateur=utilisateur)
    else:
        article.lectures.create(utilisateur=None)

    categories = Categorie.objects.order_by('nom')
    recent_articles = Article.objects.filter(is_active=True).exclude(pk=article.pk).order_by('-created_at')[:3]
    comments = article.commentaires.select_related('auteur__user').order_by('-created_at')
    related_articles = Article.objects.filter(is_active=True).exclude(pk=article.pk).order_by('-created_at')[:2]

    return render(request, 'news-detail.html', {
        'article': article,
        'article_category': article_category,
        'recent_articles': recent_articles,
        'related_articles': related_articles,
        'comments': comments,
        'blog_active': 'active',
        'categories': categories,
    })


def connexion(request):

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        user = User.objects.filter(email=email).first()
        if not user:
            return render(request, 'login.html', {'error': 'Identifiants incorrects. Veuillez réessayer.'})

        verification = authenticate(request, username=user.username, password=password)
        if verification:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {'error': 'Identifiants incorrects. Veuillez réessayer.'})

    return render(request, 'login.html')


def deconnexion(request):
    logout(request)
    return redirect('home')


def inscription(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        telephone = request.POST.get('tel', '').strip()

        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            return render(request, 'inscription.html', {'error': 'Un compte avec cette adresse e-mail existe déjà.'})

        parts = nom.split()
        first_name = parts[0] if parts else ''
        last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        
        Utilisateur.objects.create(user=user, telephone=telephone)

        login(request, user)
        return redirect('home')

    return render(request, 'inscription.html')