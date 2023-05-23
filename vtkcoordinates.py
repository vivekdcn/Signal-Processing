import vtk
import nibabel as nib
import numpy as np


# Load Nifti MRI file
filename = "sub-01_T1w.nii.gz"
nifti_img = nib.load(filename)
data = nifti_img.get_fdata()

# Define dimensions and spacing
dims = nifti_img.shape
spacing = nifti_img.header.get_zooms()

# Define VTK image data
vtk_data = vtk.vtkImageData()
vtk_data.SetDimensions(dims[1], dims[2], dims[0])
vtk_data.SetSpacing(spacing[1], spacing[2], spacing[0])
vtk_data.SetOrigin(0, 0, 0)

# Copy data into VTK image data
data_flat = np.flip(data, axis=2).flatten(order="F")
vtk_data.GetPointData().SetScalars(vtk.util.numpy_support.numpy_to_vtk(data_flat))

# Create VTK volume
volume_mapper = vtk.vtkSmartVolumeMapper()
volume_mapper.SetInputData(vtk_data)
volume_mapper.Update()

volume_property = vtk.vtkVolumeProperty()
#volume_property.SetColor(vtk_data.GetScalarRange())

# Set color transfer function
color_func = vtk.vtkColorTransferFunction()
color_func.AddRGBPoint(0, 0.0, 0.0, 0.0)
color_func.AddRGBPoint(255, 1.0, 1.0, 1.0)
volume_property.SetColor(color_func)

# Set opacity transfer function
opacity_func = vtk.vtkPiecewiseFunction()
opacity_func.AddPoint(0, 0.0)
opacity_func.AddPoint(255, 1.0)
volume_property.SetScalarOpacity(opacity_func)

volume_property.ShadeOn()
volume_property.SetInterpolationTypeToLinear()

volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Create renderer and add volume to it
renderer = vtk.vtkRenderer()
renderer.AddVolume(volume)

# Create window and add renderer to it
window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)

# Define interactor style
class MouseInteractorStyle(vtk.vtkInteractorStyleImage):
    def __init__(self):
        self.AddObserver("LeftButtonPressEvent", self.left_button_press_event)

    def left_button_press_event(self, obj, event):
        click_pos = self.GetInteractor().GetEventPosition()
        picker = vtk.vtkPropPicker()
        picker.Pick(click_pos[0], click_pos[1], 0, renderer)
        world_pos = picker.GetPickPosition()
        voxel_pos = np.array(world_pos) / spacing
        voxel_pos = np.flip(voxel_pos.astype(int), axis=0)
        print(f"Clicked voxel: {voxel_pos}")

# Set interactor style and start the window
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(MouseInteractorStyle())
window.SetInteractor(interactor)
window.Render()
interactor.Start()

