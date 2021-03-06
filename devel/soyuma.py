import matplotlib.pyplot as plt
import imcut.pycut as pspc
import torch


import numpy as np

pth = r"C:\Users\Jirik\Downloads\mSeq/mSeq.pt"
nslices=10


segparams = {
        'method': 'graphcut',
        "pairwise_alpha": 20,
        # 'use_boundary_penalties': False,
        # 'boundary_dilatation_distance': 2,
        # 'boundary_penalties_weight': 1,
        'modelparams': {
                'cvtype': 'full',
                "params": {"covariance_type": "full", "n_components": 1},
                "return_only_object_with_seeds": True,
        },
        "return_only_object_with_seeds": True,
}

X = torch.load(pth )
X = X.numpy()  ### returns a 3D numpy array


data = X
data = data.astype(np.int16)
# data = (data / 10) # .astype(np.uint8)
print(data.shape)
print(f"{data.min()} {data.max()}")

seeds = np.zeros(data.shape)
seeds[30:35, 230:290, 4:7] = 2
seeds[150:160, 150:160, 4:7] = 2
seeds[230:235, 230:290, 4:7] = 2
# seeds[245:250:, 255:280, 4:7] = 2
seeds[155:165:, 185:195, 4:5] = 1

plt.imshow(data[:,:,4])
plt.contour(seeds[:,:,4])
plt.show()

# Simple volumetric 3D viewer and seed editor
# ===========
# conda install -c mjirik -c conda-forge sed3
# import sed3
# windowW(width) and windowC(center) are used in medical imaging to define minimal and maximal displayed intensity value
# ed = sed3.sed3(data, seeds=seeds, windowC=6000, windowW=6000, zaxis=2)
# ed.show()


igc = pspc.ImageGraphCut(data[:,:,:nslices], voxelsize=[1,1,1], segparams=segparams)
igc.set_seeds(seeds[:,:,:nslices])
igc.run()
print("Calculated!")

colormap = plt.cm.get_cmap('brg')
colormap._init()
colormap._lut[:1:,3]=0

plt.imshow(data[:, :, 4], cmap='gray')
plt.contour(igc.segmentation[:, :,4], levels=[0.5])
plt.imshow(igc.seeds[:, :, 4], cmap=colormap, interpolation='none')
plt.show()

# ed = sed3.sed3(data[:,:,:nslices], contour=igc.segmentation, seeds=seeds[:,:,:nslices], windowC=6000, windowW=6000, zaxis=2)
# ed.show()
