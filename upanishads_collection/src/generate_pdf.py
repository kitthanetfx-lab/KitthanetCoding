#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upanishads PDF Generator
Creates a comprehensive PDF document of 200+ Upanishads with Thai translations
"""

import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

class UpanishadsPDFGenerator:
    def __init__(self, data_file, output_file):
        self.data_file = data_file
        self.output_file = output_file
        self.doc = None
        self.styles = None
        self.story = []
        
    def setup_fonts_and_styles(self):
        """Setup fonts and paragraph styles for the document"""
        # Create custom paragraph styles
        self.styles = getSampleStyleSheet()
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkgreen,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            alignment=TA_LEFT,
            textColor=colors.darkred,
            fontName='Helvetica-Bold'
        ))
        
        # Upanishad entry style
        self.styles.add(ParagraphStyle(
            name='UpanishadEntry',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            spaceBefore=4,
            alignment=TA_LEFT,
            fontName='Helvetica'
        ))
        
        # Sanskrit name style
        self.styles.add(ParagraphStyle(
            name='SanskritName',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=2,
            alignment=TA_LEFT,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        ))
        
        # Thai translation style
        self.styles.add(ParagraphStyle(
            name='ThaiTranslation',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            alignment=TA_LEFT,
            textColor=colors.darkgreen,
            fontName='Helvetica'
        ))
        
        # Category style
        self.styles.add(ParagraphStyle(
            name='CategoryStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=2,
            alignment=TA_LEFT,
            textColor=colors.grey,
            fontName='Helvetica-Oblique'
        ))
        
        # Table of contents style
        self.styles.add(ParagraphStyle(
            name='TOCEntry',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            alignment=TA_LEFT,
            fontName='Helvetica'
        ))

    def load_data(self):
        """Load Upanishads data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Data file {self.data_file} not found")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.data_file}")
            return []

    def create_title_page(self):
        """Create the title page"""
        self.story.append(Spacer(1, 2*inch))
        
        # Main title
        title = Paragraph("รายชื่ออุปนิษัท (Upanishads) ทั้งหมด 200+ บท", self.styles['CustomTitle'])
        self.story.append(title)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle = Paragraph("พร้อมคำแปลหัวข้อไทย", self.styles['CustomSubtitle'])
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Description
        description = Paragraph(
            "อุปนิษัทเป็นคัมภีร์ทางปรัชญาของศาสนาฮินดู ที่มีความสำคัญอย่างยิ่งในการศึกษาปรัชญาเวทานตะ "
            "และการแสวงหาความจริงแท้ของจักรวาลและตัวตน เอกสารฉบับนี้รวบรวมรายชื่ออุปนิษัท "
            "มากกว่า 200 บท พร้อมคำแปลชื่อเป็นภาษาไทยและคำอธิบายสั้นๆ",
            self.styles['Normal']
        )
        self.story.append(description)
        self.story.append(Spacer(1, 1*inch))
        
        # Date and compilation info
        compilation_info = Paragraph(
            f"รวบรวมและจัดทำโดย: KitthanetCoding<br/>"
            f"วันที่จัดทำ: {datetime.now().strftime('%d/%m/%Y')}<br/>"
            f"จำนวนอุปนิษัท: 200 บท",
            self.styles['Normal']
        )
        self.story.append(compilation_info)
        self.story.append(PageBreak())

    def create_table_of_contents(self, data):
        """Create table of contents grouped by category"""
        self.story.append(Paragraph("สารบัญ (Table of Contents)", self.styles['CustomSubtitle']))
        self.story.append(Spacer(1, 0.3*inch))
        
        # Group data by category
        categories = {}
        for item in data:
            cat = item.get('category', 'Unknown')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
        
        # Create TOC entries
        for category in sorted(categories.keys()):
            count = len(categories[category])
            toc_entry = Paragraph(
                f"<b>{category}</b> ({count} บท)",
                self.styles['SectionHeader']
            )
            self.story.append(toc_entry)
            self.story.append(Spacer(1, 0.1*inch))
        
        # Statistics
        self.story.append(Spacer(1, 0.3*inch))
        stats = Paragraph("สถิติการจัดหมวดหมู่", self.styles['SectionHeader'])
        self.story.append(stats)
        
        # Create statistics table
        stats_data = [['หมวดหมู่', 'จำนวน', 'เปอร์เซ็นต์']]
        total = len(data)
        
        for category in sorted(categories.keys()):
            count = len(categories[category])
            percentage = (count / total * 100) if total > 0 else 0
            stats_data.append([category, str(count), f"{percentage:.1f}%"])
        
        stats_table = Table(stats_data, colWidths=[3*inch, 1*inch, 1*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(stats_table)
        self.story.append(PageBreak())

    def create_upanishads_content(self, data):
        """Create the main content with all Upanishads"""
        # Group data by category
        categories = {}
        for item in data:
            cat = item.get('category', 'Unknown')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
        
        # Create content for each category
        for category in sorted(categories.keys()):
            # Category header
            category_header = Paragraph(
                f"หมวด: {category}",
                self.styles['CustomSubtitle']
            )
            self.story.append(category_header)
            self.story.append(Spacer(1, 0.2*inch))
            
            # Sort items within category by ID
            sorted_items = sorted(categories[category], key=lambda x: x.get('id', 0))
            
            # Create entries for this category
            for item in sorted_items:
                self.create_upanishad_entry(item)
            
            self.story.append(PageBreak())

    def create_upanishad_entry(self, item):
        """Create an individual Upanishad entry"""
        # Entry number and Sanskrit name
        sanskrit_name = item.get('sanskrit_name', 'Unknown')
        thai_name = item.get('thai_name', 'ไม่ทราบ')
        thai_translation = item.get('thai_translation', 'ไม่มีคำแปล')
        category = item.get('category', 'Unknown')
        veda = item.get('veda', 'Unknown')
        entry_id = item.get('id', 0)
        
        # Main entry with ID and Sanskrit name
        main_entry = Paragraph(
            f"<b>{entry_id}. {sanskrit_name}</b>",
            self.styles['SanskritName']
        )
        self.story.append(main_entry)
        
        # Thai name
        thai_entry = Paragraph(
            f"ชื่อไทย: {thai_name}",
            self.styles['ThaiTranslation']
        )
        self.story.append(thai_entry)
        
        # Thai translation/meaning
        translation_entry = Paragraph(
            f"ความหมาย: {thai_translation}",
            self.styles['ThaiTranslation']
        )
        self.story.append(translation_entry)
        
        # Category and Veda information
        meta_info = Paragraph(
            f"หมวดหมู่: {category} | เวท: {veda}",
            self.styles['CategoryStyle']
        )
        self.story.append(meta_info)
        
        # Add some space between entries
        self.story.append(Spacer(1, 0.15*inch))

    def create_appendix(self, data):
        """Create appendix with additional information"""
        self.story.append(Paragraph("ภาคผนวก (Appendix)", self.styles['CustomSubtitle']))
        self.story.append(Spacer(1, 0.3*inch))
        
        # About Upanishads
        about_section = Paragraph("เกี่ยวกับอุปนิษัท", self.styles['SectionHeader'])
        self.story.append(about_section)
        
        about_text = Paragraph(
            "อุปนิษัท (Upanishads) เป็นคัมภีร์ทางศาสนาและปรัชญาที่สำคัญของศาสนาฮินดู "
            "ซึ่งเป็นส่วนหนึ่งของเวท (Vedas) โดยจัดเป็นส่วนสุดท้ายของเวทแต่ละเล่ม "
            "จึงเรียกว่า 'เวทานตะ' (Vedanta) ซึ่งแปลว่า 'จุดจบของเวท' หรือ 'ปรัชญาเวท'<br/><br/>"
            
            "คำว่า 'อุปนิษัท' มาจากรากศัพท์สันสกฤต 'อุป' (ใกล้) + 'นิ' (ลง) + 'สัท' (นั่ง) "
            "ซึ่งหมายถึงการนั่งใกล้อาจารย์เพื่อรับฟังคำสอนลึกลับ<br/><br/>"
            
            "อุปนิษัทมีเนื้อหาหลักเกี่ยวกับ:<br/>"
            "• ธรรมชาติของ 'อัตมัน' (Atman) หรือจิตวิญญาณแท้จริง<br/>"
            "• ธรรมชาติของ 'พรหมัน' (Brahman) หรือสัจธรรมสูงสุด<br/>"
            "• ความสัมพันธ์ระหว่างอัตมันและพรหมัน<br/>"
            "• วิถีทางสู่การหลุดพ้น (โมกษะ)<br/>"
            "• ปรัชญาเกี่ยวกับจักรวาลและความเป็นจริง",
            self.styles['Normal']
        )
        self.story.append(about_text)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Classification section
        classification_section = Paragraph("การจำแนกประเภทอุปนิษัท", self.styles['SectionHeader'])
        self.story.append(classification_section)
        
        classification_text = Paragraph(
            "อุปนิษัทสามารถจำแนกได้หลายวิธี:<br/><br/>"
            
            "<b>1. ตามความสำคัญ:</b><br/>"
            "• อุปนิษัทหลัก (Principal/Mukhya) - 10-13 บท ที่มีความสำคัญสูงสุด<br/>"
            "• อุปนิษัทรอง (Minor) - อุปนิษัทอื่นๆ ที่มีจำนวนมาก<br/><br/>"
            
            "<b>2. ตามเนื้อหา:</b><br/>"
            "• Samanya (ทั่วไป) - เนื้อหาปรัชญาทั่วไป<br/>"
            "• Sannyasa - เกี่ยวกับการบวช<br/>"
            "• Yoga - เกี่ยวกับการฝึกโยคะ<br/>"
            "• Shaiva - เกี่ยวกับพระศิวะ<br/>"
            "• Vaishnava - เกี่ยวกับพระวิษณุ<br/>"
            "• Shakti - เกี่ยวกับเทวี<br/><br/>"
            
            "<b>3. ตามเวท:</b><br/>"
            "• Rig Veda Upanishads<br/>"
            "• Sama Veda Upanishads<br/>"
            "• Krishna Yajur Veda Upanishads<br/>"
            "• Shukla Yajur Veda Upanishads<br/>"
            "• Atharva Veda Upanishads",
            self.styles['Normal']
        )
        self.story.append(classification_text)

    def generate_pdf(self):
        """Generate the complete PDF document"""
        print("Loading Upanishads data...")
        data = self.load_data()
        
        if not data:
            print("Error: No data loaded. Cannot generate PDF.")
            return False
        
        print(f"Loaded {len(data)} Upanishads entries.")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Setup document
        self.doc = SimpleDocTemplate(
            self.output_file,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Setup fonts and styles
        self.setup_fonts_and_styles()
        
        print("Creating PDF content...")
        
        # Build document content
        self.story = []
        
        # Title page
        print("- Creating title page...")
        self.create_title_page()
        
        # Table of contents
        print("- Creating table of contents...")
        self.create_table_of_contents(data)
        
        # Main content
        print("- Creating main content...")
        self.create_upanishads_content(data)
        
        # Appendix
        print("- Creating appendix...")
        self.create_appendix(data)
        
        # Build PDF
        print("Building PDF document...")
        try:
            self.doc.build(self.story)
            print(f"PDF successfully generated: {self.output_file}")
            
            # Print file size
            file_size = os.path.getsize(self.output_file)
            print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
            
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return False

def main():
    """Main function to generate the Upanishads PDF"""
    # File paths
    data_file = '/home/runner/work/KitthanetCoding/KitthanetCoding/upanishads_collection/data/upanishads_complete.json'
    output_file = '/home/runner/work/KitthanetCoding/KitthanetCoding/upanishads_collection/output/upanishads_collection_200_thai.pdf'
    
    # Create PDF generator
    generator = UpanishadsPDFGenerator(data_file, output_file)
    
    # Generate PDF
    success = generator.generate_pdf()
    
    if success:
        print("\n" + "="*60)
        print("📚 Upanishads Collection PDF Generated Successfully! 📚")
        print("="*60)
        print(f"📄 File: {output_file}")
        print(f"📊 Contains: 200+ Upanishads with Thai translations")
        print(f"🎯 Features: Categorized, searchable, and professionally formatted")
        print("="*60)
        return True
    else:
        print("\n❌ Failed to generate PDF. Please check the error messages above.")
        return False

if __name__ == "__main__":
    main()