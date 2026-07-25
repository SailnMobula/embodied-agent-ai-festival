from __future__ import annotations

import argparse

from .sources import FrameSource, RealSenseSource, WebcamSource


def add_source_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--webcam", type=int, metavar="INDEX", help="Use a webcam instead of the RealSense")
    parser.add_argument("--bag", type=str, help="Play a recorded RealSense .bag instead of the live camera")
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--fps", type=int, default=30)


def build_source(args: argparse.Namespace) -> FrameSource:
    if args.webcam is not None:
        return WebcamSource(index=args.webcam, width=args.width, height=args.height)
    return RealSenseSource(width=args.width, height=args.height, fps=args.fps, bag_path=args.bag)
