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
var object_1 = require("@bokehjs/core/util/object");
var html_box_1 = require("@bokehjs/models/layouts/html_box");
var layout_1 = require("../layout");
var vtk_utils_1 = require("./vtk_utils");
var AbstractVTKView = /** @class */ (function (_super) {
    __extends(AbstractVTKView, _super);
    function AbstractVTKView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this._setting_camera = false;
        return _this;
    }
    AbstractVTKView.prototype.connect_signals = function () {
        var _this = this;
        _super.prototype.connect_signals.call(this);
        this.connect(this.model.properties.data.change, function () {
            _this.invalidate_render();
        });
        this.connect(this.model.properties.orientation_widget.change, function () {
            _this._orientation_widget_visibility(_this.model.orientation_widget);
        });
        this.connect(this.model.properties.camera.change, function () { return _this._set_camera_state(); });
    };
    AbstractVTKView.prototype._orientation_widget_visibility = function (visibility) {
        this._orientationWidget.setEnabled(visibility);
        if (visibility)
            this._widgetManager.enablePicking();
        else
            this._widgetManager.disablePicking();
        this._orientationWidget.updateMarkerOrientation();
        this._vtk_renwin.getRenderWindow().render();
    };
    AbstractVTKView.prototype._create_orientation_widget = function () {
        var _this = this;
        var axes = vtk_utils_1.vtkns.AxesActor.newInstance();
        // add orientation widget
        var orientationWidget = vtk_utils_1.vtkns.OrientationMarkerWidget.newInstance({
            actor: axes,
            interactor: this._vtk_renwin.getInteractor(),
        });
        orientationWidget.setEnabled(true);
        orientationWidget.setViewportCorner(vtk_utils_1.vtkns.OrientationMarkerWidget.Corners.BOTTOM_RIGHT);
        orientationWidget.setViewportSize(0.15);
        orientationWidget.setMinPixelSize(100);
        orientationWidget.setMaxPixelSize(300);
        this._orientationWidget = orientationWidget;
        var widgetManager = vtk_utils_1.vtkns.WidgetManager.newInstance();
        widgetManager.setRenderer(orientationWidget.getRenderer());
        var widget = vtk_utils_1.vtkns.InteractiveOrientationWidget.newInstance();
        widget.placeWidget(axes.getBounds());
        widget.setBounds(axes.getBounds());
        widget.setPlaceFactor(1);
        var vw = widgetManager.addWidget(widget);
        this._widgetManager = widgetManager;
        // Manage user interaction
        vw.onOrientationChange(function (_a) {
            var direction = _a.direction;
            var camera = _this._vtk_renwin.getRenderer().getActiveCamera();
            var focalPoint = camera.getFocalPoint();
            var position = camera.getPosition();
            var viewUp = camera.getViewUp();
            var distance = Math.sqrt(Math.pow(position[0] - focalPoint[0], 2) +
                Math.pow(position[1] - focalPoint[1], 2) +
                Math.pow(position[2] - focalPoint[2], 2));
            camera.setPosition(focalPoint[0] + direction[0] * distance, focalPoint[1] + direction[1] * distance, focalPoint[2] + direction[2] * distance);
            if (direction[0])
                camera.setViewUp(vtk_utils_1.majorAxis(viewUp, 1, 2));
            if (direction[1])
                camera.setViewUp(vtk_utils_1.majorAxis(viewUp, 0, 2));
            if (direction[2])
                camera.setViewUp(vtk_utils_1.majorAxis(viewUp, 0, 1));
            _this._orientationWidget.updateMarkerOrientation();
            _this._vtk_renwin.getRenderer().resetCameraClippingRange();
            _this._vtk_renwin.getRenderWindow().render();
        });
        this._orientation_widget_visibility(this.model.orientation_widget);
    };
    AbstractVTKView.prototype._get_camera_state = function () {
        if (!this._setting_camera) {
            this._setting_camera = true;
            var state = object_1.clone(this._vtk_renwin.getRenderer().getActiveCamera().get());
            delete state.classHierarchy;
            delete state.vtkObject;
            delete state.vtkCamera;
            delete state.viewPlaneNormal;
            this.model.camera = state;
            this._setting_camera = false;
        }
    };
    AbstractVTKView.prototype._set_camera_state = function () {
        if (!this._setting_camera) {
            this._setting_camera = true;
            try {
                if (this.model.camera)
                    this._vtk_renwin.getRenderer().getActiveCamera().set(this.model.camera);
            }
            finally {
                this._setting_camera = false;
            }
            this._orientationWidget.updateMarkerOrientation();
            this._vtk_renwin.getRenderer().resetCameraClippingRange();
            this._vtk_renwin.getRenderWindow().render();
        }
    };
    AbstractVTKView.prototype.render = function () {
        var _this = this;
        _super.prototype.render.call(this);
        this._orientationWidget = null;
        this._vtk_container = dom_1.div();
        layout_1.set_size(this._vtk_container, this.model);
        this.el.appendChild(this._vtk_container);
        this._vtk_renwin = vtk_utils_1.vtkns.FullScreenRenderWindow.newInstance({
            rootContainer: this.el,
            container: this._vtk_container
        });
        this._remove_default_key_binding();
        this._create_orientation_widget();
        this._vtk_renwin.getRenderer().getActiveCamera().onModified(function () { return _this._get_camera_state(); });
        this._set_camera_state();
        this.model.renderer_el = this._vtk_renwin;
    };
    AbstractVTKView.prototype.after_layout = function () {
        _super.prototype.after_layout.call(this);
        this._vtk_renwin.resize();
    };
    AbstractVTKView.prototype._remove_default_key_binding = function () {
        var interactor = this._vtk_renwin.getInteractor();
        document.querySelector('body').removeEventListener('keypress', interactor.handleKeyPress);
        document.querySelector('body').removeEventListener('keydown', interactor.handleKeyDown);
        document.querySelector('body').removeEventListener('keyup', interactor.handleKeyUp);
    };
    AbstractVTKView.__name__ = "AbstractVTKView";
    return AbstractVTKView;
}(layout_1.PanelHTMLBoxView));
exports.AbstractVTKView = AbstractVTKView;
var AbstractVTKPlot = /** @class */ (function (_super) {
    __extends(AbstractVTKPlot, _super);
    function AbstractVTKPlot(attrs) {
        return _super.call(this, attrs) || this;
    }
    AbstractVTKPlot.prototype.getActors = function () {
        return this.renderer_el.getRenderer().getActors();
    };
    AbstractVTKPlot.init_AbstractVTKPlot = function () {
        this.define({
            orientation_widget: [p.Boolean, false],
            camera: [p.Instance],
        });
        this.override({
            height: 300,
            width: 300
        });
    };
    AbstractVTKPlot.__name__ = "AbstractVTKPlot";
    AbstractVTKPlot.__module__ = "panel.models.vtk";
    return AbstractVTKPlot;
}(html_box_1.HTMLBox));
exports.AbstractVTKPlot = AbstractVTKPlot;
AbstractVTKPlot.init_AbstractVTKPlot();
//# sourceMappingURL=vtk_layout.js.map