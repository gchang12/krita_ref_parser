"""
Inspects for filetree differences between the previous Krita-Docs version and the current.
"""
import unittest
from pathlib import Path

@unittest.skip("Uncomment this upon pulling a new Krita-Docs version.")
class SectionDiffAlerter(unittest.TestCase):
    """
    Tests to see if any new sections have emerged since the last git-pull.
    """

    def setUp(self):
        """
        Declares the directory to check.
        """
        self.path = Path("input", "docs-krita-org", "_build", "html", "reference_manual")

    def test_for_section_diff(self):
        """
        Checks to see if the sections have changed.
        """
        expected = set([
            "blending_modes",
            "blending_modes.html",
            "blending_modes/arithmetic.html",
            "blending_modes/binary.html",
            "blending_modes/darken.html",
            "blending_modes/hsx.html",
            "blending_modes/lighten.html",
            "blending_modes/misc.html",
            "blending_modes/mix.html",
            "blending_modes/modulo.html",
            "blending_modes/negative.html",
            "blending_modes/quadratic.html",
            "brushes",
            "brushes.html",
            "brushes/brush_engines",
            "brushes/brush_engines.html",
            "brushes/brush_settings",
            "brushes/brush_settings.html",
            "brushes/brush_engines/bristle_engine.html",
            "brushes/brush_engines/chalk_engine.html",
            "brushes/brush_engines/clone_engine.html",
            "brushes/brush_engines/color_smudge_engine.html",
            "brushes/brush_engines/curve_engine.html",
            "brushes/brush_engines/deform_brush_engine.html",
            "brushes/brush_engines/dyna_brush_engine.html",
            "brushes/brush_engines/filter_brush_engine.html",
            "brushes/brush_engines/grid_brush_engine.html",
            "brushes/brush_engines/hatching_brush_engine.html",
            "brushes/brush_engines/mypaint_engine.html",
            "brushes/brush_engines/particle_brush_engine.html",
            "brushes/brush_engines/pixel_brush_engine.html",
            "brushes/brush_engines/quick_brush_engine.html",
            "brushes/brush_engines/shape_brush_engine.html",
            "brushes/brush_engines/sketch_brush_engine.html",
            "brushes/brush_engines/spray_brush_engine.html",
            "brushes/brush_engines/tangen_normal_brush_engine.html",
            "brushes/brush_settings/brush_tips.html",
            "brushes/brush_settings/locked_brush_settings.html",
            "brushes/brush_settings/masked_brush.html",
            "brushes/brush_settings/opacity_and_flow.html",
            "brushes/brush_settings/options.html",
            "brushes/brush_settings/tablet_sensors.html",
            "brushes/brush_settings/texture.html",
            "dockers",
            "dockers.html",
            "dockers/add_shape.html",
            "dockers/advanced_color_selector.html",
            "dockers/animation_curves.html",
            "dockers/animation_docker.html",
            "dockers/animation_timeline.html",
            "dockers/arrange.html",
            "dockers/artistic_color_selector.html",
            "dockers/brush_preset_docker.html",
            "dockers/brush_preset_history.html",
            "dockers/channels_docker.html",
            "dockers/color_sliders.html",
            "dockers/compositions.html",
            "dockers/digital_color_mixer.html",
            "dockers/gamut_mask_docker.html",
            "dockers/grids_and_guides.html",
            "dockers/histogram_docker.html",
            "dockers/layers.html",
            "dockers/log_viewer.html",
            "dockers/lut_management.html",
            "dockers/onion_skin.html",
            "dockers/overview.html",
            "dockers/palette_docker.html",
            "dockers/pattern_docker.html",
            "dockers/recorder_docker.html",
            "dockers/reference_images_docker.html",
            "dockers/shape_properties_docker.html",
            "dockers/small_color_selector.html",
            "dockers/snapshot_docker.html",
            "dockers/specific_color_selector.html",
            "dockers/storyboard_docker.html",
            "dockers/task_sets.html",
            "dockers/touch_docker.html",
            "dockers/undo_history.html",
            "dockers/vector_library.html",
            "dockers/wide_gamut_color_selector.html",
            "filters",
            "filters.html",
            "filters/adjust.html",
            "filters/artistic.html",
            "filters/blur.html",
            "filters/colors.html",
            "filters/edge_detection.html",
            "filters/emboss.html",
            "filters/enhance.html",
            "filters/map.html",
            "filters/other.html",
            "filters/wavelet_decompose.html",
            "layers_and_masks",
            "layers_and_masks.html",
            "layers_and_masks/fill_layer_generators",
            "layers_and_masks/fill_layer_generators.html",
            "layers_and_masks/fill_layer_generators/gradient.html",
            "layers_and_masks/fill_layer_generators/multigrid.html",
            "layers_and_masks/fill_layer_generators/pattern_fill.html",
            "layers_and_masks/fill_layer_generators/screentone.html",
            "layers_and_masks/fill_layer_generators/seexpr.html",
            "layers_and_masks/fill_layer_generators/simplex_noise.html",
            "layers_and_masks/clone_layers.html",
            "layers_and_masks/file_layers.html",
            "layers_and_masks/fill_layers.html",
            "layers_and_masks/filter_layers.html",
            "layers_and_masks/filter_masks.html",
            "layers_and_masks/group_layers.html",
            "layers_and_masks/layer_styles.html",
            "layers_and_masks/paint_layers.html",
            "layers_and_masks/selection_masks.html",
            "layers_and_masks/split_alpha.html",
            "layers_and_masks/transformation_masks.html",
            "layers_and_masks/transparency_masks.html",
            "layers_and_masks/vector_layers.html",
            "main_menu",
            "main_menu.html",
            "main_menu/edit_menu.html",
            "main_menu/file_menu.html",
            "main_menu/help_menu.html",
            "main_menu/image_menu.html",
            "main_menu/layers_menu.html",
            "main_menu/select_menu.html",
            "main_menu/settings_menu.html",
            "main_menu/tools_menu.html",
            "main_menu/view_menu.html",
            "main_menu/window_menu.html",
            "preferences",
            "preferences.html",
            "preferences/author_settings.html",
            "preferences/canvas_input_settings.html",
            "preferences/canvas_only_mode.html",
            "preferences/color_management_settings.html",
            "preferences/color_selector_settings.html",
            "preferences/display_settings.html",
            "preferences/general_settings.html",
            "preferences/g_mic_settings.html",
            "preferences/performance_settings.html",
            "preferences/popup_palette_settings.html",
            "preferences/python_plugin_manager.html",
            "preferences/shortcut_settings.html",
            "preferences/tablet_settings.html",
            "resource_management",
            "resource_management.html",
            "resource_management/paintoppresets.html",
            "resource_management/resource_brushtips.html",
            "resource_management/resource_gradients.html",
            "resource_management/resource_patterns.html",
            "resource_management/resource_workspace.html",
            "resource_management/seexpr_scripts.html",
            "tools",
            "tools.html",
            "tools/assistant.html",
            "tools/calligraphy.html",
            "tools/colorize_mask.html",
            "tools/color_sampler.html",
            "tools/contiguous_select.html",
            "tools/crop.html",
            "tools/dyna.html",
            "tools/ellipse.html",
            "tools/elliptical_select.html",
            "tools/enclose_and_fill.html",
            "tools/fill.html",
            "tools/freehand_brush.html",
            "tools/freehand_path.html",
            "tools/freehand_select.html",
            "tools/gradient_draw.html",
            "tools/gradient_edit.html",
            "tools/line.html",
            "tools/magnetic_select.html",
            "tools/measure.html",
            "tools/move.html",
            "tools/multibrush.html",
            "tools/pan.html",
            "tools/path.html",
            "tools/path_select.html",
            "tools/pattern_edit.html",
            "tools/polygonal_select.html",
            "tools/polygon.html",
            "tools/polyline.html",
            "tools/rectangle.html",
            "tools/rectangular_select.html",
            "tools/reference_images_tool.html",
            "tools/shape_edit.html",
            "tools/shape_selection.html",
            "tools/similar_select.html",
            "tools/smart_patch.html",
            "tools/text.html",
            "tools/transform.html",
            "tools/zoom.html",
            # 11-17-2025
        ])
        actual = set()
        def to_relative_path(dirpath, filename):
            """
            """
            return dirpath.joinpath(filename).relative_to(self.path)
        def is_index_file(dirpath, filename):
            """
            """
            return dirpath.joinpath(filename).with_suffix("").is_dir()
        for dirpath, dirnames, filenames in self.path.walk():
            if dirpath == self.path:
                for filename in map(
                    lambda filename: to_relative_path(dirpath, filename),
                    filter(
                        lambda filename: is_index_file(dirpath, filename),
                        filenames,
                    )):
                    actual.add(str(to_relative_path(dirpath, filename)))
                    actual.add(str(to_relative_path(dirpath, filename).with_suffix("")))
                continue
            for filename in filenames:
                actual.add(str(to_relative_path(dirpath, filename)))
                if is_index_file(dirpath, filename):
                    actual.add(str(to_relative_path(dirpath, filename).with_suffix("")))
        self.assertSetEqual(actual, expected)


