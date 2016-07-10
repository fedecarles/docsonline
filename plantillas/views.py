from django.shortcuts import (render, render_to_response,
                              RequestContext, redirect)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import plantillaForm
from .models import plantillaModel
from django.http import HttpResponse
from io import BytesIO
from weasyprint import HTML, CSS
import uuid
from taggit.models import Tag
from django.core.exceptions import PermissionDenied
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
import time


def home(request):
    return render(request, "home.html")


@login_required
def plantillas(request, doc_id=None):
    if doc_id is None:
        form = plantillaForm(request.POST or None)
    else:
        instance = plantillaModel.objects.get(doc_id=doc_id)
        form = plantillaForm(request.POST or None, instance=instance)
        if instance.is_owner(request.user):
            pass
        else:
            raise PermissionDenied
    context = {
        "form": form,
    }
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            context = {
                "form": form,
                "text": form.cleaned_data["summernote"],
                "public": form.cleaned_data["public"],
            }
            if "genpdf" in request.POST:
                return (CreateDraft(request, text=context["text"],
                                    output="pdf"))
            if "genword" in request.POST:
                return (CreateDraft(request, text=context["text"],
                                    output="docx"))
            elif "reload" in request.POST:
                instance_url = reverse('plantillas')+str(instance.doc_id)
                return redirect(instance_url)
            else:
                pass
            instance.user = request.user
            instance.creation_date = time.strftime("%d-%m-%Y")
            instance.save()
            form.save_m2m()
            if "delete" in request.POST:
                instance.delete()
                return redirect('misdocs')
        instance_url = reverse('plantillas')+str(instance.doc_id)
        return HttpResponseRedirect(instance_url, context)
    return render(request, "plantillas.html", context)


def CreateDraft(request, text=None, output=None):
    """function to build a draft of the contract. The results are not stored on
       disk"""

    file_object = BytesIO()
    response = HttpResponse(content_type='application/'+output)
    response['Content-Disposition'] = 'attachment; filename=%s' % "doc."+output
    text = str(text).replace(r"[", "").replace("]", "")
    HTML(string=text, base_url=request.build_absolute_uri()).write_pdf(
        target=file_object, stylesheets=[CSS(string=("""
                                                 @page{
                                                         font-family: arial;
                                                         @bottom-right {
                                                         content: counter(page);
                                                         font-size: 10px;
                                                         }}
                                                 body {
                                                         font-family: arial;
                                                         font-size: 12px;
                                                         }"""))])

    response.write(file_object.getvalue())
    file_object.close()
    return response


def publicmodels(request):
    public_data = plantillaModel.objects.filter(public=1)
    display_data = {
        "public_detail": public_data,
        "tag_names": [i.name for i in Tag.objects.all()]
    }
    return render_to_response("publicmodels.html", display_data,
                              context_instance=RequestContext(request))


@login_required
def mydocs(request):
    public_data = plantillaModel.objects.filter(user=request.user)
    display_data = {
        "public_detail": public_data,
        "tag_names": [i.name for i in Tag.objects.all()]
    }
    return render_to_response("misdocs.html", display_data,
                              context_instance=RequestContext(request))


def tagpagePrivate(request, tag):
    public_data = plantillaModel.objects.filter(tags__name=tag)
    display_data = {
        "public_detail": public_data,
        "tag_names": [i.name for i in Tag.objects.all()]
    }
    return render_to_response("misdocs.html", display_data,
                              context_instance=RequestContext(request))


def tagpagePublic(request, tag):
    public_data = plantillaModel.objects.filter(public=1, tags__name=tag)
    display_data = {
        "public_detail": public_data,
        "tag_names": [i.name for i in Tag.objects.all()]
    }
    return render_to_response("publicmodels.html", display_data,
                              context_instance=RequestContext(request))


@login_required
def viewdoc(request, doc_id=None):
    instance = plantillaModel.objects.get(doc_id=doc_id)
    filter_tags = plantillaModel.objects.filter(doc_id=doc_id)
    form = plantillaForm(request.POST or None, instance=instance)
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        content_type = ContentType.objects.get(model="plantillamodel")
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        new_comment, create = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data
        )

    comments = instance.comments
    context = {
        "form": form,
        "text": instance.summernote,
        "title": instance.title,
        "description": instance.description,
        "tags_data": filter_tags,
        "comments": comments,
        "comment_form": comment_form,
        "doc_id": instance.doc_id
    }

    return render(request, "viewdoc.html", context)


@login_required
def newdoc(request, doc_id=None):
    instance = plantillaModel.objects.get(doc_id=doc_id)
    form = plantillaForm(request.POST or None, instance=instance)
    context = {
        "form": form,
        "text": instance.summernote,
    }
    instance = plantillaModel.objects.get(doc_id=doc_id)
    instance.user = request.user
    instance.doc_id = str(uuid.uuid4())[:10]
    instance.pk = None
    instance.title = ""
    instance.description = ""
    instance.save()
    context = {
        "form": form,
        "doc_id": instance.doc_id,
    }
    instance_url = reverse('plantillas')+context["doc_id"]
    return HttpResponseRedirect(instance_url, context)
