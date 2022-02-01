import os
from pathlib import Path
from trame import state, controller as ctrl

from pv_visualizer.html.file_browser import ParaViewFileBrowser
from .pipeline import NAME as pipeline_name

from paraview import simple

# -----------------------------------------------------------------------------
# Working directory
# -----------------------------------------------------------------------------

BASE_PATH = "/Users/sebastien.jourdain/Desktop/sc21"

# -----------------------------------------------------------------------------
# UI module
# -----------------------------------------------------------------------------

NAME = "files"
ICON = "mdi-file-document-outline"
ICON_STYLE = {}

def create_panel(container):
    with container:
        ParaViewFileBrowser(
            BASE_PATH,
            on_load_file=ctrl.on_load_file,
            v_if=(f"active_controls == '{NAME}'",),
        )

# -----------------------------------------------------------------------------
# File handling functions
# -----------------------------------------------------------------------------

def add_prefix(file_path):
    return str(Path(os.path.join(BASE_PATH, file_path)).absolute())

def load_file(files):
    if isinstance(files, list):
        # time serie
        files_to_load = map(add_prefix, files)
        reader = simple.OpenDataFile(files_to_load)
        simple.Show(reader) # Should be defered
    elif files.endswith(".pvsm"):
        # state file
        v1 = simple.Render()
        state_to_load = add_prefix(files)
        simple.LoadState(state_to_load)
        view = simple.GetActiveView()
        view.MakeRenderWindowInteractor(True)
        ctrl.view_replace(view)
    else:
        # data file
        data_to_load = add_prefix(files)
        reader = simple.OpenDataFile(data_to_load)
        simple.Show(reader) # Should be defered

    # Switch to pipeline
    state.active_controls = pipeline_name
    ctrl.view_update(reset_camera=True)

# -----------------------------------------------------------------------------
# Update controller
# -----------------------------------------------------------------------------

ctrl.on_load_file = load_file