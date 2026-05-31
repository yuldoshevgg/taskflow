from django.contrib import admin
from .models import Category, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_by', 'created_at')
    list_filter = ('created_by',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'category', 'created_by', 'due_date')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
