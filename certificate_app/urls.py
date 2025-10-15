from django.urls import path
from . import views

urlpatterns = [
    path("", views.verification_page_open, name="home"),

    # certificate
    path("certificate_form", views.certificate_form, name="certificate_form"),
    path("certificate_preview/", views.certificate_preview, name="certificate_preview"),
    path("download_certificat/<str:file_name>/", views.certificate_download, name="download_certificat"),


    # award
    path("award_form", views.award_form, name="award_form"),
    path("award_preview/", views.award_preview, name="award_preview"),
    path("download_award/<str:file_name>/", views.award_download, name="download_award"),


    # verification Page
    path("certificate/verification/", views.certificate_verification, name="certificate_verification"),
    # path("/certificate/verification/search_certificate/", views.search_certificate, name="search_certificate"),



]
