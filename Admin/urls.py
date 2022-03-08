from django.urls import path

from Admin.views import (
    loginAdmin,indexAdmin,logoutAdmin,showPagesAdmin,createPageModel,updatePageModel,deletePage,listWaitingDoctors,
    acceptWatiingDoctor,deleteWaitingDoctor,allDoctors,profileAdminShow,changePasswordAdmin,allPatients,
    showDoctorAdmin,appoitmentsAdmin,specialitiesAdmin,updateSpecialist,reviewsAdmin,deleteReview,
    deleteSpecial,allBannersAdmin,createBannerModel,updateBannerModel,deleteBanner,alanYaziListeleAdmin,
    createAlanYaziModel,updateAlanYaziModel,deleteAlanYazi,allIndexYaziAdmin,updateIndexYaziModel,updateFooterModelAdmin,
    updateDoctorFeatureIndexAdmin,allFeaturesAdmin,createFeatureIndexAdmin,updateFeatureIndexAdmin,
    deleteFeatureIndexAdmin,updatelogoModelAdmin,deletedAppoitmentsAdmin,allInvoiceReportsAdmin,viewInvoiceDetailAdmin,
    settingsPatientMenuAdmin,patientMenuAdminEkle,deleteMenu

)






urlpatterns = [
    path('',loginAdmin,name="loginAdmin"),
    path('',logoutAdmin,name="logoutAdmin"),
    path('index-admin',indexAdmin,name="indexAdmin"),
    path('tum-sayfalar-admin',showPagesAdmin,name="showPagesAdmin"),
    path('sayfa-modeli-olustur-admin',createPageModel,name="createPageModel"),
    path('sayfa-modeli-guncelle-admin/<int:pk>',updatePageModel,name="updatePageModel"),
    path('sayfa-sil-admin/<int:pk>',deletePage,name="deletePage"),
    path('bekleyen-doktor-istekleri-admin',listWaitingDoctors,name="listWaitingDoctors"),
    path('bekleyen-doktor-istegi-kabul-et-admin/<slug:slug>',acceptWatiingDoctor,name="acceptWatiingDoctor"),
    path('bekleyen-doktor-istegi-sil-admin/<int:pk>',deleteWaitingDoctor,name="deleteWaitingDoctor"),
    path('tum-doktorlar-admin',allDoctors,name="allDoctors"),
    path('profil-goruntule-admin',profileAdminShow,name="profileAdminShow"),
    path('sifre-degistir-admin',changePasswordAdmin,name="changePasswordAdmin"),
    path('tum-hastalar-admin',allPatients,name="allPatients"),
    path('doktor-goruntule-admin/<slug:slug>',showDoctorAdmin,name="showDoctorAdmin"),
    path('randevular-admin',appoitmentsAdmin,name="appoitmentsAdmin"),
    path('tum-hizmetler-admin',specialitiesAdmin,name="specialitiesAdmin"),
    path('hizmet-guncelle/<int:pk>',updateSpecialist,name="updateSpecialist"),
    path('tum-yorumlar-admin',reviewsAdmin,name="reviewsAdmin"),
    path('yorum-sil-admin/<int:pk>',deleteReview,name="deleteReview"),
    path('deleteSpecial/<int:pk>',deleteSpecial,name="deleteSpecial"),
    path('tum-bannerlar-admin',allBannersAdmin,name="allBannersAdmin"),
    path('banner-olustur-admin',createBannerModel,name="createBannerModel"),
    path('banner-guncelle-admin/<int:pk>',updateBannerModel,name="updateBannerModel"),
    path('banner-sil-admin/<int:pk>',deleteBanner,name="deleteBanner"),
    path('alan-yazi-listele-admin',alanYaziListeleAdmin,name="alanYaziListeleAdmin"),
    path('alan-yazi-olustur-admin',createAlanYaziModel,name="createAlanYaziModel"),
    path('alan-yazi-guncelle-admin/<int:pk>',updateAlanYaziModel,name="updateAlanYaziModel"),
    path('alan-yazi-sil-admin/<int:pk>',deleteAlanYazi,name="deleteAlanYazi"),
    path('anasayfa-tum-yazilar-admin',allIndexYaziAdmin,name="allIndexYaziAdmin"),
    path('anasayfa-yazi-guncelle-admin/<int:pk>',updateIndexYaziModel,name="updateIndexYaziModel"),
    path('footer-guncelle-admin',updateFooterModelAdmin,name="updateFooterModelAdmin"),
    path('index-doktor-ozellik-guncelle-admin',updateDoctorFeatureIndexAdmin,name="updateDoctorFeatureIndexAdmin"),
    path('tum-index-ozellikler-admin',allFeaturesAdmin,name="allFeaturesAdmin"),
    path('index-ozellik-olustur-admin',createFeatureIndexAdmin,name="createFeatureIndexAdmin"),
    path('index-ozellik-guncelle-admin/<int:pk>',updateFeatureIndexAdmin,name="updateFeatureIndexAdmin"),
    path('index-ozellik-sil-admin/<int:pk>',deleteFeatureIndexAdmin,name="deleteFeatureIndexAdmin"),
    path('logo-güncelleme-admin',updatelogoModelAdmin,name="updatelogoModelAdmin"),
    path('onaylanmayan-randevular-admin',deletedAppoitmentsAdmin,name="deletedAppoitmentsAdmin"),
    path('tum-faturalar-admin',allInvoiceReportsAdmin,name="allInvoiceReportsAdmin"),
    path('fatura-detay-admin/<int:pk>',viewInvoiceDetailAdmin,name="viewInvoiceDetailAdmin"),
    path('menu-ayarlari-admin',settingsPatientMenuAdmin,name="settingsPatientMenuAdmin"),
    path('menu-ekle-admin',patientMenuAdminEkle,name="patientMenuAdminEkle"),
    path('menu-sil-admin/<int:pk>/<str:str>',deleteMenu,name="deleteMenu"),
]