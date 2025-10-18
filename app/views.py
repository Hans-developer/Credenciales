# app/views.py
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4  # Usar A4 (vertical: 595x842 puntos)
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color  # Para colores personalizados
import io
from .forms import CredencialForm
from datetime import datetime

hoy = datetime.now()


class Vista(View):
    def get(self, request):
        form = CredencialForm()  # Instancia el formulario vacío
        return render(request, 'app/index.html', {'form': form})
    
    def post(self, request):
        form = CredencialForm(request.POST, request.FILES)  # Procesa el formulario con archivos
        if form.is_valid():
            # Obtener datos del formulario
            foto = form.cleaned_data.get('foto')
            nombre_completo = form.cleaned_data['nombre_completo']
            cargo = form.cleaned_data['cargo']
            pais = form.cleaned_data['pais']
            
            # Crear el PDF con diseño vertical centrado (como para teléfono)
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)  # Usar A4 (vertical: 595x842 puntos)
            width, height = A4
            
            # Centro de la página
            center_x = width / 2
            
            # Dibujar fondo de color (gris claro) para la credencial
            p.setFillColorRGB(0.9, 0.9, 0.9)  # Color gris claro (ajusta RGB si quieres otro color)
            border_width = 400
            border_height = 600
            border_x = center_x - (border_width / 2)
            border_y = height - 650
            p.rect(border_x, border_y, border_width, border_height, fill=1, stroke=0)  # Relleno sin borde
            
            # Dibujar título "Credencial de Acceso" arriba de la foto, centrado
            p.setFillColorRGB(0, 0, 0)  # Volver a negro para el texto
            p.setFont("Helvetica-Bold", 20)
            title_y = height - 100  # Posición arriba
            p.drawCentredString(center_x, title_y, "Credencial de Acceso")
            
            # Dibujar la foto abajo del título, centrada
            if foto:
                img = ImageReader(foto)
                img_width, img_height = 200, 200  # Tamaño de la foto
                img_x = center_x - (img_width / 2)
                img_y = height - 350  # Ajustar posición debajo del título
                p.drawImage(img, img_x, img_y, width=img_width, height=img_height)
            
            # Dibujar texto abajo de la foto, centrado y ordenado
            p.setFont("Helvetica-Bold", 18)
            text_y_start = height - 400  # Posición inicial del texto (debajo de la foto)
            line_spacing = 35
            
            p.drawCentredString(center_x, text_y_start, f"Nombre: {nombre_completo}")
            p.drawCentredString(center_x, text_y_start - line_spacing, f"Cargo: {cargo}")
            p.drawCentredString(center_x, text_y_start - (2 * line_spacing), f"País: {pais}")
            p.drawCentredString(center_x, text_y_start - (3 * line_spacing), f"Fecha: {hoy.strftime("%d/%m/%Y")}")

            
            # Borde de la credencial (opcional, ahora que hay fondo)
            p.setStrokeColorRGB(0, 0, 0)  # Negro para el borde
            p.rect(border_x, border_y, border_width, border_height, fill=0, stroke=1)  # Solo borde
            
            p.showPage()
            p.save()
            
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="credencial.pdf"'
            return response
        else:
            # Si el formulario no es válido, volver a mostrarlo con errores
            return render(request, 'app/index.html', {'form': form})
