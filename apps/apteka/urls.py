from django.urls import path
from .views import (PopularPillsAPIView, LastPillsAPIView, DiscountPillsAPIView, RatingPillsAPIView, AllPillsAPIView,
                    PillDetailAPIView, CommentaryListAPIView, DoctorListAPIView, DoctorDetailAPIView,
                    PartnerListAPIView, CategoryListAPIView, AchievementListAPIView, AchievementRetrieveAPIView)

urlpatterns = [
    path('lasts-pills/', LastPillsAPIView.as_view(), name='lasts-pills'),
    path('popular-pills/', PopularPillsAPIView.as_view(), name='popular-pills'),
    path('ranked-pills/', RatingPillsAPIView.as_view(), name='ranked-pills'),
    path('discount-pills/', DiscountPillsAPIView.as_view(), name='discount-pills'),
    path('pills/', AllPillsAPIView.as_view(), name='pills-list'),
    path('pills/<int:pk>/', PillDetailAPIView.as_view(), name='pill-detail'),

    path('doctors/', DoctorListAPIView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailAPIView.as_view(), name='doctor-detail'),

    path('commentaries/', CommentaryListAPIView.as_view(), name='commentary-list'),

    path('partners/', PartnerListAPIView.as_view(), name='partners-list'),

    path('categories/', CategoryListAPIView.as_view(), name='category-list'),

    path('achievements/', AchievementListAPIView.as_view(), name='achievement-list'),
    path('achievements/<int:pk>/', AchievementRetrieveAPIView.as_view(), name='achievement-detail'),
]
