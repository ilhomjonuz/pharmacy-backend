# Generated by Django 5.0.3 on 2024-05-25 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("apteka", "0011_alter_commentary_options_alter_pill_options_and_more"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="achievement",
            table="achievements",
        ),
        migrations.AlterModelTable(
            name="category",
            table="categories",
        ),
        migrations.AlterModelTable(
            name="commentary",
            table="comments",
        ),
        migrations.AlterModelTable(
            name="doctor",
            table="doctors",
        ),
        migrations.AlterModelTable(
            name="entry",
            table="entries",
        ),
        migrations.AlterModelTable(
            name="type",
            table="types",
        ),
    ]
