from django.shortcuts import render
import markdown2
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(util.get_entry(title)),
        "title": title
    })

def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    if query in entries:
        return HttpResponseRedirect(reverse('encyclopedia:entry', args=[query]))
    else:
        matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search_results.html", {
            "entries": matching_entries,
            "search_query": query
        })
    
def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title in util.list_entries():
            return render(request, "encyclopedia/create.html", {
                "error": "An entry with this title already exists.",
                "title": title,
                "content": content
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('encyclopedia:entry', args=[title]))
    return render(request, "encyclopedia/create.html")


def edit(request, title):
    if request.method == "POST":
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('encyclopedia:entry', args=[title]))
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(reverse('encyclopedia:entry', args=[random_entry]))
