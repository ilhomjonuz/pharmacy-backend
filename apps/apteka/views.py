import os
import re

from aiogram.types import BufferedInputFile
from asgiref.sync import async_to_sync
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from bot.data.config import CHANNELS
from bot.loader import bot
from .models import Pill, Doctor, Commentary, Partner, Category, Achievement, Order, SocialLinks
from .serializers import (DiscountPillSerializer, SmallPillSerializer, LastPillSerializer, AllPillSerializer,
                          PillDetailSerializer, DoctorsListSerializer, DoctorDetailSerializer, CommentarySerializer,
                          PartnerSerializer, CategorySerializer, AchievementListSerializer, AchievementDetailSerializer,
                          OrderCreateSerializer, EntryCreateSerializer, CommentaryCreateSerializer,
                          SocialLinksSerializer)

# ------------------------ Pills views ----------------------------------------------------------------------------


class LastPillsAPIView(generics.ListAPIView):
    serializer_class = LastPillSerializer
    queryset = Pill.published_objects.all()[:10]


class AllPillsAPIView(generics.ListAPIView):
    serializer_class = AllPillSerializer
    queryset = Pill.published_objects.all()


class PopularPillsAPIView(generics.ListAPIView):
    serializer_class = SmallPillSerializer
    queryset = Pill.published_objects.filter(popular=True)


class RatingPillsAPIView(generics.ListAPIView):
    serializer_class = SmallPillSerializer

    def get_queryset(self):
        queryset = Pill.published_objects.all()
        return sorted(queryset, key=lambda obj: obj.rank, reverse=True)[:10]


class DiscountPillsAPIView(generics.ListAPIView):
    serializer_class = DiscountPillSerializer
    queryset = Pill.published_objects.all()

    def get_queryset(self):
        queryset = super(DiscountPillsAPIView, self).get_queryset()
        queryset = filter(lambda obj: obj.discount_price, queryset)
        return queryset


class PillDetailAPIView(generics.RetrieveAPIView):
    queryset = Pill.published_objects.all()
    serializer_class = PillDetailSerializer

# ------------------------ Pills views end -------------------------------------------------------------------------

# ------------------------ Doctors views ---------------------------------------------------------------------------


class DoctorListAPIView(generics.ListAPIView):
    queryset = Doctor.published_objects.all()
    serializer_class = DoctorsListSerializer


class DoctorDetailAPIView(generics.RetrieveAPIView):
    queryset = Doctor.published_objects.all()
    serializer_class = DoctorDetailSerializer

    def get_serializer_context(self):
        context = super(DoctorDetailAPIView, self).get_serializer_context()
        context.update({
            'request': self.request
        })
        return context


# ------------------------ Doctors views end -----------------------------------------------------------------------

# ------------------------ Commentary views ------------------------------------------------------------------------


class CommentaryListAPIView(generics.ListAPIView):
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer


class CommentaryCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentaryCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ------------------------ Commentary views end -------------------------------------------------------------------

# ------------------------ Partner views --------------------------------------------------------------------------


class PartnerListAPIView(generics.ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

# ------------------------ Partner views end ----------------------------------------------------------------------

# ------------------------ Category views -------------------------------------------------------------------------


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# ------------------------ Category views end ---------------------------------------------------------------------

# ------------------------ Achievement views ----------------------------------------------------------------------


class AchievementListAPIView(generics.ListAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementListSerializer


class AchievementRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementDetailSerializer

# ------------------------ Achievement views end -----------------------------------------------------------------


# ---------------------------Order views ----------------------------------------------

class OrderCreateApiView(APIView):
    serializer_class = OrderCreateSerializer

    def validate_phone_number(self, phone_number):
        if '+998' in phone_number[:4] and len(phone_number) == 13:
            return phone_number
        elif phone_number.isdigit() and len(phone_number) == 9:
            return f'+998{phone_number}'
        return None

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = request.data
        phone_number = self.validate_phone_number(data['phone_number'])

        if not phone_number:
            return Response(
                {"message": "Telefon raqam noto'g'ri kiritilgan"},
                status=400
            )

        try:
            pill = Pill.objects.get(pk=data['pill_id'])
        except Pill.DoesNotExist:
            return Response(
                {"message": "Bunday id raqamli ma'lumot topilmadi"},
                status=400
            )

        pill_data = PillDetailSerializer(pill).data
        async_to_sync(self.send_order_info)(phone_number, data, pill_data)
        serializer.save()

        return Response(
            {"message": "So'rov muvaffaqiyatli yuborildi!"},
            status=201
        )

    async def send_order_info(self, phone_number, data, pill_data):
        try:
            caption = self.generate_order_caption(phone_number, data, pill_data)
            photo = self.get_pill_image(pill_data)
            print(self.get_pill_image(pill_data))
            await bot.send_photo(
                chat_id=CHANNELS[0],
                photo=photo,
                caption=caption,
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
        finally:
            await bot.session.close()

    def clean_html(self, raw_html):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', raw_html)

    def generate_order_caption(self, phone_number, data, pill_data):
        def safe_field(value):
            return self.clean_html(str(value)) if value else 'Mavjud emas'

        base_info = f"🏷 <b>Mahsulot nomi:</b> {safe_field(pill_data['name_uz'])}\n"
        base_info += f"📝 <b>Mahsulot haqida:</b> {safe_field(pill_data['body_uz'])}\n"
        base_info += f"🧪 <b>Mahsulot tarkibi:</b> {safe_field(pill_data['information_uz'])}\n"
        base_info += f"🏷 <b>Mahsulot turi:</b> {safe_field(pill_data['type_uz'])}\n"
        base_info += f"📅 <b>Yaroqlilik muddati:</b> {safe_field(pill_data['expiration_date'])}\n"
        base_info += f"💰 <b>Narxi:</b> {safe_field(pill_data['price'])} so'm\n"

        if pill_data.get('discount_price'):
            base_info += f"🔥 <b>Chegirmadagi narx:</b> {safe_field(pill_data['discount_price'])} so'm\n\n"

        client_info = f"👤 <b>Mijoz:</b> {safe_field(data['fullname'])}\n"
        client_info += f"📞 <b>Telefon:</b> {phone_number}\n"
        client_info += f"✉️ <b>Xabar:</b> {safe_field(data.get('message', 'Mavjud emas'))}"

        header = "🛒 <b>YANGI BUYURTMA</b> 🛒\n\n"

        return header + base_info + client_info

    def get_pill_image(self, pill_data):
        relative_path = pill_data['picture'].replace('/bot/media/', '')
        absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        if not os.path.exists(absolute_path):
            raise FileNotFoundError(f"Rasm fayli topilmadi: {absolute_path}")

        with open(absolute_path, 'rb') as file:
            file_bytes = file.read()

        return BufferedInputFile(file_bytes, filename=os.path.basename(absolute_path))


class EntryCreateAPIView(APIView):
    serializer_class = EntryCreateSerializer

    def validate_phone_number(self, phone_number):
        if '+998' in phone_number[:4] and len(phone_number) == 13:
            return phone_number
        elif phone_number.isdigit() and len(phone_number) == 9:
            return f'+998{phone_number}'
        return None

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data
        phone_number = self.validate_phone_number(data['phone_number'])
        if not phone_number:
            return Response(
                {"message": "Telefon raqam noto'g'ri kiritilgan"},
                status=400
            )
        async_to_sync(self.send_order_info)(phone_number, data)
        serializer.save()
        return Response(
            {"message": "So'rov muvaffaqiyatli yuborildi!"},
            status=201
        )



    def generate_entry_caption(self, phone_number, data):

        client_info = f"👤 <b>Mijoz:</b> {data['fullname']}\n"
        client_info += f"📞 <b>Telefon:</b> {phone_number}\n"
        client_info += f"✉️ <b>Xabar:</b> {data['message']}"

        header = "👤 <b>Yangi mijoz</b> 👤\n\n"

        return header + client_info


    async def send_order_info(self, phone_number, data):
        try:
            caption = self.generate_entry_caption(phone_number, data)
            await bot.send_message(
                chat_id=CHANNELS[0],
                text=caption,
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
        finally:
            await bot.session.close()


# ----------------- SocialLink API View ---------------------------

class SocialLinksListAPIView(generics.ListAPIView):
    queryset = SocialLinks.objects.all()
    serializer_class = SocialLinksSerializer


