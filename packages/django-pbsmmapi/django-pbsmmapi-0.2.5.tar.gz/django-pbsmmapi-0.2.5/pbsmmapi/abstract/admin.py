from datetime import datetime

import pytz
from django.contrib import admin
from django.contrib.admin import site
from django.utils.safestring import mark_safe

# This removed the delete function from the Admin action dropdown.
# You can 're-add' it, if necessary, by explicitly adding it to the
# actions parameter for a given ModelAdmin instance.
site.disable_action('delete_selected')


class PBSMMAbstractAdmin(admin.ModelAdmin):
    actions = [
        'force_reingest',
        'permanently_online',
        'take_online_now',
        'conditionally_online',
        'take_offline',
    ]
    search_fields = [
        'title',
    ]

    def force_reingest(self, request, queryset):
        # queryset is the list of Asset items that were selected.
        for item in queryset:
            item.ingest_on_save = True
            # HOW DO I FIND OUT IF THE save() was successful?
            item.save()

    force_reingest.short_description = 'Reingest selected items.'

    def permanently_online(self, request, queryset):
        for item in queryset:
            item.publish_status = 1
            item.save()

    permanently_online.short_description = 'Take item PERMANTENTLY LIVE'

    def conditionally_online(self, request, queryset):
        for item in queryset:
            item.publish_status = 0
            item.save()

    conditionally_online.short_description = 'CONDITIONALLY Online using live_as_of Date'

    def take_online_now(self, request, queryset):
        for item in queryset:
            item.publish_status = 0
            item.live_as_of = datetime.now(pytz.utc)
            item.save()

    take_online_now.short_description = 'Take Live as of Right Now'

    def take_offline(self, request, queryset):
        for item in queryset:
            item.publish_status = -1
            item.save()

    take_offline.short_description = 'Take item COMPLETELY OFFLINE'

    def assemble_asset_table(self, obj):
        asset_list = obj.assets.all()
        out = get_abstract_asset_table(
            asset_list, obj.default_asset, obj.object_model_type
        )
        return mark_safe(out)

    assemble_asset_table.short_description = 'Assets'

    class Meta:
        abstract = True


def get_abstract_asset_table(object_list, default_asset, parent_type):
    url = '/admin/%s/pbsmm%sasset' % (parent_type, parent_type)
    if len(object_list) < 1:
        return "(No assets)"
    out = "<p>Highlighted row indicates which Asset will appear on the parent object's detail page.</p>"
    out += "<table width=\"100%\" border=2>"
    out += "\n<tr style=\"background-color: #999;l\"><th>Title</th><th>Type</th><th>Duration</th><th>Avail?</th><th>API</th><th>Set as Default?</th></tr>"
    for item in object_list:
        row_color = '#ffffff;'
        if default_asset is not None and item == default_asset:
            row_color = '#ffff66;'

        out += "\n<tr style=\"background-color:%s\">" % row_color
        out += "\n\t<td><a href=\"%s/%d/change/\" target=\"_new\">%s</a></td>" % (
            url, item.id, item.title
        )
        out += "\n\t<td>%s</td>" % item.object_type
        out += '\n\t<td>%s</td>' % item.formatted_duration
        out += "\n\t<td>%s</td>" % item.asset_publicly_available()
        out += "\n\t<td><a href=\"%s\" target=\"_new\">API</a></td>" % item.api_endpoint
        out += "\n\t<td>%s</td>" % item.is_default
        out += "\n</tr>"
    out += "\n</table>"
    return out
