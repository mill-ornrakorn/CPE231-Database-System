# Generated by Django 2.2.2 on 2019-11-02 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0012_auto_20191102_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicelineitem',
            name='product_code',
            field=models.ForeignKey(db_column='product_code', on_delete=django.db.models.deletion.CASCADE, to='invoice.Product'),
        ),
    ]
