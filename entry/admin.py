from django.contrib import admin
from .models import BE,BE_line

# Register your models here.
class BE_lineInline(admin.TabularInline):  # Use TabularInline or StackedInline as per your preference
    model = BE_line
    extra = 1  # Number of empty forms to display
    can_delete = True  # Allow deletion of child objects

class BEAdmin(admin.ModelAdmin):
    inlines = [BE_lineInline]

# Register the BE model with the admin site
admin.site.register(BE, BEAdmin)