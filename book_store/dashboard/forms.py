from django import forms

from book_store.admin_dashboard.models import QueryFeedback


class queryFeedbackForm(forms.ModelForm):
    query_feedback_subject = forms.CharField(max_length=100, required=True)
    query_feedback_text = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = QueryFeedback
        fields = ('query_feedback_subject', 'query_feedback_text')
