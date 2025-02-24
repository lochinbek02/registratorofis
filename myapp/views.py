from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

from aiogram import Bot
from aiogram.types import ParseMode
from aiogram.utils import executor
import asyncio


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from PIL import Image, ImageDraw, ImageFont
import io
import base64
# Bot tokenini o'zgartiring
BOT_TOKEN = '5625609522:AAEcZEsMaMQKcaEdoNhAx-if7TiKiUVCs-A'
bot = Bot(token=BOT_TOKEN)
async def send_telegram_message(user_id, message_text):
    try:
        # Foydalanuvchi Telegram ID-si va yuboriladigan xabar
        await bot.send_message(user_id, message_text, parse_mode=ParseMode.MARKDOWN)
        return
    except Exception as e:
        print(f"Xato yuz berdi: {str(e)}")
        return 
class GeneralListCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GeneralListCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Ma\'lumot muvaffaqiyatli saqlandi!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        # Add logic to handle GET requests if needed
        return Response({'message': 'This is a GET request'})
class GetQueueNumberView(APIView):
    def get(self, request, *args, **kwargs):
        # Ma'lumotlar sonini hisoblash
        last_entry = GeneralList.objects.order_by("-id").first()
        queue_number = last_entry.id  # Eng oxirgi elementning ID si
 
        return Response({'queue_number': queue_number}, status=status.HTTP_200_OK)
def get_first_generic_list_item(request):
    try:
        first_item = GenericList.objects.first()  # Birinchi obyektni olish
        data = {
            'id': first_item.id,
            'name': first_item.name,  # GenericList modelidagi kerakli fieldlarni qo'shing
            'description': first_item.description,
        }
        return JsonResponse(data, safe=False)
    except GenericList.DoesNotExist:
        return JsonResponse({'error': 'Malumot topilmadi'}, status=404)
def another_page(request):
    item_id = request.GET.get('id')
    item_name = request.GET.get('name')
    item_description = request.GET.get('description')

    return render(request, 'second.html', {
        'item_id': item_id,
        'item_name': item_name,
        'item_description': item_description,
    })
class FirstFiveRecordsView(APIView):
    def get(self, request, *args, **kwargs):
        # Eng birinchi 5 ta yozuvni olish
        first_five_records = GeneralList.objects.all().order_by("id")[:5]
        
        # Yozuvlar bo'yicha aylanish
       
        counter=0
        for record in first_five_records:
            if record.user_telegram_id:

                if counter==0:
                    user_telegram_id = record.user_telegram_id  # yoki kerakli maydonni olish
                    message_text = f"{record.service} xizmat turi bo'yicha sizning navbatingiz keldi. \nIltimos navbatingizni o'z vaqtida foydalaning"  # Yangi yozuv bo'yicha xabar matni

                    # Telegram xabarini yuborish
                    asyncio.run(send_telegram_message(user_telegram_id, message_text))
                else:
                    user_telegram_id = record.user_telegram_id  # yoki kerakli maydonni olish
                    message_text = f"{record.service} xizmat turi bo'yicha navbatingiz kelishiga {counter} ta qoldi"  # Yangi yozuv bo'yicha xabar matni

                    # Telegram xabarini yuborish
                    asyncio.run(send_telegram_message(user_telegram_id, message_text))

            counter+=1
            # Foydalanuvchi Telegram ID-sini olishingiz kerak
        
        # Ma'lumotlarni serializatsiya qilish va qaytarish
        serializer = GeneralListCreateSerializer(first_five_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class HomePageView(TemplateView):
    template_name = 'home.html'

from django.shortcuts import render
# from .forms import DataForm
#home page


def home(request):
    
    return render(request,"home.html")

#application
def application(request):
    
    return render(request,"application.html")



  

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Email orqali foydalanuvchini tekshirish
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect("home")  # Tizimga kirgandan keyin qaysi sahifaga yo‘naltirish kerak bo‘lsa
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, "login.html")

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

import random

@login_required
def task_list(request):
    first_five_records = GeneralList.objects.filter(is_completed=False, assigned_to__isnull=True).order_by("id")[:5]

        
        
    counter=0
    for record in first_five_records:
        if record.user_telegram_id:
            if counter==0:
                user_telegram_id = record.user_telegram_id  # yoki kerakli maydonni olish
                message_text = f"{record.service} xizmat turi bo'yicha sizning navbatingiz keldi. \nIltimos navbatingizni o'z vaqtida foydalaning"  # Yangi yozuv bo'yicha xabar matni

            
                asyncio.run(send_telegram_message(user_telegram_id, message_text))
            else:
                user_telegram_id = record.user_telegram_id  # yoki kerakli maydonni olish
                message_text = f"{record.service} xizmat turi bo'yicha navbatingiz kelishiga {counter} ta qoldi"  # Yangi yozuv bo'yicha xabar matni

                
                asyncio.run(send_telegram_message(user_telegram_id, message_text))

        counter+=1
        
        
        
    user = request.user
    
    task = GeneralList.objects.filter(assigned_to=user, is_completed=False).first()
    
    
    # Agar xodimning aktiv vazifasi bo‘lmasa, yangi vazifa tayinlash
    if not task:
        task = assign_task(user)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "task_updates",
        {
            "type": "send_task_update",
            "message": "Hozircha murojaat yuq",
            "new_task": {
                "id": task.id if task else None,
                "service": task.service if task else None,
                
            } if task else None
        }
    )
    return render(request, "application.html",  {"task": task})


from django.http import JsonResponse

def HomeSave(request):
    if request.method == "POST":
            service = request.POST.get("service")

            # **Yangi obyekt yaratamiz va faqat kerakli maydonlarni saqlaymiz**
            new_entry = GeneralList.objects.create(service=service)
            
            # **Rasm yaratish**
            img = Image.new("RGB", (600, 200), color=(255, 255, 255))  # Oq fonli rasm
            draw = ImageDraw.Draw(img)

            try:
                # Shriftni yuklash (agar mavjud bo'lsa)
                font = ImageFont.truetype("arial.ttf", 14)  
            except IOError:
                font = ImageFont.load_default()  # Shrift topilmasa, default yuklash

            # **Matnni tayyorlash**
            text = f"{new_entry.service}\nNavbat raqamingiz: {new_entry.service[0]}{new_entry.id}"
            # draw.text((10, 10), text, fill=(0, 0, 0), font=font)
            try:
                text_width, text_height = draw.textsize(text, font=font)
            except Exception as e:
                text_width, text_height = 0, 0
            left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
            text_width = right - left
            text_height = bottom - top
            # Matnni rasmning o'rtasiga joylashtirish
            text_x = (600 - text_width) / 2
            text_y = (200 - text_height) / 2


            try:
                draw.text((text_x, text_y), text, font=font, fill='black')
            except Exception as e:
                pass
            # **Rasmdan bayt oqimi yaratish**
            img_io = io.BytesIO()
            img.save(img_io, format="PNG")
            img_io.seek(0)

            # **Rasmni base64 formatga aylantiramiz**
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

            return JsonResponse({
                "message": "Ma'lumot muvaffaqiyatli saqlandi!",
                "image": f"data:image/png;base64,{img_base64}"
            })

        

    return JsonResponse({"error": "Faqat POST so‘rovlar qabul qilinadi!"}, status=400)

    # if request.method == "POST":
    #     service = request.POST.get("service")

    #     # **Yangi obyekt yaratamiz va faqat kerakli maydonlarni saqlaymiz**
    #     new_entry = GeneralList.objects.create(service=service)

    #     # **Rasm yaratish**
    #     img = Image.new("RGB", (300, 150), color=(255, 255, 255))  # Oq fonli rasm
    #     draw = ImageDraw.Draw(img)

    #     try:
    #         # Shriftni yuklash (agar mavjud bo'lsa)
    #         font = ImageFont.truetype("arial.ttf", 14)  
    #     except IOError:
    #         font = ImageFont.load_default()  # Shrift topilmasa, default yuklash

    #     # **Matnni tayyorlash**
    #     text = f"{new_entry.service}\nNavbat raqamingiz: {new_entry.service[0]}{new_entry.id}"
    #     draw.text((10, 10), text, fill=(0, 0, 0), font=font)
        
    #     # **Rasmdan bayt oqimi yaratish**
    #     img_io = io.BytesIO()
    #     img.save(img_io, format="PNG")
    #     img_io.seek(0)

    #     # **Rasmni base64 formatga aylantiramiz**
    #     img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    #     return JsonResponse({
    #         "message": "Ma'lumot muvaffaqiyatli saqlandi!",
    #         "image": f"data:image/png;base64,{img_base64}"
    #     })

    # return JsonResponse({"error": "Faqat POST so‘rovlar qabul qilinadi!"}, status=400)


from django.db.models import Q


def assign_task(user):
    # Bajarilmagan va hali hech kimga tayinlanmagan vazifani topish
    task = GeneralList.objects.filter(assigned_to__isnull=True, is_completed=False).first()
    
    if task:
        task.assigned_to = user
        task.save()
    
    return task



@login_required
def complete_task(request, task_id):
    first_five_records = GeneralList.objects.filter(is_completed=False, assigned_to__isnull=True).order_by("id")[:5]

    counter = 0
    for record in first_five_records:
        if record.user_telegram_id:
            user_telegram_id = record.user_telegram_id  
            if counter == 0:
                message_text = f"{record.service} xizmat turi bo'yicha sizning navbatingiz keldi. \nIltimos, navbatingizni o'z vaqtida foydalaning"
            else:
                message_text = f"{record.service} xizmat turi bo'yicha navbatingiz kelishiga {counter} ta qoldi"
            
            asyncio.run(send_telegram_message(user_telegram_id, message_text))
        counter += 1

    task = get_object_or_404(GeneralList, id=task_id)

    # ✅ Faqat o‘ziga tayinlangan vazifani bajarishi mumkin
    if task.assigned_to == request.user:
        task.is_completed = True
        task.save()
        CompletedList.objects.create(
            service=task.service,
            firstname=task.firstname,
            lastname=task.lastname,
            phone=task.phone,
            user_telegram_id=task.user_telegram_id,
            ofis_user=request.user,  
        )
        # ✅ Yangi vazifa tayinlash
        new_task = assign_task(request.user)

        # WebSocket orqali yangi vazifani jo‘natish
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "task_updates",
            {
                "type": "send_task_update",
                "message": "Hozircha murojaat yuq!",
                "new_task": {
                    "id": new_task.id if new_task else None,
                    "service": new_task.service if new_task else None,
                    
                } if new_task else None
            }
        )

        return render(request, "application.html", {"task": new_task})

    return JsonResponse({'error': 'Sizga bu vazifa tayinlanmagan!'}, status=403)

@login_required
def cancelled_task(request, task_id):
    first_five_records = GeneralList.objects.filter(is_completed=False, assigned_to__isnull=True).order_by("id")[:5]

    counter = 0
    for record in first_five_records:
        if record.user_telegram_id:
            user_telegram_id = record.user_telegram_id  
            if counter == 0:
                message_text = f"{record.service} xizmat turi bo'yicha sizning navbatingiz keldi. \nIltimos, navbatingizni o'z vaqtida foydalaning"
            else:
                message_text = f"{record.service} xizmat turi bo'yicha navbatingiz kelishiga {counter} ta qoldi"
            
            asyncio.run(send_telegram_message(user_telegram_id, message_text))
        counter += 1

    task = get_object_or_404(GeneralList, id=task_id)

    # ✅ Faqat o‘ziga tayinlangan vazifani bajarishi mumkin
    if task.assigned_to == request.user:
        task.is_completed = True
        task.save()
        CancelledList.objects.create(
            service=task.service,
            firstname=task.firstname,
            lastname=task.lastname,
            phone=task.phone,
            user_telegram_id=task.user_telegram_id,
            ofis_user=request.user,  
        )
        # ✅ Yangi vazifa tayinlash
        new_task = assign_task(request.user)

        # WebSocket orqali yangi vazifani jo‘natish
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "task_updates",
            {
                "type": "send_task_update",
                "message": "Hozircha murojaat yuq!",
                "new_task": {
                    "id": new_task.id if new_task else None,
                    "service": new_task.service if new_task else None,
                    
                } if new_task else None
            }
        )

        return render(request, "application.html", {"task": new_task})

    return JsonResponse({'error': 'Sizga bu vazifa tayinlanmagan!'}, status=403)

@login_required
def notcome_task(request, task_id):
    first_five_records = GeneralList.objects.filter(is_completed=False, assigned_to__isnull=True).order_by("id")[:5]

    counter = 0
    for record in first_five_records:
        if record.user_telegram_id:
            user_telegram_id = record.user_telegram_id  
            if counter == 0:
                message_text = f"{record.service} xizmat turi bo'yicha sizning navbatingiz keldi. \nIltimos, navbatingizni o'z vaqtida foydalaning"
            else:
                message_text = f"{record.service} xizmat turi bo'yicha navbatingiz kelishiga {counter} ta qoldi"
            
            asyncio.run(send_telegram_message(user_telegram_id, message_text))
        counter += 1

    task = get_object_or_404(GeneralList, id=task_id)
    message_text=f"{task.service} xizmat turi bo'yicha olgan navbatingiz Registrator ofisiga tashrif buyurmaganligingiz uchun rad etildi. \n Iltimos qaytadan navbat oling."
    asyncio.run(send_telegram_message(task.user_telegram_id, message_text))

    # ✅ Faqat o‘ziga tayinlangan vazifani bajarishi mumkin
    if task.assigned_to == request.user:
        task.is_completed = True
        task.save()
        NotComeList.objects.create(
            service=task.service,
            firstname=task.firstname,
            lastname=task.lastname,
            phone=task.phone,
            user_telegram_id=task.user_telegram_id,
            ofis_user=request.user,  
        )
        # ✅ Yangi vazifa tayinlash
        new_task = assign_task(request.user)

        # WebSocket orqali yangi vazifani jo‘natish
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "task_updates",
            {
                "type": "send_task_update",
                "message": "Hozircha murojaat yuq!",
                "new_task": {
                    "id": new_task.id if new_task else None,
                    "service": new_task.service if new_task else None,
                    
                } if new_task else None
            }
        )

        return render(request, "application.html", {"task": new_task})

    return JsonResponse({'error': 'Sizga bu vazifa tayinlanmagan!'}, status=403)



@login_required
def complete_work(request, task_id):
    task = get_object_or_404(GeneralList, id=task_id)
    
    # is_completed ni False ga o'zgartiramiz
    task.is_completed = False
    # assigned_to ni None qilish orqali bo'shatamiz
    task.assigned_to = None  
    task.save()

    # Foydalanuvchiga Telegram orqali xabar yuborish
    if task.user_telegram_id:
        message_text = f"{task.service} xizmat turi bo'yicha olgan navbatingiz Registrator ofisining xodimlaridan biri ish holatida emasligi uchun navbatingiz ortga surildi"
        asyncio.run(send_telegram_message(task.user_telegram_id, message_text))

    # Bajarilgandan so'ng `home.html` sahifasiga qaytarish
    return redirect("home")  # `home` - URL nomi bo'lishi kerak

    # # ✅ Faqat o‘ziga tayinlangan vazifani bajarishi mumkin
    # if task.assigned_to == request.user:
    #     task.is_completed = True
    #     task.save()
    #     NotComeList.objects.create(
    #         service=task.service,
    #         firstname=task.firstname,
    #         lastname=task.lastname,
    #         phone=task.phone,
    #         user_telegram_id=task.user_telegram_id,
    #         ofis_user=request.user,  
    #     )
    #     # ✅ Yangi vazifa tayinlash
    #     new_task = assign_task(request.user)

    #     # WebSocket orqali yangi vazifani jo‘natish
    #     channel_layer = get_channel_layer()
    #     async_to_sync(channel_layer.group_send)(
    #         "task_updates",
    #         {
    #             "type": "send_task_update",
    #             "message": "Vazifa bajarildi, sahifa yangilandi!",
    #             "new_task": {
    #                 "id": new_task.id if new_task else None,
    #                 "service": new_task.service if new_task else None,
                    
    #             } if new_task else None
    #         }
    #     )

    #     return render(request, "application.html", {"task": new_task})

    # return JsonResponse({'error': 'Sizga bu vazifa tayinlanmagan!'}, status=403)


from django.shortcuts import render
from django.http import JsonResponse
from .models import GeneralList, CompletedList, CancelledList, NotComeList
from datetime import datetime
import calendar

def statistics_view(request):
    return render(request, "charts.html")

from django.shortcuts import render
from django.http import JsonResponse
from .models import GeneralList, CompletedList, CancelledList, NotComeList
from datetime import datetime
import calendar

def statistics_view(request):
    return render(request, "charts.html")

def get_statistics_data(request):
    # Hozirgi yil va oyni aniqlash
    hozirgi_sana = datetime.now()
    hozirgi_oy = hozirgi_sana.month
    hozirgi_yil = hozirgi_sana.year

    # Oxirgi 5 yildagi ma’lumotlarni olish
    yillar = [hozirgi_yil - i for i in range(4, -1, -1)]  # Masalan: 2020, 2021, 2022, 2023, 2024

    # Yanvardan hozirgi oygacha bo'lgan oylar ro‘yxati (o‘zbek tilida)
    oylar = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
    oylar = oylar[:hozirgi_oy]  # Hozirgi oyga qadar bo'lganlarini olish

    # Har bir model uchun umumiy sonni olish
    general_count = GeneralList.objects.count()
    completed_count = CompletedList.objects.count()
    cancelled_count = CancelledList.objects.count()
    not_come_count = NotComeList.objects.count()

    # Oylik statistik ma'lumotlar
    general_monthly = [
        GeneralList.objects.filter(created_at__year=hozirgi_yil, created_at__month=i).count()
        for i in range(1, hozirgi_oy + 1)
    ]
    completed_monthly = [
        CompletedList.objects.filter(created_at__year=hozirgi_yil, created_at__month=i).count()
        for i in range(1, hozirgi_oy + 1)
    ]
    cancelled_monthly = [
        CancelledList.objects.filter(created_at__year=hozirgi_yil, created_at__month=i).count()
        for i in range(1, hozirgi_oy + 1)
    ]
    not_come_monthly = [
        NotComeList.objects.filter(created_at__year=hozirgi_yil, created_at__month=i).count()
        for i in range(1, hozirgi_oy + 1)
    ]

    # Yillik statistik ma’lumotlar
    general_yearly = [
        GeneralList.objects.filter(created_at__year=yil).count() for yil in yillar
    ]
    completed_yearly = [
        CompletedList.objects.filter(created_at__year=yil).count() for yil in yillar
    ]
    cancelled_yearly = [
        CancelledList.objects.filter(created_at__year=yil).count() for yil in yillar
    ]
    not_come_yearly = [
        NotComeList.objects.filter(created_at__year=yil).count() for yil in yillar
    ]

    # JSON javob
    data = {
        "total_counts": {
            "general": general_count,
            "completed": completed_count,
            "cancelled": cancelled_count,
            "not_come": not_come_count,
        },
        "monthly_data": {
            "labels": oylar,
            "general": general_monthly,
            "completed": completed_monthly,
            "cancelled": cancelled_monthly,
            "not_come": not_come_monthly,
        },
        "yearly_data": {
            "labels": yillar,
            "general": general_yearly,
            "completed": completed_yearly,
            "cancelled": cancelled_yearly,
            "not_come": not_come_yearly,
        }
    }
    return JsonResponse(data, safe=False)