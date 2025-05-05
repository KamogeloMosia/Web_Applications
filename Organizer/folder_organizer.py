import os
import shutil
import sys
from datetime import datetime

# Define constants
SCRIPT_NAME = os.path.basename(__file__)

def organize_current_folder():
    """
    Simple and quick folder organizer that sorts files by extension type.
    """
    print("Starting quick folder organization...")
    
    try:
        # Get the folder where this script is located
        folder_path = os.path.dirname(os.path.abspath(__file__))
        if getattr(sys, 'frozen', False):
            # If running as compiled EXE, use the directory where the EXE is located
            folder_path = os.path.dirname(sys.executable)
            
        print(f"Organizing files in: {folder_path}")
        
        # Updated category mapping with proper folder names as requested
        categories = {
            'Media': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff', 
                     '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', 
                     '.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm'],
            'Code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.php', '.json', '.xml'],
            'Programs': ['.exe', '.msi', '.bat', '.cmd', '.sh', '.app', '.dll', '.com', '.vbs', '.appx', '.appimage'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx', 
                    '.csv'],
            'Other Files': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'Backups': [],  # New category for backup files
            'Unknown Folders': []  # Category for unknown folders
        }
        
        # Track processed files to prevent duplicate moves
        processed_files = set()
        
        # Get all files in the current directory (no recursion for speed)
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        files_count = 0
        
        # Process each file
        for filename in files:
            # Skip this script to avoid moving itself during execution
            if filename == SCRIPT_NAME:
                continue
                
            # Skip files in the category directories
            parent_dir = os.path.basename(os.path.dirname(os.path.join(folder_path, filename)))
            if parent_dir in categories:
                continue
                
            file_path = os.path.join(folder_path, filename)
            file_ext = os.path.splitext(filename)[1].lower()
            
            # Find the right category
            destination_category = 'Other Files'
            for category, extensions in categories.items():
                if file_ext in extensions:
                    destination_category = category
                    break
            
            # Create destination path
            dest_folder = os.path.join(folder_path, destination_category)
            
            # Create category folder if it doesn't exist (only when needed)
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
                
            dest_path = os.path.join(dest_folder, filename)
            
            # Handle filename conflicts
            if os.path.exists(dest_path):
                base_name, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dest_path):
                    new_name = f"{base_name}_{counter}{extension}"
                    dest_path = os.path.join(dest_folder, new_name)
                    counter += 1
            
            # Move the file
            try:
                shutil.move(file_path, dest_path)
                files_count += 1
            except Exception as e:
                print(f"Error moving {filename}: {str(e)}")
        
        print(f"Successfully organized {files_count} files.")
        
        # Delete unknown folders instead of moving them
        deleted_folders = 0
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path) and item not in categories:
                try:
                    # Delete the folder instead of moving it
                    shutil.rmtree(item_path)
                    print(f"Deleted unknown folder: {item}")
                    deleted_folders += 1
                except Exception as e:
                    print(f"Error deleting folder {item}: {str(e)}")
        
        print(f"Deleted {deleted_folders} unknown folders.")
        
        # After organizing other files, handle this script
        script_path = os.path.abspath(__file__)
        if getattr(sys, 'frozen', False):
            # If running as EXE, don't try to move the script
            pass
        else:
            # Only handle the script if we're not already in a Code folder
            parent_dir = os.path.basename(os.path.dirname(script_path))
            if parent_dir != 'Code':
                code_folder = os.path.join(folder_path, 'Code')
                script_dest_path = os.path.join(code_folder, SCRIPT_NAME)
                
                # Handle filename conflicts for the script
                if os.path.exists(script_dest_path):
                    base_name, extension = os.path.splitext(SCRIPT_NAME)
                    counter = 1
                    while os.path.exists(script_dest_path):
                        new_name = f"{base_name}_{counter}{extension}"
                        script_dest_path = os.path.join(code_folder, new_name)
                        counter += 1
                
                # Copy the script instead of moving it to avoid disruption
                shutil.copy2(script_path, script_dest_path)
                print(f"Script copied to: {script_dest_path}")
        
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == '__main__':
    print("Starting quick folder organizer...")
    success = organize_current_folder()
    if success:
        print("Organization complete!")
    else:
        print("Organization process encountered errors.")
    
    input("Press Enter to exit...")