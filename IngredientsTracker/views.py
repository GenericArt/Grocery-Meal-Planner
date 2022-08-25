from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json
from .forms import IngredientItemForm, BarcodeScanner
from .models import IngredientItem, IngredientInventory


def index(request):
    context = {'form': BarcodeScanner()}
    # return render(request, "IngredientsTracker/add_inventory.html", context)
    return render(request, "IngredientsTracker/add_inventory.html", context)


def check_scanned_barcode(request):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        print(post_data)

        scanned_barcode = str(post_data['barcode']).strip()
        item_info = {}

        # check if barcode exists
        check_barcode_exist = IngredientItem.objects.filter(barcode=scanned_barcode).values()
        if check_barcode_exist:
            exists = True

            # todo Take in only Barcode and check for a default Quantity. Then always provide a pop confirmation
            '''A better idea may be to not use a Django Form and then just use Javascript to check if the
            barcode exists and get the default quanitity. Then ask user if this is right and then submit to db'''
            add_ingredient_inventory(barcode=scanned_barcode,
                                     quantity=check_barcode_exist[0]['default_quantity'],
                                     ingredient_id=check_barcode_exist[0]['id'])
        else:
            exists = False

        context = {
            'msg': 'This was posted: {}'.format(scanned_barcode),
            'exists': exists,
            'item_info': item_info,
        }

        return JsonResponse(context, status=200)


def add_new_ingredient(request):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))

        barcode_nbr = str(post_data['barcode']).strip()
        barcode_name = str(post_data['name']).strip()
        barcode_qty = int(str(post_data['quantity']).strip())
        barcode_desc = str(post_data['description']).strip()
        barcode_expire = str(post_data['expire_date']).strip()

        # Check if needed information exists before adding to the database
        if not barcode_nbr or not barcode_name:
            return JsonResponse({'server_msg': 'Missing either the barcode number or name'}, status=422)
        else:
            new_item_entry = IngredientItem.objects.create(
                barcode=barcode_nbr,
                name=barcode_name,
                default_quantity=barcode_qty,
                description=barcode_desc,
            )
            new_item_entry.save()
            new_item_entry.ingredient_id = new_item_entry.id
            new_item_entry.save()

            new_inventory = IngredientInventory.objects.create(
                ingredient_id=new_item_entry,
                quantity=barcode_qty,
                expiration_date=barcode_expire,
            )
            new_inventory.save()

            return JsonResponse({'server_msg': 'Added new item successfully'}, status=200)

    return JsonResponse({'server_msg': 'This should have been a POST request but was not'}, status=401)


def barcode_scanned(request):
    if request.method == 'POST':
        this_form = BarcodeScanner(request.POST)

        barcode_num = this_form['barcode'].value()
        # quantity = this_form['quantity'].value()

        print('Scan Happened: {}'.format(barcode_num))

        # check if barcode exists
        check_barcode_exist = IngredientItem.objects.filter(barcode=barcode_num).values()
        if check_barcode_exist:
            # todo Take in only Barcode and check for a default Quantity. Then always provide a pop confirmation
            '''A better idea may be to not use a Django Form and then just use Javascript to check if the
            barcode exists and get the default quanitity. Then ask user if this is right and then submit to db'''
            add_ingredient_inventory(barcode=barcode_num,
                                     quantity=check_barcode_exist[0]['default_quantity'],
                                     ingredient_id=check_barcode_exist[0]['id'])
        else:
            # todo Need to Redirect with the Barcode and Quantity to add new Ingredient Item to db
            pass


def add_ingredient_inventory_check(request):
    if request.method == 'POST':
        form = IngredientItemForm(request.POST)

        barcode = form.barcode.strip()
        name = form.name.strip()
        description = form.description.strip()

        '''
        Check if ingredient exists.
        If does, add the inventory
        If does not add new Ingredient and then add inventory
        '''
        query_db = IngredientItem.objects.filter(barcode=form.barcode.strip()).values()
        if len(query_db) == 1:
            add_ingredient_inventory(barcode, name, description)
            add_new_ingredient_item(barcode, name, description)
        elif not query_db:
            add_new_ingredient_item(barcode, name, description)
        elif len(query_db) > 1:
            pass
        else:
            return HttpResponse(status=404)


def add_ingredient_inventory(barcode, quantity, ingredient_id):
    ingredient = IngredientItem.objects.get(barcode=barcode)
    new_entry = IngredientInventory(

    )


def add_new_ingredient_item(barcode, name, description):
    new_entry = IngredientItem(
        barcode=barcode,
        name=name,
        description=description if description else '',
    )
    new_entry.save()
