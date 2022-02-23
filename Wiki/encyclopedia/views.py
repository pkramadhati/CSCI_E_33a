from encodings import search_function
from pickle import GET
from django.shortcuts import render
from django import forms
from . import util
import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry Page #

def page(request, title):

  #util.get_entry(title) gets the content of the page from entries #
  getContent=util.get_entry(title)
   
   #Check if the entry exits#
  if getContent :
        return render (request,"encyclopedia/page.html",{
           "title":title,
            #markdown.markdown converts markdown to html stores it in a variable called pageContent#
           "pageContent":markdown.markdown(getContent)})
    # Display error if it doesn't
  else:
        return render (request, "encyclopedia/error.html",{
             "title":title
        })
#Search Page#

def search(request):


   if request.method == GET:
        return render (request,"encyclopedia/search.html",{
         })
