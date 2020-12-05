import random
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic import View
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Menu
from .models import Restaurant
from .models import Visit
from .forms import AddMenuFormSet
from .forms import RestaurantFilterForm
from .forms import RestaurantForm
from datetime import datetime, timedelta
from django.utils.translation import gettext as _
from braces.views import AjaxResponseMixin
from braces.views import JsonRequestResponseMixin


class StartPageView(TemplateView):
    template_name = "startup/index.html"

    def get_context_data(self, **kwargs):
        context = super(
            StartPageView, self
        ).get_context_data(**kwargs)

        context.update({
            'active_tab': 'home',
        })
        return context


class RestaurantListView(ListView):
    template_name = "startup/restau_list.html"

    def get_queryset(self):
        queryset = Restaurant.objects.all()

        self.q = self.request.GET.get('q')
        self.restau_type = self.request.GET.get('restau_type')

        if self.q:
            queryset = queryset.filter(name__icontains=self.q)
        if self.restau_type:
            queryset = queryset.filter(restau_type=int(self.restau_type))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            RestaurantListView, self
        ).get_context_data(**kwargs)

        filter_form = RestaurantFilterForm(data=self.request.GET)

        north = 10.533332
        east = 123.849997

        south = 10.333332
        west = 123.749997

        selected_markers = self.get_queryset().filter(
            latitude__range=(south, north),
            longitude__range=(west, east)
        )

        context.update({
            'active_tab': 'restau',
            'filter_form': filter_form,
            'selected_markers': selected_markers,
        })
        return context


class CRUDRestaurantView(FormView):
    template_name = "startup/restau_action.html"
    form_class  = RestaurantForm
    model = Restaurant

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            CRUDRestaurantView, self
        ).get_context_data(**kwargs)
        
        queryset = self.get_queryset()
        context.update({
            'active_tab': 'add',
        })
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if 'create_random' in self.request.POST:
            Restaurant.objects.all().delete()
            Menu.objects.all().delete()
            sample_name = [
                'Jollibee', 'McDo',
                'Starbucks', 'Samgyupsalamat',
                'KFC', 'Chowking',
                'Kenny Rogers', 'Krispy Kreme',
                'Dunkin Donuts', 'Greenwich'
            ]
            sample_img_url = [
                'https://1000logos.net/wp-content/uploads/2019/03/Jollibee-Logo.png',
                'https://cdn.mos.cms.futurecdn.net/xDGQ9dbLmMpeEqhiWayMRB.jpg',
                'https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Starbucks_Corporation_Logo_2011.svg/1200px-Starbucks_Corporation_Logo_2011.svg.png',
                'https://app.aranetacity.com/files/establishments/image/31cd6c69-393f-4ca2-b1c6-4b72af1e002e/Samyupsalamat%20logo.jpg',
                'https://logos-world.net/wp-content/uploads/2020/04/KFC-Logo-2014%E2%80%932018.png',
                'https://upload.wikimedia.org/wikipedia/en/thumb/d/d6/Chowking_logo.svg/1200px-Chowking_logo.svg.png',
                'https://seekvectorlogo.net/wp-content/uploads/2018/06/kenny-rogers-roasters-vector-logo.png',
                'https://1000logos.net/wp-content/uploads/2017/12/krispy-kreme-logo.png',
                'https://i.pinimg.com/originals/5a/f4/2b/5af42b2e31010a24ac46d2cb5a0e60a6.png',
                'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Greenwich_Pizza_logo.svg/1200px-Greenwich_Pizza_logo.svg.png',
            ]
            sample_food = [
                'Chicken Joy', 'BFF Fries',
                'Ice Latte', 'Beef Bulgogi',
                'Zinger', 'Sweet n Sour Chicken',
                'Roasted Chicken', 'Honey Glazed Donut',
                'Choco Butternut Donut', 'Hawaiian Overload Pizza'
            ]
            for index, item in enumerate(sample_name):
                lat = round(random.uniform(10.333332, 10.533332), 6)
                longitude = round(random.uniform(123.749997, 123.969997), 6)
                store_type = random.uniform(1, 6)
                restau = Restaurant.objects.create(
                    name=item,
                    description='lorem ipsum lorem ipsum lorem ipsum',
                    longitude=longitude,
                    latitude=lat,
                    restau_img_url=sample_img_url[index],
                    restau_type=store_type
                )
                for i in range(1, 4):
                    is_specialty = True
                    if i > 1:
                        is_specialty = False
                    Menu.objects.create(
                        name='%s%s' % (sample_food[index], i),
                        description='lorem ipsum lorem ipsum lorem ipsum',
                        price=round(random.uniform(1, 50), 2),
                        restaurant=restau,
                        is_specialty=is_specialty,
                    )



            messages.success(self.request, _('Successfully created sample data.'))
        else:
            if form.is_valid():
                form.save()
                messages.success(self.request, _('Successfully created.'))
                return self.form_valid(form)
            else:
                messages.error(self.request, _('Error Saving.'))
                return self.form_invalid(form)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('restau_action')


class RestaurantDataAjax(
    JsonRequestResponseMixin,
    AjaxResponseMixin,
    View,
):
    def get_ajax(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)

        restau_object = Restaurant.objects.get(pk=int(pk))

        if restau_object.specialty():
            specialty = 'Restaurant specialty %s' % restau_object.specialty()
        else:
            specialty = 'No specialty is currently registered in this Restaurant'
        data = {
            'name': restau_object.name,
            'desc': restau_object.description,
            'latitude': restau_object.latitude,
            'longitude': restau_object.longitude,
            'url': restau_object.restau_img_url,
            'type': 'Restaurant that offer %s' % restau_object.get_restau_type_display(),
            'specialty': specialty,
            'pk': restau_object.pk,
        }

        return self.render_json_response(data)


class RestaurantMenuView(ListView):
    template_name = "startup/add_menu.html"

    def get_queryset(self):
        queryset = Restaurant.objects.all()

        return queryset

    def get_object(self):
        restau = self.kwargs.get("pk", None)
        if restau:
            return self.get_queryset().get(
                pk=int(restau),
            )
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super(
            RestaurantMenuView, self
        ).get_context_data(**kwargs)

        form_set = None
        if self.get_object():
            form_set = AddMenuFormSet(
                instance=self.get_object(),
                queryset=Menu.objects.filter(restaurant=self.get_object()),
                data=self.request.POST or None,
            )
        context.update({
            'active_tab': 'add_menu',
            'object': self.get_object(),
            'form_set': form_set,
        })
        return context

    def post(self, request, *args, **kwargs):
        form_set = AddMenuFormSet(
            instance=self.get_object(),
            queryset=Menu.objects.filter(restaurant=self.get_object()),
            data=self.request.POST or None,
        )
        if form_set.is_valid():
            form_set.save()
            messages.success(self.request, _('Successfully created.'))
        else:
            return self.form_invalid(form_set)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            'menu_view',
            kwargs={
                'pk': self.get_object().pk,
            }
        )

    def form_invalid(self, form):
        messages.error(self.request, _('Duplicate Data.'))
        self.object_list = self.get_queryset()
        return self.render_to_response(
            self.get_context_data(
                form_set=form,
                object=self.get_object(),
                active_tab='add_menu',
            )
        )


class MenuListView(TemplateView):
    template_name = "startup/menu_list.html"

    def dispatch(self, request, *args, **kwargs):
        restau = self.kwargs.get("pk", None)
        add_visitor = self.kwargs.get("add_visitor", None)
        # if add_visitor, it will add visitor to restau and return to a page with listing of menu
        # two different url but same view is created, one is for adding of visitor and the other one
        # is listing of menus
        self.object = Restaurant.objects.get(
            pk=int(restau),
        )
        if add_visitor == 'True':
            Visit.objects.create(
                restaurant=self.object,
            )
            return redirect(reverse(
                'menu_list_view',
                kwargs={'pk': int(restau)}
            ))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            MenuListView, self
        ).get_context_data(**kwargs)

        context.update({
            'active_tab': 'restau',
            'object': self.object,
        })
        return context


class StatisticsView(ListView):
    template_name = "startup/statistics.html"

    def get_queryset(self):
        queryset = Restaurant.objects.all()

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super(
            StatisticsView, self
        ).get_context_data(**kwargs)

        today = datetime.today().date()

        start_date = today - timedelta(days=4)
        data_list = []
        for i in range(1, 6):
            per_day = []
            per_day.append(start_date.strftime('%m/%d/%Y'))
            for restau in self.get_queryset():
                count = Visit.objects.filter(
                    restaurant=restau,
                    created__date=start_date,
                ).count()
                per_day.append(count)
            start_date = start_date + timedelta(days=1)
            data_list.append(per_day)

        context.update({
            'active_tab': 'statistics',
            'data_list': data_list,
        })
        return context
