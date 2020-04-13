from django.shortcuts import render
from .models import Topic, Entry
from django.shortcuts import redirect
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    """the home page for learning log"""
    return render (request, 'l_logs/index.html')


@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owener = request.user).order_by('date_added')
    context  = {
        "topics": topics
    }
    return render(request, 'l_logs/topics.html', context)


@login_required
def topic(request, t_id):
    """Show a single topic and all its entries"""
    topic  = Topic.objects.get(id = t_id)
    if topic.owener != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {
        'topic':topic,
        'entries': entries
    }
    return render(request, 'l_logs/topic.html', context)


@login_required
def new_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owener = request.user
            new_topic.save()
            return redirect('topics')
    
    else:
        form = TopicForm()
    
    context = {
        'form': form
    }
    return render (request, 'l_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect('/topic/%d'%topic.id)
    
    context = {
        'form': form,
        'topic': topic
    }
    return render(request, 'l_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id= entry_id)
    topic = entry.topic
    if topic.owener != request.user:
        raise Http404

    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(request.POST,instance=entry)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/topic/%d'%topic.id)

    context = {
        'form':form,
        'topic':topic,
        'entry':entry
    }
    return render (request, 'l_logs/edit_entry.html', context)


@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic
    if topic.owener != request.user:
        raise Http404

    if request.method == 'POST':
        entry.delete()
        return HttpResponseRedirect('/topic/%d'%topic.id)
    
    context = {
        'topic': topic,
        'entry': entry        
    }
    return render(request, 'l_logs/delete_entry.html', context)




@login_required
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id = topic_id)   
    if topic.owener != request.user:
        raise Http404 

    if request.method == 'POST':
        topic.delete()
        return redirect('topics')
    
    context = {
        'topic': topic               
    }
    return render(request, 'l_logs/delete_topic.html', context)