import argparse
from pathlib import Path

import numpy as np
from PIL import Image

from perception import viewer
from perception.sources import RealSenseSource, estimated_intrinsics
from perception.zeroshot import GroundedSam


def frames_from_images(paths):
    for path in paths:
        rgb = np.array(Image.open(path).convert("RGB"))
        yield path, rgb, estimated_intrinsics(rgb.shape[1], rgb.shape[0])


def frames_from_bag(bag: str, stride: int, limit: int):
    kept = 0
    with RealSenseSource(bag_path=bag, bag_repeat=False, bag_realtime=False, warmup_frames=0) as source:
        for index, frame in enumerate(source.frames()):
            if index % stride:
                continue
            yield f"{bag}#{index}", frame.color_rgb, frame.intrinsics
            kept += 1
            if kept >= limit:
                return


def main() -> None:
    parser = argparse.ArgumentParser(description="Zero-shot footage: prompt -> GroundingDINO boxes -> SAM masks")
    parser.add_argument("images", nargs="*", help="Image files to annotate")
    parser.add_argument("--bag", help="A recorded RealSense .bag to sample frames from")
    parser.add_argument("--stride", type=int, default=15, help="Sample every Nth bag frame")
    parser.add_argument("--limit", type=int, default=20, help="Stop after this many bag frames")
    parser.add_argument("--prompt", default="person.", help="Lowercase phrases, each ending in a period")
    args = parser.parse_args()

    if not args.images and not args.bag:
        parser.error("give one or more image files, or --bag <file>")
    missing = [path for path in args.images if not Path(path).is_file()]
    if missing:
        parser.error(f"no such image file(s): {', '.join(missing)}")

    source = frames_from_bag(args.bag, args.stride, args.limit) if args.bag else frames_from_images(args.images)

    model = GroundedSam()
    viewer.init("footage")

    for name, rgb, intrinsics in source:
        detections, segmentation = model.detect_and_segment(rgb, args.prompt)
        print(f"{name}: {[f'{d.label} {d.score:.2f}' for d in detections]}")

        viewer.log_camera(intrinsics)
        viewer.log_image(rgb)
        viewer.log_detections(detections)
        viewer.log_segmentation(segmentation)


if __name__ == "__main__":
    main()
