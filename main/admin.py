from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import News, Category, Menu, Reservation, Hall


class MarriedFilter(admin.SimpleListFilter):
    title = "Статус меню"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Внесено'),
            ('single', 'Не внесено'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'image']
    prepopulated_fields = {"slug": ("title", )}
    list_display = ('title', 'post_photo', 'time_create', 'is_published')
    list_display_links = ('title', )
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', )
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith']
    save_on_top = True

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, main: News):
        if main.image:
            return mark_safe(f"<img src='{main.image.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=News.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=News.Status.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'cat']
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'post_photo', 'time_create', 'is_published')
    list_display_links = ('title',)
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']
    save_on_top = True

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, main: Menu):
        if main.photo:
            return mark_safe(f"<img src='{main.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Menu.StatusMenu.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Menu.StatusMenu.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации!", messages.WARNING)


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    fields = ['name']
