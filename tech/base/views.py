from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from . import models
from django.contrib.auth.models import User,auth
import requests
import threading
from django.http import JsonResponse
import os
import subprocess
from django.utils.safestring import mark_safe
from PIL import Image
from bs4 import BeautifulSoup
from datetime import datetime
import random
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from pathlib import Path 
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def login(request):
    if request.method=="POST":
        username=request.POST['email']
        password=request.POST['password']
        # print(authenticate(username=username,password=password))
        try:
            check=authenticate(username=User.objects.get(email=username),password=password)
        except:
            check=authenticate(username=username,password=password)
        if check is not None:
            auth.login(request,check)
            return redirect('home')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('login')
        
    return render(request,'login.html')


def register(request):
    if request.method=='POST':
        name=request.POST['name']
        username=request.POST['username']
        email=request.POST['email']
        phoneno=request.POST['phoneno']
        state=request.POST['state']
        district=request.POST['district']
        p1=request.POST['password1']
        p2=request.POST['password2']
        if models.User.objects.filter(email=email).exists():
            messages.info(request,'email already registered')
            return redirect('register')
        elif models.User.objects.filter(username=username).exists():
            messages.info(request,'Username already exists')
            return redirect('register')
        elif p1!=p2:
            messages.info(request,"Password and Confirm password didn't match")
            return redirect('register')
        else:
            new_user=models.User.objects.create(username=username,email=email)
            new_user.set_password(p1)  
            new_user.save()
            new_prof=models.Profile.objects.create(user=new_user,name=name,state=state,city=district,phoneno=phoneno)
            new_prof.save()
            auth.login(request,new_user)
            return redirect('home')
    return render(request,'register.html')

@login_required(login_url='login')
def home(request):
    prof=models.Profile.objects.get(user=request.user)
    return render(request,'homePage.html',{'prof':prof})
 
@login_required(login_url='login')
def profile(request):
    prof=models.Profile.objects.get(user=request.user)
    return render(request,'profile.html',{'prof':prof})

@login_required(login_url='login')
def Aboutus(request):
    prof=models.Profile.objects.get(user=request.user)
    return render(request,'about.html',{'prof':prof})

@login_required(login_url='login')
def schemes(request):
    prof=models.Profile.objects.get(user=request.user)
    return render(request,'schemes.html',{'prof':prof})

@login_required(login_url='login')
def loan(request):
    data=models.loan.objects.all()
    prof=models.Profile.objects.get(user=request.user)
    return render(request,'loan.html',{'data':data,'prof':prof})

@login_required(login_url='login')
def crop(request):
    prof=models.Profile.objects.get(user=request.user)
    return render(request,'cropmange.html',{'prof':prof})

# @login_required(login_url='login')
def make_api_request(url, all_data):
    response = requests.get(url)
    data = response.json()
    if data:
        all_data.append(data)

@login_required(login_url='login')
def market(request):
    try:
        curr = models.Profile.objects.get(user=request.user)
        state_filter=curr.state
        district_filter=curr.city
        limit=1
        if request.method=='POST':
            state_filter=request.POST['state']
            district_filter=request.POST['district']
        all_data=[]
        api_urls=[f"https://api.data.gov.in/resource/e3f56f8b-d881-4850-b1fd-ee14480fce8e?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f"https://api.data.gov.in/resource/c94a4a82-b0cf-435a-ba4b-a6d8ee26b0c8?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f"https://api.data.gov.in/resource/78329234-2d42-4f71-867c-a376a3b10c45?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f"https://api.data.gov.in/resource/d2d6f030-b49b-417a-897a-5a0e41eb3fdd?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f"https://api.data.gov.in/resource/9442098e-9c72-4e41-bdd1-0ac3be157c07?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f"https://api.data.gov.in/resource/641dd73b-1c8e-4ddf-a8d2-a53741b34a2c?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f"https://api.data.gov.in/resource/61792629-e13b-46f0-850f-727c1f148a82?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f"https://api.data.gov.in/resource/73cd6b13-f480-436a-9347-9f81a2845909?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f"requests.get(f'https://api.data.gov.in/resource/3b21a673-c236-460b-864d-9f39016a719d?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f"https://api.data.gov.in/resource/2191b45a-3a28-4f72-9942-dbc1cc7a91b5?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f"https://api.data.gov.in/resource/4e0dd1cf-98ac-4e78-9024-8e93f9737f56?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f"https://api.data.gov.in/resource/51c5b28a-d27b-4529-bdf8-007f67e9f347?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f"requests.get(f'https://api.data.gov.in/resource/da7c92ff-0e50-447f-9f92-48fabb4a105a?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}",
        f'https://api.data.gov.in/resource/a2118264-db52-4cfd-b04f-6ce8b0f146a3?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/03db0d1e-39a4-46c7-9de8-77ad0c853475?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/7cb6ad9c-f8a9-4ce3-8db8-dc5b1a70de3a?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/766ddd21-e10c-4048-9289-1b4ec1ac058b?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/264eb10d-53c6-434c-afb2-d70ede0fb364?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/e863c509-81a9-4b55-aae3-685a01324b1c?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/a61861b2-fe5b-47ed-b373-930af0c0eb73?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/fb208485-bbdb-45c7-9a38-aefbfd4c596e?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/c7ae43c6-920d-483c-9f8e-974ac2d49c72?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/a7856635-c351-4b20-8333-1c826da5249c?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/8f618ca8-7c10-48f4-83b2-43e711d32109?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/1266b30e-ced4-4847-a504-c1cddfb0b85d?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/cf7c3c0e-7c5f-4d89-85dd-aaf5fa20e6ec?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}',
        f'https://api.data.gov.in/resource/8a11f00c-09ca-44eb-aea2-93961a548194?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit={limit}&filters%5B_state_%5D={state_filter}&filters%5Bdistrict%5D={district_filter}']
        
        threads = [threading.Thread(target=make_api_request, args=(url, all_data)) for url in api_urls]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        prof=models.Profile.objects.get(user=request.user)
        cont = {'response': all_data,'prof':prof}
        return render(request,'marketprice.html',cont)
    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle the error gracefully, maybe redirect to an error page or render an error message
        return HttpResponse("An error occurred while processing your request.")

@login_required(login_url='login')
def estimate(request):
    return render(request,'estimate.html')

@login_required(login_url='login')
def run_streamlit_app():
    streamlit_command = ["streamlit", "run", "base/.streamlit/chatbot1.py"]
    subprocess.run(streamlit_command)

@login_required(login_url='login')
def crop2(request):
    path=str(BASE_DIR)+"/.streamlit/chatbot1.py"
    streamlit_command = ["streamlit", "run", path]

    # Run the Streamlit app as a separate process
    process = subprocess.Popen(streamlit_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the process to finish (optional)
    process.wait()

    # Capture the output and errors (optional)
    output, errors = process.communicate()

    # Pass the output or errors to the template context (optional)
    context = {'output': output, 'errors': errors}
    
    # Render your template or return an HTTP response
    return render(request, 'crop2.html', context)

@login_required(login_url='login')
def news(request):
    prof=models.Profile.objects.get(user=request.user)
    url='https://economictimes.indiatimes.com/news/economy/agriculture?from=mdr'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    webpage=requests.get(url,headers=headers).text
    soup=BeautifulSoup(webpage, 'lxml')
    len(soup.find_all('h3'))

    news_heading = []

    for h3_tag in soup.find_all('h3'):
        if 'm-heading3' not in h3_tag.get('class', []):
            news_heading.append(h3_tag.text.strip())
        else:
            h3_tag.extract()

    news_date = []


    for time_tag in soup.find_all('time', class_='date-format'):
        date_string = time_tag.text.strip()
        date_components = date_string.split(', ')  # Split the string by comma and space
        month_day_year = date_components[0].split(' ')  # Split the first part into month, day, and year
        month = month_day_year[0]  # Extract month abbreviation
        day = month_day_year[1].strip(',')  # Extract day and remove trailing comma
        year = date_components[1].strip()  # Extract year
        date_only = f"{month} {day}, {year}"  # Construct the date string
        news_date.append(date_only)

    news_about = []


    for p_tag in soup.find_all('p', class_='wrapLines'):
        news_about.append(p_tag.text.strip())

    img_containers = soup.find_all('span', class_='imgContainer')

    len(img_containers)

    news_img = []
    for container in img_containers:
        img_tag = container.find('img')
        if img_tag:
            src_link = img_tag.get('src')
            news_img.append(src_link)

    news_link = []

    for h3_tag in soup.find_all('h3'):
        a_tag = h3_tag.find('a')  # Find the <a> tag within the <h3> tag
        if a_tag:
            href_link = a_tag.get('href')  # Extract the href attribute
            full_link = "https://economictimes.indiatimes.com" + href_link  # Append the specified line before the href tag
            news_link.append(full_link)

    news_dict = {
    "news_heading": news_heading,
    "news_date": news_date,
    "news_about": news_about,
    "news_img": news_img,
    "news_link":news_link
    }
    news_dict_list = []

    for i in range(len(news_heading)):
         news_dict_list.append({
        "news_heading": news_heading[i],
        "news_date": news_date[i],
        "news_about": news_about[i],
        "news_img": news_img[i] if i < len(news_img) else None,
        "news_link": news_link[i]
    })

    return render(request,'news.html',{'news':news_dict_list,'prof':prof})
def isnight(time):
    time=int(time)
    if (time >= 12):
        return True
    
    return False

@login_required(login_url='login')
def weather(request):
    prof=models.Profile.objects.get(user=request.user)
    curr=models.Profile.objects.get(user=request.user)
    city = curr.city
    API_key = 'ec3c5349acccf30efb4e7c6727731563'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}'
    url2 = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_key}'
    city_weather = requests.get(url).json()
    city_weather2 = requests.get(url2).json()
    curr_date = datetime.now().strftime('%A, %B %d')
    curr_time = datetime.now().strftime('%I:%M %p')
    current_time = datetime.now()
    now = datetime.now().date()
    
    time= datetime.now().strftime('%H:%M')
    temp = int(city_weather['main']['temp'] - 273.15)
    icons_dict={ 'Clear': {'icon': "☀️", 'color': "#ffeb3b"},
        'Sunny': {'icon': "☀️", 'color': "#ffeb3b"},
        'Mostly Sunny': {'icon': "🌤️", 'color': "#ffeb3b"},
        'Partly Sunny': {'icon': "⛅", 'color': "#ffeb3b"},
        'Clouds': {'icon': "☁️", 'color': "#cfd8dc"},
        'Mostly Cloudy': {'icon': "☁️", 'color': "grey"},
        'Partly Cloudy': {'icon': "⛅", 'color': "grey"},'Rain':{'icon':"🌧️",'color':'#81d4fa'},'Thunderstorm':{'icon':"⛈️",'color':''},'Haze':{'icon':"🌫️",'color':''},'Mist':{ 'icon':"🌫️",'color':''},'Fog':{ 'icon':"🌫️",'color':''},'Smoke':{ 'icon':"🌫️",'color':''},'Drizzle': {'icon':"🌧️",'color':''},'Showers': {'icon':"🌧️",'color':''},'Sunny Intervals':{'icon':"⛅",'color':''},'Overcast':{'icon':"☁️",'color':''},'Mild': {'icon':"⛅",'color':''},'Night':{'icon':'🌙','color':'#cfd8dc'},'Snow':{'icon': "❄️", 'color': "white"}}

    filtered_weather = [item for item in city_weather2['list'] if item['dt_txt'][:10] == str(now)]
    for item in filtered_weather:
        item['main']['temp'] = int(item['main']['temp'] - 273.15)
        main_weather = item['weather'][0]['main']  
        if main_weather in icons_dict:  
            if main_weather == 'Clear' and isnight(item['dt_txt'][11:13]):
                item['icon'] = icons_dict['Night']['icon']  
                item['color'] = icons_dict['Night']['color']
            else:
                item['icon'] = icons_dict[main_weather]['icon']  
                item['color'] = icons_dict[main_weather]['color']
    date_checked = set()
    filtered_weather2 = []
    for item in city_weather2['list']:
        if item['dt_txt'][:10] != str(now) and item['dt_txt'][:10] not in date_checked:
            filtered_weather2.append(item)
            date_checked.add(item['dt_txt'][:10])
        
    for item in filtered_weather2:
        item['main']['temp_min'] = int(item['main']['temp_min'] - 273.15)
        item['main']['temp_max'] = int(item['main']['temp_max'] - 273.15)
        dt_txt = item['dt_txt']
        date_obj = datetime.strptime(dt_txt[:10], '%Y-%m-%d')
        day_name = date_obj.strftime('%A')
        item['formatted_date'] = f"{day_name}, {date_obj.strftime('%B %d')}"
        main_weather = item['weather'][0]['main']  
        if main_weather in icons_dict:
            item['icon'] = icons_dict[main_weather]['icon']  
            item['color'] = icons_dict[main_weather]['color']

        if city_weather['weather'][0]['main'] == 'Clear' and isnight(time[:2]):
                icon = icons_dict['Night']['icon']  
        else:
            icon = icons_dict[city_weather['weather'][0]['main']]['icon']


    return render(request, 'weather.html', {'simple':city_weather,'weather': filtered_weather,'weather2':filtered_weather2,'desc': city_weather['weather'][0]['main'],
    'state': 'Rajasthan', 'city': city, 'curr_date': curr_date,'curr_time': time, 'temp': temp,'icon':icon,'prof':prof,'s':int(time[0:2])})

@login_required(login_url='login')
def detail(request,pk):
    prof=models.Profile.objects.get(user=request.user)
    sch=models.Schemes.objects.get(id=pk)
    return render(request,'detail.html',{'details':sch,'prof':prof})

@login_required(login_url='login')
def services(request):
    prof=models.Profile.objects.get(user=request.user)
    return render(request,'services.html',{'prof':prof})

@login_required(login_url='login')
def chatbot(request):
    path=str(BASE_DIR)+"/.streamlit/chatbot2.py"
    streamlit_command = ["streamlit", "run", path]
    process = subprocess.Popen(streamlit_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()

@login_required(login_url='login')
def edit(request):
    prof=models.Profile.objects.get(user=request.user)
    curr_user=User.objects.get(username=request.user.username)
    if request.method=="POST":
        if request.FILES.get('image')==None:
            img=prof.profimag
            name=request.POST['name']
            username=request.POST['username']
            phoneno=request.POST['phoneno']
            email=request.POST['email']

            curr_user.username=username
            curr_user.email=email
            curr_user.save()
            prof.profimag=img
            prof.name=name
            prof.phoneno=phoneno
            prof.save()
            return redirect('profile')
        else:
            img=request.FILES.get('image')
            name=request.POST['name']
            username=request.POST['username']
            phoneno=request.POST['phoneno']
            email=request.POST['email']

            curr_user.username=username
            curr_user.email=email
            curr_user.save()
            prof.profimag=img
            prof.name=name
            prof.phoneno=phoneno
            prof.save()
            return redirect('profile')

    return render(request,'editProfile.html',{'prof':prof})

def logout(request):
    auth.logout(request)
    return redirect('login')

def sale(request):
    post=models.posts.objects.all()
    prof=models.Profile.objects.get(user=request.user)

    return render(request,'sale.html',{'post':post,'prof':prof})

def posts(request):
    prof=models.Profile.objects.get(user=request.user)
    post=models.posts.objects.filter(post_user=prof)
    return render(request,'posts.html',{'post':post})

def add_post(request):
    prof=models.Profile.objects.get(user=request.user)
    if request.method=='POST':
        crop_name=request.POST['crop_name']
        price=request.POST['price']
        address=request.POST['address']
        crop_icons = {
        "Rice": "🌾",
        "Wheat": "🌾",
        "Maize": "🌽",
        "Barley": "🌾",
        "Sugarcane": "🎋",
        "Cotton": "🌱",
        "Tea": "🍵",
        "Coffee": "☕",
        "Pulses": "🌱",
        "Oilseeds": "🌻",
        "Fruits": "🍎",
        "Vegetables": "🥕",
        "Spices": "🌶️",
        "Jute": "🌿",
        "Rubber": "🌳",
        "Tobacco": "🌿",
        "Soybeans": "🌱",
        "Sesame": "🌱",
        "Groundnuts": "🌱",
        "Coconut": "🥥",
        }
        icon = crop_icons.get(crop_name)
        print(icon)
        new_post=models.posts.objects.create(post_user=prof,crop=crop_name,price=price,address=address,icon=icon)
        new_post.save()
        return redirect('sale')
    
def delete(request):
    idd=request.GET.get('post_id')
    to_deleted=models.posts.objects.get(post_id=idd)
    to_deleted.delete()
    return redirect('posts')
