import pickle
import numpy as np
import random
import argparse
import os
import skimage


def read_meta(data,
        path, 
        scale_factor_detector=1,
        scale_factor_voxel=1,
):
    key_to_name = {
        "PROJECTION":(int, "PROJECTION"),
        "MM_SOD": (float, "DSO"),
        "MM_SID": (float, "DSD"),
        "DET_NU": (int, "nDetector_X_orig"),
        "DET_NV": (int, "nDetector_Y_orig"),
        "DET_PU": (float, "dDetector_X_orig"),
        "DET_PV": (float, "dDetector_Y_orig"),
        "REC_NX": (int, "nVoxel_X_orig"),
        "REC_NY": (int, "nVoxel_Y_orig"),
        "REC_NZ": (int, "nVoxel_Z_orig"),
        "REC_PX": (float, "dVoxel_X_orig"),
        "REC_PY": (float, "dVoxel_Y_orig"),
        "REC_PZ": (float, "dVoxel_Z_orig"),
        "POST_LIMIT_HIGH": (int, "post_limit_high"),
        # Recon.mrni
        "TotalAngle": (float, "totalAngle"),
        "InitAngle": (float, "startAngle"),

    }

    with open(os.path.join(path, "Recon.prm")) as f:
        for line in f:
            for key, (typ, name) in key_to_name.items():
                if line.startswith(key) and line.split("=")[0].split()[0] == key:
                    data[name] = typ(line.split("=")[-1].split("#")[0])
    with open(os.path.join(path, "Recon.mnri"), encoding="cp932") as f:
        for line in f:
            line = line.replace("\0", "")
            for key, (typ, name) in key_to_name.items():
                if line.startswith(key):

                    data[name] = typ(line.split("=")[-1].split("#")[0])


    # rescale so that the data fits into the memory
    data["nDetector"] = [
        int(data["nDetector_X_orig"] * scale_factor_detector),
        int(data["nDetector_Y_orig"] * scale_factor_detector)
    ]
    data["dDetector"] = [
        data["dDetector_X_orig"] / scale_factor_detector,   
        data["dDetector_Y_orig"] / scale_factor_detector
    ]
    data["nVoxel"] = [
        int(data["nVoxel_X_orig"] * scale_factor_voxel),
        int(data["nVoxel_Y_orig"] * scale_factor_voxel),
        int(data["nVoxel_Z_orig"] * scale_factor_voxel)
    ]
    # data["dVoxel"] = [
    #     data["dVoxel_X_orig"] / scale_factor_voxel,
    #     data["dVoxel_Y_orig"] / scale_factor_voxel,
    #     data["dVoxel_Z_orig"] / scale_factor_voxel
    # ]


    # as we do not have the reconstruction data, we create a dummy one
    data["image"] = np.zeros(data["nVoxel"], dtype=np.float64)
    return data


def read_raw(indices, data, path):
    angles = []
    projections = []
    for index in indices:
        angle_degree = data["startAngle"] + data["totalAngle"] * index / data["PROJECTION"]
        angle = angle_degree * np.pi / 180.0  # convert to radians
        angles.append(angle)
        with open(os.path.join(path, f"{index:05d}.RAW"), "rb") as f:
            raw_data = np.fromfile(f, dtype=np.int16)
        raw_data = raw_data.reshape((data["nDetector_X_orig"], data["nDetector_Y_orig"])) / data["post_limit_high"]
        raw_data = np.rot90(raw_data, k=3)
        raw_data = skimage.transform.resize(
            raw_data,
            (data["nDetector"][1], data["nDetector"][0]),
            mode='reflect',
            anti_aliasing=False
        ).astype(np.float32)
        projections.append(raw_data)
    projections = -np.array(projections)
    projections -= projections.min()
    return {
        "angles": np.array(angles),
        "projections": projections
    }

def read_image(data, path, train_num=40, val_num=40):
    # we use randomly selected angles for training and validation
    data["numTrain"] = train_num
    data["numVal"] = val_num

    indices = random.sample(range(0, data["PROJECTION"]), train_num + val_num)
    train_indices = sorted(indices[:train_num])
    val_indices = sorted(indices[train_num:])

    data["train"] = read_raw(train_indices, data, path)
    data["val"] = read_raw(val_indices, data, path)

    return data


def main(args):
    data = {
        'offOrigin': [0, 0, 0],
        'offDetector': [0, 0],
        'dVoxel' : [1, 1, 1],
        'accuracy': 0.2,
        'filter': None,
        "mode": "cone"
    }
    data = read_meta(
        data, 
        args.data,
        args.scale_factor_detector, 
        args.scale_factor_voxel,
    )
    data = read_image(
        data, 
        args.data,
        args.train_num,
        args.val_num
)

    data["nDetector"] = data["nDetector"][::-1]
    # save the data to a pickle file
    with open(os.path.join(args.data, args.output_name), "wb") as f:
        pickle.dump(data, f)

# settings for argument parser
def get_parser():
    parser = argparse.ArgumentParser(description="Initialize the scene.")
    parser.add_argument(
        "--data",
        type=str,
        help="Path to the data directory containing the .RAW files and Recon.prm.",
        required=True,
    ),
    parser.add_argument(
        "--output_name",
        type=str,
        default="data.pkl",
        help="Name of the output file to save the data.",
    )
    parser.add_argument(
        "--scale_factor_detector",
        type=float,
        default=1, 
        help="Scale factor for the detector resolution.",
    )
    parser.add_argument(
        "--scale_factor_voxel",
        type=float,
        default=1,
        help="Scale factor for the voxel resolution.",
    )
    parser.add_argument(
        "--train_num",
        type=int,
        default=40,
        help="Number of training angles.",
    )
    parser.add_argument(
        "--val_num",
        type=int,
        default=40,
        help="Number of validation angles.",
    )

    return parser

"""
usage:
python read_prm_mnri.py --data data/CR_20250618_170040 --scale_factor_detector 0.25 --scale_factor_voxel 0.25 --train_num 40 --val_num 40 --output_name data.pkl
"""

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)