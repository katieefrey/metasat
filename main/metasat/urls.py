from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update', views.update, name='update'),
    path('term/<element>', views.element, name='element'),
    path('edit/<element>', views.edit, name='edit'),
    path('<element>', views.element, name='element'),
]


# schema.space/metasat/elementIdHere


# schema.space/metasat
# schema.space/metasat/families
# schema.space/metasat/segments

# schema.space/sort/alphabetical
# schema.space/sort/family
# schema.space/sort/segment

# schema.space/metasat
# schema.space/families
# schema.space/segments