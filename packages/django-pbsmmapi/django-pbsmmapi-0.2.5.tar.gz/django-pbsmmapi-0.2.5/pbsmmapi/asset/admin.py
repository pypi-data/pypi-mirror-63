from django.contrib import admin
from django.utils.safestring import mark_safe


class PBSMMAbstractAssetAdmin(admin.ModelAdmin):
    # Why so many readonly_fields?  Because we don't want to override what's coming from the API, but we do
    # want to be able to view it in the context of the Django system.
    #
    # Most things here are fields, some are method output and some are
    # properties.
    readonly_fields = [
        'api_endpoint_link', 'asset_publicly_available', 'availability',
        'can_embed_player', 'canonical_image', 'canonical_image_tag', 'chapters',
        'content_rating', 'content_rating_description', 'date_created',
        'date_last_api_update', 'description_long', 'description_short', 'duration',
        'geo_profile', 'images', 'is_excluded_from_dfp', 'language',
        'last_api_status_color', 'links', 'object_type', 'platforms', 'player_code',
        'player_code_preview', 'slug', 'tags', 'title', 'title_sortable', 'topics',
        'updated_at', 'windows'
    ]
    search_fields = ('title', )

    # If we're viewing a record, make it pretty.
    fieldsets = [
        (
            None,
            {
                'fields': (
                    'ingest_on_save',
                    'override_default_asset',
                    (
                        'date_created', 'date_last_api_update', 'updated_at',
                        'last_api_status_color'
                    ),
                    'api_endpoint_link',
                    ('object_id', 'legacy_tp_media_id'),
                ),
            },
        ),
        (
            'Title and Availability',
            {
                'fields': (
                    'title',
                    'title_sortable',
                    'asset_publicly_available',
                ),
            },
        ),
        (
            'Images',
            {
                'classes': ('collapse', ),
                'fields': (
                    'images',
                    'canonical_image_type_override',
                    'canonical_image_tag',
                ),
            },
        ),
        (
            'Description',
            {
                'classes': ('collapse', ),
                'fields': (
                    'slug',
                    'description_long',
                    'description_short',
                ),
            },
        ),
        (
            'Asset Metadata',
            {
                'classes': ('collapse', ),
                'fields': (
                    ('object_type', 'duration'),
                    ('can_embed_player', 'is_excluded_from_dfp'),
                    'availability',
                    'content_rating',
                    'content_rating_description',
                    'language',
                    'topics',
                    'tags',
                    'chapters',
                ),
            },
        ),
        (
            'Asset Preview',
            {
                'classes': ('collapse', ),
                'fields': (
                    'player_code',
                    'player_code_preview',
                ),
            },
        ),
        (
            'Additional Metadata',
            {
                'classes': ('collapse', ),
                'fields': ('links', 'geo_profile', 'platforms', 'windows'),
            },
        ),
    ]

    def player_code_preview(self, obj):
        out = ''
        if obj.player_code and len(obj.player_code) > 1:
            out += '<div style=\"width:640px; height: 360px;\">'
            out += obj.player_code
            out += '</div>'
        return mark_safe(out)

    class Meta:
        abstract = True
