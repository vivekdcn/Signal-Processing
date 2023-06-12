pip install nibabel nilearn

import nibabel as nib
from nilearn import datasets

# Load MNI coordinates
mni_coords = [x, y, z]

# Load brain atlas
atlas = datasets.fetch_atlas_aal()
atlas_img = nib.load(atlas.maps)
atlas_data = atlas_img.get_fdata()

from nilearn import image

# Create a transformation matrix
mni_to_vox = image.coord_transform(x, y, z,
                                   atlas_img.affine,
                                   inverse=True)

# Apply the transformation to MNI coordinates
voxel_coords = image.apply_affine(mni_to_vox, mni_coords)

region_indices = atlas_data[int(voxel_coords[0]),
                            int(voxel_coords[1]),
                            int(voxel_coords[2])]

# Get the corresponding label(s) from the atlas
region_labels = [atlas.labels[int(index) - 1]
                 for index in np.unique(region_indices)
                 if index != 0]

print("Brain region(s) at MNI coordinates {}: ".format(mni_coords))
for label in region_labels:
    print(label)
    

###For Brodmann Atlas#####    
pip install nibabel nilearn
import nibabel as nib
from nilearn import datasets

# Load MNI coordinates
mni_coords = [x, y, z]

# Load Brodmann atlas
atlas = datasets.fetch_atlas_brodmann_1905()
atlas_img = nib.load(atlas['maps'])
atlas_data = atlas_img.get_fdata()

from nilearn import image

# Create a transformation matrix
mni_to_vox = image.coord_transform(x, y, z,
                                   atlas_img.affine,
                                   inverse=True)

# Apply the transformation to MNI coordinates
voxel_coords = image.apply_affine(mni_to_vox, mni_coords)

brodmann_areas = atlas_data[int(voxel_coords[0]),
                            int(voxel_coords[1]),
                            int(voxel_coords[2])]

# Get the unique Brodmann area(s)
unique_areas = set(brodmann_areas.flatten())

print("Brodmann area(s) at MNI coordinates {}: ".format(mni_coords))
for area in unique_areas:
    print(area)
