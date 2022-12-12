from django.urls import path
from accounts.views import RegestraionView,Login,Logout\
    ,activate,DashBoard,ForgetPassword,resetpassword_validate,resetpassword
urlpatterns=[
    path('register' ,RegestraionView.as_view() , name='register' ),
    path('login/' ,Login.as_view() , name='login'),
    path('logout/' ,Logout.as_view() , name='logout'),
    path('activation/<uidb64>/<token>/' ,activate , name='activation' ),
    path('dashboard/' , DashBoard.as_view() , name='dashboard'),
    path('forgetpassword/' ,ForgetPassword , name='forgetpassword'),
    path('resetpassword_validate/<uidb64>/<token>/' , resetpassword_validate , name='resetpassword_validate'),
    path('resetpassword/' ,resetpassword , name='resetpassword' )

]