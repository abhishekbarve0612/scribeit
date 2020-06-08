from django.contrib import admin
from .models import Post, no_of_views, ContactAdmin, BlogRequest


class PostModelAdmin(admin.ModelAdmin):
    list_display = [ "title", "created_on", "updated_on" ]
    list_display_links = ["title"]
    list_filter = ["updated_on", "created_on"]
    search_fields = [ "title", "content"]

    class Meta:
        model = Post

class ContactModelAdmin(admin.ModelAdmin):
    list_display = [ "name", "emailid", "subject", "message" ]
    list_filter = ["name", "emailid"]
    search_fields = ["name", "message", "emailid", "subject"]

    ordering = ['-id']

    class Meta:
        model = ContactAdmin

class ViewsModelAdmin(admin.ModelAdmin):
    list_display = [ "post", "views", "updated" ]
    list_filter = ["views", "updated"]
    search_fields = ["post"]

    class Meta:
        model = no_of_views

admin.site.register(no_of_views, ViewsModelAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(ContactAdmin, ContactModelAdmin)
admin.site.register(BlogRequest)
