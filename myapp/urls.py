from django.urls import path
from myapp import views


urlpatterns=[
    path("",views.index_page,name="index"),
    # path("task/",views.task_page,name="task"),
    path('all-analytics',views.all_analytics,name="all_analytics"),
    path('display_urls',views.display_urls,name="display_urls"),
    path('delete_urls/<int:url_id>',views.delete_urls,name="delete_urls"),

    path('<slug:short_url>',views.redirect_url)
]