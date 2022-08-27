from django.db import models
from .validators import validate_file_extension


# Ended up not using this for now as it dampens the user experience.
class Store(models.Model):
    id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=200)
    description = models.TextField(null=True)

    class Meta:
        ordering = ['id']
        db_table = 'stores'
        managed = True


class IngredientCategory(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    name = models.CharField(max_length=200)
    date_created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id']
        db_table = 'ingredient_category'
        managed = True

# todo Meta tag images for searching when adding an icon to a new item
# todo Maybe add new Meta tags to icons for specific users when they use it?
class IngredientIcon(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    name = models.CharField(max_length=200)
    icon_image = models.FileField(upload_to="ingredient_icons_uploaded/", validators=[validate_file_extension])
    date_created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id']
        db_table = 'ingredient_icon'
        managed = True


# todo Optionally track cost of items
class IngredientItem(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    icon = models.ForeignKey(IngredientIcon, related_name='icon_data',
                             on_delete=models.PROTECT)
    ingredient_id = models.IntegerField(null=True)
    barcode = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    category = models.ForeignKey(IngredientCategory, related_name='category_data', on_delete=models.PROTECT)
    default_quantity = models.FloatField(null=True)
    date_created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id']
        db_table = 'ingredient_item'
        managed = True


class IngredientCostLogging(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    cost = models.FloatField()
    currency = models.CharField(max_length=10)
    date_created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id']
        db_table = 'ingredient_cost_logging'
        managed = True


class IngredientInventory(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    ingredient_id = models.ForeignKey(IngredientItem, related_name='ingredient_data', on_delete=models.PROTECT)
    quantity = models.FloatField()
    cost = models.ForeignKey(IngredientCostLogging, related_name='ingredient_cost_data',
                             on_delete=models.PROTECT, null=True)
    expiration_date = models.DateField()
    date_created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id']
        db_table = 'ingredient_inventory'
        managed = True


class AppFeatureList(models.Model):
    id = models.AutoField(primary_key=True)
    feature_name = models.CharField(max_length=200)
    description = models.TextField(null=True)

    class Meta:
        ordering = ['id']
        db_table = 'app_feature_list'
        managed = True


class UserFeatureList(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    feature = models.ForeignKey(AppFeatureList, related_name='feature_data', on_delete=models.PROTECT)
    enabled = models.BooleanField(default=0)

    class Meta:
        ordering = ['id']
        db_table = 'user_feature_list'
        managed = True
