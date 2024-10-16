from django.contrib import admin
from CarritoApp.models import Empleados, TipoEmpleado, TipoProductos, Productos, Sucursales, TipoMovimiento


# Register your models here.
# @admin.display(description="TipoEmpleado")
# def tipoEmpleado(obj):
#     return f"{obj.stipoempleado}"


# @admin.display(description="Tipo_Empleado")
# def tipoEmp(obj):
#     return f"{obj.iidtipoempleado.stipoempleado}"

@admin.register(Empleados)
class EmpleadosAdmin(admin.ModelAdmin):
    list_display = ["tipoEmp","upper_case_name", "upper_case_apellido", "documento", "usuario"]    
    search_fields = ["snombre", "sapellido"]
    list_per_page = 5
    list_select_related = True

    @admin.display(description="Nombre")
    def upper_case_name(self,obj):
        return f"{obj.snombre}".upper()

    @admin.display(description="Apellido")
    def upper_case_apellido(self,obj):
        return f"{obj.sapellido}".upper()

    @admin.display(description="Documento")
    def documento(self,obj):
        return f"{obj.idni}"

    def tipoEmp(self, obj):
        return obj.iidtipoempleado.stipoempleado
    
    def usuario(self, obj):
        return obj.user.username

    tipoEmp.admin_order_field = 'tipoempleado'

@admin.register(TipoEmpleado)
class TipoEmpleadoAdmin(admin.ModelAdmin):
    list_display = ["iidtipoempleado", "stipoempleado"]

@admin.register(TipoProductos)
class TipoProductosAdmin(admin.ModelAdmin):
    list_display = ["tipoProducto"]
    #pass

    @admin.display(description="Tipo de producto")
    def tipoProducto(self, obj):
        return f"{obj.snombretipoproducto}"

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ["iidtipoproducto","snombreproducto","sdescripcion","istock","dprecio","surl"]


@admin.register(Sucursales)
class SucursalesAdmin(admin.ModelAdmin):
    list_display = ["snombre"]

class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display = ('stipomovimiento',)  # Muestra el nombre del tipo de movimiento en la lista

admin.site.register(TipoMovimiento, TipoMovimientoAdmin)