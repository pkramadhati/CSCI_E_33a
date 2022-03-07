from encodings import search_function
from http.client import HTTPResponse
from pickle import GET
from django.shortcuts import render
from django import forms
from . import util
import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
import re
from random import choice


# Index Page #

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry Page #


def page(request, title):

    # util.get_entry(title) gets the content of the page from entries #
    getContent = util.get_entry(title)

    # Check if the entry exits#
    if getContent:
        return render(request, "encyclopedia/page.html", {
            "title": title,
            # converts markdown to html#
            "content": markdown.markdown(getContent)})
    # Display error if it doesn't
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })


# Search Page#


def search(request):

    if request.method == "GET":
        # get a list of existisng pages
        entries = util.list_entries()

        # loop through the list and convert the strings to lowercase
        for i in range(len(entries)):
            entries[i]=entries[i].lower()
        
        # get the search query and convert it into lowercase
        title = request.GET['q']
        title = title.lower()
       
        # ref : https://stackoverflow.com/questions/9542738/python-find-in-list#
        # check to see if the search-query is in the list already
        if title in entries:
            return page(request, title)

        else:
        # ref :https://www.geeksforgeeks.org/python-finding-strings-with-given-substring-in-list/#
        # check if the search-query is in the substring of the list elements
            search_results = [x for x in entries if re.search(title, x)]
            print(f"{search_results}")
            return render(request, "encyclopedia/search.html", {
                "search_results": search_results,
                "search_term": title
            })


#New Page#

class NewEntryForm(forms.Form):
    title=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'Title', 'required': True}))
    content=forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Content', 'required': True}))

def newpage(request):
        # get a list of existisng pages
        entries = util.list_entries()

        # loop through the list and convert the strings to lowercase
        for i in range(len(entries)):
            entries[i]=entries[i].lower()

        # check to see if the form is being submited or just requested. If submitted then
        if request.method=="POST":

            # store the data from the form in a variable called form
             form=NewEntryForm(request.POST)
             title = request.POST['title']
             title=title.lower()

            # check to see if there is already an entry with the same title. Display error if yes 
             if title in entries:
                return render(request, "encyclopedia/newpage.html",{
                    "error": "A page with this title already exists.",
                    "form":NewEntryForm()
                })

            # check to see if form is valid
             else:
                 if form.is_valid():
                    title=form.cleaned_data["title"]
                    content=form.cleaned_data["content"]

                    # Save the new form and render the new page      
                    util.save_entry(title,content)
                    return page(request, title)

                 else:
                     return render(request, "encyclopedia/newpage.html",{
                    "error": "The format of the content is invalid, Try again",
                    "form":NewEntryForm()
                })


        # If the form is not being submitted simply display the form                    
        else:
            return render(request, "encyclopedia/newpage.html",{
          "form":NewEntryForm()
    
        })                   

# Edit Page#


def editpage(request,title):
  
  # store the existing data in a variable. 
  existing_data={
      'title':title,
      'content':util.get_entry(title)
  }

  existing_form = NewEntryForm(existing_data)

  # check to see if the form is called or being submitted. If being submitted 
  if request.method =='POST':
      form = NewEntryForm(request.POST)
     
       # check to see if form is valid
      if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            print(f"{title}")
            #Save the new form and render the new page      
            util.save_entry(title,content)
            return page(request, title)
            
      else:
          return render(request, "encyclopedia/editpage.html",{
          "error": "The format of the content is invalid, Try again",
          "form":existing_form
            
       })
  # If the form is not being submitted simply display the form                    
  else:
      return render(request, "encyclopedia/editpage.html",{
      "form":existing_form
      })


# random page#
# choice returns a random title from entries 
# https://www.w3schools.com/python/ref_random_choice.asp
def random(request):
    entries = util.list_entries()
    title = choice(entries)
    return page(request, title)