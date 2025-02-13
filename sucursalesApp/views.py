from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from CarritoApp.models import Sucursales
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from .forms import SucursalForm

class SucursalesListView(View):
    def get(self, request):
        # Verificar si la solicitud es AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            sucursales = Sucursales.objects.all().values('iidsucursal', 'snombre', 'iidestado')
            sucursales_list = list(sucursales)
            return JsonResponse({'data': sucursales_list})
        # Título para la página
        title = "Bienvenido a mi sitio"
        # Contexto para la plantilla HTML
        context = {
            'title': title,
        }
        # Renderizar la plantilla HTML para solicitudes normales
        return render(request, 'listSucursales.html', context)

class SucursalCreateView(CreateView):
    model = Sucursales
    form_class = SucursalForm
    template_name = 'sucursales_form.html'
    success_url = reverse_lazy('api_sucursales')

    def form_valid(self, form):
        form.save()
        return JsonResponse({'form_is_valid': True, 'message': 'La sucursal se agregó correctamente'})

    def form_invalid(self, form):
        return JsonResponse({
            'form_is_valid': False,
            'errors': form.errors.as_json()
        })

class SucursalUpdateView(UpdateView):
    model = Sucursales
    form_class = SucursalForm
    template_name = 'sucursales_form.html'
    success_url = reverse_lazy('api_sucursales')

    def form_valid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form.save()
            return JsonResponse({'form_is_valid': True})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'form_is_valid': False, 'html_form': render(self.request, self.template_name, {'form': form}).content.decode()})
        return super().form_invalid(form)

class SucursalDeleteView(DeleteView):
    model = Sucursales
    template_name = 'cliente_confirm_delete.html'
    success_url = reverse_lazy('api_clientes')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'form_is_valid': True})
        return response


# class SucursalCreateView(CreateView):
#     model = Sucursales
#     form_class = SucursalForm
#     template_name = 'sucursales_form.html'
#     success_url = reverse_lazy('api_sucursales')

#     def form_valid(self, form):
#         form.save()
#         if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             return JsonResponse({'form_is_valid': True, 'message': 'La sucursal se agregó correctamente'})
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             return JsonResponse({
#                 'form_is_valid': False,
#                 'html_form': render_to_string(self.template_name, {'form': form}, request=self.request)
#             })
#         return super().form_invalid(form)