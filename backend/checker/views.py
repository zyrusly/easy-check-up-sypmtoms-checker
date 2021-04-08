from django.shortcuts import render, redirect,HttpResponse
from decouple import config
from hashlib import md5
from urllib.parse import urlencode
from .models import SymptomsModel, IssuesDetail
import requests
import hmac
import base64
import json



BASE_URI = 'https://sandbox-healthservice.priaid.ch'


# Hmac md5 hashing for Authorization and Authentication as per Api docs
def generate_token():
    AUTH_URI = 'https://sandbox-authservice.priaid.ch/login'
    API_KEY = config('API_KEY')
    SECRET_API_KEY = config('SECRET_API_KEY')

    hashed = hmac.new(str.encode(SECRET_API_KEY), AUTH_URI.encode('UTF-8'),md5).digest()
    hashed_key = base64.b64encode(hashed).decode()

    headers = {
        'Authorization': f'Bearer {API_KEY}:{hashed_key}'
    }
    token_request = requests.post(url= AUTH_URI, data = {}, headers=headers)
    ACCESS_TOKEN = token_request.json().get('Token')
    
    return ACCESS_TOKEN


#Api call to list the symptoms
def symptoms_listing():
    access_token = generate_token()
    endpoint = f"{BASE_URI}/symptoms?token={access_token}&format=json&language=en-gb"
    symptoms_request = requests.get(endpoint)
    symptoms_request.encoding = 'utf-8-sig'
    symptoms_array = symptoms_request.json()

    return symptoms_array


#passing symptoms to the database
def pass_symptoms_to_model():
    s_listing = symptoms_listing()
    s_model = SymptomsModel()

    for lists in s_listing:
        sl = lists['ID']
        sn = lists['Name']
        s_model, created = SymptomsModel.objects.get_or_create(ID =f'{sl}', Name = f'{sn}' )
        s_model.save()


# creat_symptoms_model = pass_symptoms_to_model()

#========================================================================================================================================
#========================================================================================================================================


#render symtoms and forms 
def get_symptoms(request):
    try:
        access_token = generate_token()
        request.session['access_token'] = access_token
    except:
        return HttpResponse('<h4> The API has failed to respond</h4>')

    symptoms = SymptomsModel.objects.all()
    context = {'symptoms':symptoms}

    if request.method == 'POST':
        pass
        symptoms_list = request.POST.getlist('proposed_symptoms')
        gender = request.POST.get('gender')
        birth_year = request.POST.get('year_of_birth')    
        query_string =urlencode({
            'symptoms_list':symptoms_list,
            'gender':gender,
            'birth_year':birth_year
        })
        url = '{}?{}'.format('/diagnosis/',query_string)
        return redirect(url)

    return render(request, 'checker/symptoms.html', context)



# Receiving data from <get_symptoms> and passing to <get_diagnosis>
# Passing the the data to End point taken from GET to call the API
def get_diagnosis(request):
    access_token = request.session.get('access_token')
    s_list = request.GET.get('symptoms_list')
    gender = request.GET.get('gender')
    birth_year = request.GET.get('birth_year')
    issue_Model = IssuesDetail()
    issue_item = []

    try:
# API call to correlate the taken symptoms
        diagnosis_endpoint =  f"{BASE_URI}/diagnosis?symptoms={s_list}&gender={gender}&year_of_birth={birth_year}&token={access_token}&format=json&language=en-gb"
        diagnosis_request = requests.get(diagnosis_endpoint)

    # Checking if the API returns Meaningful Data
        if (diagnosis_request.text =='[]'): 
            return HttpResponse("<h2>Listed Symptoms cannot be correlated, try another</h2>")
            #Insert a reverse url sometime

        else:
            diagnosis_request.encoding = 'utf-8-sig'
            diagnosis = diagnosis_request.json()

    #Looping through the list of Diagnoses to check for database entry; create otherwise
    # --see django docs method 'get_or_create' for an alternative solution--
            for issues in diagnosis:
                print(issues)
                issue_id = issues['Issue']['ID']
                try:
                    issue_item.append(IssuesDetail.objects.get(Issue_Id = issue_id))

                except:
                    ISSUE_ENDPOINT = f'https://sandbox-healthservice.priaid.ch/issues/{issue_id}/info?token={access_token}&format=json&language=en-gb'
                    issue_request = requests.get(ISSUE_ENDPOINT)
                    issue_request.encoding = 'utf-8'
                    issue_json = issue_request.json()
                    issue_Model = IssuesDetail.objects.create(
                        Issue_Id=issue_id,
                        Name=issue_json['Name'],
                        DescriptionShort=issue_json['DescriptionShort'],
                        MedicalCondition=issue_json['MedicalCondition'],
                        ProfName=issue_json['ProfName'],
                        TreatmentDescription=issue_json['TreatmentDescription'])
                    issue_Model.save()
                    issue_item.append(IssuesDetail.objects.get(Issue_Id = issue_id))

            context = {'diagnosis':diagnosis, 'issue_item':issue_item}
    except:
        return HttpResponse("<h2>Somthing is wrong...</h2> </br> <h4>'insert error code and reverse sometime'</h4><br/>")

    return render(request, 'checker/diagnosis.html', context )




    