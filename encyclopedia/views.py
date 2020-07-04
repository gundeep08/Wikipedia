from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
import secrets

markdowner = Markdown()

class SearchPageForm(forms.Form):
    q = forms.CharField()
    
class NewPageForm(forms.Form):
    pagetitle = forms.CharField(label="Page Title")
    pagecontent = forms.CharField(label="Page Content", widget=forms.Textarea)

class EditPageForm(forms.Form):
    editedcontent = forms.CharField()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def add(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["pagetitle"]
            content = form.cleaned_data["pagecontent"]
            pageExists=util.get_entry(title)
            if pageExists:
                return render(request, "encyclopedia/error.html", {
                "message":   title + " page already exists"
            })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", args=[title]))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html")


def random(request):
    entries=util.list_entries()
    randomPage= secrets.choice(entries)
    return HttpResponseRedirect(reverse('entry', args=[randomPage]))

def search(request):
    if request.method == "POST": 
        searchform = SearchPageForm(request.POST)
        if searchform.is_valid():
            pageTitle = searchform.cleaned_data["q"]
            doesPageExists=util.get_entry(pageTitle)
            if doesPageExists:
                return render(request, "encyclopedia/entry.html", {
                    "title": pageTitle,
                    "content":markdowner.convert(util.get_entry(pageTitle))
                })
            else:
                allEntries= util.list_entries()
                newList=[]
                for entry in allEntries:
                    if pageTitle in entry:
                        newList.append(entry)
                if len(newList)>0:
                    return render(request, "encyclopedia/index.html", {
                        "entries": newList
                    })
                else:
                    return render(request, "encyclopedia/error.html", {
                        "message": "No page exists matching your search of " + pageTitle
                    })  
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "Invalid Form" 
            })        
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Request Method is not POST" 
        }) 

def entry(request,name):
    entrydata=util.get_entry(name)
    if entrydata:
        content=markdowner.convert(entrydata)
        if content:
            return render(request, "encyclopedia/entry.html", {
                "title": name,
                "content":content
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "No content to edit for " +  name  + " page"
            })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": name + " page does not exist"
        })

def edit(request,name):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["editedcontent"]
            if content:
                util.save_entry(name, content)
                return render(request, "encyclopedia/entry.html", {
                    "title": name,
                    "content":content
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "No content to edit for " +  name  + " page"
                }) 
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "Invalid Form" 
            }) 
    else:
        content=markdowner.convert(util.get_entry(name))
        if content:
            return render(request, "encyclopedia/edit.html", {
                "title": name,
                "content":content
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "No content to edit for " +  name  + " page"
            })
        
    


