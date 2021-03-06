# Generated by Django 3.2.13 on 2022-05-25 15:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Author name', max_length=150, unique=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Author phone number', max_length=128, null=True, region=None)),
                ('birth_date', models.DateField(blank=True, help_text='Author birth date', null=True)),
                ('death_date', models.DateField(blank=True, help_text='Author death date', null=True)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
                'db_table': 'authors',
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('name', models.CharField(help_text='Category name', max_length=150)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('title', models.TextField(help_text='Name of the Book')),
                ('publisher_name', models.TextField(help_text='Name of the publisher')),
                ('published_date', models.DateField(help_text='Book published date')),
                ('price', models.FloatField(help_text='Price of the book', validators=[django.core.validators.MinValueValidator(1.0)])),
                ('units_sold', models.PositiveSmallIntegerField(db_index=True, default=0, help_text='Number of books sold')),
                ('author', models.ForeignKey(help_text='Author of the book', on_delete=django.db.models.deletion.CASCADE, related_name='books', to='book_store.author')),
                ('category', models.ForeignKey(help_text='Book category', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='book_store.category')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
                'db_table': 'books',
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
                'unique_together': {('slug', 'author_id')},
            },
        ),
    ]
