from django.db import models
from django.utils.translation import ugettext_lazy as _


class Data(models.Model):
    type = models.CharField(max_length=64)
    f1 = models.CharField(max_length=64)
    f2 = models.CharField(max_length=64)



class ProcessDefinition(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_("Name"))
    image = models.ImageField(upload_to="django-simple-workflow/process-definitions/", null=True, blank=True, verbose_name=_("Image"))

    class Meta:
        verbose_name = _("Process Definition")
        verbose_name_plural = _("Process Definitions")

    def __str__(self):
        return self.name

class Role(models.Model):
    pd = models.ForeignKey(ProcessDefinition, on_delete=models.CASCADE, related_name="roles", verbose_name=_("Process Definition"))
    name = models.CharField(max_length=64, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Simple Workflow Role")
        verbose_name_plural = _("Simple Workflow Role")
        unique_together = [
            ("pd", "name"),
        ]

    def __str__(self):
        return self.name

class Node(models.Model):
    pd = models.ForeignKey(ProcessDefinition, on_delete=models.CASCADE, related_name="nodes", verbose_name=_("Process Definition"))
    title = models.CharField(max_length=64, verbose_name=_("Title"))
    order = models.IntegerField(default=999, verbose_name=_("Order"))
    is_end = models.BooleanField(default=False, verbose_name=_("Is End Node"))

    class Meta:
        verbose_name = _("Simple Workflow Node")
        verbose_name_plural = _("Simple Workflow Node")
        ordering = ["pd", "order", "pk"]
    def __str__(self):
        return self.title

class Transition(models.Model):
    pd = models.ForeignKey(ProcessDefinition, on_delete=models.CASCADE, related_name="transitions", verbose_name=_("Process Definition"))
    start = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="outs", verbose_name=_("Start Node"))
    end = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="ins", verbose_name=_("End Node"))
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="+", verbose_name=_("Role"))
    title = models.CharField(max_length=64, verbose_name=_("Title"))
    order = models.IntegerField(default=999, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Simple Workflow Transition")
        verbose_name_plural = _("Simple Workflow Transition")
        ordering = ["pd", "start", "order", "pk"]

    def __str__(self):
        return self.title
