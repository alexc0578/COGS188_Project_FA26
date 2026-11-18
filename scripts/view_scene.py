"""Open the pen-cap scene in MuJoCo's interactive viewer."""

from pathlib import Path

import mujoco
import mujoco.viewer


SCENE = Path(__file__).resolve().parents[1] / "envs" / "pen_cap_scene.xml"


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(SCENE))
    data = mujoco.MjData(model)
    mujoco.viewer.launch(model, data)


if __name__ == "__main__":
    main()
