import kagglehub
import os
import shutil

# Download latest version
path = kagglehub.dataset_download("khushikyad001/smoking-and-other-risk-factors-dataset")
print("Path to dataset files:", path)

# Copy files to current directory for easier access
current_dir = os.getcwd()
for file in os.listdir(path):
    if file.endswith('.csv'):
        shutil.copy(os.path.join(path, file), current_dir)
        print(f"Copied {file} to {current_dir}")

print("Dataset downloaded and copied successfully!")
