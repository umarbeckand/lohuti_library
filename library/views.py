from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Book, Author, Category, News, Event


def home(request):
    """Главная страница"""
    latest_books = Book.objects.filter(is_published=True)[:6]
    latest_news = News.objects.filter(is_published=True)[:3]
    upcoming_events = Event.objects.filter(is_active=True)[:3]
    
    context = {
        'latest_books': latest_books,
        'latest_news': latest_news,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'library/home.html', context)


def about(request):
    """Страница о библиотеке"""
    return render(request, 'library/about.html')


def book_list(request):
    """Список всех книг"""
    books = Book.objects.all()
    categories = Category.objects.all()
    
    # Фильтрация по категории
    category_slug = request.GET.get('category')
    if category_slug:
        books = books.filter(category__slug=category_slug)
    
    # Поиск
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(authors__first_name__icontains=query) |
            Q(authors__last_name__icontains=query)
        ).distinct()
    
    # Пагинация
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    }
    return render(request, 'library/book_list.html', context)


def book_detail(request, slug):
    """Детальная страница книги"""
    book = get_object_or_404(Book, slug=slug)
    related_books = Book.objects.filter(category=book.category).exclude(id=book.id)[:4]
    
    context = {
        'book': book,
        'related_books': related_books,
    }
    return render(request, 'library/book_detail.html', context)


def author_list(request):
    """Список авторов"""
    authors = Author.objects.all()
    
    # Поиск
    query = request.GET.get('q')
    if query:
        authors = authors.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(middle_name__icontains=query)
        )
    
    paginator = Paginator(authors, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'library/author_list.html', context)


def author_detail(request, pk):
    """Детальная страница автора"""
    author = get_object_or_404(Author, pk=pk)
    books = author.books.all()
    
    context = {
        'author': author,
        'books': books,
    }
    return render(request, 'library/author_detail.html', context)


def news_list(request):
    """Список новостей"""
    news = News.objects.filter(is_published=True)
    
    paginator = Paginator(news, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'library/news_list.html', context)


def news_detail(request, slug):
    """Детальная страница новости"""
    news_item = get_object_or_404(News, slug=slug, is_published=True)
    
    context = {
        'news_item': news_item,
    }
    return render(request, 'library/news_detail.html', context)


def events_list(request):
    """Список мероприятий"""
    events = Event.objects.filter(is_active=True)
    
    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'library/events_list.html', context)


def event_detail(request, slug):
    """Детальная страница мероприятия"""
    event = get_object_or_404(Event, slug=slug, is_active=True)
    
    context = {
        'event': event,
    }
    return render(request, 'library/event_detail.html', context)


def contact(request):
    """Страница контактов"""
    return render(request, 'library/contact.html')


def services(request):
    """Страница услуг"""
    return render(request, 'library/services.html')
