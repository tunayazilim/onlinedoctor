from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    index,register_doctor,register_patient,loginindex,logoutindex,showDoctorProfileSettings,clinicImageDelete,deleteEducation,
    changePasswordDoctor,updateSocialMediaDoctor,showUserProfileSettings,changePasswordPatient,showDoctorProfile,addReplyComment,
    addDoctorToFavorites,showFavouritesOfPatients,removeFavouritesOfPatients,showCommentsInDoctorDashboard,listCommentsAdmin,
    schedule,change_active_day,activate,listWaitingComments,deleteWaitingComment,acceptWaitingComment,detailWaitingComment,
    deleteTimeScheduleModel,getStartingandFinishingTime,showAciklamaYazisi,showAllDoctors,save_clinic_images,
    searchFilter,doctorDashboard,doctorAppoitments,doctorPatients,doctorInvoices,invoicesView,randevuDetayi,patientDashboard,
    booking,contact,createPeerIdToUser,getOtherUserByPeerId,checkout,resultOfPayment,success,failure,acceptAppointment,deleteAppointment,
    pastAppoitments,deletedAppoitments,makePayment,gizlilikPolitikasi,kullanimKosullari,patientIletisimSettings
    

)







urlpatterns = [
    path('',index,name="index"),
    path('doktor-kaydi',register_doctor,name="register_doctor"),
    path('hasta-kaydi',register_patient,name="register_patient"),
    path('giris',loginindex,name="login"),
    path('cikis',logoutindex,name="logout"),
    path('doktor-profil-ayarlari',showDoctorProfileSettings,name="showDoctorProfileSettings"),
    path('klinik-foto-sil/<int:pk>',clinicImageDelete,name="clinicImageDelete"),
    path('eğitim-sil/<int:pk>',deleteEducation,name="deleteEducation"),
    path('doktor-sifre-degistir',changePasswordDoctor,name="changePasswordDoctor"),
    path('doktor-sosyal-medya-güncelle',updateSocialMediaDoctor,name="updateSocialMediaDoctor"),
    path('kullanici-profil-ayarlari',showUserProfileSettings,name="showUserProfileSettings"),
    path('kullanici-sifre-degistir',changePasswordPatient,name="changePasswordPatient"),
    path('doktor-profili-görüntüle/<slug:slug>',showDoctorProfile,name="showDoctorProfile"),
    path('yanit-yaz/<slug:slug>/<int:pk>',addReplyComment,name="addReplyComment"),
    path('favorilerime-ekle/<slug:slug>',addDoctorToFavorites,name="addDoctorToFavorites"),
    path('favori-doktorlarim',showFavouritesOfPatients,name="showFavouritesOfPatients"),
    path('favorilerimden-kaldır/<slug:slug>',removeFavouritesOfPatients,name="removeFavouritesOfPatients"),
    path('yorumlarim/<int:pk>',showCommentsInDoctorDashboard,name="showCommentsInDoctorDashboard"),
    path('yorumlarim',listCommentsAdmin,name="listCommentsAdmin"),
    path('schedule',schedule,name="schedule"),
    path('change_active_day/<str:day>',change_active_day,name="change_active_day"),
    path('activate/<uidb64>/<token>/',activate, name='activate'),
    path('bekleyen-yorumlar',listWaitingComments,name="listWaitingComments"),
    path('bekleyen-yorum-sil/<int:pk>',deleteWaitingComment,name="deleteWaitingComment"),
    path('bekleyen-yorumu-kabul-et/<int:pk>',acceptWaitingComment,name="acceptWaitingComment"),
    path('bekleyen-yorum-detay/<int:pk>',detailWaitingComment,name="detailWaitingComment"),
    path('randevu-tarih-sil/<int:pk>',deleteTimeScheduleModel,name="deleteTimeScheduleModel"),
    path('getStartingandFinishingTime/<int:pk>',getStartingandFinishingTime,name="getStartingandFinishingTime"),
    path('aciklama-yazisi',showAciklamaYazisi,name="showAciklamaYazisi"),
    path('tüm-doktorlar',showAllDoctors,name="showAllDoctors"),    
    path('save_clinic_images',save_clinic_images,name="save_clinic_images"),    
    path('arama-filtreleme',searchFilter,name="searchFilter"),    
    path('doktor-anasayfasi',doctorDashboard,name="doctorDashboard"),   
    path('randevularim',doctorAppoitments,name="doctorAppoitments"),  
    path('hastalarim',doctorPatients,name="doctorPatients"),  
    path('faturalarim',doctorInvoices,name="doctorInvoices"),   
    path('fatura-detayi/<int:pk>',invoicesView,name="invoicesView"),
    path('randevu-detayi/<int:pk>',randevuDetayi,name="randevuDetayi"),
    path('anasayfam',patientDashboard,name="patientDashboard"),   
    path('randevu-al/<slug:slug>',booking,name="booking"),
    path('iletisim',contact,name="contact"),  
    path('sifremi-unuttum/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('sifremi-unuttum/bitti/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('sifremi-sifirla/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('sifremi-sifirla/bitti/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('createPeerIdToUser',createPeerIdToUser,name="createPeerIdToUser"),  
    path('getOtherUserByPeerId',getOtherUserByPeerId,name="getOtherUserByPeerId"),  
    path('odeme-sayfasi/<int:pk>',checkout,name="checkout"),  
    path('odeme-sonucu',resultOfPayment,name="resultOfPayment"),  
    path('basarili-odeme/<int:pk>',success,name="success"),  
    path('hatali-odeme',failure,name="failure"),  
    path('randevu-kabul-et/<int:pk>',acceptAppointment,name="acceptAppointment"),  
    path('randevu-reddet/<int:pk>',deleteAppointment,name="deleteAppointment"),  
    path('gecmis-randevular',pastAppoitments,name="pastAppoitments"),  
    path('iptal-edilen-randevular',deletedAppoitments,name="deletedAppoitments"),  
    path('odeme-yap/<int:pk>',makePayment,name="makePayment"),  
    path('gizlilik-politikasi-ve-aydinlatma-metni',gizlilikPolitikasi,name="gizlilikPolitikasi"),  
    path('uygulama-kullanim-kosullari',kullanimKosullari,name="kullanimKosullari"),  
    path('iletisim-ayarlari',patientIletisimSettings,name="patientIletisimSettings"),  
    
   
]


