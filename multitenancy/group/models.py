from groups_manager.models import Group, GroupType
from django.db.models.signals import post_save, post_delete
from groups_manager.models import group_save, group_delete


class Project(Group):
    # objects = ProjectManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.group_type:
            self.group_type = GroupType.objects.get_or_create(label='Project')[0]
        super(Project, self).save(*args, **kwargs)

class WorkGroup(Group):
    # objects = WorkGroupManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.group_type:
            self.group_type = GroupType.objects.get_or_create(label='Workgroup')[0]
        super(WorkGroup, self).save(*args, **kwargs)


post_save.connect(group_save, sender=Project)
post_delete.connect(group_delete, sender=Project)
post_save.connect(group_save, sender=WorkGroup)
post_delete.connect(group_delete, sender=WorkGroup)

