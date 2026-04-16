"""
Certificate Generation Module
Generates certificates using ReportLab
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from datetime import datetime
import os
from pathlib import Path


class CertificateGenerator:
    """Generates PDF certificates for event participation"""
    
    def __init__(self, output_dir='certificates'):
        """Initialize certificate generator"""
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    def generate_certificate(self, student_name, event_name, event_date, 
                            certificate_number, organizer_name='Campus Administration'):
        """
        Generate a professional certificate
        
        Args:
            student_name: Name of the student
            event_name: Name of the event
            event_date: Date of the event
            certificate_number: Unique certificate number
            organizer_name: Name of the event organizer
        
        Returns:
            Path to generated PDF file
        """
        try:
            # Create filename
            safe_name = student_name.replace(' ', '_').lower()
            filename = f"certificate_{certificate_number}_{safe_name}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # Page setup
            page_width = 11 * inch
            page_height = 8.5 * inch
            
            # Create PDF
            c = canvas.Canvas(filepath, pagesize=(page_width, page_height))
            
            # Set background color (light cream)
            c.setFillColor(colors.HexColor('#fffef0'))
            c.rect(0, 0, page_width, page_height, fill=1, stroke=0)
            
            # Border
            c.setLineWidth(3)
            c.setStrokeColor(colors.HexColor('#2c3e50'))
            c.rect(0.3 * inch, 0.3 * inch, page_width - 0.6 * inch, page_height - 0.6 * inch)
            
            # Inner border
            c.setLineWidth(1)
            c.setStrokeColor(colors.HexColor('#34495e'))
            c.rect(0.5 * inch, 0.5 * inch, page_width - 1 * inch, page_height - 1 * inch)
            
            # Title
            c.setFont("Helvetica-Bold", 48)
            c.setFillColor(colors.HexColor('#2c3e50'))
            c.drawCentredString(page_width / 2, page_height - 1.2 * inch, "CERTIFICATE")
            
            # Subtitle
            c.setFont("Helvetica-Bold", 24)
            c.setFillColor(colors.HexColor('#34495e'))
            c.drawCentredString(page_width / 2, page_height - 1.8 * inch, "OF PARTICIPATION")
            
            # Decorative line
            c.setLineWidth(2)
            c.setStrokeColor(colors.HexColor('#e74c3c'))
            c.line(2 * inch, page_height - 2.1 * inch, page_width - 2 * inch, page_height - 2.1 * inch)
            
            # Body text
            c.setFont("Helvetica", 14)
            c.setFillColor(colors.HexColor('#2c3e50'))
            c.drawCentredString(page_width / 2, page_height - 2.7 * inch, "This is to certify that")
            
            # Student name
            c.setFont("Helvetica-Bold", 32)
            c.setFillColor(colors.HexColor('#e74c3c'))
            c.drawCentredString(page_width / 2, page_height - 3.3 * inch, student_name)
            
            # Achievement text
            c.setFont("Helvetica", 14)
            c.setFillColor(colors.HexColor('#2c3e50'))
            c.drawCentredString(page_width / 2, page_height - 3.9 * inch, 
                               "has successfully participated in")
            
            # Event name
            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(colors.HexColor('#27ae60'))
            c.drawCentredString(page_width / 2, page_height - 4.4 * inch, event_name)
            
            # Event date
            c.setFont("Helvetica", 12)
            c.setFillColor(colors.HexColor('#34495e'))
            date_str = datetime.strptime(str(event_date), '%Y-%m-%d').strftime('%B %d, %Y')
            c.drawCentredString(page_width / 2, page_height - 4.9 * inch, f"On {date_str}")
            
            # Certificate number
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor('#7f8c8d'))
            c.drawCentredString(page_width / 2, page_height - 5.4 * inch, 
                               f"Certificate No. {certificate_number}")
            
            # Signature lines
            sig_y = page_height - 6.5 * inch
            
            # Left signature
            c.setLineWidth(1)
            c.setStrokeColor(colors.HexColor('#34495e'))
            c.line(1.5 * inch, sig_y, 3.5 * inch, sig_y)
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor('#2c3e50'))
            c.drawCentredString(2.5 * inch, sig_y - 0.3 * inch, "Organizer")
            
            # Right signature
            c.line(7.5 * inch, sig_y, 9.5 * inch, sig_y)
            c.drawCentredString(8.5 * inch, sig_y - 0.3 * inch, "Director")
            
            # Issue date and seal area
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor('#34495e'))
            c.drawString(1 * inch, 1 * inch, f"Date: {datetime.now().strftime('%B %d, %Y')}")
            
            # Watermark
            c.setFillColor(colors.HexColor('#ecf0f1')) # Light grey for watermark
            c.setFont("Helvetica", 60)
            c.saveState()
            c.rotate(45)
            c.drawString(2 * inch, 3 * inch, "OFFICIAL")
            c.restoreState()
            
            c.save()
            
            return filepath
        
        except Exception as e:
            print(f"Error generating certificate: {e}")
            return None
    
    def generate_certificate_batch(self, certificates_data):
        """
        Generate multiple certificates
        
        Args:
            certificates_data: List of dicts with keys:
                - student_name
                - event_name
                - event_date
                - certificate_number
        
        Returns:
            List of generated file paths
        """
        results = []
        
        for cert_data in certificates_data:
            filepath = self.generate_certificate(
                student_name=cert_data.get('student_name'),
                event_name=cert_data.get('event_name'),
                event_date=cert_data.get('event_date'),
                certificate_number=cert_data.get('certificate_number')
            )
            
            if filepath:
                results.append(filepath)
        
        return results
    
    def verify_certificate_file(self, file_path):
        """Verify if certificate file exists and is readable"""
        try:
            return os.path.exists(file_path) and os.path.isfile(file_path)
        except Exception as e:
            print(f"Error verifying certificate: {e}")
            return False


def get_certificate_generator(output_dir='certificates'):
    """Factory function to get CertificateGenerator instance"""
    return CertificateGenerator(output_dir)
