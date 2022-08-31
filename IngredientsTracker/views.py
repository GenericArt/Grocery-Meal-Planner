from django.shortcuts import render, redirect, Http404
from django.http import JsonResponse
import json
from .forms import BarcodeScanner, LoginForm
from .models import IngredientItem, IngredientInventory, IngredientCategory, UserFeatureList
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework import status


@login_required(login_url='loginpage/')
def index(request):
    context = {'form': BarcodeScanner()}
    return render(request, "IngredientsTracker/add_inventory.html", context)


def login_page(request):
    context = {'login_form': LoginForm}
    try:
        msg = request.session['msg']
    except KeyError as e:
        msg = None

    if msg:
        context['msg'] = msg
    else:
        context['msg'] = ''

    return render(request, 'IngredientsTracker/login_page.html', context)


def validate_user_login(request):
    if request.method == 'POST':
        user_email = request.POST.get('user_email', '')
        user_password = request.POST.get('user_password', '')

        user = authenticate(request, email=user_email, password=user_password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            request.session['msg'] = 'Oops! Wrong credentials!'
            return redirect('login_page')


def log_user_out(request):
    logout(request)
    return redirect('/loginpage')


@csrf_exempt
def check_initial_data_entry(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post_data = json.loads(request.body.decode("utf-8"))
            exists = False
            print(post_data)

            scanned_barcode = str(post_data['barcode']).strip()
            name_entered = str(post_data['name']).strip()
            item_info = {}

            user_id = request.user.id
            user_features = UserFeatureList.objects.filter(id=user_id, enabled=True)
            user_features_list = [x.feature.feature_name for x in user_features]

            # check if barcode exists
            if scanned_barcode:
                check_barcode_exist = IngredientItem.objects.filter(barcode=scanned_barcode, id=request.user.id)
                if check_barcode_exist:
                    exists = True

                    existing_item = check_barcode_exist[0]
                    item_info['name'] = existing_item.name
                    item_info['category'] = existing_item.category.name
                    item_info['default_quantity'] = existing_item.default_quantity
                    item_info['barcode'] = existing_item.barcode

                    if existing_item.description:
                        item_info['description'] = existing_item.description

                else:
                    exists = False
            elif name_entered:
                check_name_exists = IngredientItem.objects.filter(name=name_entered, id=request.user.id)
                if check_name_exists:
                    exists = True

                    existing_item = check_name_exists[0]
                    item_info['name'] = existing_item.name
                    item_info['category'] = existing_item.category.name
                    item_info['default_quantity'] = existing_item.default_quantity
                    item_info['barcode'] = existing_item.barcode

                    if existing_item.description:
                        item_info['description'] = existing_item.description
                else:
                    exists = False
            else:
                exists = False

            context = {
                'msg': 'This was posted: {}'.format(scanned_barcode),
                'exists': exists,
                'item_info': item_info,
                'categories': list(IngredientCategory.objects.all().values_list('name', flat=True)),
                'user_features_list': user_features_list,
            }

            return JsonResponse(context, status=200)
        else:
            JsonResponse({'server_msg': 'Expected a POST'}, status=400)
    else:
        JsonResponse({'server_msg': 'User is not logged in'}, status=401)


@csrf_exempt
def add_new_ingredient(request):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))

        barcode_nbr = str(post_data['barcode']).strip()
        barcode_name = str(post_data['name']).strip()
        barcode_qty = int(str(post_data['quantity']).strip())
        barcode_desc = str(post_data['description']).strip()
        barcode_expire = str(post_data['expire_date']).strip()
        barcode_category = str(post_data['category']).strip()

        # Check if needed information exists before adding to the database
        if not barcode_nbr or not barcode_name or not barcode_expire or not barcode_category:
            return JsonResponse({'server_msg': 'Missing either the barcode number, expiry date, category or name'},
                                status=422)
        else:
            category_instance = IngredientCategory.objects.get(name=barcode_category)
            new_item_entry = IngredientItem.objects.create(
                user_id=request.user.id,
                barcode=barcode_nbr,
                name=barcode_name,
                default_quantity=barcode_qty,
                description=barcode_desc,
                category=category_instance,
            )
            new_item_entry.save()
            new_item_entry.ingredient_id = new_item_entry.id
            new_item_entry.save()

            new_inventory = IngredientInventory.objects.create(
                user_id=request.user.id,
                ingredient_id=new_item_entry,
                quantity=barcode_qty,
                expiration_date=barcode_expire,
            )
            new_inventory.save()

            return JsonResponse({'server_msg': 'Added new item successfully'}, status=200)

    return JsonResponse({'server_msg': 'This should have been a POST request but was not'}, status=401)


