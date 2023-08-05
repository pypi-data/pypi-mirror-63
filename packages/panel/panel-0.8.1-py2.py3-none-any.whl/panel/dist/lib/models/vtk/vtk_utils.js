"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var serialization_1 = require("@bokehjs/core/util/serialization");
var array_1 = require("@bokehjs/core/util/array");
exports.vtk = window.vtk;
exports.vtkns = {};
if (exports.vtk) {
    exports.vtkns['DataArray'] = exports.vtk.Common.Core.vtkDataArray;
    exports.vtkns['ImageData'] = exports.vtk.Common.DataModel.vtkImageData;
    exports.vtkns['OutlineFilter'] = exports.vtk.Filters.General.vtkOutlineFilter;
    exports.vtkns['CubeSource'] = exports.vtk.Filters.Sources.vtkCubeSource;
    exports.vtkns['LineSource'] = exports.vtk.Filters.Sources.vtkLineSource;
    exports.vtkns['PlaneSource'] = exports.vtk.Filters.Sources.vtkPlaneSource;
    exports.vtkns['PointSource'] = exports.vtk.Filters.Sources.vtkPointSource;
    exports.vtkns['OrientationMarkerWidget'] = exports.vtk.Interaction.Widgets.vtkOrientationMarkerWidget;
    exports.vtkns['DataAccessHelper'] = exports.vtk.IO.Core.DataAccessHelper;
    exports.vtkns['HttpSceneLoader'] = exports.vtk.IO.Core.vtkHttpSceneLoader;
    exports.vtkns['ImageSlice'] = exports.vtk.Rendering.Core.vtkImageSlice;
    exports.vtkns['Actor'] = exports.vtk.Rendering.Core.vtkActor;
    exports.vtkns['AxesActor'] = exports.vtk.Rendering.Core.vtkAxesActor;
    exports.vtkns['Mapper'] = exports.vtk.Rendering.Core.vtkMapper;
    exports.vtkns['ImageMapper'] = exports.vtk.Rendering.Core.vtkImageMapper;
    exports.vtkns['SphereMapper'] = exports.vtk.Rendering.Core.vtkSphereMapper;
    exports.vtkns['WidgetManager'] = exports.vtk.Widgets.Core.vtkWidgetManager;
    exports.vtkns['InteractiveOrientationWidget'] = exports.vtk.Widgets.Widgets3D.vtkInteractiveOrientationWidget;
    exports.vtkns['PixelSpaceCallbackMapper'] = exports.vtk.Rendering.Core.vtkPixelSpaceCallbackMapper;
    exports.vtkns['FullScreenRenderWindow'] = exports.vtk.Rendering.Misc.vtkFullScreenRenderWindow;
    exports.vtkns['VolumeController'] = exports.vtk.Interaction.UI.vtkVolumeController;
    exports.vtkns['Volume'] = exports.vtk.Rendering.Core.vtkVolume;
    exports.vtkns['VolumeMapper'] = exports.vtk.Rendering.Core.vtkVolumeMapper;
    exports.vtkns['ColorTransferFunction'] = exports.vtk.Rendering.Core.vtkColorTransferFunction;
    exports.vtkns['PiecewiseFunction'] = exports.vtk.Common.DataModel.vtkPiecewiseFunction;
    exports.vtkns['BoundingBox'] = exports.vtk.Common.DataModel.vtkBoundingBox;
}
function hexToRGB(color) {
    return [parseInt(color.slice(1, 3), 16) / 255,
        parseInt(color.slice(3, 5), 16) / 255,
        parseInt(color.slice(5, 7), 16) / 255];
}
exports.hexToRGB = hexToRGB;
function valToHex(val) {
    var hex = Math.min(Math.max(Math.round(val), 0), 255).toString(16);
    return hex.length == 2 ? hex : "0" + hex;
}
function rgbToHex(r, g, b) {
    return '#' + valToHex(r) + valToHex(g) + valToHex(b);
}
exports.rgbToHex = rgbToHex;
function vtkLutToMapper(vtk_lut) {
    //For the moment only linear colormapper are handle
    var _a = vtk_lut.get('scale', 'nodes'), scale = _a.scale, nodes = _a.nodes;
    if (scale !== exports.vtkns.ColorTransferFunction.Scale.LINEAR)
        throw ('Error transfer function scale not handle');
    var x = nodes.map(function (a) { return a.x; });
    var low = Math.min.apply(Math, x);
    var high = Math.max.apply(Math, x);
    var vals = array_1.linspace(low, high, 255);
    var rgb = [0, 0, 0];
    var palette = (vals).map(function (val) {
        vtk_lut.getColor(val, rgb);
        return rgbToHex((rgb[0] * 255), (rgb[1] * 255), (rgb[2] * 255));
    });
    return { low: low, high: high, palette: palette };
}
exports.vtkLutToMapper = vtkLutToMapper;
function utf8ToAB(utf8_str) {
    var buf = new ArrayBuffer(utf8_str.length); // 2 bytes for each char
    var bufView = new Uint8Array(buf);
    for (var i = 0, strLen = utf8_str.length; i < strLen; i++) {
        bufView[i] = utf8_str.charCodeAt(i);
    }
    return buf;
}
function data2VTKImageData(data) {
    var source = exports.vtkns.ImageData.newInstance({
        spacing: data.spacing
    });
    source.setDimensions(data.dims);
    source.setOrigin(data.origin != null ? data.origin : data.dims.map(function (v) { return v / 2; }));
    var dataArray = exports.vtkns.DataArray.newInstance({
        name: "scalars",
        numberOfComponents: 1,
        values: new serialization_1.ARRAY_TYPES[data.dtype](utf8ToAB(atob(data.buffer)))
    });
    source.getPointData().setScalars(dataArray);
    return source;
}
exports.data2VTKImageData = data2VTKImageData;
function majorAxis(vec3, idxA, idxB) {
    var axis = [0, 0, 0];
    var idx = Math.abs(vec3[idxA]) > Math.abs(vec3[idxB]) ? idxA : idxB;
    var value = vec3[idx] > 0 ? 1 : -1;
    axis[idx] = value;
    return axis;
}
exports.majorAxis = majorAxis;
function cartesian_product() {
    var arrays = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        arrays[_i] = arguments[_i];
    }
    return arrays.reduce(function (acc, curr) {
        return acc.flatMap(function (c) { return curr.map(function (n) { return [].concat(c, n); }); });
    });
}
exports.cartesian_product = cartesian_product;
//# sourceMappingURL=vtk_utils.js.map