#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick PDF Generator Script for Upanishads Collection
รันสคริปต์นี้เพื่อสร้าง PDF ใหม่อย่างรวดเร็ว
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and print status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} - สำเร็จ")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ผิดพลาด: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("📚 Upanishads Collection PDF Generator")
    print("=" * 60)
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check if required files exist
    required_files = [
        'src/create_upanishads_data.py',
        'src/generate_pdf.py',
        'requirements.txt'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file not found: {file}")
            return False
    
    # Install dependencies if needed
    print("\n1. ตรวจสอบและติดตั้ง dependencies...")
    if not run_command("pip install -r requirements.txt", "ติดตั้ง Python packages"):
        return False
    
    # Generate data
    print("\n2. สร้างข้อมูลอุปนิษัท...")
    if not run_command("python src/create_upanishads_data.py", "สร้างข้อมูลอุปนิษัท"):
        return False
    
    # Generate PDF
    print("\n3. สร้างไฟล์ PDF...")
    if not run_command("python src/generate_pdf.py", "สร้างไฟล์ PDF"):
        return False
    
    # Check output
    output_file = "output/upanishads_collection_200_thai.pdf"
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"\n✅ PDF สร้างเสร็จแล้ว!")
        print(f"📄 ไฟล์: {output_file}")
        print(f"📊 ขนาด: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        # Try to open the file (on some systems)
        print(f"🔍 ตำแหน่งไฟล์เต็ม: {os.path.abspath(output_file)}")
        
        return True
    else:
        print(f"\n❌ ไม่พบไฟล์ PDF: {output_file}")
        return False

if __name__ == "__main__":
    success = main()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 สำเร็จ! Upanishads Collection PDF ถูกสร้างแล้ว")
        print("📖 เปิดไฟล์ PDF เพื่อดูเนื้อหา")
    else:
        print("💥 เกิดข้อผิดพลาด! กรุณาตรวจสอบข้อความ error ข้างต้น")
        sys.exit(1)
    print("=" * 60)