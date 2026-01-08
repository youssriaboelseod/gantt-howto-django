
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
import reportlab
from reportlab.pdfbase.ttfonts import TTFont
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
#from config.utlilities import static_path,input_path,BASE_DIR
from .models import Task as model_name 
###################################################
import os
import locale

import arabic_reshaper

from bidi.algorithm import get_display

from django.http import HttpResponse
import io
from reportlab.pdfgen import canvas
import numpy as np
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#_____enaple arabic fonts
#locale.setlocale(locale.LC_ALL, '')
#locale._override_localeconv = {'mon_thousands_sep': '.'}
reportlab.rl_config.TTFSearchPath.append(str(settings.BASE_DIR))
print("_____os.chdir_____",os.getcwd())
pdfmetrics.registerFont(TTFont('Arabic',os.path.join(BASE_DIR, r'font/ttf/trado.ttf')))

#_____enaple arabic fonts

#init the style sheet
styles = getSampleStyleSheet()

arabic_text_style = ParagraphStyle(
'border', # border on
parent = styles['Normal'] , # Normal is a defaul style  in  getSampleStyleSheet
borderColor= '#333333',
borderWidth =  1,
borderPadding  =  2,
fontName="Arabic" #previously we named our custom font "Arabic"
)

#_________________________
def Workflow_pdf(request, pk):
#init the style sheet
#_________________________
    # Teh Invoice

    invoice = model_name.objects.get(pk=pk)
    response = HttpResponse(content_type='application/pdf')
    #_____________arabic
    reshaped_title = arabic_reshaper.reshape(invoice.step_details)
    bidi_title = get_display(reshaped_title) 
    
    pdf_name = _("Document{}.pdf").format(bidi_title)
    
    response['Content-Disposition'] = 'attachment; filename=%s' %bidi_title
    # Los productos de la orden ya en una matriz

    products = model_name.objects.filter(f71workflow_id=pk).only(
                            'a','b', 'c','d','e', 'f','file','image','document_id','f39mother_id',
                            'f127means_id','f141data_id','f53information_id','f37help_id',
                            'format_x','format_y','format_size','format_z','format_colour_r','format_colour_b','format_colour_g')
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    print("_______________________",invoice,products)
    #canvas.drawString(x - 100, y, ar)
    # Create the PDF object, using the buffer as its "file."
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont('Arabic', 32)

    
    #if not os.path.exists(static_path+'/t18doer'):
    #    os.makedirs(static_path+'/t18doer')
    # Header corporativa
    #archivo_imagen =os.path.join(static_path,'t18doer','logo.png')
    # Definimos el tamaño de la imagen a cargar y las coordenadas
    #pdf.drawImage(archivo_imagen, 30, 710, 120, 90, preserveAspectRatio=True)
    pdf.setLineWidth(.3)
    pdf.line(30, 735, 582, 735)

    pdf.setFont('Helvetica', 8)


    title = ('{} Document # {}').format(invoice.f51objects_id, bidi_title)
    pdf.setFont('Helvetica', 22)
    pdf.drawString(30, 710, title)#x,y

    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(250, 40, 'Issue Date:')#x - y

    # pdf.setFont('Helvetica-Bold', 12)
    # pdf.drawString(180, 625, 'Seller:')

    today = timezone.now()
    pdf.setFont('Helvetica', 12)
    pdf.drawString(250, 25, today.strftime("%Y-%m-%d %H:%M:%S"))#x,y

    # pdf.setFont('Helvetica', 12)
    # pdf.drawString(180, 610, 'Nombre del Vendedor')

    # Alto y ancho de la hoja
    width, height = letter

    # A hight of header all tables
    high = 690

    # Header de la tabla
    data_header = []
    data_header.append([
        # "Producto",
        _('a'),
        _('b'),
        _('c'),
        _('d'),
    ])

    # head of columns
    table = Table(
        data_header,
        colWidths=[7*cm, 3*cm, 3*cm, 3*cm, 3.5*cm]
    )
    table.setStyle(
        TableStyle([
            # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.black),
            # ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('ALIGN', (1, 0), (-1, 0), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
        ])
    )
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 10, high) #columsn header hign

    if products:
        # Cuerpo de la tabla
        _data_table = []
                #_____enaple arabic fonts

        
    
        #pdf.append(Spacer(1,8))
        #pdf.append(Paragraph(bidi_text,arabic_text_style))
        for _product in products:
            #__________________________arabic text____________
            rehaped_text_a = arabic_reshaper.reshape(_product.a)
            bidi_text_a = get_display(rehaped_text_a)   

            rehaped_text_b = arabic_reshaper.reshape(_product.b)
            bidi_text_b = get_display(rehaped_text_b) 

            rehaped_text_c = arabic_reshaper.reshape(_product.c)
            bidi_text_c = get_display(rehaped_text_c) 

            rehaped_text_d = arabic_reshaper.reshape(_product.d)
            bidi_text_d = get_display(rehaped_text_d) 
            _data_table.append(
                [
                Paragraph(bidi_text_a,arabic_text_style),
            #_________________________________________________ 
                Paragraph(bidi_text_b,arabic_text_style),
                Paragraph(bidi_text_c,arabic_text_style),
                Paragraph(bidi_text_d,arabic_text_style),
                ]
            )
            #adjust high all pages
            #يتم ضبطها من الصفحة الرئيية
            records_high=int(invoice.format_nxt_high)
            high = high - records_high  
        # add photo of document

            if len(str(_product.image))>=2:
                print("_product.image",_product.image,len(str(_product.image)),"y",high+_product.format_y,"x",_product.format_x,"size",_product.format_size,"z",_product.format_z)
                
    
                file2=sub_model_name._meta.verbose_name_raw
                image_document =os.path.join(input_path,str(_product.f39mother_id),str(_product.f127means_id),str(_product.f141data_id),str(_product.f53information_id),file2+"-"+str(_product.document_id)+".gif")
                pdf.drawImage(image_document, _product.format_x,_product.format_y, _product.format_size, _product.format_z, preserveAspectRatio=True)#(y,x,size,x_oposit)
    #________________________
        # #table content________________________
        table = Table(
            _data_table,
            colWidths=[7*cm, 3*cm, 7*cm, 3*cm, 3.5*cm]   
        )
        table.setStyle(
            TableStyle([
                # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                # ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ])
        )

    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 30, high)

    # Footer de la tabla
    data_foot = []
   
    data_foot.append(
        ["", _('Document number') + ":", "." + locale._format('%.2f', invoice.f51objects_id, grouping=True, monetary=True)]
    )
    data_foot.append(
        ["", _('workflow number') + ":", "." + locale._format('%.2f', invoice.id_workflow, grouping=True, monetary=True)]
    )
    data_foot.append(
        ["", _('page') + ":", "." + locale._format('%.2f', invoice.order, grouping=True, monetary=True)]
    )
    
    high = high - (22 * 22)     #footer y
    # Imprimir cuerpo la tabla
    table = Table(
        data_foot,
        colWidths=[11*cm, 5*cm, 3.5*cm]
    )


    table.setStyle(
        TableStyle([
            # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            # ('LINEBELOW', (1, 0), (2, 0), 1.5, colors.black),
            # ('LINEBELOW', (1, 0), (2, 2), 0.5, colors.black),
            ('LINEBELOW', (1, 3), (2, 3), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (1, 0), (1, 5), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (1, 2), (1, 2), 'Helvetica-Bold'),
        ])
    )
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 30, high)

    # Close the PDF object cleanly, and we're done.
    pdf.showPage()
    pdf.save()
    print("___________products____________",pdf)

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    response.write(buffer.getvalue())

    return response
