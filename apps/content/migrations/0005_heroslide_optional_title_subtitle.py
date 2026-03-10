from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0004_add_value_to_homefeature"),
    ]

    operations = [
        migrations.AlterField(
            model_name="heroslide",
            name="title",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Título principal de la diapositiva en español.",
                max_length=200,
                verbose_name="Título (Español)",
            ),
        ),
        migrations.AlterField(
            model_name="heroslide",
            name="subtitle",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Texto secundario que aparece debajo del título.",
                verbose_name="Subtítulo (Español)",
            ),
        ),
    ]
