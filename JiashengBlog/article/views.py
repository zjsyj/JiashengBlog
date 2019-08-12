from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import ArticlePostForm
from .models import ArticlePost
import markdown

# Create your views here.
def article_create(request):
	if request.method == "POST":
		article_post_form = ArticlePostForm(data=request.POST)

		if article_post_form.is_valid():
			new_article = article_post_form.save(commit=False)
			new_article.author = User.objects.get(id=1)
			new_article.save()
			return redirect("article:article_list")
		else:
			return HttpResponse("There are errors in form, please correct")
	else:
		article_post_form = ArticlePostForm()
		context = {'article_post_form':article_post_form}
		return render(request, 'article/create.html', context)

def article_list(request):
	article_list = ArticlePost.objects.all()

	paginator = Paginator(article_list, 4)

	page = request.GET.get('page')

	articles = paginator.get_page(page)

	context = {'articles':articles}

	return render(request, 'article/list.html', context)

def article_detail(request, id):
	article = ArticlePost.objects.get(id=id)
	article.body = markdown.markdown(article.body,
		extensions = [
		'markdown.extensions.extra',
		'markdown.extensions.codehilite',
		])
	context = {'article':article}
	return render(request, 'article/detail.html', context)

@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
	user = ArticlePost.objects.get(id=id).author

	if request.user == user:
		article = ArticlePost.objects.get(id=id)
		article.delete()
		return redirect('article:article_list')
	else:
		return HttpResponse("You are not author")

@login_required(login_url='/userprofile/login/')
def article_update(request, id):
	"""
	update the exist article by article id
	sumbit form with POST method, GET get into
	the inital pages
	"""
	article = ArticlePost.objects.get(id=id)
	if request.user == article.author:
		if request.method == "POST":
			article_post_form = ArticlePostForm(data=request.POST)
			if article_post_form.is_valid():
				article.title = request.POST['title']
				article.body = request.POST['body']
				article.save()
				return redirect('article:article_detail', id=id)
			else:
				return HttpResponse("Erros in form, Please correct it")
		else:
			article_post_form = ArticlePostForm()
			context = {'article':article, 'article_post_form':article_post_form}
			return render(request, 'article/update.html', context)
	else:
		return HttpResponse("You are not author")