import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color, HexColor
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import test_login

class TestReportGenerator:
    def __init__(self):
        self.colors = {
            'primary': '#1f4e79',
            'secondary': '#4472c4', 
            'success': '#70ad47',
            'error': '#c5504b',
            'warning': '#f4b942',
            'light_gray': '#f5f5f5',
            'dark_gray': '#6c757d'
        }
        
    def run_tests_and_get_results(self):
        """
        Ejecuta las pruebas de integración y retorna un resumen de los resultados.
        """
        from io import StringIO
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            test_login.main()
        except Exception as e:
            print(f"[ERROR] Error ejecutando pruebas: {e}")

        sys.stdout = old_stdout
        output = captured_output.getvalue()
        
        results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "details": [],
            "execution_time": datetime.datetime.now()
        }
        
        for line in output.split('\n'):
            line = line.strip()
            if line:
                if "[OK]" in line or "PASSED" in line.upper():
                    results["passed"] += 1
                    results["details"].append(("PASSED", line))
                elif "[ERROR]" in line or "FAILED" in line.upper():
                    results["failed"] += 1
                    results["details"].append(("FAILED", line))
                elif "[WARNING]" in line or "WARN" in line.upper():
                    results["warnings"] += 1
                    results["details"].append(("WARNING", line))
                else:
                    results["details"].append(("INFO", line))
        
        results["total_tests"] = results["passed"] + results["failed"]
        results["success_rate"] = (results["passed"] / results["total_tests"] * 100) if results["total_tests"] > 0 else 0
        
        return results, output

    def generate_modern_chart(self, results, filename="test_results.png"):
        """
        Genera un gráfico moderno y atractivo de los resultados.
        """
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Gráfico de barras mejorado
        categories = ['Aprobadas', 'Fallidas']
        if results['warnings'] > 0:
            categories.append('Advertencias')
            values = [results['passed'], results['failed'], results['warnings']]
            colors_bar = [self.colors['success'], self.colors['error'], self.colors['warning']]
        else:
            values = [results['passed'], results['failed']]
            colors_bar = [self.colors['success'], self.colors['error']]
        
        bars = ax1.bar(categories, values, color=colors_bar, alpha=0.8, edgecolor='white', linewidth=2)
        
        # Añadir valores en las barras
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(value)}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        ax1.set_title('Resumen de Pruebas', fontsize=16, fontweight='bold', color=self.colors['primary'])
        ax1.set_ylabel('Cantidad de Pruebas', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, max(values) * 1.2 if values else 1)
        
        # Gráfico circular (donut)
        if results['total_tests'] > 0:
            sizes = [results['passed'], results['failed']]
            labels = ['Aprobadas', 'Fallidas']
            colors_pie = [self.colors['success'], self.colors['error']]
            
            wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors_pie, 
                                             autopct='%1.1f%%', startangle=90,
                                             wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
            
            # Mejorar el texto del gráfico circular
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(11)
            
            ax2.set_title(f'Tasa de Éxito: {results["success_rate"]:.1f}%', 
                         fontsize=16, fontweight='bold', color=self.colors['primary'])
        else:
            ax2.text(0.5, 0.5, 'Sin datos\ndisponibles', ha='center', va='center',
                    transform=ax2.transAxes, fontsize=14, color=self.colors['dark_gray'])
            ax2.set_title('Tasa de Éxito: N/A', fontsize=16, fontweight='bold', color=self.colors['primary'])
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return filename

    def generate_enhanced_pdf_report(self, results, chart_filename, detailed_output, filename="Test_Report_Enhanced.pdf"):
        """
        Genera un reporte PDF mejorado y más profesional.
        """
        doc = SimpleDocTemplate(filename, pagesize=A4, 
                              rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor(self.colors['primary']),
            alignment=1  # Centrado
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=HexColor(self.colors['secondary']),
            borderWidth=1,
            borderColor=HexColor(self.colors['secondary']),
            borderPadding=10,
            backColor=HexColor('#f8f9fa')
        )
        
        # Header con logo de la universidad
        header_data = []
        try:
            logo_path = "unal.png"
            if os.path.exists(logo_path):
                logo_img = Image(logo_path, width=100, height=100)
                
                # Crear párrafos separados para mejor espaciado
                title_para = Paragraph("REPORTE DE PRUEBAS DE INTEGRACIÓN", 
                                     ParagraphStyle('HeaderTitle',
                                                  fontSize=18,
                                                  fontName='Helvetica-Bold',
                                                  textColor=HexColor(self.colors['primary']),
                                                  spaceAfter=8))
                
                date_para = Paragraph(f"📅 {results['execution_time'].strftime('%d/%m/%Y %H:%M:%S')}", 
                                    ParagraphStyle('HeaderDate',
                                                 fontSize=12,
                                                 fontName='Helvetica',
                                                 textColor=HexColor(self.colors['secondary']),
                                                 spaceAfter=8))
                
                uni_para = Paragraph("Universidad Nacional de Colombia", 
                                   ParagraphStyle('HeaderUni',
                                                fontSize=11,
                                                fontName='Helvetica-Oblique',
                                                textColor=HexColor(self.colors['dark_gray'])))
                
                # Crear una tabla anidada para el contenido del header
                header_content = [[title_para], [date_para], [uni_para]]
                content_table = Table(header_content, colWidths=[4.5*inch])
                content_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ]))
                
                # Tabla principal con logo y contenido
                header_table = Table([[logo_img, content_table]], 
                                   colWidths=[1.8*inch, 4.5*inch])
                header_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 12),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                    ('TOPPADDING', (0, 0), (-1, -1), 15),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
                ]))
                story.append(header_table)
                story.append(Spacer(1, 40))
            else:
                print(f"⚠️  Logo no encontrado en {logo_path}. Usando título estándar.")
                # Si no hay logo, usar el título centrado como antes
                story.append(Paragraph("🔬 REPORTE DE PRUEBAS DE INTEGRACIÓN", title_style))
                story.append(Spacer(1, 20))
        except Exception as e:
            print(f"⚠️  Error cargando logo: {e}. Usando título estándar.")
            # En caso de error, usar el título centrado
            story.append(Paragraph("🔬 REPORTE DE PRUEBAS DE INTEGRACIÓN", title_style))
            story.append(Spacer(1, 20))
        
        # Información del reporte
        info_data = [
            ['📅 Fecha de Ejecución:', results['execution_time'].strftime('%d/%m/%Y %H:%M:%S')],
            ['📊 Total de Pruebas:', str(results['total_tests'])],
            ['✅ Pruebas Aprobadas:', str(results['passed'])],
            ['❌ Pruebas Fallidas:', str(results['failed'])],
            ['📈 Tasa de Éxito:', f"{results['success_rate']:.1f}%"]
        ]
        
        if results['warnings'] > 0:
            info_data.append(['⚠️ Advertencias:', str(results['warnings'])])
        
        info_table = Table(info_data, colWidths=[2*inch, 2*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (0, -1), HexColor(self.colors['primary'])),
            ('TEXTCOLOR', (1, 0), (1, -1), HexColor(self.colors['dark_gray'])),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 30))
        
        # Gráfico de resultados
        story.append(Paragraph("📈 Visualización de Resultados", subtitle_style))
        story.append(Spacer(1, 10))
        
        try:
            chart_img = Image(chart_filename, width=6*inch, height=2.5*inch)
            story.append(chart_img)
        except Exception as e:
            story.append(Paragraph(f"⚠️ Error cargando gráfico: {e}", styles['Normal']))
        
        story.append(Spacer(1, 30))
        
        # Log detallado
        story.append(Paragraph("📋 Registro Detallado", subtitle_style))
        story.append(Spacer(1, 10))
        
        # Crear tabla para el log detallado
        log_data = []
        for status, detail in results['details'][:50]:  # Limitar a 50 líneas
            icon = "✅" if status == "PASSED" else "❌" if status == "FAILED" else "⚠️" if status == "WARNING" else "ℹ️"
            color = (self.colors['success'] if status == "PASSED" 
                    else self.colors['error'] if status == "FAILED"
                    else self.colors['warning'] if status == "WARNING"
                    else self.colors['dark_gray'])
            
            # Truncar líneas muy largas
            detail = detail[:100] + "..." if len(detail) > 100 else detail
            log_data.append([icon, detail])
        
        if log_data:
            log_table = Table(log_data, colWidths=[0.3*inch, 5.5*inch])
            log_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(log_table)
        else:
            story.append(Paragraph("No hay registros detallados disponibles.", styles['Normal']))
        
        # Pie de página con información adicional
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=HexColor(self.colors['dark_gray']),
            alignment=1
        )
        story.append(Paragraph("Generado automáticamente por el Sistema de Pruebas de Integración", footer_style))
        
        # Construir PDF
        doc.build(story)
        print(f"✅ Reporte PDF mejorado generado: {filename}")

    def generate_report(self):
        """
        Función principal para ejecutar pruebas y generar el reporte completo.
        """
        print("🚀 Iniciando ejecución de pruebas de integración...")
        results, detailed_output = self.run_tests_and_get_results()
        
        print("📊 Generando gráficos...")
        chart_filename = self.generate_modern_chart(results)
        
        print("📄 Generando reporte PDF...")
        self.generate_enhanced_pdf_report(results, chart_filename, detailed_output)
        
        # Limpiar archivos temporales
        if os.path.exists(chart_filename):
            os.remove(chart_filename)
        
        print("✨ ¡Reporte completado exitosamente!")
        print(f"📈 Resumen: {results['passed']} aprobadas, {results['failed']} fallidas")
        print(f"🎯 Tasa de éxito: {results['success_rate']:.1f}%")

def main():
    """
    Función principal mejorada.
    """
    generator = TestReportGenerator()
    generator.generate_report()

if __name__ == "__main__":
    main()