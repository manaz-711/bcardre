from django.shortcuts import render
import io
import os
from PIL import Image
import io as StringIO
import json
import pandas as pd
from google.cloud import vision
from google.cloud import language
from google.cloud import language_v1
from google.cloud.language import enums
from google.cloud.language import types
# from google.cloud import language_vp1
from google.cloud.language_v1 import enums
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import re as rg

from django.core.exceptions import ValidationError

from .models import Person
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from .serializers import PersonSerializer

import time
from bcard.settings import CREDENTIAL,JOB_TITLES
# Create your views here.



def index(request):
    return render(request, 'gapii/imupload.html')

def data(request):
    # print('hello')
    if request.method == 'POST' :
        if 'myfile' in request.FILES:
            myfile = request.FILES.get('myfile', None)


            # credential_path = "/home/abdul/env/bcard/gapii/g-vision-api-511b7da8c0b7.json"
            # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
            os.environ['GOOGLE_APPLICATION_CREDENTIALS']=CREDENTIAL

            client = vision.ImageAnnotatorClient()
            client1 = language.LanguageServiceClient()
            client2 = language_v1.LanguageServiceClient()

            # file_name = strdata
            type_ = enums.Document.Type.PLAIN_TEXT
            languagee = "en"


            # with io.open(myfile, 'rb') as image_file:
            content = myfile.read()
            image = vision.types.Image(content=content)
            response = client.text_detection(image=image)  # returns TextAnnotation
            df = pd.DataFrame(columns=['locale', 'description'])
            texts = response.text_annotations
            # print(texts)
            for text in texts:
                df = df.append(
                    dict(
                        locale=text.locale,
                        description=text.description
                    ),
                    ignore_index=True
                )

            re = df['description'][0]
            print(re)

            text = re
            textd = re
            card_data=re.replace(',', '\n')

            document = types.Document(
                content=text,
                type=enums.Document.Type.PLAIN_TEXT)

            sentiment = client1.analyze_sentiment(document=document).document_sentiment

            # print('Text: {}'.format(text))

            document = {"content": text, "type": type_, "language": languagee}

            encoding_type = enums.EncodingType.UTF8

            response1 = client2.analyze_entities(document, encoding_type=encoding_type)

            largest_salience = -1

            for entity in response1.entities:
                # print(format(enums.Entity.Type))
                na = ""

                if format(enums.Entity.Type(entity.type).name) == "PERSON":

                    n1 = format(entity.name)

                    for k, v in JOB_TITLES:

                        try:

                            n1 = n1.replace(k, v)
                        except:
                            continue

                    na = n1

                    ss = float(format(entity.salience))
                    if ss > largest_salience and n1 != "":
                        largest_salience = ss
                        na = format(entity.name)
                        nm = na

                    if (ss <= 0.03 or na == "" or len(na) <= 1):
                        continue
            for k, v in JOB_TITLES:
                try:
                    nm = nm.replace(k, v)
                except:
                    continue

            print("Name: " + nm)
            # print("Salience:%f"%ss)

            match = rg.findall(r'[\w\.-]+@[\w\.-]+', text)
            for i in match:
                print("Email Id:" + i)
                em = i

            mathf = rg.findall(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]', text)
            for j in mathf:
                print("Phone:" + j)
                ph = j
            matchweb = rg.findall(
                r'\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b',
                text)
            for k in matchweb:
                wid = k

            print("Website:" + wid)
            text2=textd
            text2 = text2.replace(nm, '')
            text2 = text2.replace(em, '')
            text2 = text2.replace(ph, '')
            text2 = text2.replace(wid, '')

            document2 = types.Document(
                content=text2,
                type=enums.Document.Type.PLAIN_TEXT)

            response2 = client2.analyze_entities(document, encoding_type=encoding_type)
            address = []
            for entity in response2.entities:
                # print(format(enums.Entity.Type))
                if format(enums.Entity.Type(entity.type).name) == "ORGANIZATION" or format(
                        enums.Entity.Type(entity.type).name) == "LOCATION" or format(
                        enums.Entity.Type(entity.type).name) == "ADDRESS":
                    sd = float(format(entity.salience))

                    address.append(format(entity.name))
                   
            add = str(address)
            s = ""
            for i in address:
                s = s + i +", "+"\n"

            print("Address: " + s)

            p = Person()
            p.img = myfile
            # print(myfile)
            p.save()

            print(myfile)
            obj = Person.objects.latest('id')

            imagere = obj.img
            print(imagere)

            # print(imagere)


            return render(request, 'gapii/imupload.html',
                          {"name": nm, "email": em, "phonenumber": ph, "website": wid, "address": s,"image":imagere,"data":card_data})

        else:
            return render(request, 'gapii/imupload.html')
    return render(request, 'gapii/imupload.html')

def save(request):
    if request.method == 'POST':
            a = Person()

            a.name = request.POST.get("name")
            a.email =request.POST.get("email")
            a.phone = request.POST.get("phonenumber")
            a.address = request.POST.get("address")
            a.website=request.POST.get("website")
            a.save()
            # messages.success(request, 'Account Created')
            return render(request, "gapii/imupload.html")
    else:
        # form = CreateUser()
         return HttpResponse("aaa")

def bcarddetails(request):
    datas=Person.objects.all()
    return render(request,"gapii/bcardata.html",{"data":datas})

@api_view(['GET', 'POST'])
@csrf_exempt
def imageupload(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Person.objects.all()
        serializer = PersonSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PersonSerializer(data=request.data, context={'request':request})
        print(request.data)
        print('Hello')
        print(Person.img)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def apiupload(request):
    if request.method=='POST':
        print(request.data)
        myfile=request.data.get('img')
        serializer = PersonSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():


            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIAL

            client = vision.ImageAnnotatorClient()
            client1 = language.LanguageServiceClient()
            client2 = language_v1.LanguageServiceClient()

            # file_name = strdata
            type_ = enums.Document.Type.PLAIN_TEXT
            languagee = "en"


            # with io.open(myfile, 'rb') as image_file:
            content = myfile.read()

            image = vision.types.Image(content=content)
            # t_vision =time.time()
            response = client.text_detection(image=image)  # returns TextAnnotation
            df = pd.DataFrame(columns=['locale', 'description'])
            texts = response.text_annotations

            # print(texts)
            for text in texts:
                df = df.append(
                    dict(
                        locale=text.locale,
                        description=text.description
                    ),
                    ignore_index=True
                )

            re = df['description'][0]
            # t_evision=time.time()
            # print("total time:"+t_vision-t_evision)
            print(re)

            text = re
            textd = re
            document = types.Document(
                content=text,
                type=enums.Document.Type.PLAIN_TEXT)

            # sentiment = client1.analyze_sentiment(document=document).document_sentiment

            # print('Text: {}'.format(text))

            document = {"content": text, "type": type_, "language": languagee}

            encoding_type = enums.EncodingType.UTF8

            response1 = client2.analyze_entities(document, encoding_type=encoding_type)

            largest_salience = -1
            other_salience=-1
            nm = ""
            for entity in response1.entities:
                # print(format(enums.Entity.Type))
                na = ""

                if format(enums.Entity.Type(entity.type).name) == "PERSON":

                    n1 = format(entity.name)

                    for k, v in JOB_TITLES:

                        try:

                            n1 = n1.replace(k, v)
                        except:
                            continue

                    na = n1

                    ss = float(format(entity.salience))
                    if ss > largest_salience and n1 != "":
                        largest_salience = ss
                        na = format(entity.name)
                        nm = na

                    if (ss <= 0.03 or na == "" or len(na) <= 1):
                        continue
            for k, v in JOB_TITLES:
                try:
                    nm = nm.replace(k, v)
                except:
                    continue

            print("Name: " + nm)
            # print("Salience:%f"%ss)

            match = rg.findall(r'[\w\.-]+@[\w\.-]+', text)
            for i in match:
                print("Email Id:" + i)
                em = i

            mathf = rg.findall(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]', text)
            for j in mathf:
                print("Phone:" + j)
                ph = j
            matchweb = rg.findall(
                r'\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b',
                text)
            for k in matchweb:
                wid = k

                print("Website:" + wid)

            no=""
            if nm == "" or nm == " ":
                for entity in response1.entities:
                    # print(format(enums.Entity.Type))
                    na = ""

                    if format(enums.Entity.Type(entity.type).name) == "OTHER":

                        n1 = format(entity.name)

                        for k, v in JOB_TITLES:

                            try:

                                n1 = n1.replace(k, v)
                            except:
                                continue

                        na = n1

                        ss = float(format(entity.salience))
                        if ss > other_salience and n1 != "":
                            other_salience = ss
                            na = format(entity.name)
                            nm = na

            text2 = textd
            text2 = textd.replace(nm, '')
            text2 = text2.replace(em, '')
            text2 = text2.replace(ph, '')
            text2 = text2.replace(wid, '')

            document2 = types.Document(
                content=text2,
                type=enums.Document.Type.PLAIN_TEXT)

            response2 = client2.analyze_entities(document, encoding_type=encoding_type)
            address = []
            for entity in response2.entities:
                # print(format(enums.Entity.Type))
                if format(enums.Entity.Type(entity.type).name) == "ORGANIZATION" or format(enums.Entity.Type(entity.type).name) == "LOCATION" or format(enums.Entity.Type(entity.type).name) == "ADDRESS":
                    sd = float(format(entity.salience))

                    address.append(format(entity.name))

            add = str(address)
            s = ""
            for i in address:
                s = s + i + ", " + "\n"

            print("Address: " + s)

            datas = {}
            datas["name"] = nm

            datas["email"] = em
            datas["phonenumber"] = ph
            datas["website"] = wid
            datas["address"] = s
            # datas["image"] = imagea
            # datas["data"] = textview
            return Response(datas, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

