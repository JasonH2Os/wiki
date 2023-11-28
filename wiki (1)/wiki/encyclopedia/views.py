
import random
import markdown2
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, 'encyclopedia/error.html', {'message': 'The requested page was not found.'}, status=404)
    else:
        return render(request, 'encyclopedia/entry.html', {'title': title, 'content': content})

def search(request):
    query = request.GET.get('q', '')  
    entries = util.list_entries()
    
    if query in entries:
        return redirect('entry', title=query)


    filtered_entries = [entry for entry in entries if query.lower() in entry.lower()]
    
    return render(request, 'encyclopedia/search_results.html', {
        'query': query,
        'entries': filtered_entries
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        
        if util.get_entry(title):
            
            return render(request, 'encyclopedia/new_page.html', {
                'error': 'An entry with this title already exists.'
            })
        
        util.save_entry(title, content)
        return redirect('entry', title=title)

    else:
        return render(request, 'encyclopedia/new_page.html')
    
def edit_page(request, title):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect('entry', title=title)

    content = util.get_entry(title)
    if content is None:
        return render(request, 'encyclopedia/error.html', {'message': 'The requested page was not found.'}, status=404)

    return render(request, 'encyclopedia/edit_page.html', {'title': title, 'content': content})

def random_page(request):
    entries = util.list_entries()
    if not entries:
        return redirect('index')

    random_title = random.choice(entries)
    return redirect('entry', title=random_title)

def entry(request, title):
    markdown_content = util.get_entry(title)
    if markdown_content is None:
        return render(request, 'encyclopedia/error.html', {'message': 'The requested page was not found.'}, status=404)

    html_content = markdown2.markdown(markdown_content)
    return render(request, 'encyclopedia/entry.html', {'title': title, 'content': html_content})

