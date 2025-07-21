# -*- coding: utf-8 -*-
import os
import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
import test_extended_functionality

class ExtendedTestReportGenerator:
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

    def get_module_from_line(self, line):
        lower_line = line.lower()
        if "perfil" in lower_line:
            return "Perfil"
        elif "reportes" in lower_line or "crud" in lower_line:
            return "Reportes"
        elif "notificaci" in lower_line:
            return "Notificaciones"
        else:
            return "General"

    def run_tests_and_get_results(self):
        """
        Ejecuta las pruebas de funcionalidad extendida y retorna un resumen de los resultados.
        """
        from io import StringIO
        import sys

        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            test_extended_functionality.main()
        except Exception as e:
            print(f"[FATAL] Error ejecutando las pruebas extendidas: {e}")

        sys.stdout = old_stdout
        output = captured_output.getvalue()

        results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "details": [],
            "execution_time": datetime.datetime.now()
        }

        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue
            module = self.get_module_from_line(line)
            if "[SUCCESS]" in line:
                results["passed"] += 1
                results["details"].append(("PASSED", line, module))
            elif "[FAILURE]" in line or "[ERROR]" in line or "[FATAL]" in line:
                results["failed"] += 1
                results["details"].append(("FAILED", line, module))
            else:
                results["details"].append(("INFO", line, module))

        results["total_tests"] = results["passed"] + results["failed"]
        results["success_rate"] = (results["passed"] / results["total_tests"] * 100) if results["total_tests"] > 0 else 0

        return results, output

    def generate_chart(self, results, filename="extended_test_results.png"):
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(8, 5))

        categories = ['Aprobadas', 'Fallidas']
        values = [results['passed'], results['failed']]
        colors_bar = [self.colors['success'], self.colors['error']]

        bars = ax.bar(categories, values, color=colors_bar, alpha=0.8, edgecolor='white', linewidth=2)

        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 0.1, f'{int(value)}', ha='center', va='bottom', fontweight='bold')

        ax.set_title('Resumen de Pruebas de Funcionalidad Extendida', fontsize=16, fontweight='bold', color=self.colors['primary'])
        ax.set_ylabel('Cantidad de Casos de Prueba', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, max(values) * 1.2 if values else 1)

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        return filename

    def generate_pdf_report(self, results, chart_filename, filename="Test_Report_Extended_Functionality.pdf"):
        doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=22, spaceAfter=25,
                                     textColor=HexColor(self.colors['primary']), alignment=1)
        story.append(Paragraph("Reporte de Pruebas de Funcionalidad Extendida", title_style))

        # Logo y cabecera
        try:
            logo_path = "unal.png"
            if os.path.exists(logo_path):
                logo_img = Image(logo_path, width=80, height=80)
                header_table = Table([[logo_img, f"Generado el: {results['execution_time'].strftime('%d/%m/%Y %H:%M:%S')}"]],
                                     colWidths=[1.2 * inch, 4.5 * inch])
                story.append(header_table)
                story.append(Spacer(1, 30))
        except Exception as e:
            print(f"[WARNING] No se pudo cargar el logo: {e}")

        # Tabla de resumen
        info_data = [
            ['Total de Casos de Prueba:', str(results['total_tests'])],
            ['Casos Aprobados:', str(results['passed'])],
            ['Casos Fallidos:', str(results['failed'])],
            ['Tasa de Éxito:', f"{results['success_rate']:.1f}%"]
        ]
        info_table = Table(info_data, colWidths=[2 * inch, 2 * inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (0, -1), HexColor(self.colors['primary'])),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))

        # Gráfico
        story.append(Paragraph("Visualización de Resultados", styles['h2']))
        story.append(Image(chart_filename, width=6 * inch, height=3.75 * inch))
        story.append(Spacer(1, 20))

        # Log detallado
        story.append(Paragraph("Registro de Ejecución Detallado", styles['h2']))
        log_data = [['Estado', 'Módulo', 'Descripción']]
        for status, detail, module in results['details']:
            icon = "✅" if status == "PASSED" else "❌" if status == "FAILED" else "ℹ️"
            log_data.append([icon, module, Paragraph(detail, styles['Normal'])])

        log_table = Table(log_data, colWidths=[0.5 * inch, 1.3 * inch, 4.2 * inch])
        log_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f2f2f2')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor(self.colors['primary'])),
        ]))
        story.append(log_table)

        doc.build(story)
        print(f"\n[SUCCESS] Reporte PDF generado: {filename}")

    def generate_report(self):
        print("--- Iniciando Generación de Reporte Extendido ---")
        results, _ = self.run_tests_and_get_results()

        if results["total_tests"] == 0:
            print("[ERROR] No se ejecutaron pruebas o no se detectaron resultados. Abortando reporte.")
            return

        print("\n--- Generando Gráfico ---")
        chart_filename = self.generate_chart(results)

        print("\n--- Generando Reporte PDF ---")
        self.generate_pdf_report(results, chart_filename)

        if os.path.exists(chart_filename):
            os.remove(chart_filename)

        print("\n--- Proceso de Reporte Finalizado ---")

if __name__ == "__main__":
    generator = ExtendedTestReportGenerator()
    generator.generate_report()
