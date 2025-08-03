#!/usr/bin/env python3
"""
Create monthly folders (Aug_25 through Dec_25) for all clients
"""

import os

def create_monthly_folders_all_clients():
    """Create monthly folders for all clients in the Clients directory"""
    
    # Base clients directory
    base_client_dir = r"Z:\Main Drive\360TFT Resources\Workflows\N8N\Content Factory Pro\Clients"
    
    # Monthly folders to create
    monthly_folders = ['Aug_25', 'Sep_25', 'Oct_25', 'Nov_25', 'Dec_25']
    
    if not os.path.exists(base_client_dir):
        print(f"[ERROR] Clients directory not found: {base_client_dir}")
        return
    
    # Get all client folders
    client_folders = []
    for item in os.listdir(base_client_dir):
        item_path = os.path.join(base_client_dir, item)
        if os.path.isdir(item_path):
            client_folders.append(item)
    
    print(f"[INFO] Found {len(client_folders)} client folders")
    print(f"[INFO] Creating monthly folders: {', '.join(monthly_folders)}")
    print()
    
    # Create monthly folders for each client
    for client_name in sorted(client_folders):
        client_path = os.path.join(base_client_dir, client_name)
        
        print(f"[PROCESSING] {client_name}")
        
        # Create each monthly folder
        created_folders = []
        for month in monthly_folders:
            month_path = os.path.join(client_path, month)
            
            if not os.path.exists(month_path):
                os.makedirs(month_path, exist_ok=True)
                created_folders.append(month)
            else:
                print(f"  - {month} (already exists)")
        
        if created_folders:
            print(f"  - Created: {', '.join(created_folders)}")
        else:
            print(f"  - All monthly folders already exist")
        
        print()
    
    print(f"[SUCCESS] Monthly folder structure created for all {len(client_folders)} clients")
    print(f"[STRUCTURE] Each client now has: {', '.join(monthly_folders)}")

def verify_folder_structure():
    """Verify all monthly folders were created successfully"""
    
    base_client_dir = r"Z:\Main Drive\360TFT Resources\Workflows\N8N\Content Factory Pro\Clients"
    monthly_folders = ['Aug_25', 'Sep_25', 'Oct_25', 'Nov_25', 'Dec_25']
    
    print("\n[VERIFICATION] Checking folder structure...")
    
    client_folders = []
    for item in os.listdir(base_client_dir):
        item_path = os.path.join(base_client_dir, item)
        if os.path.isdir(item_path):
            client_folders.append(item)
    
    all_good = True
    for client_name in sorted(client_folders):
        client_path = os.path.join(base_client_dir, client_name)
        missing_folders = []
        
        for month in monthly_folders:
            month_path = os.path.join(client_path, month)
            if not os.path.exists(month_path):
                missing_folders.append(month)
        
        if missing_folders:
            print(f"[WARNING] {client_name}: Missing {', '.join(missing_folders)}")
            all_good = False
        else:
            print(f"[OK] {client_name}: All monthly folders present")
    
    if all_good:
        print(f"\n[SUCCESS] All {len(client_folders)} clients have complete monthly folder structure!")
    else:
        print(f"\n[WARNING] Some clients have missing monthly folders")

if __name__ == "__main__":
    create_monthly_folders_all_clients()
    verify_folder_structure()