import os
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
def generate_forensic_report(case_info, image_info, file_system_info, timeline, notable_files, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    if 'Heading2' not in styles:
        styles.add(ParagraphStyle(name='Heading2', fontSize=14, spaceBefore=12, spaceAfter=6))
    heading2_style = styles['Heading2']
    elements = []
    elements.append(Paragraph("FORENSIC REPORT GENERATOR ", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("KIRANRAJ, HAARIESHRAJ,BHUVANESH", styles['Title']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Case Information", heading2_style))
    case_data = [
        ['Case Number:', case_info['case_number']],
        ['Investigator:', case_info['investigator']],
        ['Date:', case_info['date']],
        ['Description:', case_info['description']]
    ]
    elements.append(Table(case_data, colWidths=[2*inch, 4*inch], style=[('GRID', (0,0), (-1,-1), 1, colors.black)]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Image Information", heading2_style))
    image_data = [
        ['Image Type:', image_info['image_type']],
        ['Image Hash:', image_info['image_hash']],
        ['Acquisition Date:', image_info['acquisition_date']],
        ['Device Model:', image_info['device_model']],
        ['Total Capacity:', image_info['total_capacity']]
    ]
    elements.append(Table(image_data, colWidths=[2*inch, 4*inch], style=[('GRID', (0,0), (-1,-1), 1, colors.black)]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("File System Information", heading2_style))
    fs_data = [
        ['File System Type:', file_system_info['fs_type']],
        ['Volume Label:', file_system_info['volume_label']],
        ['Created Date:', file_system_info['created_date']],
        ['Last Mounted:', file_system_info['last_mounted']]
    ]
    elements.append(Table(fs_data, colWidths=[2*inch, 4*inch], style=[('GRID', (0,0), (-1,-1), 1, colors.black)]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Timeline of Key Events", heading2_style))
    timeline_data = [['Date/Time', 'Event']] + timeline
    elements.append(Table(timeline_data, colWidths=[2*inch, 4*inch], style=[
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Notable Files", heading2_style))
    files_data = [['Filename', 'Path', 'Size', 'Last Modified']] + notable_files
    elements.append(Table(files_data, colWidths=[1.5*inch, 2.5*inch, 1*inch, 1.5*inch], style=[
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ]))
    doc.build(elements)
    print(f"Report generated: {output_file}")
def main():
    parser = argparse.ArgumentParser(description="Forensic Report Generator")
    parser.add_argument('--case-number', required=True, help='Case number')
    parser.add_argument('--investigator', required=True, help='Investigator name')
    parser.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'), help='Investigation date (YYYY-MM-DD)')
    parser.add_argument('--description', required=True, help='Case description')
    parser.add_argument('--image-type', default='E01', help='Image file type')
    parser.add_argument('--image-hash', required=True, help='Image file hash')
    parser.add_argument('--acquisition-date', required=True, help='Image acquisition date')
    parser.add_argument('--device-model', required=True, help='Device model')
    parser.add_argument('--capacity', required=True, help='Total device capacity')
    parser.add_argument('--fs-type', required=True, help='File system type')
    parser.add_argument('--volume-label', required=True, help='Volume label')
    parser.add_argument('--fs-created', required=True, help='File system created date')
    parser.add_argument('--last-mounted', required=True, help='Last mounted date')
    parser.add_argument('--timeline', nargs='+', required=True, help='Timeline events in format: "YYYY-MM-DD HH:MM,Event description"')
    parser.add_argument('--notable-files', nargs='+', required=True, help='Notable files in format: "filename,path,size,last_modified"')
    parser.add_argument('--output', default='forensic_report.pdf', help='Output PDF file name')
    args = parser.parse_args()
    case_info = {
        'case_number': args.case_number,
        'investigator': args.investigator,
        'date': args.date,
        'description': args.description
    }
    image_info = {
        'image_type': args.image_type,
        'image_hash': args.image_hash,
        'acquisition_date': args.acquisition_date,
        'device_model': args.device_model,
        'total_capacity': args.capacity
    }
    file_system_info = {
        'fs_type': args.fs_type,
        'volume_label': args.volume_label,
        'created_date': args.fs_created,
        'last_mounted': args.last_mounted
    }
    timeline = [event.split(',', 1) for event in args.timeline]
    notable_files = [file.split(',') for file in args.notable_files]
    generate_forensic_report(case_info, image_info, file_system_info, timeline, notable_files, args.output)
    if os.path.exists(args.output):
        os.startfile(args.output) 
    else:
        print(f"Failed to generate the report: {args.output}")
if __name__ == "__main__":
    main()