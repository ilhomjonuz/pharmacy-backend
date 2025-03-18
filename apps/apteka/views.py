from rest_framework import generics
from .models import Pill, Doctor, Commentary, Partner, Category, Achievement
from .serializers import (DiscountPillSerializer, SmallPillSerializer, LastPillSerializer, AllPillSerializer,
                          PillDetailSerializer, DoctorsListSerializer, DoctorDetailSerializer, CommentarySerializer,
                          PartnerSerializer, CategorySerializer, AchievementListSerializer, AchievementDetailSerializer)

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
