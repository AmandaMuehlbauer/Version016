from django.contrib import admin
from .models import Product, Price, Donation, Subscription

class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0

class DonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'stripe_checkout_session_id']
    search_fields = ['user__username', 'amount']
    list_filter = []

admin.site.register(Donation, DonationAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'subscription_plan_id', 'stripe_checkout_session_id', 'created_at']
    search_fields = ['user__username', 'amount', 'subscription_plan_id']
    list_filter = []

admin.site.register(Subscription, SubscriptionAdmin)

class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInlineAdmin]

admin.site.register(Product, ProductAdmin)
