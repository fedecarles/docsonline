from django.shortcuts import (render, redirect)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import plantillaForm
from .forms import userForm
from .forms import userProfileForm
from .models import plantillaModel
from .models import User
from .models import userProfile
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
    latest = plantillaModel.objects.all().order_by('-creation_date')[:5]
    context = {
        'latest': latest,
        'tag_names': [i.name for i in Tag.objects.all()[:5]]
    }
    return render(request, "home.html", context)


@login_required
def plantillas(request, doc_id=None):
    """ Main view to create models, allowing to create templates, save them
    or delete them, only if the user owns the instance.
    The view takes a doc_id (uuid) parameter which is either provided on the url
    or if there is None, created on the spot."""
    user = request.user
    profile = user.profile
    profile_form = userProfileForm(instance=profile)
    if doc_id is None:
        form = plantillaForm(request.POST or None)
        context = {
            "form": form,
            "profile_form": profile_form,
        }
    else:
        instance = plantillaModel.objects.get(doc_id=doc_id)
        form = plantillaForm(request.POST or None, instance=instance)
        context = {
            "form": form,
            "profile_form": profile_form,
        }
        if instance.is_owner(request.user):
            pass
        else:
            raise PermissionDenied
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            # Run CreateDraft function if the POST is pdf.
            if "genpdf" in request.POST:
                return (CreateDraft(request, text=instance.summernote,
                                    output="pdf"))
            # Reload the saved instance.
            elif "reload" in request.POST:
                instance_url = reverse('plantillas')+str(instance.doc_id)
                return redirect(instance_url)
            # delete the instance from the database.
            elif "delete" in request.POST:
                instance.delete()
                instance_url = reverse('view_profile')+str(request.user.id)
                return redirect(instance_url)
            if doc_id is None:
                doc_id = str(uuid.uuid4())[:10]
            else:
                pass
            instance.user = request.user
            instance.creation_date = time.strftime("%d-%m-%Y")
            instance.doc_id = doc_id
            instance.save()
            form.save_m2m()
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
                                                         }
                                                 #parte2 {
                                                     margin-left: 20%;
                                                     }"""))])

    response.write(file_object.getvalue())
    file_object.close()
    return response


def publicmodels(request, tag=None):
    """List view of all templates that are stored as Public. Users can
    browse the list without having to be loged in."""

    if tag is None:
        public_data = plantillaModel.objects.filter(public=1).order_by('-creation_date')
    else:
        public_data = plantillaModel.objects.filter(public=1, tags__name=tag).order_by('-creation_date')
    display_data = {
        "public_detail": public_data,
        "tag_names": [i.name for i in Tag.objects.all()]
    }
    return render(request, "publicmodels.html", display_data)


def viewdoc(request, doc_id=None):
    """View only view of public docs. Users cannot edit content, but can
    fork a copy of the doc for their own use."""

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
        "date": instance.creation_date,
        "title": instance.title,
        "pais": instance.pais,
        "description": instance.description,
        "tags_data": filter_tags,
        "comments": comments,
        "comment_form": comment_form,
        "doc_id": instance.doc_id,
        "instance": instance
    }
    return render(request, "viewdoc.html", context)


@login_required
def newdoc(request, doc_id=None):
    """View to create a new instance of a copied doc. It copy a saved
    template and provides a new uuid for it."""

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


@login_required
def update_profile(request):
    """Profile view for logged user."""
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        user_form = userForm(request.POST, instance=user)
        profile_form = userProfileForm(request.POST, request.FILES,
                                       instance=profile)
        if all([user_form.is_valid(), profile_form.is_valid()]):
            user_form.save()
            profile_form.save()
            instance_url = reverse('view_profile')+str(user.id)
            return redirect(instance_url)
    else:
        user_form = userForm(instance=user)
        profile_form = userProfileForm(instance=profile)
    return render(request, 'update_profile.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def view_profile(request, id=None, tag=None):
    """Profile View for a user other than the logged user (not editable)."""
    userdata = User.objects.get(pk=id)
    userprofile = userProfile.objects.get(user_id=id)
    if tag is None:
        public_data = plantillaModel.objects.filter(user_id=id).order_by('-creation_date')
    else:
        public_data = plantillaModel.objects.filter(user_id=id, tags__name=tag).order_by('-creation_date')

    context = {
        "uuid": str(id),
        "req_id": str(request.user.id),
        "username": userdata.username,
        "nombre": userdata.first_name,
        "apellido": userdata.last_name,
        "email": userdata.email,
        "website": userprofile.website,
        "pais": userprofile.pais,
        "public_detail": public_data,
        "tag_names": [i.name for i in Tag.objects.all()]
    }
    return render(request, 'view_profile.html', context)
