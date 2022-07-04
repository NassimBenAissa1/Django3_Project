from django.contrib import admin, messages

from .models import *

# Register your models here.
#admin.site.register([Project, Student, Coach])


class ProjectInline(admin.TabularInline):
    model = Project
    fieldsets = [
        (
            None,
            {
                'fields': ['project_name']
            }
        )
    ]


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'email'
    )
    fields = (
        ('last_name', 'first_name'),
        'email'
    )
    inlines = [
        ProjectInline
    ]


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'email'
    )
    fields = (
        ('last_name', 'first_name'),
        'email'
    )
    search_fields = ['last_name']


class ProjetDurationListFilter(admin.SimpleListFilter):
    title = 'Duration'
    parameter_name = 'duration'

    def lookups(self, request, model_admin):
        return (
            ('1 month', ("less than a month")),
            ('3 months', ("More than 3 months"))
        )

    def queryset(self, request, queryset):
        if self.value() == '1 month':
            return queryset.filter(project_duration__lte=30)
        if self.value() == '3 months':
            return queryset.filter(project_duration__lte=90, project_duration__gte=30)


def set_Valid(modeladmin, request, queryset):
    rows_updated = queryset.update(isValid=True)
    if rows_updated == 1:
        message = "1 project was"
    else:
        message = f"{rows_updated} projects were"
    messages.success(
        request, message="%s successfully marked as valid" % message)


set_Valid.short_description = "Validate"


class ProjectAdmin(admin.ModelAdmin):
    def set_to_No_Valid(self, request, queryset):
        rows_NoValid = queryset.filter(isValid=False)
        if rows_NoValid.count() > 0:
            messages.error(
                request, f"{rows_NoValid.count()} projects are already marked as No Valid")
        else:
            rows_updated = queryset.update(isValid=False)
            if rows_updated == 1:
                message = "1 project was"
            else:
                message = f"{rows_updated} projects were"
            self.message_user(request, level='success',
                              message="%s successfully marked as not valid" % message)

    set_to_No_Valid.short_description = "Refuse"
    actions = [set_Valid, 'set_to_No_Valid']
    actions_on_bottom = True
    actions_on_top = True

    list_display = (
        'project_name',
        'project_duration',
        'creator',
        'supervisor'
    )

    list_filter = (
        'creator',
        'isValid',
        ProjetDurationListFilter,
    )

    #date_hierarchy = 'updated_at'
    # radio_fields = {"supervisor": admin.VERTICAL}
    # readonly_fields = ('created_at',)

    autocomplete_fields = ['supervisor']

    fieldsets = (
        (
            'Etat',
            {
                'fields': ('isValid',)
            }
        ),
        (
            'A Propos',
            {
                'classes': ('collapse',),
                'fields': (
                    'project_name',
                    (
                        'creator',
                        'supervisor',
                    ),
                    'needs',
                    'description',
                ),
            }
        ),
        (
            'Durées',
            {
                'fields': (
                    (
                        'project_duration',
                        'time_allocated'
                    ),
                )
            }
        ),
    )

    empty_value_display = '-empty-'


admin.site.register(Student, StudentAdmin)

# admin.site.register(Coach)
admin.site.register(MembershipInProject)

admin.site.register(Project, ProjectAdmin)
