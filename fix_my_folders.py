import os
import shutil

# 1. Dataset ka rasta
dataset_path = r'C:\thala final\Vitamin_dataset'
folders = ['train', 'test', 'val']

print("Starting Nuclear Cleanup...")

for folder in folders:
    main_dir = os.path.join(dataset_path, folder)
    if not os.path.exists(main_dir): continue

    # 2. Saara kachra (labels, cache) delete karein
    for junk in ['labels', 'labels.cache', 'images.cache', 'images']:
        path = os.path.join(main_dir, junk)
        if os.path.exists(path):
            if os.path.isdir(path):
                # Agar 'images' folder hai toh photos nikal kar bahar rakho
                if junk == 'images':
                    for f in os.listdir(path):
                        shutil.move(os.path.join(path, f), os.path.join(main_dir, f))
                shutil.rmtree(path)
            else:
                os.remove(path)

    # 3. Zaroori folders banayein (Normal aur Deficient)
    norm_p = os.path.join(main_dir, 'Normal')
    defi_p = os.path.join(main_dir, 'Deficient')
    os.makedirs(norm_p, exist_ok=True)
    os.makedirs(defi_p, exist_ok=True)

    # 4. Saari photos ko in do folders mein barabar baantein
    all_photos = [f for f in os.listdir(main_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if len(all_photos) > 0:
        half = len(all_photos) // 2
        for i, photo in enumerate(all_photos):
            src = os.path.join(main_dir, photo)
            dest = os.path.join(norm_p if i < half else defi_p, photo)
            shutil.move(src, dest)
        print(f"✅ {folder} folder perfectly organize ho gaya!")
    else:
        # Agar koi photos bahar nahi hain, toh check karein kya folders khali toh nahi
        if not os.listdir(norm_p) and not os.listdir(defi_p):
            print(f"⚠️ Warning: {folder} mein koi photos nahi mili!")

print("\nCleanup Complete! Ab aapka dataset AI ke liye taiyar hai.")