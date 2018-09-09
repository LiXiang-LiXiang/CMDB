
from django.urls import path
from . import views

app_name = "Sansa"

urlpatterns = [
    path(r'report/', views.asset_report, name='asset_report'),
    path(r'report/asset_with_no_asset_id/', views.asset_with_no_asset_id, name='acquire_asset_id'),
    path(r'^new_assets/approval/', views.new_assets_approval, name="new_assets_approval"),
]
