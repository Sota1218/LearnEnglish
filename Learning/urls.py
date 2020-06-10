from django.urls import path
from . import views

urlpatterns = [
    path('',views.redirect_entrance),
    path('learning',views.dashboard),
    path('addWords',views.addWord),
    path('delete/<int:id>',views.delete),
    path("update/<int:id>",views.update),
    path("logout",views.logout),
    # test page
    path("test",views.test),
    # path("testMake",views.testMake),
    path("test/calculate",views.calculate),
    path("test/result",views.result),
]