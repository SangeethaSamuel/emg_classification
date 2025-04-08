import os
from PIL import Image
from torchvision import transforms
from tqdm import tqdm

# Paths
input_dir_healthy = r"C:\Users\USER\Desktop\A_final_data\CWT\hea_plots"
input_dir_unhealthy = r"C:\Users\USER\Desktop\A_final_data\CWT\myo_plots"

aug_output_healthy = input_dir_healthy + "_aug"
aug_output_unhealthy = input_dir_unhealthy + "_aug"

os.makedirs(aug_output_healthy, exist_ok=True)
os.makedirs(aug_output_unhealthy, exist_ok=True)

# Define augmentations (safe for scalograms)
augment = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomRotation(15),
    transforms.RandomResizedCrop(224, scale=(0.9, 1.0)),
    transforms.ColorJitter(brightness=0.1, contrast=0.1),
    transforms.GaussianBlur(kernel_size=3),
])

# Number of augmentations per image
n_augment = 5

def augment_images(input_dir, output_dir, label_prefix):
    files = [f for f in os.listdir(input_dir) if f.endswith('.png')]
    
    for img_file in tqdm(files, desc=f"Augmenting {label_prefix}"):
        img_path = os.path.join(input_dir, img_file)
        image = Image.open(img_path).convert('RGB')
        
        for i in range(n_augment):
            aug_img = augment(image)
            aug_img.save(os.path.join(output_dir, f"{label_prefix}_{img_file[:-4]}_aug{i+1}.png"))

# Apply augmentation
augment_images(input_dir_healthy, aug_output_healthy, "H")
augment_images(input_dir_unhealthy, aug_output_unhealthy, "M")

print("Augmentation complete.")
