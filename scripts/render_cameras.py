"""Save a still RGB image from each camera in the pen-cap scene.

Run from any directory: uv run scripts/render_cameras.py
"""

from pathlib import Path
import struct
import zlib

import mujoco


ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "envs" / "pen_cap_scene.xml"
OUTPUT = ROOT / "camera_previews"
CAMERAS = {"overhead": (640, 480), "robot_wrist_camera": (960, 540)}


def png_chunk(kind: bytes, content: bytes) -> bytes:
    return (struct.pack(">I", len(content)) + kind + content
            + struct.pack(">I", zlib.crc32(kind + content) & 0xFFFFFFFF))


def save_png(path: Path, rgb) -> None:
    height, width, channels = rgb.shape
    if channels != 3:
        raise ValueError("Expected an RGB image")
    rows = b"".join(b"\0" + row.tobytes() for row in rgb)
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", header)
                     + png_chunk(b"IDAT", zlib.compress(rows))
                     + png_chunk(b"IEND", b""))


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(SCENE))
    data = mujoco.MjData(model)
    # The camera looks along the gripper. Preview an approach pose aimed at
    # the cap; at the robot's zero pose it points across the room.
    for name, angle in {
        "robot_shoulder_pan": -0.7,
        "robot_shoulder_lift": -0.5,
        "robot_elbow_flex": 0.3,
        "robot_wrist_flex": 1.4,
    }.items():
        joint = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name)
        data.qpos[model.jnt_qposadr[joint]] = angle
    mujoco.mj_forward(model, data)
    OUTPUT.mkdir(exist_ok=True)
    for camera, (width, height) in CAMERAS.items():
        with mujoco.Renderer(model, height=height, width=width) as renderer:
            renderer.update_scene(data, camera=camera)
            path = OUTPUT / f"{camera}.png"
            save_png(path, renderer.render())
            print(path)


if __name__ == "__main__":
    main()
