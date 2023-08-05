"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
var p = __importStar(require("@bokehjs/core/properties"));
var dom_1 = require("@bokehjs/core/dom");
var vtk_layout_1 = require("./vtk_layout");
var vtk_utils_1 = require("./vtk_utils");
var VTKPlotView = /** @class */ (function (_super) {
    __extends(VTKPlotView, _super);
    function VTKPlotView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this._axes_initialized = false;
        return _this;
    }
    VTKPlotView.prototype.connect_signals = function () {
        var _this = this;
        _super.prototype.connect_signals.call(this);
        this.connect(this.model.properties.axes.change, function () {
            _this._delete_axes();
            if (_this.model.axes)
                _this._set_axes();
            _this._vtk_renwin.getRenderWindow().render();
        });
        this.el.addEventListener('mouseenter', function () {
            var interactor = _this._vtk_renwin.getInteractor();
            if (_this.model.enable_keybindings) {
                document.querySelector('body').addEventListener('keypress', interactor.handleKeyPress);
                document.querySelector('body').addEventListener('keydown', interactor.handleKeyDown);
                document.querySelector('body').addEventListener('keyup', interactor.handleKeyUp);
            }
        });
        this.el.addEventListener('mouseleave', function () {
            var interactor = _this._vtk_renwin.getInteractor();
            document.querySelector('body').removeEventListener('keypress', interactor.handleKeyPress);
            document.querySelector('body').removeEventListener('keydown', interactor.handleKeyDown);
            document.querySelector('body').removeEventListener('keyup', interactor.handleKeyUp);
        });
    };
    VTKPlotView.prototype.render = function () {
        _super.prototype.render.call(this);
        this._axes = null;
        this._axes_initialized = false;
        this._plot();
    };
    VTKPlotView.prototype.after_layout = function () {
        if (!this._axes_initialized) {
            this._render_axes_canvas();
            this._axes_initialized = true;
        }
    };
    VTKPlotView.prototype._render_axes_canvas = function () {
        var _this = this;
        var canvas_list = this._vtk_container.getElementsByTagName('canvas');
        if (canvas_list.length != 1)
            throw Error('Error at initialization of the 3D scene, container should have one and only one canvas');
        else
            canvas_list[0].classList.add('scene3d-canvas');
        var axes_canvas = dom_1.canvas({
            style: {
                position: "absolute",
                top: "0",
                left: "0",
                width: "100%",
                height: "100%"
            }
        });
        axes_canvas.classList.add('axes-canvas');
        this._vtk_container.appendChild(axes_canvas);
        this._vtk_renwin.setResizeCallback(function () {
            var dims = _this._vtk_container.getBoundingClientRect();
            var width = Math.floor(dims.width * window.devicePixelRatio);
            var height = Math.floor(dims.height * window.devicePixelRatio);
            axes_canvas.setAttribute('width', width.toFixed());
            axes_canvas.setAttribute('height', height.toFixed());
        });
    };
    VTKPlotView.prototype._delete_axes = function () {
        var _this = this;
        if (this._axes == null)
            return;
        Object.keys(this._axes).forEach(function (key) { return _this._vtk_renwin.getRenderer().removeActor(_this._axes[key]); });
        var axesCanvas = this._vtk_renwin.getContainer().getElementsByClassName('axes-canvas')[0];
        var textCtx = axesCanvas.getContext("2d");
        if (textCtx)
            textCtx.clearRect(0, 0, axesCanvas.clientWidth * window.devicePixelRatio, axesCanvas.clientHeight * window.devicePixelRatio);
        this._axes = null;
    };
    VTKPlotView.prototype._set_axes = function () {
        if (this.model.axes) {
            var axesCanvas = this._vtk_renwin.getContainer().getElementsByClassName('axes-canvas')[0];
            var _a = this.model.axes.create_axes(axesCanvas), psActor = _a.psActor, axesActor = _a.axesActor, gridActor = _a.gridActor;
            this._axes = { psActor: psActor, axesActor: axesActor, gridActor: gridActor };
            this._vtk_renwin.getRenderer().addActor(psActor);
            this._vtk_renwin.getRenderer().addActor(axesActor);
            this._vtk_renwin.getRenderer().addActor(gridActor);
        }
    };
    VTKPlotView.prototype._plot = function () {
        var _this = this;
        if (!this.model.data) {
            this._vtk_renwin.getRenderWindow().render();
            return;
        }
        var dataAccessHelper = vtk_utils_1.vtkns.DataAccessHelper.get('zip', {
            zipContent: atob(this.model.data),
            callback: function (_zip) {
                var sceneImporter = vtk_utils_1.vtkns.HttpSceneLoader.newInstance({
                    renderer: _this._vtk_renwin.getRenderer(),
                    dataAccessHelper: dataAccessHelper,
                });
                var fn = vtk_utils_1.vtk.macro.debounce(function () {
                    if (_this._axes == null && _this.model.axes)
                        _this._set_axes();
                    _this.model.properties.camera.change.emit();
                }, 100);
                sceneImporter.setUrl('index.json');
                sceneImporter.onReady(fn);
            }
        });
    };
    VTKPlotView.__name__ = "VTKPlotView";
    return VTKPlotView;
}(vtk_layout_1.AbstractVTKView));
exports.VTKPlotView = VTKPlotView;
var VTKPlot = /** @class */ (function (_super) {
    __extends(VTKPlot, _super);
    function VTKPlot(attrs) {
        var _this = _super.call(this, attrs) || this;
        _this.outline = vtk_utils_1.vtkns.OutlineFilter.newInstance(); //use to display bouding box of a selected actor
        var mapper = vtk_utils_1.vtkns.Mapper.newInstance();
        mapper.setInputConnection(_this.outline.getOutputPort());
        _this.outline_actor = vtk_utils_1.vtkns.Actor.newInstance();
        _this.outline_actor.setMapper(mapper);
        return _this;
    }
    VTKPlot.init_VTKPlot = function () {
        this.prototype.default_view = VTKPlotView;
        this.define({
            data: [p.String],
            axes: [p.Instance],
            enable_keybindings: [p.Boolean, false],
        });
    };
    VTKPlot.__name__ = "VTKPlot";
    return VTKPlot;
}(vtk_layout_1.AbstractVTKPlot));
exports.VTKPlot = VTKPlot;
VTKPlot.init_VTKPlot();
//# sourceMappingURL=vtk.js.map