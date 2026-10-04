from django.contrib import admin
from .models import Profile, PredictionHistory

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'store_name', 'license_number', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('user__username', 'store_name', 'license_number')

@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer_name', 'churn_risk', 'churn_probability', 'created_at')
    list_filter = ('churn_risk', 'subscription_type')
    search_fields = ('customer_name', 'customer_email', 'user__username')
