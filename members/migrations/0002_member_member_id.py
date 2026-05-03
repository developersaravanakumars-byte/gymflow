from django.db import migrations, models


def backfill_member_ids(apps, schema_editor):
    Member = apps.get_model('members', 'Member')
    for member in Member.objects.select_related('branch').order_by('id'):
        branch_prefix = ''.join(
            c for c in member.branch.name.upper() if c.isalpha()
        )[:3]
        member.member_id = f'GF-{branch_prefix}-{member.id:04d}'
        member.save(update_fields=['member_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        # Step 1: Add field WITHOUT unique constraint first
        migrations.AddField(
            model_name='member',
            name='member_id',
            field=models.CharField(blank=True, editable=False, max_length=20, default=''),
            preserve_default=False,
        ),
        # Step 2: Backfill all existing rows with real unique IDs
        migrations.RunPython(backfill_member_ids, reverse_code=migrations.RunPython.noop),
        # Step 3: Now safely apply the unique constraint
        migrations.AlterField(
            model_name='member',
            name='member_id',
            field=models.CharField(blank=True, editable=False, max_length=20, unique=True),
        ),
    ]
