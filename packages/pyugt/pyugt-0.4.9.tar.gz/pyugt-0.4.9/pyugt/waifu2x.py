import json, sys, numpy as np
from scipy import signal
from PIL import Image
infile, outfile, modelpath = sys.argv[1:]
model = json.load(open(modelpath))
im = Image.open(infile).convert("YCbCr")
im = np.asarray(im.resize((2*im.size[0], 2*im.size[1]), resample=Image.NEAREST)).astype("float32")
planes = [np.pad(im[:,:,0], len(model), "edge") / 255.0]
for step in model:
    o_planes = [sum([signal.convolve2d(ip, np.float32(kernel), "valid")
            for ip, kernel in zip(planes, weights)]) + np.float32(bias)
        for bias, weights in zip(step["bias"], step["weight"])]
    planes = [np.maximum(p, 0) + 0.1 * np.minimum(p, 0) for p in o_planes]
im[:,:,0] = np.clip(planes[0], 0, 1) * 255
misc.toimage(im, mode="YCbCr").convert("RGB").save(outfile)