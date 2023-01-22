from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import Markdown
from django.urls import reverse
from . import util
from random import choice

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
})

def entry(request, entry_title):

    # Initialise variables 
    entry = util.get_entry(entry_title)
    markdowner = Markdown()
    
    # If entry retrieved, convert to HTML and render in entry page
    if not entry:
        return render(request, "encyclopedia/apology.html", {
            "message": "The requested page could not be found."
        })
        
    # If no entry returned, redirect to error page
    else: 
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry_title,  
            "html_content": markdowner.convert(entry)
        })

def search(request):
    
    if request.method == "POST":
        
        # Initialise variables: search term, list of encyclopedia entries, list of matches
        search_term = request.POST['q']
        entries = util.list_entries()
        matches = []
        markdowner = Markdown()

        # Loop through list of pages, redirect to article if exact match to search query
        for entry in entries:
            if search_term.upper() == entry.upper():  
                return render(request, "encyclopedia/entry.html", {
                    "entry_title": search_term,  
                    "html_content": markdowner.convert(util.get_entry(entry))
                })
        
        # Otherwise, check for substring matches and build list of potential matching pages
            elif search_term.upper() in entry.upper():
                matches.append(entry)

        # Redirect to matches.html displaying potential matches or notifying of no matches
        if len(matches) >= 1:
            return render(request, "encyclopedia/matches.html", {
                "matches": matches
            })
        else:
            return render(request, "encyclopedia/apology.html", {
                "message": "We're sorry, no possible matches were found for your search query."
})
            
def add(request):
    
    if request.method == "POST":

        # Initialise variables
        add_title = request.POST["add_title"]
        add_content = request.POST["content"]
        entries = util.list_entries()
        markdowner = Markdown()

        # Check if new article title already exists, display message if applicable
        for entry in entries:
            if add_title.upper() == entry.upper():  
                return render(request, "encyclopedia/apology.html", {
                    "message": "An article already exists under this name. Please select an alternative title."
                    })
        
        # If article title does not already exist, save entry   
        util.save_entry(add_title, add_content)
        return render(request, "encyclopedia/entry.html", {
            "entry_title": markdowner.convert(add_title),  
            "html_content": markdowner.convert(add_content)
            })

    # If request method is GET, take user to add entry form 
    else:
        return render(request, "encyclopedia/add.html")

def edit(request):

    if request.method == "GET":

        # Display edit page form pre-populated with article content
        edit_title = request.GET.get("edit_title")
        edit_content = util.get_entry(edit_title)
        return render(request, "encyclopedia/edit.html", {
            "edit_title": edit_title,  
            "content": edit_content
            })
    
    if request.method == "POST":
        
        # Retrieve form content
        edit_title = request.POST["edit_title"]
        edit_content = request.POST["content"]
        markdowner = Markdown()
    
        # Save revised content
        util.save_entry(edit_title, edit_content)

        # Redirect user to entry page
        return render(request, "encyclopedia/entry.html", {
            "entry_title": markdowner.convert(edit_title),  
            "html_content": markdowner.convert(edit_content)
            })

def random(request):      
    entries = util.list_entries()
    entry = choice(entries)
    markdowner = Markdown()

    return render(request, "encyclopedia/entry.html", {
        "entry_title": entry,
        "html_content": markdowner.convert(util.get_entry(entry))    
        })





