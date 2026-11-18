# COGS188 Project template
Fork this repo.

Once you do it is is your repo. You are free to manage the repo as you see fit, edit this README, add data files, add scripts, etc. 

Also, you are free and encouraged to share this project after the course and to add it to your portfolio. Just be sure to fork it to your GitHub at the end of the quarter!

## SGS pen cap simulation

The MuJoCo scene is in `envs/pen_cap_scene.xml`. It references the SO-101 robot
model in `robots/so101_arm/` and the marker, cap, and holder meshes in `assets/`.
The original calibrated robot XML is preserved; the camera variant adds the
public SO-101 wrist mount and lens camera. Camera mount sources and license are
noted in `robots/so101_arm/so101_new_calib_wrist_camera.xml`.

From the repository root, install dependencies and open the scene:

```bash
uv sync
uv run scripts/view_scene.py
```

To save overhead and wrist camera previews:

```bash
uv run scripts/render_cameras.py
```

The preview script uses a cap approach pose for the wrist view; it does not
change the scene's default reset pose. The overhead camera placement and exact
physical wrist camera model still need comparison with the real setup.
