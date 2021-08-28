# Generated by Django 3.2.5 on 2021-08-21 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210821_1518'),
        ('admin_dashboard', '0003_auto_20210814_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='DealVoucher',
            fields=[
                ('deal_voucher_id', models.AutoField(primary_key=True, serialize=False)),
                ('Description', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=100)),
                ('credit', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='book_mode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.mode'),
        ),
        migrations.CreateModel(
            name='DealVoucherUser',
            fields=[
                ('deal_voucher_user', models.AutoField(primary_key=True, serialize=False)),
                ('valid_up_to', models.DateField()),
                ('deal_voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_dashboard.dealvoucher')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]