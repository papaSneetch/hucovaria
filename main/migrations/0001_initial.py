# Generated by Django 4.0.2 on 2022-04-04 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('symbol', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('organism', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('virus', models.CharField(max_length=60)),
                ('host', models.CharField(max_length=60)),
                ('interaction', models.CharField(max_length=60)),
                ('strain', models.CharField(max_length=60)),
                ('localization', models.CharField(max_length=60)),
                ('tissue_expression', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('time', models.DateTimeField()),
                ('file', models.FileField(upload_to='')),
                ('annotation', models.CharField(max_length=60)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VirusResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.result')),
            ],
        ),
        migrations.CreateModel(
            name='TissueExpressionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.result')),
            ],
        ),
        migrations.CreateModel(
            name='StrainResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.result')),
            ],
        ),
        migrations.CreateModel(
            name='LocalizationResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.result')),
            ],
        ),
        migrations.CreateModel(
            name='KeggResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.result')),
            ],
        ),
        migrations.CreateModel(
            name='KEGG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=100)),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.gene')),
            ],
        ),
        migrations.CreateModel(
            name='InteractionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.result')),
            ],
        ),
        migrations.CreateModel(
            name='HostResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.result')),
            ],
        ),
        migrations.CreateModel(
            name='GO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=10)),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.gene')),
            ],
        ),
        migrations.CreateModel(
            name='GeneOntologyResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.result')),
            ],
        ),
    ]
