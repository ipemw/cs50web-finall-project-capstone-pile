from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, ProductImage, Chat, Message

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'is_sold', 'timestamp')
    search_fields = ('title', 'brand', 'model', 'description')
    list_filter = ('is_sold', 'timestamp', 'brand', 'model')
    fields = ('user', 'title', 'brand', 'model', 'storage', 'color', 'sim_card_status', 'description', 'price', 'is_sold')
    inlines = [ProductImageInline]

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('product', 'seller', 'buyer', 'timestamp')
    search_fields = ('product__title', 'seller__username', 'buyer__username')
    list_filter = ('timestamp', 'product')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'content', 'timestamp')
    search_fields = ('content', 'sender__username', 'chat__product__title')
    list_filter = ('timestamp', 'sender')

admin.site.register(User, UserAdmin)