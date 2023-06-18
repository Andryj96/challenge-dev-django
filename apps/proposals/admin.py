from django.contrib import admin
from .models import ProposalField, ProposalFieldValue, LoanProposal


class ProposalFieldAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + \
        ('slug', 'type', 'required', 'is_active')
    list_filter = ('is_active',)


class ProposalFieldValueInline(admin.TabularInline):
    """
    To show proposal field values inside loan proposals
    """
    model = ProposalFieldValue
    extra = 0

    # We may disable crud actions for field values data inside
    # loan proposal model with this functions

    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class LoanProposalAdmin(admin.ModelAdmin):
    inlines = [ProposalFieldValueInline]
    list_display = admin.ModelAdmin.list_display + \
        ('status', 'analyzed_at', 'created_at')
    list_filter = ('status',)


admin.site.register(ProposalField, ProposalFieldAdmin)
admin.site.register(LoanProposal, LoanProposalAdmin)
