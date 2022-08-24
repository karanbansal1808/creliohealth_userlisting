import requests
from multiprocessing import context
from urllib.request import Request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Userdetails
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
from django.http import JsonResponse
from django.db.models import Q
import pandas as pd
import datetime
Userdetails_PER_PAGE = 5


def index(request):
    if len(Userdetails.objects.all()) == 0:
        return redirect(getdata)
    search = request.GET.get('search', "")
    gendercheck = request.GET.get('gender', "")
    if search:
        User = Userdetails.objects.filter(
            Q(name__icontains=search) | Q(id__icontains=search))

    else:
        User = Userdetails.objects.all()

    if gendercheck:
        User = User.filter(gender=gendercheck)

    # Pagination
    page = request.GET.get('page', 1)
    Userdetails_paginator = Paginator(User, Userdetails_PER_PAGE)
    try:
        User = Userdetails_paginator.page(page)
    except EmptyPage:
        User = Userdetails_paginator.page(Userdetails_paginator.num_pages)
    except:
        User = Userdetails_paginator.page(Userdetails_PER_PAGE)
    return render(request, "index.html", {"user": User, 'page_obj': User, 'is_paginated': True, 'paginator': Userdetails_paginator})


def details(request, detail):
    User = Userdetails.objects.get(uuid=detail)
    return render(request, "basic.html", {"user": User})


def getdata(request):
    if len(Userdetails.objects.all()) > 0:
        Userdetails.objects.all().delete()
    count = request.GET.get("result", "20")
    response = requests.get('https://randomuser.me/api/?results='+count)
    if response.status_code != 200:
        return render(request, "error.html")
    datas = response.json(cls=json.JSONDecoder)["results"]
    data = pd.json_normalize(datas)
    data.to_csv("inputs.csv")
    data["location.street.number"] = data["location.street.number"].apply(str)
    add = pd.DataFrame()
    add["gender"] = data["gender"]
    add["name"] = data[["name.title", "name.first", "name.last"]].apply(
        lambda x: " ".join(x), axis=1)
    add["location"] = data[["location.street.number", "location.street.name"]].apply(
        lambda x: " ".join(x), axis=1)
    add["city"] = data["location.city"]
    add["state"] = data["location.state"]
    add["country"] = data["location.country"]
    add["postcode"] = data["location.postcode"]
    add["email"] = data["email"]
    add["username"] = data["login.username"]
    add["uuid"] = data["login.uuid"]
    add["dob"] = data["dob.date"]
    add["registered"] = data["registered.date"]
    add["phone"] = data["phone"]
    add["cell"] = data["cell"]
    add["id"] = data[["id.name", "id.value"]].fillna(
        " ").apply(lambda x: "".join(x), axis=1)
    add["picture"] = data["picture.thumbnail"]
    add["nationality"] = data["nat"]
    for i in add.to_dict(orient="records"):
        userdetail = Userdetails()
        for k, v in i.items():
            if k == "dob" or k == "registered":
                setattr(userdetail, k, datetime.datetime.strptime(
                    v, '%Y-%m-%dT%H:%M:%S.%fZ'))
            else:
                setattr(userdetail, k, v)
        userdetail.save()
    return redirect(index)
