from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_alter_heroslide_options_alter_homeabout_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homefeature',
            name='value',
            field=models.CharField(blank=True, default='', help_text="Cifra destacada, ej: '+ 8,000', '15 Minutos'. Déjelo vacío si no aplica.", max_length=50, verbose_name='Valor / Cifra'),
        ),
        migrations.AlterField(
            model_name='homefeature',
            name='icon',
            field=models.CharField(choices=[('Coffee', 'Café'), ('Award', 'Premio'), ('Leaf', 'Hoja'), ('Truck', 'Camión'), ('Heart', 'Corazón'), ('MessageSquare', 'Mensaje'), ('Users', 'Usuarios'), ('Globe', 'Globo'), ('Clock', 'Reloj'), ('Star', 'Estrella'), ('ShieldCheck', 'Escudo'), ('Zap', 'Rayo')], default='Coffee', help_text='Seleccione el icono que mejor represente esta característica.', max_length=50, verbose_name='Icono'),
        ),
    ]
