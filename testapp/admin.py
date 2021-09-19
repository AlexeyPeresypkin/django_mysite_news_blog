from django.contrib import admin
# from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin

from testapp.models import Rubric, Article

# admin.site.register(Rubric, MPTTModelAdmin)
admin.site.register(Article)

admin.site.register(
    Rubric,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)
