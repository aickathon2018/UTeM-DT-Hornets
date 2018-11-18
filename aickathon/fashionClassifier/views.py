from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse, reverse_lazy

import requests 
import json     
import os, glob
import time
from collections import Counter

# Create your views here.

def index(request):
    return render(request, 'fashionClassifier/index.html')

def classify(request):
    # Path of image (jpg/jpeg/png)
    folderpath = request.POST['filepath']
    folder_path = folderpath
    
    urlfashion = "https://fashion.recoqnitics.com/analyze"
    accessKey = "f875950af9fa76141729"
    secretKey = "2f2ffd21de62e45439e7269d38b17e0b9619b493"
    
    urlface = "https://face.recoqnitics.com/analyze"
    # access_key and secret_key
    data = {'access_key': accessKey,
            'secret_key': secretKey}
    
    male = 0
    female = 0
    i = 0
    child = 0
    teen = 0
    adult = 0
    
    listBajuChild = []
    listBajuTeen = []
    listBajuAdult = []
    

    for file in glob.glob(os.path.join(folder_path, '*.*')):
            
        if file.endswith( ".jpg" ) or file.endswith( ".png" ) or file.endswith( ".jpeg" ):
            i += 1
            time.sleep(12)
        
            filename = {'filename': open(file,'rb')}
            rfashion = requests.post(urlfashion, files = filename, data=data)
            contentfashion = json.loads(rfashion.content)
            print(str(i) + " fashion process")
                #print(contentfashion)
                #print("\n")
            filename = {'filename': open(file,'rb')}
            rface = requests.post(urlface, files = filename, data=data)
            contentface = json.loads(rface.content)
            print(str(i) + " face process")
                #print(contentface)
            print("\n")
            jantina = (contentface.get('faces')[0]['gender']['value'])
                
            if jantina == 'Female':
                female += 1
            elif jantina == 'Male':
                male += 1
                    
            if contentface.get('faces')[0]['age'] < 14:
                child += 1
                    
                try:
                    listBajuChild.append(contentfashion.get('person').get('garments')[0]['typeName'])
                except:
                    continue
                
            elif contentface.get('faces')[0]['age'] < 22:
                teen += 1
                    
                try:
                    listBajuTeen.append(contentfashion.get('person').get('garments')[0]['typeName'])
                except:
                    continue
            else:
                adult += 1
                    
                try:
                    listBajuAdult.append(contentfashion.get('person').get('garments')[0]['typeName'])
                except:
                    continue
        
    print("Total images openned : " + str(i))
    print("The amount of male pictures are : " + str(male))
    print("The amount of female pictures are: " + str(female))
    print("The amount of child pictures are: " + str(child))
    print("The amount of teenage pictures are: " + str(teen))
    print("The amount of adult pictures are: " + str(adult))
        
    bilChild = Counter(listBajuChild)
    bilTeen = Counter(listBajuTeen)
    bilAdult = Counter(listBajuAdult)
        
    def cariBanyak(countt):
        i = 0
        banyaknya = 'banyak'
        for k,v in countt.items():
                
            if i == 0 :
                maxx = v
                banyaknya = k
                i += 1
                
            else:
                if v >= maxx :
                    banyaknya = k
                    
        return banyaknya
    fChild = cariBanyak(bilChild)
    fTeen = cariBanyak(bilTeen)
    fAdult = cariBanyak(bilAdult)
    print(fChild)
    print(fTeen)
    print(fAdult)
    return render(request, 'fashionClassifier/results.html', {'fChild' : fChild,
                                                                  'fTeen' : fTeen,
                                                                  'fAdult' : fAdult,})