from django.contrib import admin, messages
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.forms import TextInput, inlineformset_factory, modelformset_factory
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from .models import Career, Category_training, Curricula, Lesson, Project, Training

# Formset that edits the Curricula (main topics) linked to a single Training.
# Curricula <-> Training is Many-to-Many, so the queryset is scoped to the
# current training and the link is managed manually on save.
CurriculaFormSet = modelformset_factory(
    Curricula,
    fields=["curricula_name"],
    extra=1,
    can_delete=True,
    widgets={"curricula_name": TextInput(attrs={"class": "vTextField"})},
)

# Formset that edits the Lessons (subtopics) of a single Curricula via its FK.
LessonFormSet = inlineformset_factory(
    Curricula,
    Lesson,
    fields=["lesson_name"],
    fk_name="lesson_curricula",
    extra=1,
    can_delete=True,
    widgets={"lesson_name": TextInput(attrs={"class": "vTextField"})},
)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Curricula)
class CurriculaAdmin(admin.ModelAdmin):
    list_display = ["curricula_name"]
    search_fields = ["curricula_name"]
    filter_horizontal = ["curricula_train"]
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["lesson_name", "lesson_curricula"]
    list_filter = ["lesson_curricula"]
    search_fields = ["lesson_name"]


@admin.register(Category_training)
class CategoryTrainingAdmin(admin.ModelAdmin):
    list_display = ["cat_training_name"]
    prepopulated_fields = {"cat_slug": ("cat_training_name",)}


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ["training_name", "training_category"]
    list_filter = ["training_category"]
    search_fields = ["training_name"]
    prepopulated_fields = {"training_slug": ("training_name",)}

    def _linked_curricula(self, training):
        """Curricula attached to this training, via the M2M relation."""
        return Curricula.objects.filter(curricula_train=training).order_by(
            "curricula_id"
        )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """One-page editor: Training fields + its Curricula + each Curricula's Lessons.

        The standard add view is left untouched: create the Training first, then
        open it here to manage curricula and lessons together.
        """
        training = self.get_object(request, unquote(object_id))
        if training is None:
            return self._get_obj_does_not_exist_redirect(
                request, self.model._meta, object_id
            )
        if not self.has_change_permission(request, training):
            raise PermissionDenied

        ModelForm = self.get_form(request, training)
        linked = list(self._linked_curricula(training))

        if request.method == "POST":
            form = ModelForm(request.POST, request.FILES, instance=training)
            curricula_fs = CurriculaFormSet(
                request.POST,
                request.FILES,
                prefix="curricula",
                queryset=self._linked_curricula(training),
            )
            lesson_formsets = {
                cur.pk: LessonFormSet(
                    request.POST,
                    request.FILES,
                    instance=cur,
                    prefix="lessons_%s" % cur.pk,
                )
                for cur in linked
            }

            all_valid = (
                form.is_valid()
                and curricula_fs.is_valid()
                and all(fs.is_valid() for fs in lesson_formsets.values())
            )

            if all_valid:
                with transaction.atomic():
                    form.save()
                    deleted_curricula_pks = set()
                    for cform in curricula_fs.forms:
                        cleaned = getattr(cform, "cleaned_data", None)
                        if not cleaned:
                            continue
                        if cleaned.get("DELETE"):
                            # Unlink from THIS training rather than hard-deleting,
                            # because a curricula may be shared by other trainings.
                            if cform.instance.pk:
                                cform.instance.curricula_train.remove(training)
                                deleted_curricula_pks.add(cform.instance.pk)
                            continue
                        if not cleaned.get("curricula_name") and not cform.instance.pk:
                            continue  # skip the empty "add" row
                        curricula = cform.save()
                        curricula.curricula_train.add(training)

                    # Save lessons only for curricula still attached to this training.
                    for cur in linked:
                        if cur.pk in deleted_curricula_pks:
                            continue
                        lesson_formsets[cur.pk].save()

                self.message_user(
                    request,
                    "Training, curricula and lessons saved successfully.",
                    messages.SUCCESS,
                )
                return redirect(request.path)

            self.message_user(
                request, "Please correct the errors below.", messages.ERROR
            )
        else:
            form = ModelForm(instance=training)
            curricula_fs = CurriculaFormSet(
                prefix="curricula", queryset=self._linked_curricula(training)
            )
            lesson_formsets = {
                cur.pk: LessonFormSet(instance=cur, prefix="lessons_%s" % cur.pk)
                for cur in linked
            }

        # Pair each curricula form with its lesson formset. The trailing blank
        # "add" row has no pk yet, so it has no lesson formset (None).
        curricula_blocks = [
            (cform, lesson_formsets.get(cform.instance.pk))
            for cform in curricula_fs.forms
        ]

        media = form.media + curricula_fs.media
        for fs in lesson_formsets.values():
            media = media + fs.media

        context = {
            **self.admin_site.each_context(request),
            "title": "Edit %s" % training,
            "opts": self.model._meta,
            "original": training,
            "object_id": object_id,
            "form": form,
            "curricula_fs": curricula_fs,
            "curricula_blocks": curricula_blocks,
            "media": media,
            "change": True,
            "add": False,
            "is_popup": False,
            "save_as": False,
            "has_change_permission": True,
            **(extra_context or {}),
        }
        return TemplateResponse(
            request, "admin/trainings/training_change.html", context
        )


admin.site.register(Project)
admin.site.register(Career)
