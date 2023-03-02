from django.contrib import admin

from .models import  User, Reset, Product, Review, Order,OrderItem,ShippingAddress

from django.contrib.auth.admin import UserAdmin
#------------------------------------------------------------------site register custom view
class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','last_login','date_joined', 'is_active')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    

admin.site.register(User, AccountAdmin)
admin.site.register(Reset)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)