from django.contrib import admin
from .models import Product, Price, Donation, Subscription

class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0

class DonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'stripe_checkout_session_id', 'completed', 'checkout_status']
    search_fields = ['user__username', 'amount', 'stripe_checkout_session_id']
    list_filter = ['completed', 'checkout_status']

admin.site.register(Donation, DonationAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'subscription_plan_id', 'stripe_checkout_session_id', 'created_at', 'is_active', 'completed', 'checkout_status']
    search_fields = ['user__username', 'amount', 'subscription_plan_id', 'stripe_checkout_session_id']
    list_filter = ['is_active', 'completed', 'checkout_status']

admin.site.register(Subscription, SubscriptionAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'stripe_product_id']
    inlines = [PriceInlineAdmin]

admin.site.register(Product, ProductAdmin)
