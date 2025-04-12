from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import Type, Pill, Doctor, Partner, Achievement, Category, Commentary, Entry


@admin.register(Type)
class TypeAdmin(TabbedTranslationAdmin):
    list_display = ('name', )
    search_fields = ('name_uz', 'name_ru', 'name_en',)


@admin.register(Pill)
class PillAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'price', 'type', 'published')
    list_filter = ('published', 'type')
    search_fields = ('name_uz', 'name_ru', 'name_en', 'information')


@admin.register(Doctor)
class DoctorAdmin(TabbedTranslationAdmin):
    list_display = ('fullname', 'direction', 'published')
    list_filter = ('published',)
    search_fields = ('name', 'direction')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('picture',)


@admin.register(Achievement)
class AchievementAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'picture')
    search_fields = ('title', 'description')


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'created_at')
    search_fields = ('author', 'body')
    list_filter = ('author',)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'phone_number', 'created_at')
    search_fields = ('fullname', 'phone_number')
    list_filter = ('created_at',)
