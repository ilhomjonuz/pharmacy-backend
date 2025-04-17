from typing import List, Dict, Any

from rest_framework import serializers
from .models import Pill, Doctor, Partner, Commentary, Category, Achievement, Order, Entry


# ------------------------ Pills serializers -----------------------------------------------------------------------


class LastPillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pill
        fields = [
            'id',
            'name_uz', 'name_ru', 'name_en',
            'body_uz', 'body_ru', 'body_en',
            'picture',
            'created_at', 'updated_at',
        ]


class SmallPillSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField("get_price")

    class Meta:
        model = Pill
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en', 'picture', 'price', 'rank'
        ]

    def get_price(self, object) -> float:
        if object.discount_price:
            return object.discount_price
        else:
            return object.price


class AllPillSerializer(serializers.ModelSerializer):
    categories_uz = serializers.SerializerMethodField('get_categories_uz')
    categories_ru = serializers.SerializerMethodField('get_categories_ru')
    categories_en = serializers.SerializerMethodField('get_categories_en')
    price = serializers.SerializerMethodField("get_price")

    class Meta:
        model = Pill
        fields = [
            'id', 'categories_uz', 'categories_ru', 'categories_en', 'name_uz', 'name_ru', 'name_en', 'picture', 'price',
        ]

    def get_categories_uz(self, obj) -> list[str]:
        categories = obj.categories.all()
        return [obj.name_uz for obj in categories]

    def get_categories_ru(self, obj) -> list[str]:
        categories = obj.categories.all()
        return [obj.name_ru for obj in categories]

    def get_categories_en(self, obj) -> list[str]:
        categories = obj.categories.all()
        return [obj.name_en for obj in categories]

    def get_price(self, object) -> float:
        if object.discount_price:
            return object.discount_price
        else:
            return object.price


class DiscountPillSerializer(serializers.ModelSerializer):
    percentage = serializers.SerializerMethodField("get_percentage", read_only=True)

    class Meta:
        model = Pill
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en',
            'body_uz', 'body_ru', 'body_en',
            'price', 'percentage', 'discount_price',
            'picture',
            'created_at', 'updated_at',
        ]

    def get_percentage(self, obj) -> float:
        return (obj.price - obj.discount_price) / obj.price * 100


class PillDetailSerializer(serializers.ModelSerializer):
    type_uz = serializers.SerializerMethodField('get_type_uz')
    type_ru = serializers.SerializerMethodField('get_type_ru')
    type_en = serializers.SerializerMethodField('get_type_en')

    class Meta:
        model = Pill
        fields = [
            'id',
            'picture',
            'name_uz', 'name_ru', 'name_en',
            'body_uz', 'body_ru', 'body_en',
            'price', 'discount_price',
            'type_uz', 'type_ru', 'type_en',
            'expiration_date',
            'rank',
            'information_uz', 'information_ru', 'information_en',
            'usage_url',
            'created_at', 'updated_at',
        ]

    def get_type_uz(self, obj) -> str:
        type_name = obj.type.name_uz
        return type_name

    def get_type_ru(self, obj) -> str:
        type_name = obj.type.name_ru
        return type_name

    def get_type_en(self, obj) -> str:
        type_name = obj.type.name_en
        return type_name

# ------------------------ Pills serializers end -------------------------------------------------------------------

# ------------------------ Doctors serializers ---------------------------------------------------------------------


class DoctorsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'fullname', 'direction_uz', 'direction_ru', 'direction_en',
                  'call', 'body_uz', 'body_ru', 'body_en', 'picture',]


class DoctorDetailSerializer(serializers.ModelSerializer):
    advices = serializers.SerializerMethodField('get_advices')

    class Meta:
        model = Doctor
        fields = ['id',
                  'fullname',
                  'direction_uz', 'direction_ru', 'direction_en',
                  'call',
                  'body_uz', 'body_ru', 'body_en',
                  'picture',
                  'advices']

    def get_advices(self, obj) -> List[Dict[str, Any]]:
        pills = obj.advices.all()
        return SmallPillSerializer(pills, many=True).data

# ------------------------ Doctors serializers end -----------------------------------------------------------------

# ------------------------ Commentary serializers ------------------------------------------------------------------


class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = ['id', 'author', 'body', 'created_at']

# ------------------------ Commentary serializers end --------------------------------------------------------------

# ------------------------ Partner serializers ---------------------------------------------------------------------


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'picture']

# ------------------------ Partner serializers end -----------------------------------------------------------------

# ------------------------ Category serializers -------------------------------------------------------------------


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name_uz', 'name_ru', 'name_en']

# ------------------------ Category serializers end ---------------------------------------------------------------

# ------------------------ Achievement serializers ----------------------------------------------------------------


class AchievementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'picture', 'title_uz', 'title_ru', 'title_en']


class AchievementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'picture', 'title_uz', 'title_ru', 'title_en',
                  'description_uz', 'description_ru', 'description_en',
                  'created_at', 'updated_at']

# ------------------------ Achievement serializers end ------------------------------------------------------------

# --------------------------- Order serializers -----------------------------------

class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['pill_id', 'fullname', 'phone_number', 'message']



# ------------------------------ Entry serializers -----------------------------------------

class EntryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ['fullname', 'phone_number', 'message']

