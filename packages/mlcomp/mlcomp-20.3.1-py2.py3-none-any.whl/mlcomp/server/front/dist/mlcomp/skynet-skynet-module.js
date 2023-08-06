(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["skynet-skynet-module"],{

/***/ "./src/app/skynet/memory/memory-add-dialog.html":
/*!******************************************************!*\
  !*** ./src/app/skynet/memory/memory-add-dialog.html ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div mat-dialog-content>\n  <mat-form-field>\n    <mat-label>Model</mat-label>\n    <input matInput [(ngModel)]=\"data.model\">\n  </mat-form-field>\n</div>\n\n<div mat-dialog-content>\n  <mat-form-field>\n    <mat-label>Variant</mat-label>\n    <input matInput [(ngModel)]=\"data.variant\">\n  </mat-form-field>\n</div>\n\n<div mat-dialog-content>\n  <mat-form-field>\n    <mat-label>Num classes</mat-label>\n    <input matInput [(ngModel)]=\"data.num_classes\">\n  </mat-form-field>\n</div>\n\n<div mat-dialog-content>\n  <mat-form-field>\n    <mat-label>Image size</mat-label>\n    <input matInput [(ngModel)]=\"data.img_size\">\n  </mat-form-field>\n</div>\n\n<div mat-dialog-content>\n  <mat-form-field>\n    <mat-label>Batch size</mat-label>\n    <input matInput [(ngModel)]=\"data.batch_size\">\n  </mat-form-field>\n</div>\n\n<div mat-dialog-content>\n  <mat-form-field>\n    <mat-label>Memory</mat-label>\n    <input matInput [(ngModel)]=\"data.memory\">\n  </mat-form-field>\n</div>\n\n\n<div mat-dialog-actions>\n  <button mat-button (click)=\"onNoClick()\">Cancel</button>\n  <button mat-button [mat-dialog-close]=\"data\" cdkFocusInitial>Ok</button>\n</div>"

/***/ }),

/***/ "./src/app/skynet/memory/memory-add-dialog.ts":
/*!****************************************************!*\
  !*** ./src/app/skynet/memory/memory-add-dialog.ts ***!
  \****************************************************/
/*! exports provided: MemoryAddDialogComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MemoryAddDialogComponent", function() { return MemoryAddDialogComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_material__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/material */ "./node_modules/@angular/material/esm5/material.es5.js");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../models */ "./src/app/models.ts");




var MemoryAddDialogComponent = /** @class */ (function () {
    function MemoryAddDialogComponent(dialogRef, data) {
        this.dialogRef = dialogRef;
        this.data = data;
    }
    MemoryAddDialogComponent.prototype.onNoClick = function () {
        this.dialogRef.close();
    };
    MemoryAddDialogComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'memory-add-dialog',
            template: __webpack_require__(/*! ./memory-add-dialog.html */ "./src/app/skynet/memory/memory-add-dialog.html"),
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__param"](1, Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"])(_angular_material__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"])),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_material__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"],
            _models__WEBPACK_IMPORTED_MODULE_3__["Memory"]])
    ], MemoryAddDialogComponent);
    return MemoryAddDialogComponent;
}());



/***/ }),

/***/ "./src/app/skynet/memory/memory.component.css":
/*!****************************************************!*\
  !*** ./src/app/skynet/memory/memory.component.css ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3NreW5ldC9tZW1vcnkvbWVtb3J5LmNvbXBvbmVudC5jc3MifQ== */"

/***/ }),

/***/ "./src/app/skynet/memory/memory.component.html":
/*!*****************************************************!*\
  !*** ./src/app/skynet/memory/memory.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<button mat-raised-button style=\"margin-top: 15px\"\n        (click)=\"filter_hidden=!filter_hidden\">\n    Filters {{filter_applied_text}}\n</button>\n\n<div [hidden]=\"filter_hidden\">\n    <mat-form-field style=\"width: 150px\">\n        <input matInput (keyup)=\"model=$event.target.value;onchange()\"\n               placeholder=\"Model\">\n    </mat-form-field>\n\n    <mat-form-field style=\"width: 150px\">\n        <input matInput (keyup)=\"variant=$event.target.value;onchange()\"\n               placeholder=\"Variant\">\n    </mat-form-field>\n</div>\n\n\n<button mat-raised-button\n        style=\"margin-top: 15px\"\n        (click)=\"add()\">\n    Add\n</button>\n\n<button mat-raised-button\n        style=\"margin-top: 15px\"\n        [disabled]=\"selected==null\"\n        (click)=\"edit()\">\n    Edit\n</button>\n\n\n<button mat-raised-button\n        style=\"margin-top: 15px\"\n        [disabled]=\"selected==null\"\n        (click)=\"copy()\">\n    Copy\n</button>\n\n\n<button mat-raised-button\n        style=\"margin-top: 15px\"\n        [disabled]=\"selected==null\"\n        (click)=\"remove()\">\n    Remove\n</button>\n\n\n<div class=\"mat-elevation-z8\">\n    <table mat-table [dataSource]=\"dataSource\" matSort>\n\n        <ng-container matColumnDef=\"model\">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                Model\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                {{element.model}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"variant\">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                Variant\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                {{element.variant}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"num_classes\">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                Num classes\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                {{element.num_classes}}\n            </td>\n        </ng-container>\n        l\n        <ng-container matColumnDef=\"img_size\">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                Image size\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                {{element.img_size}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"batch_size\">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                Batch size\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                {{element.batch_size}}\n            </td>\n        </ng-container>\n\n        <ng-container matColumnDef=\"memory\">\n            <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                Memory\n            </th>\n\n            <td mat-cell *matCellDef=\"let element\">\n                {{element.memory}}\n            </td>\n        </ng-container>\n\n        <tr mat-header-row *matHeaderRowDef=\"displayed_columns\"></tr>\n        <tr mat-row *matRowDef=\"let row; columns: displayed_columns;\"\n            (click)=\"selected=row\"\n            [style.background]=\"selected==row ? 'lightblue' : ''\"></tr>\n    </table>\n\n    <mat-paginator [pageSizeOptions]=\"[default_page_size, 30, 100]\"\n                   [length]=\"total\"\n                   [pageSize]=\"default_page_size\">\n\n    </mat-paginator>\n\n</div>\n\n"

/***/ }),

/***/ "./src/app/skynet/memory/memory.component.ts":
/*!***************************************************!*\
  !*** ./src/app/skynet/memory/memory.component.ts ***!
  \***************************************************/
/*! exports provided: MemoryComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MemoryComponent", function() { return MemoryComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _paginator__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../paginator */ "./src/app/paginator.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _memory_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./memory.service */ "./src/app/skynet/memory/memory.service.ts");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../models */ "./src/app/models.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm5/dialog.es5.js");
/* harmony import */ var _memory_add_dialog__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./memory-add-dialog */ "./src/app/skynet/memory/memory-add-dialog.ts");
/* harmony import */ var _helpers__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../helpers */ "./src/app/helpers.ts");









var MemoryComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](MemoryComponent, _super);
    function MemoryComponent(service, location, dialog) {
        var _this = _super.call(this, service, location) || this;
        _this.service = service;
        _this.location = location;
        _this.dialog = dialog;
        _this.displayed_columns = [
            'model',
            'variant',
            'num_classes',
            'batch_size',
            'img_size',
            'memory'
        ];
        _this.filter_hidden = true;
        _this.filter_applied_text = '';
        return _this;
    }
    MemoryComponent.prototype.onchange = function () {
        this.change.emit();
        var count = 0;
        if (this.model)
            count += 1;
        if (this.variant)
            count += 1;
        this.filter_applied_text = count > 0 ? "(" + count + " applied)" : '';
    };
    MemoryComponent.prototype.get_filter = function () {
        var res = new _models__WEBPACK_IMPORTED_MODULE_5__["MemoryFilter"]();
        res.paginator = _super.prototype.get_filter.call(this);
        res.model = this.model;
        res.variant = this.variant;
        return res;
    };
    MemoryComponent.prototype.add = function () {
        var _this = this;
        var dialogRef = this.dialog.open(_memory_add_dialog__WEBPACK_IMPORTED_MODULE_7__["MemoryAddDialogComponent"], {
            width: '600px', height: '700px',
            data: { 'name': '' }
        });
        dialogRef.afterClosed().subscribe(function (result) {
            if (result) {
                _this.service.add(result).subscribe(function (_) {
                    _this.change.emit();
                });
            }
        });
    };
    MemoryComponent.prototype.edit = function () {
        var _this = this;
        var dialogRef = this.dialog.open(_memory_add_dialog__WEBPACK_IMPORTED_MODULE_7__["MemoryAddDialogComponent"], {
            width: '600px', height: '700px',
            data: _helpers__WEBPACK_IMPORTED_MODULE_8__["Helpers"].clone(this.selected)
        });
        dialogRef.afterClosed().subscribe(function (result) {
            if (result) {
                _this.service.edit(result).subscribe(function (_) {
                    _this.change.emit();
                });
            }
        });
    };
    MemoryComponent.prototype.copy = function () {
        var _this = this;
        var dialogRef = this.dialog.open(_memory_add_dialog__WEBPACK_IMPORTED_MODULE_7__["MemoryAddDialogComponent"], {
            width: '600px', height: '700px',
            data: _helpers__WEBPACK_IMPORTED_MODULE_8__["Helpers"].clone(this.selected)
        });
        dialogRef.afterClosed().subscribe(function (result) {
            if (result) {
                _this.service.add(result).subscribe(function (_) {
                    _this.change.emit();
                });
            }
        });
    };
    MemoryComponent.prototype.remove = function () {
        var _this = this;
        this.service.remove(this.selected.id).subscribe(function (result) {
            _this.selected = null;
            _this.change.emit();
        });
    };
    MemoryComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-memory',
            template: __webpack_require__(/*! ./memory.component.html */ "./src/app/skynet/memory/memory.component.html"),
            styles: [__webpack_require__(/*! ./memory.component.css */ "./src/app/skynet/memory/memory.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_memory_service__WEBPACK_IMPORTED_MODULE_4__["MemoryService"],
            _angular_common__WEBPACK_IMPORTED_MODULE_3__["Location"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__["MatDialog"]])
    ], MemoryComponent);
    return MemoryComponent;
}(_paginator__WEBPACK_IMPORTED_MODULE_2__["Paginator"]));



/***/ }),

/***/ "./src/app/skynet/memory/memory.service.ts":
/*!*************************************************!*\
  !*** ./src/app/skynet/memory/memory.service.ts ***!
  \*************************************************/
/*! exports provided: MemoryService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MemoryService", function() { return MemoryService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _base_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../base.service */ "./src/app/base.service.ts");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../models */ "./src/app/models.ts");
/* harmony import */ var _app_settings__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../app-settings */ "./src/app/app-settings.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");






var MemoryService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](MemoryService, _super);
    function MemoryService() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.collection_part = 'memories';
        _this.single_part = 'memory';
        return _this;
    }
    MemoryService.prototype.add = function (data) {
        var message = this.constructor.name + ".add";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/add';
        return this.http.post(url, data).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["BaseResult"]())));
    };
    MemoryService.prototype.edit = function (data) {
        var message = this.constructor.name + ".edit";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/edit';
        return this.http.post(url, data).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["BaseResult"]())));
    };
    MemoryService.prototype.remove = function (id) {
        var message = this.constructor.name + ".remove";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/remove';
        return this.http.post(url, { 'id': id }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["BaseResult"]())));
    };
    MemoryService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Injectable"])({
            providedIn: 'root'
        })
    ], MemoryService);
    return MemoryService;
}(_base_service__WEBPACK_IMPORTED_MODULE_1__["BaseService"]));



/***/ }),

/***/ "./src/app/skynet/skynet-routing.module.ts":
/*!*************************************************!*\
  !*** ./src/app/skynet/skynet-routing.module.ts ***!
  \*************************************************/
/*! exports provided: SkynetRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SkynetRoutingModule", function() { return SkynetRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _skynet_skynet_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./skynet/skynet.component */ "./src/app/skynet/skynet/skynet.component.ts");
/* harmony import */ var _space_space_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./space/space.component */ "./src/app/skynet/space/space.component.ts");
/* harmony import */ var _memory_memory_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./memory/memory.component */ "./src/app/skynet/memory/memory.component.ts");






var routes = [
    {
        path: '',
        component: _skynet_skynet_component__WEBPACK_IMPORTED_MODULE_3__["SkynetComponent"],
        children: [
            { path: 'space', component: _space_space_component__WEBPACK_IMPORTED_MODULE_4__["SpaceComponent"] },
            { path: 'memory', component: _memory_memory_component__WEBPACK_IMPORTED_MODULE_5__["MemoryComponent"] },
        ]
    }
];
var SkynetRoutingModule = /** @class */ (function () {
    function SkynetRoutingModule() {
    }
    SkynetRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)
            ],
            exports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]
            ]
        })
    ], SkynetRoutingModule);
    return SkynetRoutingModule;
}());



/***/ }),

/***/ "./src/app/skynet/skynet.module.ts":
/*!*****************************************!*\
  !*** ./src/app/skynet/skynet.module.ts ***!
  \*****************************************/
/*! exports provided: SkynetModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SkynetModule", function() { return SkynetModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../shared.module */ "./src/app/shared.module.ts");
/* harmony import */ var _skynet_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./skynet-routing.module */ "./src/app/skynet/skynet-routing.module.ts");
/* harmony import */ var _skynet_skynet_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./skynet/skynet.component */ "./src/app/skynet/skynet/skynet.component.ts");
/* harmony import */ var _space_space_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./space/space.component */ "./src/app/skynet/space/space.component.ts");
/* harmony import */ var _memory_memory_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./memory/memory.component */ "./src/app/skynet/memory/memory.component.ts");
/* harmony import */ var _memory_memory_add_dialog__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./memory/memory-add-dialog */ "./src/app/skynet/memory/memory-add-dialog.ts");
/* harmony import */ var _space_space_add_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./space/space-add-dialog */ "./src/app/skynet/space/space-add-dialog.ts");
/* harmony import */ var _space_space_run_dialog__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./space/space-run-dialog */ "./src/app/skynet/space/space-run-dialog.ts");










var SkynetModule = /** @class */ (function () {
    function SkynetModule() {
    }
    SkynetModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [
                _skynet_routing_module__WEBPACK_IMPORTED_MODULE_3__["SkynetRoutingModule"],
                _shared_module__WEBPACK_IMPORTED_MODULE_2__["SharedModule"]
            ],
            declarations: [
                _skynet_skynet_component__WEBPACK_IMPORTED_MODULE_4__["SkynetComponent"],
                _space_space_component__WEBPACK_IMPORTED_MODULE_5__["SpaceComponent"],
                _memory_memory_component__WEBPACK_IMPORTED_MODULE_6__["MemoryComponent"],
                _memory_memory_add_dialog__WEBPACK_IMPORTED_MODULE_7__["MemoryAddDialogComponent"],
                _space_space_add_dialog__WEBPACK_IMPORTED_MODULE_8__["SpaceAddDialogComponent"],
                _space_space_run_dialog__WEBPACK_IMPORTED_MODULE_9__["SpaceRunDialogComponent"]
            ],
            entryComponents: [
                _memory_memory_add_dialog__WEBPACK_IMPORTED_MODULE_7__["MemoryAddDialogComponent"],
                _space_space_add_dialog__WEBPACK_IMPORTED_MODULE_8__["SpaceAddDialogComponent"],
                _space_space_run_dialog__WEBPACK_IMPORTED_MODULE_9__["SpaceRunDialogComponent"]
            ]
        })
    ], SkynetModule);
    return SkynetModule;
}());



/***/ }),

/***/ "./src/app/skynet/skynet/skynet.component.css":
/*!****************************************************!*\
  !*** ./src/app/skynet/skynet/skynet.component.css ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3NreW5ldC9za3luZXQvc2t5bmV0LmNvbXBvbmVudC5jc3MifQ== */"

/***/ }),

/***/ "./src/app/skynet/skynet/skynet.component.html":
/*!*****************************************************!*\
  !*** ./src/app/skynet/skynet/skynet.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<nav>\n  <a routerLink=\"./space\" routerLinkActive=\"active\">Space</a>\n  <a routerLink=\"./memory\" routerLinkActive=\"active\">Memory</a>\n</nav>\n\n<router-outlet></router-outlet>"

/***/ }),

/***/ "./src/app/skynet/skynet/skynet.component.ts":
/*!***************************************************!*\
  !*** ./src/app/skynet/skynet/skynet.component.ts ***!
  \***************************************************/
/*! exports provided: SkynetComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SkynetComponent", function() { return SkynetComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");


var SkynetComponent = /** @class */ (function () {
    function SkynetComponent() {
    }
    SkynetComponent.prototype.ngOnInit = function () {
    };
    SkynetComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-skynet',
            template: __webpack_require__(/*! ./skynet.component.html */ "./src/app/skynet/skynet/skynet.component.html"),
            styles: [__webpack_require__(/*! ./skynet.component.css */ "./src/app/skynet/skynet/skynet.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [])
    ], SkynetComponent);
    return SkynetComponent;
}());



/***/ }),

/***/ "./src/app/skynet/space/space-add-dialog.html":
/*!****************************************************!*\
  !*** ./src/app/skynet/space/space-add-dialog.html ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div mat-dialog-content>\n    <mat-form-field>\n        <mat-label>Name</mat-label>\n        <input matInput [(ngModel)]=\"data.space.name\">\n    </mat-form-field>\n</div>\n\n\n<div mat-dialog-content>\n    <mat-form-field style=\"width: 400px\">\n        <mat-label>Content</mat-label>\n        <textarea\n            #textarea\n            matInput\n            [(ngModel)]=\"data.space.content\"\n            (keyup)=\"key_up($event)\"\n            (keydown)=\"key_down($event)\"\n            style=\"height:300px;width: 300px\">\n\n      </textarea>\n    </mat-form-field>\n</div>\n\n<pre style=\"color: red\" *ngIf=\"error\">\n    Error:\n\n    {{error}}\n</pre>\n\n<div mat-dialog-actions>\n    <button mat-button (click)=\"onNoClick()\">Cancel</button>\n    <button mat-button (click)=\"on_ok_click()\" cdkFocusInitial>Ok</button>\n</div>\n\n"

/***/ }),

/***/ "./src/app/skynet/space/space-add-dialog.ts":
/*!**************************************************!*\
  !*** ./src/app/skynet/space/space-add-dialog.ts ***!
  \**************************************************/
/*! exports provided: SpaceAddDialogComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SpaceAddDialogComponent", function() { return SpaceAddDialogComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_material__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/material */ "./node_modules/@angular/material/esm5/material.es5.js");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../models */ "./src/app/models.ts");
/* harmony import */ var _space_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./space.service */ "./src/app/skynet/space/space.service.ts");
/* harmony import */ var _helpers__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../helpers */ "./src/app/helpers.ts");






var SpaceAddDialogComponent = /** @class */ (function () {
    function SpaceAddDialogComponent(dialogRef, data, service) {
        this.dialogRef = dialogRef;
        this.data = data;
        this.service = service;
    }
    SpaceAddDialogComponent.prototype.onNoClick = function () {
        this.dialogRef.close();
    };
    SpaceAddDialogComponent.prototype.on_ok_click = function () {
        var _this = this;
        if (this.data.method == 'add') {
            this.service.add(this.data.space).subscribe(function (res) {
                _this.error = res.error;
                if (res.success) {
                    _this.dialogRef.close();
                }
            });
        }
        else if (this.data.method == 'edit') {
            this.service.edit(this.data.space).subscribe(function (res) {
                _this.error = res.error;
                if (res.success) {
                    _this.dialogRef.close();
                }
            });
        }
        else if (this.data.method == 'copy') {
            this.service.copy(this.data.space, this.data.old_space).subscribe(function (res) {
                _this.error = res.error;
                if (res.success) {
                    _this.dialogRef.close();
                }
            });
        }
    };
    SpaceAddDialogComponent.prototype.key_down = function (event) {
        var content = _helpers__WEBPACK_IMPORTED_MODULE_5__["Helpers"].handle_textarea_down_key(event, this.textarea.nativeElement);
        if (content) {
            this.data.space.content = content;
        }
    };
    SpaceAddDialogComponent.prototype.key_up = function (event) {
        this.data.space.content = event.target.value;
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])('textarea'),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], SpaceAddDialogComponent.prototype, "textarea", void 0);
    SpaceAddDialogComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'space-add-dialog',
            template: __webpack_require__(/*! ./space-add-dialog.html */ "./src/app/skynet/space/space-add-dialog.html"),
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__param"](1, Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"])(_angular_material__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"])),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_material__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"],
            _models__WEBPACK_IMPORTED_MODULE_3__["SpaceAdd"],
            _space_service__WEBPACK_IMPORTED_MODULE_4__["SpaceService"]])
    ], SpaceAddDialogComponent);
    return SpaceAddDialogComponent;
}());



/***/ }),

/***/ "./src/app/skynet/space/space-run-dialog.html":
/*!****************************************************!*\
  !*** ./src/app/skynet/space/space-run-dialog.html ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-dags use_select=\"True\" default_page_size=\"5\">\n\n</app-dags>\n\n<div mat-dialog-content>\n    <mat-form-field style=\"width: 300px\">\n        <mat-label>File changes</mat-label>\n        <textarea\n            #textarea\n            matInput\n            [(ngModel)]=\"data.file_changes\"\n            (keyup)=\"key_up($event)\"\n            (keydown)=\"key_down($event)\"\n            style=\"height:300px;width: 600px\">\n\n      </textarea>\n    </mat-form-field>\n</div>\n\n<pre style=\"color: red\" *ngIf=\"error\">\n    Error:\n\n    {{error}}\n</pre>\n\n<div mat-dialog-actions>\n    <button mat-button (click)=\"onNoClick()\">Cancel</button>\n    <button mat-button (click)=\"on_ok_click()\" cdkFocusInitial\n            [disabled]=\"!dags.selected\">Ok\n    </button>\n</div>\n\n"

/***/ }),

/***/ "./src/app/skynet/space/space-run-dialog.ts":
/*!**************************************************!*\
  !*** ./src/app/skynet/space/space-run-dialog.ts ***!
  \**************************************************/
/*! exports provided: SpaceRunDialogComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SpaceRunDialogComponent", function() { return SpaceRunDialogComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_material__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/material */ "./node_modules/@angular/material/esm5/material.es5.js");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../models */ "./src/app/models.ts");
/* harmony import */ var _space_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./space.service */ "./src/app/skynet/space/space.service.ts");
/* harmony import */ var _dag_dags_dags_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../dag/dags/dags.component */ "./src/app/dag/dags/dags.component.ts");
/* harmony import */ var _helpers__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../helpers */ "./src/app/helpers.ts");







var SpaceRunDialogComponent = /** @class */ (function () {
    function SpaceRunDialogComponent(dialogRef, data, service) {
        this.dialogRef = dialogRef;
        this.data = data;
        this.service = service;
    }
    SpaceRunDialogComponent.prototype.onNoClick = function () {
        this.dialogRef.close();
    };
    SpaceRunDialogComponent.prototype.on_ok_click = function () {
        var _this = this;
        this.data.dag = this.dags.selected.id;
        this.service.run(this.data).subscribe(function (res) {
            if (res.success) {
                _this.dialogRef.close();
            }
            else {
                _this.error = res.error;
            }
        });
    };
    SpaceRunDialogComponent.prototype.key_down = function (event) {
        var content = _helpers__WEBPACK_IMPORTED_MODULE_6__["Helpers"].handle_textarea_down_key(event, this.textarea.nativeElement);
        if (content) {
            this.data.file_changes = content;
        }
    };
    SpaceRunDialogComponent.prototype.key_up = function (event) {
        this.data.file_changes = event.target.value;
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])(_dag_dags_dags_component__WEBPACK_IMPORTED_MODULE_5__["DagsComponent"]),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], SpaceRunDialogComponent.prototype, "dags", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])('textarea'),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", Object)
    ], SpaceRunDialogComponent.prototype, "textarea", void 0);
    SpaceRunDialogComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'space-run-dialog',
            template: __webpack_require__(/*! ./space-run-dialog.html */ "./src/app/skynet/space/space-run-dialog.html"),
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__param"](1, Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"])(_angular_material__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"])),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_angular_material__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"],
            _models__WEBPACK_IMPORTED_MODULE_3__["SpaceRun"],
            _space_service__WEBPACK_IMPORTED_MODULE_4__["SpaceService"]])
    ], SpaceRunDialogComponent);
    return SpaceRunDialogComponent;
}());



/***/ }),

/***/ "./src/app/skynet/space/space.component.css":
/*!**************************************************!*\
  !*** ./src/app/skynet/space/space.component.css ***!
  \**************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "table {\n  width: 100%;\n  min-width: 800px;\n}\n\n.column {\n  float: left;\n  width: 45%;\n}\n\n/* Clear floats after the columns */\n\n.row:after {\n  content: \"\";\n  display: table;\n  clear: both;\n}\n\n.mat-header-cell{\n  text-align: center !important;\n}\n\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvc2t5bmV0L3NwYWNlL3NwYWNlLmNvbXBvbmVudC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxXQUFXO0VBQ1gsZ0JBQWdCO0FBQ2xCOztBQUVBO0VBQ0UsV0FBVztFQUNYLFVBQVU7QUFDWjs7QUFFQSxtQ0FBbUM7O0FBQ25DO0VBQ0UsV0FBVztFQUNYLGNBQWM7RUFDZCxXQUFXO0FBQ2I7O0FBRUE7RUFDRSw2QkFBNkI7QUFDL0IiLCJmaWxlIjoic3JjL2FwcC9za3luZXQvc3BhY2Uvc3BhY2UuY29tcG9uZW50LmNzcyIsInNvdXJjZXNDb250ZW50IjpbInRhYmxlIHtcbiAgd2lkdGg6IDEwMCU7XG4gIG1pbi13aWR0aDogODAwcHg7XG59XG5cbi5jb2x1bW4ge1xuICBmbG9hdDogbGVmdDtcbiAgd2lkdGg6IDQ1JTtcbn1cblxuLyogQ2xlYXIgZmxvYXRzIGFmdGVyIHRoZSBjb2x1bW5zICovXG4ucm93OmFmdGVyIHtcbiAgY29udGVudDogXCJcIjtcbiAgZGlzcGxheTogdGFibGU7XG4gIGNsZWFyOiBib3RoO1xufVxuXG4ubWF0LWhlYWRlci1jZWxse1xuICB0ZXh0LWFsaWduOiBjZW50ZXIgIWltcG9ydGFudDtcbn1cbiJdfQ== */"

/***/ }),

/***/ "./src/app/skynet/space/space.component.html":
/*!***************************************************!*\
  !*** ./src/app/skynet/space/space.component.html ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"row\">\n\n    <div class=\"column\">\n        <button mat-raised-button style=\"margin-top: 15px\"\n                (click)=\"filter_hidden=!filter_hidden\">\n            Filters {{filter_applied_text}}\n        </button>\n\n        <div [hidden]=\"filter_hidden\">\n            <mat-form-field style=\"width: 150px\">\n                <input matInput (keyup)=\"name=$event.target.value;onchange()\"\n                       placeholder=\"Name\">\n            </mat-form-field>\n\n\n            <mat-form-field\n                    class=\"example-chip-list\"\n                    (click)=\"update_filter_all_tags()\"\n                    (keyup)=\"update_filter_all_tags($event)\">\n                <mat-chip-list #chipFilter>\n                    <mat-chip\n                            *ngFor=\"let tag of filter_tags\"\n                            [selectable]=\"false\"\n                            [removable]=\"true\"\n                            (removed)=\"filter_remove_tag(tag)\">\n                        {{tag}}\n\n\n                        <mat-icon matChipRemove\n                                  svgIcon=\"delete\"></mat-icon>\n                    </mat-chip>\n\n                    <input\n                            placeholder=\"Tags\"\n                            [matAutocomplete]=\"autoFilter\"\n                            [matChipInputFor]=\"chipFilter\"\n                            [matChipInputSeparatorKeyCodes]=\"separatorKeysCodes\"\n                            (matChipInputTokenEnd)=\"filter_tag_add($event)\">\n                </mat-chip-list>\n\n                <mat-autocomplete #autoFilter=\"matAutocomplete\"\n                                  (optionSelected)=\"filter_tag_selected($event)\">\n                    <mat-option *ngFor=\"let tag of filter_all_tags\"\n                                [value]=\"tag\">\n                        {{tag}}\n                    </mat-option>\n                </mat-autocomplete>\n\n            </mat-form-field>\n\n\n        </div>\n\n        <button mat-raised-button\n                style=\"margin-top: 15px\"\n                (click)=\"run()\">\n            Run\n        </button>\n\n\n        <button mat-raised-button\n                style=\"margin-top: 15px\"\n                (click)=\"add()\">\n            Add\n        </button>\n\n        <button mat-raised-button\n                style=\"margin-top: 15px\"\n                [disabled]=\"selected==null\"\n                (click)=\"edit()\">\n            Edit\n        </button>\n\n\n        <button mat-raised-button\n                style=\"margin-top: 15px\"\n                [disabled]=\"selected==null\"\n                (click)=\"copy()\">\n            Copy\n        </button>\n\n\n        <button mat-raised-button\n                style=\"margin-top: 15px\"\n                [disabled]=\"selected==null\"\n                (click)=\"remove()\">\n            Remove\n        </button>\n\n\n        <div class=\"mat-elevation-z8\" style=\"margin-bottom: 30px\">\n            <table mat-table [dataSource]=\"dataSource\" matSort>\n\n                <ng-container matColumnDef=\"name\">\n                    <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                        Name\n                    </th>\n\n                    <td mat-cell *matCellDef=\"let element\">\n                        {{element.name}}\n                    </td>\n                </ng-container>\n\n                <ng-container matColumnDef=\"created\">\n                    <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                        Created\n                    </th>\n\n                    <td mat-cell *matCellDef=\"let element\">\n                        {{element.created| date:\"MM.dd H:mm:ss\"}}\n                    </td>\n                </ng-container>\n\n                <ng-container matColumnDef=\"changed\">\n                    <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                        Changed\n                    </th>\n\n                    <td mat-cell *matCellDef=\"let element\">\n                        {{element.changed| date:\"MM.dd H:mm:ss\"}}\n                    </td>\n                </ng-container>\n\n\n                <ng-container matColumnDef=\"tags\">\n                    <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                        Tags\n                    </th>\n\n                    <td mat-cell *matCellDef=\"let element\">\n\n                        <mat-form-field class=\"example-chip-list\"\n                                        (click)=\"update_tags()\"\n                                        (keyup)=\"update_tags($event)\">\n                            <mat-chip-list #chipList>\n                                <mat-chip\n                                        *ngFor=\"let tag of element.tags\"\n                                        [selectable]=\"false\"\n                                        [removable]=\"true\"\n                                        (removed)=\"remove_tag(element, tag)\">\n                                    {{tag}}\n                                    <mat-icon matChipRemove\n                                              svgIcon=\"delete\"></mat-icon>\n                                </mat-chip>\n\n                                <input\n                                        placeholder=\"\"\n                                        [matAutocomplete]=\"auto\"\n                                        [matChipInputFor]=\"chipList\"\n                                        [matChipInputSeparatorKeyCodes]=\"separatorKeysCodes\"\n                                        (matChipInputTokenEnd)=\"tag_add(element, $event)\">\n                            </mat-chip-list>\n\n                            <mat-autocomplete #auto=\"matAutocomplete\"\n                                              (optionSelected)=\"tag_selected(element, $event)\">\n                                <mat-option *ngFor=\"let tag of tags\"\n                                            [value]=\"tag\">\n                                    {{tag}}\n                                </mat-option>\n                            </mat-autocomplete>\n\n                        </mat-form-field>\n\n                    </td>\n                </ng-container>\n\n\n                <tr mat-header-row *matHeaderRowDef=\"displayed_columns\"></tr>\n                <tr mat-row *matRowDef=\"let row; columns: displayed_columns;\"\n                    (click)=\"onSelected(row)\"\n                    [style.background]=\"selected==row ? 'lightblue' : ''\"></tr>\n            </table>\n\n            <mat-paginator [pageSizeOptions]=\"[10, 30, 100]\"\n                           [length]=\"total\"\n                           [pageSize]=\"10\">\n\n            </mat-paginator>\n\n\n            <mat-form-field\n                    (click)=\"update_names()\"\n                    (keyup)=\"update_names($event)\"\n                    class=\"example-chip-list\">\n                <mat-chip-list #chipList>\n                    <mat-chip\n                            *ngFor=\"let space of chosen_spaces\"\n                            [selectable]=\"false\"\n                            [removable]=\"true\"\n                            (removed)=\"space.type=='const'?chosen_remove_space(space):chosen_fix_space(space)\">\n                        {{space.value}}\n\n\n                        <mat-icon matChipRemove\n                                  svgIcon=\"delete\"\n                                  *ngIf=\"space.type=='const'\"></mat-icon>\n                        <mat-icon matChipRemove svgIcon=\"pin\"\n                                  *ngIf=\"space.type=='tmp'\"></mat-icon>\n                    </mat-chip>\n\n                    <input\n                            placeholder=\"\"\n                            [matAutocomplete]=\"auto\"\n                            [matChipInputFor]=\"chipList\"\n                            [matChipInputSeparatorKeyCodes]=\"separatorKeysCodes\"\n                            (matChipInputTokenEnd)=\"chosen_space_add($event)\">\n                </mat-chip-list>\n\n                <mat-autocomplete #auto=\"matAutocomplete\"\n                                  (optionSelected)=\"chosen_space_selected($event)\">\n                    <mat-option *ngFor=\"let name of names\"\n                                [value]=\"name\">\n                        {{name}}\n                    </mat-option>\n                </mat-autocomplete>\n\n            </mat-form-field>\n\n\n        </div>\n    </div>\n\n    <div class=\"column\" style=\"margin-left: 5%; width: 50% !important;\">\n        <button mat-raised-button style=\"margin-top: 15px\"\n                (click)=\"relation_filter_hidden=!relation_filter_hidden\">\n            Filters {{relation_filter_applied_text}}\n        </button>\n\n        <div [hidden]=\"relation_filter_hidden\">\n            <mat-form-field style=\"width: 150px\">\n                <input matInput\n                       (keyup)=\"relation_name=$event.target.value;relation_changed()\"\n                       placeholder=\"Name\">\n            </mat-form-field>\n\n\n            <mat-form-field\n                    class=\"example-chip-list\"\n                    (click)=\"update_filter_all_tags_related()\"\n                    (keyup)=\"update_filter_all_tags_related($event)\">\n                <mat-chip-list #chipFilterRelated>\n                    <mat-chip\n                            *ngFor=\"let tag of filter_tags_related\"\n                            [selectable]=\"false\"\n                            [removable]=\"true\"\n                            (removed)=\"filter_remove_tag_related(tag)\">\n                        {{tag}}\n\n\n                        <mat-icon matChipRemove\n                                  svgIcon=\"delete\"></mat-icon>\n                    </mat-chip>\n\n                    <input\n                            placeholder=\"Tags\"\n                            [matAutocomplete]=\"autoFilterRelated\"\n                            [matChipInputFor]=\"chipFilterRelated\"\n                            [matChipInputSeparatorKeyCodes]=\"separatorKeysCodes\"\n                            (matChipInputTokenEnd)=\"filter_tag_add_related($event)\">\n                </mat-chip-list>\n\n                <mat-autocomplete #autoFilterRelated=\"matAutocomplete\"\n                                  (optionSelected)=\"filter_tag_selected_related($event)\">\n                    <mat-option *ngFor=\"let tag of filter_all_tags_related\"\n                                [value]=\"tag\">\n                        {{tag}}\n                    </mat-option>\n                </mat-autocomplete>\n\n            </mat-form-field>\n\n        </div>\n\n        <button mat-raised-button\n                style=\"margin-top: 15px\"\n                [disabled]=\"relation_selected==null || relation_selected.relation==1\"\n                (click)=\"relation_append()\">\n            Append\n        </button>\n\n        <button mat-raised-button\n                style=\"margin-top: 15px\"\n                [disabled]=\"relation_selected==null || !relation_selected.relation\"\n                (click)=\"relation_remove()\">\n            Remove\n        </button>\n\n\n        <div class=\"mat-elevation-z8\">\n            <table mat-table [dataSource]=\"relation_dataSource\" matSort\n                   #relation_sort=\"matSort\">\n\n                <ng-container matColumnDef=\"name\">\n                    <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                        Name\n                    </th>\n\n                    <td mat-cell *matCellDef=\"let element\">\n                        {{element.name}}\n                    </td>\n                </ng-container>\n\n                <ng-container matColumnDef=\"created\">\n                    <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                        Created\n                    </th>\n\n                    <td mat-cell *matCellDef=\"let element\">\n                        {{element.created| date:\"MM.dd H:mm:ss\"}}\n                    </td>\n                </ng-container>\n\n                <ng-container matColumnDef=\"changed\">\n                    <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                        Changed\n                    </th>\n\n                    <td mat-cell *matCellDef=\"let element\">\n                        {{element.changed| date:\"MM.dd H:mm:ss\"}}\n                    </td>\n                </ng-container>\n\n                <ng-container matColumnDef=\"tags\">\n                    <th mat-header-cell *matHeaderCellDef mat-sort-header>\n                        Tags\n                    </th>\n\n                    <td mat-cell *matCellDef=\"let element\">\n\n                        <mat-form-field class=\"example-chip-list\"\n                                        (click)=\"update_tags()\"\n                                        (keyup)=\"update_tags($event)\">\n                            <mat-chip-list #chipList>\n                                <mat-chip\n                                        *ngFor=\"let tag of element.tags\"\n                                        [selectable]=\"false\"\n                                        [removable]=\"true\"\n                                        (removed)=\"remove_tag(element, tag)\">\n                                    {{tag}}\n                                    <mat-icon matChipRemove\n                                              svgIcon=\"delete\"></mat-icon>\n                                </mat-chip>\n\n                                <input\n                                        placeholder=\"\"\n                                        [matAutocomplete]=\"auto\"\n                                        [matChipInputFor]=\"chipList\"\n                                        [matChipInputSeparatorKeyCodes]=\"separatorKeysCodes\"\n                                        (matChipInputTokenEnd)=\"tag_add(element, $event)\">\n                            </mat-chip-list>\n\n                            <mat-autocomplete #auto=\"matAutocomplete\"\n                                              (optionSelected)=\"tag_selected(element, $event)\">\n                                <mat-option *ngFor=\"let tag of tags\"\n                                            [value]=\"tag\">\n                                    {{tag}}\n                                </mat-option>\n                            </mat-autocomplete>\n\n                        </mat-form-field>\n\n                    </td>\n                </ng-container>\n\n\n                <tr mat-header-row *matHeaderRowDef=\"displayed_columns\"></tr>\n                <tr mat-row *matRowDef=\"let row; columns: displayed_columns;\"\n                    (click)=\"relation_selected=row\"\n                    [style.background]=\"relation_selected==row ?\n            'lightblue' : row.relation? '#2ECC71': ''\">\n\n                </tr>\n            </table>\n\n            <mat-paginator [pageSizeOptions]=\"[10, 30, 100]\"\n                           [length]=\"relation_total\"\n                           #relation_paginator\n                           [pageSize]=\"10\">\n\n            </mat-paginator>\n\n        </div>\n\n    </div>\n\n</div>\n"

/***/ }),

/***/ "./src/app/skynet/space/space.component.ts":
/*!*************************************************!*\
  !*** ./src/app/skynet/space/space.component.ts ***!
  \*************************************************/
/*! exports provided: SpaceComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SpaceComponent", function() { return SpaceComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _paginator__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../paginator */ "./src/app/paginator.ts");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../models */ "./src/app/models.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm5/dialog.es5.js");
/* harmony import */ var _space_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./space.service */ "./src/app/skynet/space/space.service.ts");
/* harmony import */ var _helpers__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../helpers */ "./src/app/helpers.ts");
/* harmony import */ var _space_add_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./space-add-dialog */ "./src/app/skynet/space/space-add-dialog.ts");
/* harmony import */ var _angular_material_table__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/table */ "./node_modules/@angular/material/esm5/table.es5.js");
/* harmony import */ var _angular_material_paginator__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/paginator */ "./node_modules/@angular/material/esm5/paginator.es5.js");
/* harmony import */ var _angular_material_sort__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/material/sort */ "./node_modules/@angular/material/esm5/sort.es5.js");
/* harmony import */ var _space_run_dialog__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./space-run-dialog */ "./src/app/skynet/space/space-run-dialog.ts");
/* harmony import */ var _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/cdk/keycodes */ "./node_modules/@angular/cdk/esm5/keycodes.es5.js");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/icon */ "./node_modules/@angular/material/esm5/icon.es5.js");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm5/platform-browser.js");
















var SpaceComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](SpaceComponent, _super);
    function SpaceComponent(service, location, dialog, iconRegistry, sanitizer) {
        var _this = _super.call(this, service, location) || this;
        _this.service = service;
        _this.location = location;
        _this.dialog = dialog;
        _this.displayed_columns = [
            'name',
            'created',
            'changed',
            'tags'
        ];
        _this.filter_hidden = true;
        _this.filter_applied_text = '';
        _this.relation_dataSource = new _angular_material_table__WEBPACK_IMPORTED_MODULE_9__["MatTableDataSource"]();
        _this.relation_total = 0;
        _this.relation_filter_hidden = true;
        _this.relation_filter_applied_text = '';
        _this.separatorKeysCodes = [_angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_13__["ENTER"], _angular_cdk_keycodes__WEBPACK_IMPORTED_MODULE_13__["COMMA"]];
        _this.tags = [];
        _this.chosen_spaces = [];
        _this.names = [];
        _this.filter_tags = [];
        _this.filter_all_tags = [];
        _this.filter_tags_related = [];
        _this.filter_all_tags_related = [];
        _this.id_column = 'name';
        iconRegistry.addSvgIcon('delete', sanitizer.bypassSecurityTrustResourceUrl('assets/img/delete.svg'));
        iconRegistry.addSvgIcon('pin', sanitizer.bypassSecurityTrustResourceUrl('assets/img/pin.svg'));
        return _this;
    }
    SpaceComponent.prototype.filter_remove_tag = function (tag) {
        var index = this.filter_tags.indexOf(tag);
        this.filter_tags.splice(index, 1);
        this.change.emit();
    };
    SpaceComponent.prototype.filter_remove_tag_related = function (tag) {
        var index = this.filter_tags_related.indexOf(tag);
        this.filter_tags_related.splice(index, 1);
        this.relation_changed();
    };
    SpaceComponent.prototype.filter_tag_add = function (event) {
        var input = event.input;
        var value = event.value;
        // Add our fruit
        if ((value || '').trim()) {
            value = value.trim();
            this.filter_tags.push(value);
        }
        // Reset the input value
        if (input) {
            input.value = '';
        }
        this.change.emit();
    };
    SpaceComponent.prototype.filter_tag_add_related = function (event) {
        var input = event.input;
        var value = event.value;
        // Add our fruit
        if ((value || '').trim()) {
            value = value.trim();
            this.filter_tags_related.push(value);
        }
        // Reset the input value
        if (input) {
            input.value = '';
        }
        this.relation_changed();
    };
    SpaceComponent.prototype.filter_tag_selected = function (event) {
        this.filter_tags.push(event.option.viewValue);
        this.change.emit();
    };
    SpaceComponent.prototype.filter_tag_selected_related = function (event) {
        this.filter_tags_related.push(event.option.viewValue);
        this.relation_changed();
    };
    SpaceComponent.prototype.chosen_remove_space = function (space) {
        var index = this.chosen_spaces.indexOf(space);
        this.chosen_spaces.splice(index, 1);
    };
    SpaceComponent.prototype.chosen_fix_space = function (space) {
        space.type = 'const';
    };
    SpaceComponent.prototype.chosen_space_add = function (event) {
        var input = event.input;
        var value = event.value;
        // Add our fruit
        if ((value || '').trim()) {
            value = value.trim();
            this.chosen_spaces.push({ 'value': value, 'type': 'const' });
        }
        // Reset the input value
        if (input) {
            input.value = '';
        }
    };
    SpaceComponent.prototype.chosen_space_selected = function (event) {
        this.chosen_spaces.push({
            'value': event.option.viewValue,
            'type': 'const'
        });
    };
    SpaceComponent.prototype.onchange = function () {
        this.change.emit();
        var count = 0;
        if (this.name)
            count += 1;
        this.filter_applied_text = count > 0 ? "(" + count + " applied)" : '';
    };
    SpaceComponent.prototype.get_filter = function () {
        var res = new _models__WEBPACK_IMPORTED_MODULE_3__["SpaceFilter"]();
        res.paginator = _super.prototype.get_filter.call(this);
        res.name = this.name;
        res.tags = this.filter_tags;
        return res;
    };
    SpaceComponent.prototype._ngOnInit = function () {
        var _this = this;
        _super.prototype._ngOnInit.call(this);
        this.relation_paginator.page.subscribe(function (x) {
            _this.relation_changed();
        });
        this.relation_sort.sortChange.subscribe(function (x) {
            _this.relation_changed();
        });
    };
    SpaceComponent.prototype.update_tags = function (event) {
        var _this = this;
        if (event === void 0) { event = null; }
        var name = '';
        if (event) {
            name = event.target.value;
        }
        this.service.tags({ 'name': name }).subscribe(function (x) {
            _this.tags = x.tags;
        });
    };
    SpaceComponent.prototype.update_names = function (event) {
        var _this = this;
        if (event === void 0) { event = null; }
        var name = '';
        if (event) {
            name = event.target.value;
        }
        this.service.names({ 'name': name }).subscribe(function (x) {
            _this.names = x.names;
        });
    };
    SpaceComponent.prototype.update_filter_all_tags = function (event) {
        var _this = this;
        if (event === void 0) { event = null; }
        var name = '';
        if (event) {
            name = event.target.value;
        }
        this.service.tags({ 'name': name }).subscribe(function (x) {
            _this.filter_all_tags = x.tags;
        });
    };
    SpaceComponent.prototype.update_filter_all_tags_related = function (event) {
        var _this = this;
        if (event === void 0) { event = null; }
        var name = '';
        if (event) {
            name = event.target.value;
        }
        this.service.tags({ 'name': name }).subscribe(function (x) {
            _this.filter_all_tags_related = x.tags;
        });
    };
    SpaceComponent.prototype.run = function () {
        this.dialog.open(_space_run_dialog__WEBPACK_IMPORTED_MODULE_12__["SpaceRunDialogComponent"], {
            width: '2000px', height: '900px',
            data: { 'spaces': this.chosen_spaces.map(function (x) { return x.value; }) }
        });
    };
    SpaceComponent.prototype.add = function () {
        var _this = this;
        var dialogRef = this.dialog.open(_space_add_dialog__WEBPACK_IMPORTED_MODULE_8__["SpaceAddDialogComponent"], {
            width: '600px', height: '700px',
            data: { method: 'add', space: { 'name': '' } }
        });
        dialogRef.afterClosed().subscribe(function (result) {
            _this.change.emit();
        });
    };
    SpaceComponent.prototype.edit = function () {
        var _this = this;
        var dialogRef = this.dialog.open(_space_add_dialog__WEBPACK_IMPORTED_MODULE_8__["SpaceAddDialogComponent"], {
            width: '600px', height: '700px',
            data: { method: 'edit', space: _helpers__WEBPACK_IMPORTED_MODULE_7__["Helpers"].clone(this.selected) }
        });
        dialogRef.afterClosed().subscribe(function (result) {
            _this.change.emit();
        });
    };
    SpaceComponent.prototype.copy = function () {
        var _this = this;
        var dialogRef = this.dialog.open(_space_add_dialog__WEBPACK_IMPORTED_MODULE_8__["SpaceAddDialogComponent"], {
            width: '600px', height: '700px',
            data: {
                method: 'copy',
                space: _helpers__WEBPACK_IMPORTED_MODULE_7__["Helpers"].clone(this.selected),
                'old_space': this.selected.name
            }
        });
        dialogRef.afterClosed().subscribe(function (result) {
            _this.change.emit();
        });
    };
    SpaceComponent.prototype.remove = function () {
        var _this = this;
        this.service.remove(this.selected.name).subscribe(function (result) {
            _this.selected = null;
            _this.relation_selected = null;
            _this.relation_dataSource.data = [];
            _this.relation_paginator.pageIndex = 0;
            _this.change.emit();
        });
    };
    SpaceComponent.prototype.relation_changed = function () {
        var _this = this;
        var filter = {
            'parent': this.selected.name,
            'paginator': {
                'page_number': this.relation_paginator.pageIndex,
                'page_size': this.relation_paginator.pageSize,
                'sort_column': this.relation_sort.active ? this.relation_sort.active : '',
                'sort_descending': this.relation_sort.direction ?
                    this.relation_sort.direction == 'desc' : true
            },
            'name': this.relation_name,
            'tags': this.filter_tags_related
        };
        this.service.get_paginator(filter).subscribe(function (res) {
            _this.relation_dataSource.data = res.data;
            _this.relation_total = res.total;
        });
    };
    SpaceComponent.prototype.onSelected = function (row) {
        if (this.chosen_spaces.length > 0) {
            var last_index = this.chosen_spaces.length - 1;
            if (this.chosen_spaces[last_index].type == 'tmp') {
                this.chosen_spaces.splice(last_index, 1);
            }
        }
        var found = false;
        for (var _i = 0, _a = this.chosen_spaces; _i < _a.length; _i++) {
            var s = _a[_i];
            if (s.value == row.name) {
                found = true;
                break;
            }
        }
        if (!found) {
            this.chosen_spaces.push({ 'value': row.name, 'type': 'tmp' });
        }
        this.selected = row;
        this.relation_selected = null;
        this.relation_paginator.pageIndex = 0;
        this.relation_changed();
    };
    SpaceComponent.prototype.relation_append = function () {
        var _this = this;
        this.service.relation_append(this.selected.name, this.relation_selected.name).subscribe(function (res) {
            _this.relation_changed();
        });
    };
    SpaceComponent.prototype.relation_remove = function () {
        var _this = this;
        this.service.relation_remove(this.selected.name, this.relation_selected.name).subscribe(function (res) {
            _this.relation_changed();
        });
    };
    SpaceComponent.prototype.remove_tag = function (space, tag) {
        var _this = this;
        this.service.tag_remove(space.name, tag).subscribe(function (res) {
            _this.change.emit();
        });
        this.relation_changed();
    };
    SpaceComponent.prototype.tag_add = function (space, event) {
        var input = event.input;
        var value = event.value;
        // Add our fruit
        if ((value || '').trim()) {
            value = value.trim();
            space.tags.push(value);
            this.service.tag_add(space.name, value).subscribe(function (res) {
            });
        }
        // Reset the input value
        if (input) {
            input.value = '';
        }
        this.relation_changed();
    };
    SpaceComponent.prototype.tag_selected = function (space, event) {
        this.service.tag_add(space.name, event.option.viewValue).subscribe(function (res) {
        });
        space.tags.push(event.option.viewValue);
        this.relation_changed();
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])('relation_paginator'),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _angular_material_paginator__WEBPACK_IMPORTED_MODULE_10__["MatPaginator"])
    ], SpaceComponent.prototype, "relation_paginator", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])('relation_sort'),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:type", _angular_material_sort__WEBPACK_IMPORTED_MODULE_11__["MatSort"])
    ], SpaceComponent.prototype, "relation_sort", void 0);
    SpaceComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-space',
            template: __webpack_require__(/*! ./space.component.html */ "./src/app/skynet/space/space.component.html"),
            styles: [__webpack_require__(/*! ./space.component.css */ "./src/app/skynet/space/space.component.css")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [_space_service__WEBPACK_IMPORTED_MODULE_6__["SpaceService"],
            _angular_common__WEBPACK_IMPORTED_MODULE_4__["Location"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialog"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_14__["MatIconRegistry"],
            _angular_platform_browser__WEBPACK_IMPORTED_MODULE_15__["DomSanitizer"]])
    ], SpaceComponent);
    return SpaceComponent;
}(_paginator__WEBPACK_IMPORTED_MODULE_2__["Paginator"]));



/***/ }),

/***/ "./src/app/skynet/space/space.service.ts":
/*!***********************************************!*\
  !*** ./src/app/skynet/space/space.service.ts ***!
  \***********************************************/
/*! exports provided: SpaceService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SpaceService", function() { return SpaceService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _base_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../base.service */ "./src/app/base.service.ts");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _models__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../models */ "./src/app/models.ts");
/* harmony import */ var _app_settings__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../app-settings */ "./src/app/app-settings.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");






var SpaceService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](SpaceService, _super);
    function SpaceService() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.collection_part = 'spaces';
        _this.single_part = 'space';
        return _this;
    }
    SpaceService.prototype.add = function (data) {
        var message = this.constructor.name + ".add";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/add';
        return this.http.post(url, data).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["BaseResult"]())));
    };
    SpaceService.prototype.copy = function (data, old_space) {
        var message = this.constructor.name + ".copy";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/copy';
        return this.http.post(url, {
            'space': data,
            'old_space': old_space
        }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["BaseResult"]())));
    };
    SpaceService.prototype.edit = function (data) {
        var message = this.constructor.name + ".edit";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/edit';
        return this.http.post(url, data).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["BaseResult"]())));
    };
    SpaceService.prototype.remove = function (name) {
        var message = this.constructor.name + ".remove";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/remove';
        return this.http.post(url, { 'name': name }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["BaseResult"]())));
    };
    SpaceService.prototype.relation_append = function (parent, child) {
        var message = this.constructor.name + ".relation_append";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/relation_append';
        return this.http.post(url, {
            'parent': parent,
            'child': child
        }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["BaseResult"]())));
    };
    SpaceService.prototype.relation_remove = function (parent, child) {
        var message = this.constructor.name + ".relation_remove";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/relation_remove';
        return this.http.post(url, {
            'parent': parent,
            'child': child
        }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["BaseResult"]())));
    };
    SpaceService.prototype.run = function (data) {
        var message = this.constructor.name + ".run";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/run';
        return this.http.post(url, data).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["BaseResult"]())));
    };
    SpaceService.prototype.tag_add = function (space, tag) {
        var message = this.constructor.name + ".tag_add";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/tag_add';
        return this.http.post(url, {
            'space': space,
            'tag': tag
        }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["BaseResult"]())));
    };
    SpaceService.prototype.tag_remove = function (space, tag) {
        var message = this.constructor.name + ".tag_remove";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/tag_remove';
        return this.http.post(url, {
            'space': space,
            'tag': tag
        }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["BaseResult"]())));
    };
    SpaceService.prototype.tags = function (data) {
        var message = this.constructor.name + ".tags";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/tags';
        return this.http.post(url, data).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["TagResult"]())));
    };
    SpaceService.prototype.names = function (data) {
        var message = this.constructor.name + ".names";
        var url = _app_settings__WEBPACK_IMPORTED_MODULE_4__["AppSettings"].API_ENDPOINT + this.single_part + '/names';
        return this.http.post(url, data).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])(this.handleError(message, new _models__WEBPACK_IMPORTED_MODULE_3__["NamesResult"]())));
    };
    SpaceService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Injectable"])({
            providedIn: 'root'
        })
    ], SpaceService);
    return SpaceService;
}(_base_service__WEBPACK_IMPORTED_MODULE_1__["BaseService"]));



/***/ })

}]);
//# sourceMappingURL=skynet-skynet-module.js.map