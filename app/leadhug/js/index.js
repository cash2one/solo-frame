var model = avalon.define({
    $id: "nav",
    path: ''
})
avalon.ready(
    function(){
        avalon.vmodels.nav.path = location.pathname;
    }
)
!function(a) {
    "function" == typeof define && define.amd ? define(["jquery"], a) : a(jQuery)
} (function(a) {
    function b(b, d) {
        var e, f, g, h = b.nodeName.toLowerCase();
        return "area" === h ? (e = b.parentNode, f = e.name, b.href && f && "map" === e.nodeName.toLowerCase() ? (g = a("img[usemap='#" + f + "']")[0], !!g && c(g)) : !1) : (/input|select|textarea|button|object/.test(h) ? !b.disabled: "a" === h ? b.href || d: d) && c(b)
    }
    function c(b) {
        return a.expr.filters.visible(b) && !a(b).parents().addBack().filter(function() {
            return "hidden" === a.css(this, "visibility")
        }).length
    }
    function d(a) {
        for (var b, c; a.length && a[0] !== document;) {
            if (b = a.css("position"), ("absolute" === b || "relative" === b || "fixed" === b) && (c = parseInt(a.css("zIndex"), 10), !isNaN(c) && 0 !== c)) return c;
            a = a.parent()
        }
        return 0
    }
    function e() {
        this._curInst = null,
        this._keyEvent = !1,
        this._disabledInputs = [],
        this._datepickerShowing = !1,
        this._inDialog = !1,
        this._mainDivId = "ui-datepicker-div",
        this._inlineClass = "ui-datepicker-inline",
        this._appendClass = "ui-datepicker-append",
        this._triggerClass = "ui-datepicker-trigger",
        this._dialogClass = "ui-datepicker-dialog",
        this._disableClass = "ui-datepicker-disabled",
        this._unselectableClass = "ui-datepicker-unselectable",
        this._currentClass = "ui-datepicker-current-day",
        this._dayOverClass = "ui-datepicker-days-cell-over",
        this.regional = [],
        this.regional[""] = {
            closeText: "Done",
            prevText: "Prev",
            nextText: "Next",
            currentText: "Today",
            monthNames: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            monthNamesShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            dayNames: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            dayNamesShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
            dayNamesMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
            weekHeader: "Wk",
            dateFormat: "mm/dd/yy",
            firstDay: 0,
            isRTL: !1,
            showMonthAfterYear: !1,
            yearSuffix: ""
        },
        this._defaults = {
            showOn: "focus",
            showAnim: "fadeIn",
            showOptions: {},
            defaultDate: null,
            appendText: "",
            buttonText: "...",
            buttonImage: "",
            buttonImageOnly: !1,
            hideIfNoPrevNext: !1,
            navigationAsDateFormat: !1,
            gotoCurrent: !1,
            changeMonth: !1,
            changeYear: !1,
            yearRange: "c-10:c+10",
            showOtherMonths: !1,
            selectOtherMonths: !1,
            showWeek: !1,
            calculateWeek: this.iso8601Week,
            shortYearCutoff: "+10",
            minDate: null,
            maxDate: null,
            duration: "fast",
            beforeShowDay: null,
            beforeShow: null,
            onSelect: null,
            onChangeMonthYear: null,
            onClose: null,
            numberOfMonths: 1,
            showCurrentAtPos: 0,
            stepMonths: 1,
            stepBigMonths: 12,
            altField: "",
            altFormat: "",
            constrainInput: !0,
            showButtonPanel: !1,
            autoSize: !1,
            disabled: !1
        },
        a.extend(this._defaults, this.regional[""]),
        this.regional.en = a.extend(!0, {},
        this.regional[""]),
        this.regional["en-US"] = a.extend(!0, {},
        this.regional.en),
        this.dpDiv = f(a("<div id='" + this._mainDivId + "' class='ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all'></div>"))
    }
    function f(b) {
        var c = "button, .ui-datepicker-prev, .ui-datepicker-next, .ui-datepicker-calendar td a";
        return b.delegate(c, "mouseout",
        function() {
            a(this).removeClass("ui-state-hover"),
            -1 !== this.className.indexOf("ui-datepicker-prev") && a(this).removeClass("ui-datepicker-prev-hover"),
            -1 !== this.className.indexOf("ui-datepicker-next") && a(this).removeClass("ui-datepicker-next-hover")
        }).delegate(c, "mouseover", g)
    }
    function g() {
        a.datepicker._isDisabledDatepicker(i.inline ? i.dpDiv.parent()[0] : i.input[0]) || (a(this).parents(".ui-datepicker-calendar").find("a").removeClass("ui-state-hover"), a(this).addClass("ui-state-hover"), -1 !== this.className.indexOf("ui-datepicker-prev") && a(this).addClass("ui-datepicker-prev-hover"), -1 !== this.className.indexOf("ui-datepicker-next") && a(this).addClass("ui-datepicker-next-hover"))
    }
    function h(b, c) {
        a.extend(b, c);
        for (var d in c) null == c[d] && (b[d] = c[d]);
        return b
    }
    a.ui = a.ui || {},
    a.extend(a.ui, {
        version: "1.11.2",
        keyCode: {
            BACKSPACE: 8,
            COMMA: 188,
            DELETE: 46,
            DOWN: 40,
            END: 35,
            ENTER: 13,
            ESCAPE: 27,
            HOME: 36,
            LEFT: 37,
            PAGE_DOWN: 34,
            PAGE_UP: 33,
            PERIOD: 190,
            RIGHT: 39,
            SPACE: 32,
            TAB: 9,
            UP: 38
        }
    }),
    a.fn.extend({
        scrollParent: function(b) {
            var c = this.css("position"),
            d = "absolute" === c,
            e = b ? /(auto|scroll|hidden)/: /(auto|scroll)/,
            f = this.parents().filter(function() {
                var b = a(this);
                return d && "static" === b.css("position") ? !1 : e.test(b.css("overflow") + b.css("overflow-y") + b.css("overflow-x"))
            }).eq(0);
            return "fixed" !== c && f.length ? f: a(this[0].ownerDocument || document)
        },
        uniqueId: function() {
            var a = 0;
            return function() {
                return this.each(function() {
                    this.id || (this.id = "ui-id-" + ++a)
                })
            }
        } (),
        removeUniqueId: function() {
            return this.each(function() { / ^ui - id - \d + $ / .test(this.id) && a(this).removeAttr("id")
            })
        }
    }),
    a.extend(a.expr[":"], {
        data: a.expr.createPseudo ? a.expr.createPseudo(function(b) {
            return function(c) {
                return !! a.data(c, b)
            }
        }) : function(b, c, d) {
            return !! a.data(b, d[3])
        },
        focusable: function(c) {
            return b(c, !isNaN(a.attr(c, "tabindex")))
        },
        tabbable: function(c) {
            var d = a.attr(c, "tabindex"),
            e = isNaN(d);
            return (e || d >= 0) && b(c, !e)
        }
    }),
    a("<a>").outerWidth(1).jquery || a.each(["Width", "Height"],
    function(b, c) {
        function d(b, c, d, f) {
            return a.each(e,
            function() {
                c -= parseFloat(a.css(b, "padding" + this)) || 0,
                d && (c -= parseFloat(a.css(b, "border" + this + "Width")) || 0),
                f && (c -= parseFloat(a.css(b, "margin" + this)) || 0)
            }),
            c
        }
        var e = "Width" === c ? ["Left", "Right"] : ["Top", "Bottom"],
        f = c.toLowerCase(),
        g = {
            innerWidth: a.fn.innerWidth,
            innerHeight: a.fn.innerHeight,
            outerWidth: a.fn.outerWidth,
            outerHeight: a.fn.outerHeight
        };
        a.fn["inner" + c] = function(b) {
            return void 0 === b ? g["inner" + c].call(this) : this.each(function() {
                a(this).css(f, d(this, b) + "px")
            })
        },
        a.fn["outer" + c] = function(b, e) {
            return "number" != typeof b ? g["outer" + c].call(this, b) : this.each(function() {
                a(this).css(f, d(this, b, !0, e) + "px")
            })
        }
    }),
    a.fn.addBack || (a.fn.addBack = function(a) {
        return this.add(null == a ? this.prevObject: this.prevObject.filter(a))
    }),
    a("<a>").data("a-b", "a").removeData("a-b").data("a-b") && (a.fn.removeData = function(b) {
        return function(c) {
            return arguments.length ? b.call(this, a.camelCase(c)) : b.call(this)
        }
    } (a.fn.removeData)),
    a.ui.ie = !!/msie [\w.]+/.exec(navigator.userAgent.toLowerCase()),
    a.fn.extend({
        focus: function(b) {
            return function(c, d) {
                return "number" == typeof c ? this.each(function() {
                    var b = this;
                    setTimeout(function() {
                        a(b).focus(),
                        d && d.call(b)
                    },
                    c)
                }) : b.apply(this, arguments)
            }
        } (a.fn.focus),
        disableSelection: function() {
            var a = "onselectstart" in document.createElement("div") ? "selectstart": "mousedown";
            return function() {
                return this.bind(a + ".ui-disableSelection",
                function(a) {
                    a.preventDefault()
                })
            }
        } (),
        enableSelection: function() {
            return this.unbind(".ui-disableSelection")
        },
        zIndex: function(b) {
            if (void 0 !== b) return this.css("zIndex", b);
            if (this.length) for (var c, d, e = a(this[0]); e.length && e[0] !== document;) {
                if (c = e.css("position"), ("absolute" === c || "relative" === c || "fixed" === c) && (d = parseInt(e.css("zIndex"), 10), !isNaN(d) && 0 !== d)) return d;
                e = e.parent()
            }
            return 0
        }
    }),
    a.ui.plugin = {
        add: function(b, c, d) {
            var e, f = a.ui[b].prototype;
            for (e in d) f.plugins[e] = f.plugins[e] || [],
            f.plugins[e].push([c, d[e]])
        },
        call: function(a, b, c, d) {
            var e, f = a.plugins[b];
            if (f && (d || a.element[0].parentNode && 11 !== a.element[0].parentNode.nodeType)) for (e = 0; f.length > e; e++) a.options[f[e][0]] && f[e][1].apply(a.element, c)
        }
    },
    a.extend(a.ui, {
        datepicker: {
            version: "1.11.2"
        }
    });
    var i;
    a.extend(e.prototype, {
        markerClassName: "hasDatepicker",
        maxRows: 4,
        _widgetDatepicker: function() {
            return this.dpDiv
        },
        setDefaults: function(a) {
            return h(this._defaults, a || {}),
            this
        },
        _attachDatepicker: function(b, c) {
            var d, e, f;
            d = b.nodeName.toLowerCase(),
            e = "div" === d || "span" === d,
            b.id || (this.uuid += 1, b.id = "dp" + this.uuid),
            f = this._newInst(a(b), e),
            f.settings = a.extend({},
            c || {}),
            "input" === d ? this._connectDatepicker(b, f) : e && this._inlineDatepicker(b, f)
        },
        _newInst: function(b, c) {
            var d = b[0].id.replace(/([^A-Za-z0-9_\-])/g, "\\\\$1");
            return {
                id: d,
                input: b,
                selectedDay: 0,
                selectedMonth: 0,
                selectedYear: 0,
                drawMonth: 0,
                drawYear: 0,
                inline: c,
                dpDiv: c ? f(a("<div class='" + this._inlineClass + " ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all'></div>")) : this.dpDiv
            }
        },
        _connectDatepicker: function(b, c) {
            var d = a(b);
            c.append = a([]),
            c.trigger = a([]),
            d.hasClass(this.markerClassName) || (this._attachments(d, c), d.addClass(this.markerClassName).keydown(this._doKeyDown).keypress(this._doKeyPress).keyup(this._doKeyUp), this._autoSize(c), a.data(b, "datepicker", c), c.settings.disabled && this._disableDatepicker(b))
        },
        _attachments: function(b, c) {
            var d, e, f, g = this._get(c, "appendText"),
            h = this._get(c, "isRTL");
            c.append && c.append.remove(),
            g && (c.append = a("<span class='" + this._appendClass + "'>" + g + "</span>"), b[h ? "before": "after"](c.append)),
            b.unbind("focus", this._showDatepicker),
            c.trigger && c.trigger.remove(),
            d = this._get(c, "showOn"),
            ("focus" === d || "both" === d) && b.focus(this._showDatepicker),
            ("button" === d || "both" === d) && (e = this._get(c, "buttonText"), f = this._get(c, "buttonImage"), c.trigger = a(this._get(c, "buttonImageOnly") ? a("<img/>").addClass(this._triggerClass).attr({
                src: f,
                alt: e,
                title: e
            }) : a("<button type='button'></button>").addClass(this._triggerClass).html(f ? a("<img/>").attr({
                src: f,
                alt: e,
                title: e
            }) : e)), b[h ? "before": "after"](c.trigger), c.trigger.click(function() {
                return a.datepicker._datepickerShowing && a.datepicker._lastInput === b[0] ? a.datepicker._hideDatepicker() : a.datepicker._datepickerShowing && a.datepicker._lastInput !== b[0] ? (a.datepicker._hideDatepicker(), a.datepicker._showDatepicker(b[0])) : a.datepicker._showDatepicker(b[0]),
                !1
            }))
        },
        _autoSize: function(a) {
            if (this._get(a, "autoSize") && !a.inline) {
                var b, c, d, e, f = new Date(2009, 11, 20),
                g = this._get(a, "dateFormat");
                g.match(/[DM]/) && (b = function(a) {
                    for (c = 0, d = 0, e = 0; a.length > e; e++) a[e].length > c && (c = a[e].length, d = e);
                    return d
                },
                f.setMonth(b(this._get(a, g.match(/MM/) ? "monthNames": "monthNamesShort"))), f.setDate(b(this._get(a, g.match(/DD/) ? "dayNames": "dayNamesShort")) + 20 - f.getDay())),
                a.input.attr("size", this._formatDate(a, f).length)
            }
        },
        _inlineDatepicker: function(b, c) {
            var d = a(b);
            d.hasClass(this.markerClassName) || (d.addClass(this.markerClassName).append(c.dpDiv), a.data(b, "datepicker", c), this._setDate(c, this._getDefaultDate(c), !0), this._updateDatepicker(c), this._updateAlternate(c), c.settings.disabled && this._disableDatepicker(b), c.dpDiv.css("display", "block"))
        },
        _dialogDatepicker: function(b, c, d, e, f) {
            var g, i, j, k, l, m = this._dialogInst;
            return m || (this.uuid += 1, g = "dp" + this.uuid, this._dialogInput = a("<input type='text' id='" + g + "' style='position: absolute; top: -100px; width: 0px;'/>"), this._dialogInput.keydown(this._doKeyDown), a("body").append(this._dialogInput), m = this._dialogInst = this._newInst(this._dialogInput, !1), m.settings = {},
            a.data(this._dialogInput[0], "datepicker", m)),
            h(m.settings, e || {}),
            c = c && c.constructor === Date ? this._formatDate(m, c) : c,
            this._dialogInput.val(c),
            this._pos = f ? f.length ? f: [f.pageX, f.pageY] : null,
            this._pos || (i = document.documentElement.clientWidth, j = document.documentElement.clientHeight, k = document.documentElement.scrollLeft || document.body.scrollLeft, l = document.documentElement.scrollTop || document.body.scrollTop, this._pos = [i / 2 - 100 + k, j / 2 - 150 + l]),
            this._dialogInput.css("left", this._pos[0] + 20 + "px").css("top", this._pos[1] + "px"),
            m.settings.onSelect = d,
            this._inDialog = !0,
            this.dpDiv.addClass(this._dialogClass),
            this._showDatepicker(this._dialogInput[0]),
            a.blockUI && a.blockUI(this.dpDiv),
            a.data(this._dialogInput[0], "datepicker", m),
            this
        },
        _destroyDatepicker: function(b) {
            var c, d = a(b),
            e = a.data(b, "datepicker");
            d.hasClass(this.markerClassName) && (c = b.nodeName.toLowerCase(), a.removeData(b, "datepicker"), "input" === c ? (e.append.remove(), e.trigger.remove(), d.removeClass(this.markerClassName).unbind("focus", this._showDatepicker).unbind("keydown", this._doKeyDown).unbind("keypress", this._doKeyPress).unbind("keyup", this._doKeyUp)) : ("div" === c || "span" === c) && d.removeClass(this.markerClassName).empty())
        },
        _enableDatepicker: function(b) {
            var c, d, e = a(b),
            f = a.data(b, "datepicker");
            e.hasClass(this.markerClassName) && (c = b.nodeName.toLowerCase(), "input" === c ? (b.disabled = !1, f.trigger.filter("button").each(function() {
                this.disabled = !1
            }).end().filter("img").css({
                opacity: "1.0",
                cursor: ""
            })) : ("div" === c || "span" === c) && (d = e.children("." + this._inlineClass), d.children().removeClass("ui-state-disabled"), d.find("select.ui-datepicker-month, select.ui-datepicker-year").prop("disabled", !1)), this._disabledInputs = a.map(this._disabledInputs,
            function(a) {
                return a === b ? null: a
            }))
        },
        _disableDatepicker: function(b) {
            var c, d, e = a(b),
            f = a.data(b, "datepicker");
            e.hasClass(this.markerClassName) && (c = b.nodeName.toLowerCase(), "input" === c ? (b.disabled = !0, f.trigger.filter("button").each(function() {
                this.disabled = !0
            }).end().filter("img").css({
                opacity: "0.5",
                cursor: "default"
            })) : ("div" === c || "span" === c) && (d = e.children("." + this._inlineClass), d.children().addClass("ui-state-disabled"), d.find("select.ui-datepicker-month, select.ui-datepicker-year").prop("disabled", !0)), this._disabledInputs = a.map(this._disabledInputs,
            function(a) {
                return a === b ? null: a
            }), this._disabledInputs[this._disabledInputs.length] = b)
        },
        _isDisabledDatepicker: function(a) {
            if (!a) return ! 1;
            for (var b = 0; this._disabledInputs.length > b; b++) if (this._disabledInputs[b] === a) return ! 0;
            return ! 1
        },
        _getInst: function(b) {
            try {
                return a.data(b, "datepicker")
            } catch(c) {
                throw "Missing instance data for this datepicker"
            }
        },
        _optionDatepicker: function(b, c, d) {
            var e, f, g, i, j = this._getInst(b);
            return 2 === arguments.length && "string" == typeof c ? "defaults" === c ? a.extend({},
            a.datepicker._defaults) : j ? "all" === c ? a.extend({},
            j.settings) : this._get(j, c) : null: (e = c || {},
            "string" == typeof c && (e = {},
            e[c] = d), void(j && (this._curInst === j && this._hideDatepicker(), f = this._getDateDatepicker(b, !0), g = this._getMinMaxDate(j, "min"), i = this._getMinMaxDate(j, "max"), h(j.settings, e), null !== g && void 0 !== e.dateFormat && void 0 === e.minDate && (j.settings.minDate = this._formatDate(j, g)), null !== i && void 0 !== e.dateFormat && void 0 === e.maxDate && (j.settings.maxDate = this._formatDate(j, i)), "disabled" in e && (e.disabled ? this._disableDatepicker(b) : this._enableDatepicker(b)), this._attachments(a(b), j), this._autoSize(j), this._setDate(j, f), this._updateAlternate(j), this._updateDatepicker(j))))
        },
        _changeDatepicker: function(a, b, c) {
            this._optionDatepicker(a, b, c)
        },
        _refreshDatepicker: function(a) {
            var b = this._getInst(a);
            b && this._updateDatepicker(b)
        },
        _setDateDatepicker: function(a, b) {
            var c = this._getInst(a);
            c && (this._setDate(c, b), this._updateDatepicker(c), this._updateAlternate(c))
        },
        _getDateDatepicker: function(a, b) {
            var c = this._getInst(a);
            return c && !c.inline && this._setDateFromField(c, b),
            c ? this._getDate(c) : null
        },
        _doKeyDown: function(b) {
            var c, d, e, f = a.datepicker._getInst(b.target),
            g = !0,
            h = f.dpDiv.is(".ui-datepicker-rtl");
            if (f._keyEvent = !0, a.datepicker._datepickerShowing) switch (b.keyCode) {
            case 9:
                a.datepicker._hideDatepicker(),
                g = !1;
                break;
            case 13:
                return e = a("td." + a.datepicker._dayOverClass + ":not(." + a.datepicker._currentClass + ")", f.dpDiv),
                e[0] && a.datepicker._selectDay(b.target, f.selectedMonth, f.selectedYear, e[0]),
                c = a.datepicker._get(f, "onSelect"),
                c ? (d = a.datepicker._formatDate(f), c.apply(f.input ? f.input[0] : null, [d, f])) : a.datepicker._hideDatepicker(),
                !1;
            case 27:
                a.datepicker._hideDatepicker();
                break;
            case 33:
                a.datepicker._adjustDate(b.target, b.ctrlKey ? -a.datepicker._get(f, "stepBigMonths") : -a.datepicker._get(f, "stepMonths"), "M");
                break;
            case 34:
                a.datepicker._adjustDate(b.target, b.ctrlKey ? +a.datepicker._get(f, "stepBigMonths") : +a.datepicker._get(f, "stepMonths"), "M");
                break;
            case 35:
                (b.ctrlKey || b.metaKey) && a.datepicker._clearDate(b.target),
                g = b.ctrlKey || b.metaKey;
                break;
            case 36:
                (b.ctrlKey || b.metaKey) && a.datepicker._gotoToday(b.target),
                g = b.ctrlKey || b.metaKey;
                break;
            case 37:
                (b.ctrlKey || b.metaKey) && a.datepicker._adjustDate(b.target, h ? 1 : -1, "D"),
                g = b.ctrlKey || b.metaKey,
                b.originalEvent.altKey && a.datepicker._adjustDate(b.target, b.ctrlKey ? -a.datepicker._get(f, "stepBigMonths") : -a.datepicker._get(f, "stepMonths"), "M");
                break;
            case 38:
                (b.ctrlKey || b.metaKey) && a.datepicker._adjustDate(b.target, -7, "D"),
                g = b.ctrlKey || b.metaKey;
                break;
            case 39:
                (b.ctrlKey || b.metaKey) && a.datepicker._adjustDate(b.target, h ? -1 : 1, "D"),
                g = b.ctrlKey || b.metaKey,
                b.originalEvent.altKey && a.datepicker._adjustDate(b.target, b.ctrlKey ? +a.datepicker._get(f, "stepBigMonths") : +a.datepicker._get(f, "stepMonths"), "M");
                break;
            case 40:
                (b.ctrlKey || b.metaKey) && a.datepicker._adjustDate(b.target, 7, "D"),
                g = b.ctrlKey || b.metaKey;
                break;
            default:
                g = !1
            } else 36 === b.keyCode && b.ctrlKey ? a.datepicker._showDatepicker(this) : g = !1;
            g && (b.preventDefault(), b.stopPropagation())
        },
        _doKeyPress: function(b) {
            var c, d, e = a.datepicker._getInst(b.target);
            return a.datepicker._get(e, "constrainInput") ? (c = a.datepicker._possibleChars(a.datepicker._get(e, "dateFormat")), d = String.fromCharCode(null == b.charCode ? b.keyCode: b.charCode), b.ctrlKey || b.metaKey || " " > d || !c || c.indexOf(d) > -1) : void 0
        },
        _doKeyUp: function(b) {
            var c, d = a.datepicker._getInst(b.target);
            if (d.input.val() !== d.lastVal) try {
                c = a.datepicker.parseDate(a.datepicker._get(d, "dateFormat"), d.input ? d.input.val() : null, a.datepicker._getFormatConfig(d)),
                c && (a.datepicker._setDateFromField(d), a.datepicker._updateAlternate(d), a.datepicker._updateDatepicker(d))
            } catch(e) {}
            return ! 0
        },
        _showDatepicker: function(b) {
            if (b = b.target || b, "input" !== b.nodeName.toLowerCase() && (b = a("input", b.parentNode)[0]), !a.datepicker._isDisabledDatepicker(b) && a.datepicker._lastInput !== b) {
                var c, e, f, g, i, j, k;
                c = a.datepicker._getInst(b),
                a.datepicker._curInst && a.datepicker._curInst !== c && (a.datepicker._curInst.dpDiv.stop(!0, !0), c && a.datepicker._datepickerShowing && a.datepicker._hideDatepicker(a.datepicker._curInst.input[0])),
                e = a.datepicker._get(c, "beforeShow"),
                f = e ? e.apply(b, [b, c]) : {},
                f !== !1 && (h(c.settings, f), c.lastVal = null, a.datepicker._lastInput = b, a.datepicker._setDateFromField(c), a.datepicker._inDialog && (b.value = ""), a.datepicker._pos || (a.datepicker._pos = a.datepicker._findPos(b), a.datepicker._pos[1] += b.offsetHeight), g = !1, a(b).parents().each(function() {
                    return g |= "fixed" === a(this).css("position"),
                    !g
                }), i = {
                    left: a.datepicker._pos[0],
                    top: a.datepicker._pos[1]
                },
                a.datepicker._pos = null, c.dpDiv.empty(), c.dpDiv.css({
                    position: "absolute",
                    display: "block",
                    top: "-1000px"
                }), a.datepicker._updateDatepicker(c), i = a.datepicker._checkOffset(c, i, g), c.dpDiv.css({
                    position: a.datepicker._inDialog && a.blockUI ? "static": g ? "fixed": "absolute",
                    display: "none",
                    left: i.left + "px",
                    top: i.top + "px"
                }), c.inline || (j = a.datepicker._get(c, "showAnim"), k = a.datepicker._get(c, "duration"), c.dpDiv.css("z-index", d(a(b)) + 1), a.datepicker._datepickerShowing = !0, a.effects && a.effects.effect[j] ? c.dpDiv.show(j, a.datepicker._get(c, "showOptions"), k) : c.dpDiv[j || "show"](j ? k: null), a.datepicker._shouldFocusInput(c) && c.input.focus(), a.datepicker._curInst = c))
            }
        },
        _updateDatepicker: function(b) {
            this.maxRows = 4,
            i = b,
            b.dpDiv.empty().append(this._generateHTML(b)),
            this._attachHandlers(b);
            var c, d = this._getNumberOfMonths(b),
            e = d[1],
            f = 17,
            h = b.dpDiv.find("." + this._dayOverClass + " a");
            h.length > 0 && g.apply(h.get(0)),
            b.dpDiv.removeClass("ui-datepicker-multi-2 ui-datepicker-multi-3 ui-datepicker-multi-4").width(""),
            e > 1 && b.dpDiv.addClass("ui-datepicker-multi-" + e).css("width", f * e + "em"),
            b.dpDiv[(1 !== d[0] || 1 !== d[1] ? "add": "remove") + "Class"]("ui-datepicker-multi"),
            b.dpDiv[(this._get(b, "isRTL") ? "add": "remove") + "Class"]("ui-datepicker-rtl"),
            b === a.datepicker._curInst && a.datepicker._datepickerShowing && a.datepicker._shouldFocusInput(b) && b.input.focus(),
            b.yearshtml && (c = b.yearshtml, setTimeout(function() {
                c === b.yearshtml && b.yearshtml && b.dpDiv.find("select.ui-datepicker-year:first").replaceWith(b.yearshtml),
                c = b.yearshtml = null
            },
            0))
        },
        _shouldFocusInput: function(a) {
            return a.input && a.input.is(":visible") && !a.input.is(":disabled") && !a.input.is(":focus")
        },
        _checkOffset: function(b, c, d) {
            var e = b.dpDiv.outerWidth(),
            f = b.dpDiv.outerHeight(),
            g = b.input ? b.input.outerWidth() : 0,
            h = b.input ? b.input.outerHeight() : 0,
            i = document.documentElement.clientWidth + (d ? 0 : a(document).scrollLeft()),
            j = document.documentElement.clientHeight + (d ? 0 : a(document).scrollTop());
            return c.left -= this._get(b, "isRTL") ? e - g: 0,
            c.left -= d && c.left === b.input.offset().left ? a(document).scrollLeft() : 0,
            c.top -= d && c.top === b.input.offset().top + h ? a(document).scrollTop() : 0,
            c.left -= Math.min(c.left, c.left + e > i && i > e ? Math.abs(c.left + e - i) : 0),
            c.top -= Math.min(c.top, c.top + f > j && j > f ? Math.abs(f + h) : 0),
            c
        },
        _findPos: function(b) {
            for (var c, d = this._getInst(b), e = this._get(d, "isRTL"); b && ("hidden" === b.type || 1 !== b.nodeType || a.expr.filters.hidden(b));) b = b[e ? "previousSibling": "nextSibling"];
            return c = a(b).offset(),
            [c.left, c.top]
        },
        _hideDatepicker: function(b) {
            var c, d, e, f, g = this._curInst; ! g || b && g !== a.data(b, "datepicker") || this._datepickerShowing && (c = this._get(g, "showAnim"), d = this._get(g, "duration"), e = function() {
                a.datepicker._tidyDialog(g)
            },
            a.effects && (a.effects.effect[c] || a.effects[c]) ? g.dpDiv.hide(c, a.datepicker._get(g, "showOptions"), d, e) : g.dpDiv["slideDown" === c ? "slideUp": "fadeIn" === c ? "fadeOut": "hide"](c ? d: null, e), c || e(), this._datepickerShowing = !1, f = this._get(g, "onClose"), f && f.apply(g.input ? g.input[0] : null, [g.input ? g.input.val() : "", g]), this._lastInput = null, this._inDialog && (this._dialogInput.css({
                position: "absolute",
                left: "0",
                top: "-100px"
            }), a.blockUI && (a.unblockUI(), a("body").append(this.dpDiv))), this._inDialog = !1)
        },
        _tidyDialog: function(a) {
            a.dpDiv.removeClass(this._dialogClass).unbind(".ui-datepicker-calendar")
        },
        _checkExternalClick: function(b) {
            if (a.datepicker._curInst) {
                var c = a(b.target),
                d = a.datepicker._getInst(c[0]); (c[0].id !== a.datepicker._mainDivId && 0 === c.parents("#" + a.datepicker._mainDivId).length && !c.hasClass(a.datepicker.markerClassName) && !c.closest("." + a.datepicker._triggerClass).length && a.datepicker._datepickerShowing && (!a.datepicker._inDialog || !a.blockUI) || c.hasClass(a.datepicker.markerClassName) && a.datepicker._curInst !== d) && a.datepicker._hideDatepicker()
            }
        },
        _adjustDate: function(b, c, d) {
            var e = a(b),
            f = this._getInst(e[0]);
            this._isDisabledDatepicker(e[0]) || (this._adjustInstDate(f, c + ("M" === d ? this._get(f, "showCurrentAtPos") : 0), d), this._updateDatepicker(f))
        },
        _gotoToday: function(b) {
            var c, d = a(b),
            e = this._getInst(d[0]);
            this._get(e, "gotoCurrent") && e.currentDay ? (e.selectedDay = e.currentDay, e.drawMonth = e.selectedMonth = e.currentMonth, e.drawYear = e.selectedYear = e.currentYear) : (c = new Date, e.selectedDay = c.getDate(), e.drawMonth = e.selectedMonth = c.getMonth(), e.drawYear = e.selectedYear = c.getFullYear()),
            this._notifyChange(e),
            this._adjustDate(d)
        },
        _selectMonthYear: function(b, c, d) {
            var e = a(b),
            f = this._getInst(e[0]);
            f["selected" + ("M" === d ? "Month": "Year")] = f["draw" + ("M" === d ? "Month": "Year")] = parseInt(c.options[c.selectedIndex].value, 10),
            this._notifyChange(f),
            this._adjustDate(e)
        },
        _selectDay: function(b, c, d, e) {
            var f, g = a(b);
            a(e).hasClass(this._unselectableClass) || this._isDisabledDatepicker(g[0]) || (f = this._getInst(g[0]), f.selectedDay = f.currentDay = a("a", e).html(), f.selectedMonth = f.currentMonth = c, f.selectedYear = f.currentYear = d, this._selectDate(b, this._formatDate(f, f.currentDay, f.currentMonth, f.currentYear)))
        },
        _clearDate: function(b) {
            var c = a(b);
            this._selectDate(c, "")
        },
        _selectDate: function(b, c) {
            var d, e = a(b),
            f = this._getInst(e[0]);
            c = null != c ? c: this._formatDate(f),
            f.input && f.input.val(c),
            this._updateAlternate(f),
            d = this._get(f, "onSelect"),
            d ? d.apply(f.input ? f.input[0] : null, [c, f]) : f.input && f.input.trigger("change"),
            f.inline ? this._updateDatepicker(f) : (this._hideDatepicker(), this._lastInput = f.input[0], "object" != typeof f.input[0] && f.input.focus(), this._lastInput = null)
        },
        _updateAlternate: function(b) {
            var c, d, e, f = this._get(b, "altField");
            f && (c = this._get(b, "altFormat") || this._get(b, "dateFormat"), d = this._getDate(b), e = this.formatDate(c, d, this._getFormatConfig(b)), a(f).each(function() {
                a(this).val(e)
            }))
        },
        noWeekends: function(a) {
            var b = a.getDay();
            return [b > 0 && 6 > b, ""]
        },
        iso8601Week: function(a) {
            var b, c = new Date(a.getTime());
            return c.setDate(c.getDate() + 4 - (c.getDay() || 7)),
            b = c.getTime(),
            c.setMonth(0),
            c.setDate(1),
            Math.floor(Math.round((b - c) / 864e5) / 7) + 1
        },
        parseDate: function(b, c, d) {
            if (null == b || null == c) throw "Invalid arguments";
            if (c = "object" == typeof c ? "" + c: c + "", "" === c) return null;
            var e, f, g, h, i = 0,
            j = (d ? d.shortYearCutoff: null) || this._defaults.shortYearCutoff,
            k = "string" != typeof j ? j: (new Date).getFullYear() % 100 + parseInt(j, 10),
            l = (d ? d.dayNamesShort: null) || this._defaults.dayNamesShort,
            m = (d ? d.dayNames: null) || this._defaults.dayNames,
            n = (d ? d.monthNamesShort: null) || this._defaults.monthNamesShort,
            o = (d ? d.monthNames: null) || this._defaults.monthNames,
            p = -1,
            q = -1,
            r = -1,
            s = -1,
            t = !1,
            u = function(a) {
                var c = b.length > e + 1 && b.charAt(e + 1) === a;
                return c && e++,
                c
            },
            v = function(a) {
                var b = u(a),
                d = "@" === a ? 14 : "!" === a ? 20 : "y" === a && b ? 4 : "o" === a ? 3 : 2,
                e = "y" === a ? d: 1,
                f = RegExp("^\\d{" + e + "," + d + "}"),
                g = c.substring(i).match(f);
                if (!g) throw "Missing number at position " + i;
                return i += g[0].length,
                parseInt(g[0], 10)
            },
            w = function(b, d, e) {
                var f = -1,
                g = a.map(u(b) ? e: d,
                function(a, b) {
                    return [[b, a]]
                }).sort(function(a, b) {
                    return - (a[1].length - b[1].length)
                });
                if (a.each(g,
                function(a, b) {
                    var d = b[1];
                    return c.substr(i, d.length).toLowerCase() === d.toLowerCase() ? (f = b[0], i += d.length, !1) : void 0
                }), -1 !== f) return f + 1;
                throw "Unknown name at position " + i
            },
            x = function() {
                if (c.charAt(i) !== b.charAt(e)) throw "Unexpected literal at position " + i;
                i++
            };
            for (e = 0; b.length > e; e++) if (t)"'" !== b.charAt(e) || u("'") ? x() : t = !1;
            else switch (b.charAt(e)) {
            case "d":
                r = v("d");
                break;
            case "D":
                w("D", l, m);
                break;
            case "o":
                s = v("o");
                break;
            case "m":
                q = v("m");
                break;
            case "M":
                q = w("M", n, o);
                break;
            case "y":
                p = v("y");
                break;
            case "@":
                h = new Date(v("@")),
                p = h.getFullYear(),
                q = h.getMonth() + 1,
                r = h.getDate();
                break;
            case "!":
                h = new Date((v("!") - this._ticksTo1970) / 1e4),
                p = h.getFullYear(),
                q = h.getMonth() + 1,
                r = h.getDate();
                break;
            case "'":
                u("'") ? x() : t = !0;
                break;
            default:
                x()
            }
            if (c.length > i && (g = c.substr(i), !/^\s+/.test(g))) throw "Extra/unparsed characters found in date: " + g;
            if ( - 1 === p ? p = (new Date).getFullYear() : 100 > p && (p += (new Date).getFullYear() - (new Date).getFullYear() % 100 + (k >= p ? 0 : -100)), s > -1) for (q = 1, r = s; f = this._getDaysInMonth(p, q - 1), !(f >= r);) q++,
            r -= f;
            if (h = this._daylightSavingAdjust(new Date(p, q - 1, r)), h.getFullYear() !== p || h.getMonth() + 1 !== q || h.getDate() !== r) throw "Invalid date";
            return h
        },
        ATOM: "yy-mm-dd",
        COOKIE: "D, dd M yy",
        ISO_8601: "yy-mm-dd",
        RFC_822: "D, d M y",
        RFC_850: "DD, dd-M-y",
        RFC_1036: "D, d M y",
        RFC_1123: "D, d M yy",
        RFC_2822: "D, d M yy",
        RSS: "D, d M y",
        TICKS: "!",
        TIMESTAMP: "@",
        W3C: "yy-mm-dd",
        _ticksTo1970: 864e9 * (718685 + Math.floor(492.5) - Math.floor(19.7) + Math.floor(4.925)),
        formatDate: function(a, b, c) {
            if (!b) return "";
            var d, e = (c ? c.dayNamesShort: null) || this._defaults.dayNamesShort,
            f = (c ? c.dayNames: null) || this._defaults.dayNames,
            g = (c ? c.monthNamesShort: null) || this._defaults.monthNamesShort,
            h = (c ? c.monthNames: null) || this._defaults.monthNames,
            i = function(b) {
                var c = a.length > d + 1 && a.charAt(d + 1) === b;
                return c && d++,
                c
            },
            j = function(a, b, c) {
                var d = "" + b;
                if (i(a)) for (; c > d.length;) d = "0" + d;
                return d
            },
            k = function(a, b, c, d) {
                return i(a) ? d[b] : c[b]
            },
            l = "",
            m = !1;
            if (b) for (d = 0; a.length > d; d++) if (m)"'" !== a.charAt(d) || i("'") ? l += a.charAt(d) : m = !1;
            else switch (a.charAt(d)) {
            case "d":
                l += j("d", b.getDate(), 2);
                break;
            case "D":
                l += k("D", b.getDay(), e, f);
                break;
            case "o":
                l += j("o", Math.round((new Date(b.getFullYear(), b.getMonth(), b.getDate()).getTime() - new Date(b.getFullYear(), 0, 0).getTime()) / 864e5), 3);
                break;
            case "m":
                l += j("m", b.getMonth() + 1, 2);
                break;
            case "M":
                l += k("M", b.getMonth(), g, h);
                break;
            case "y":
                l += i("y") ? b.getFullYear() : (10 > b.getYear() % 100 ? "0": "") + b.getYear() % 100;
                break;
            case "@":
                l += b.getTime();
                break;
            case "!":
                l += 1e4 * b.getTime() + this._ticksTo1970;
                break;
            case "'":
                i("'") ? l += "'": m = !0;
                break;
            default:
                l += a.charAt(d)
            }
            return l
        },
        _possibleChars: function(a) {
            var b, c = "",
            d = !1,
            e = function(c) {
                var d = a.length > b + 1 && a.charAt(b + 1) === c;
                return d && b++,
                d
            };
            for (b = 0; a.length > b; b++) if (d)"'" !== a.charAt(b) || e("'") ? c += a.charAt(b) : d = !1;
            else switch (a.charAt(b)) {
            case "d":
            case "m":
            case "y":
            case "@":
                c += "0123456789";
                break;
            case "D":
            case "M":
                return null;
            case "'":
                e("'") ? c += "'": d = !0;
                break;
            default:
                c += a.charAt(b)
            }
            return c
        },
        _get: function(a, b) {
            return void 0 !== a.settings[b] ? a.settings[b] : this._defaults[b]
        },
        _setDateFromField: function(a, b) {
            if (a.input.val() !== a.lastVal) {
                var c = this._get(a, "dateFormat"),
                d = a.lastVal = a.input ? a.input.val() : null,
                e = this._getDefaultDate(a),
                f = e,
                g = this._getFormatConfig(a);
                try {
                    f = this.parseDate(c, d, g) || e
                } catch(h) {
                    d = b ? "": d
                }
                a.selectedDay = f.getDate(),
                a.drawMonth = a.selectedMonth = f.getMonth(),
                a.drawYear = a.selectedYear = f.getFullYear(),
                a.currentDay = d ? f.getDate() : 0,
                a.currentMonth = d ? f.getMonth() : 0,
                a.currentYear = d ? f.getFullYear() : 0,
                this._adjustInstDate(a)
            }
        },
        _getDefaultDate: function(a) {
            return this._restrictMinMax(a, this._determineDate(a, this._get(a, "defaultDate"), new Date))
        },
        _determineDate: function(b, c, d) {
            var e = function(a) {
                var b = new Date;
                return b.setDate(b.getDate() + a),
                b
            },
            f = function(c) {
                try {
                    return a.datepicker.parseDate(a.datepicker._get(b, "dateFormat"), c, a.datepicker._getFormatConfig(b))
                } catch(d) {}
                for (var e = (c.toLowerCase().match(/^c/) ? a.datepicker._getDate(b) : null) || new Date, f = e.getFullYear(), g = e.getMonth(), h = e.getDate(), i = /([+\-]?[0-9]+)\s*(d|D|w|W|m|M|y|Y)?/g, j = i.exec(c); j;) {
                    switch (j[2] || "d") {
                    case "d":
                    case "D":
                        h += parseInt(j[1], 10);
                        break;
                    case "w":
                    case "W":
                        h += 7 * parseInt(j[1], 10);
                        break;
                    case "m":
                    case "M":
                        g += parseInt(j[1], 10),
                        h = Math.min(h, a.datepicker._getDaysInMonth(f, g));
                        break;
                    case "y":
                    case "Y":
                        f += parseInt(j[1], 10),
                        h = Math.min(h, a.datepicker._getDaysInMonth(f, g))
                    }
                    j = i.exec(c)
                }
                return new Date(f, g, h)
            },
            g = null == c || "" === c ? d: "string" == typeof c ? f(c) : "number" == typeof c ? isNaN(c) ? d: e(c) : new Date(c.getTime());
            return g = g && "Invalid Date" == "" + g ? d: g,
            g && (g.setHours(0), g.setMinutes(0), g.setSeconds(0), g.setMilliseconds(0)),
            this._daylightSavingAdjust(g)
        },
        _daylightSavingAdjust: function(a) {
            return a ? (a.setHours(a.getHours() > 12 ? a.getHours() + 2 : 0), a) : null
        },
        _setDate: function(a, b, c) {
            var d = !b,
            e = a.selectedMonth,
            f = a.selectedYear,
            g = this._restrictMinMax(a, this._determineDate(a, b, new Date));
            a.selectedDay = a.currentDay = g.getDate(),
            a.drawMonth = a.selectedMonth = a.currentMonth = g.getMonth(),
            a.drawYear = a.selectedYear = a.currentYear = g.getFullYear(),
            e === a.selectedMonth && f === a.selectedYear || c || this._notifyChange(a),
            this._adjustInstDate(a),
            a.input && a.input.val(d ? "": this._formatDate(a))
        },
        _getDate: function(a) {
            var b = !a.currentYear || a.input && "" === a.input.val() ? null: this._daylightSavingAdjust(new Date(a.currentYear, a.currentMonth, a.currentDay));
            return b
        },
        _attachHandlers: function(b) {
            var c = this._get(b, "stepMonths"),
            d = "#" + b.id.replace(/\\\\/g, "\\");
            b.dpDiv.find("[data-handler]").map(function() {
                var b = {
                    prev: function() {
                        a.datepicker._adjustDate(d, -c, "M")
                    },
                    next: function() {
                        a.datepicker._adjustDate(d, +c, "M")
                    },
                    hide: function() {
                        a.datepicker._hideDatepicker()
                    },
                    today: function() {
                        a.datepicker._gotoToday(d)
                    },
                    selectDay: function() {
                        return a.datepicker._selectDay(d, +this.getAttribute("data-month"), +this.getAttribute("data-year"), this),
                        !1
                    },
                    selectMonth: function() {
                        return a.datepicker._selectMonthYear(d, this, "M"),
                        !1
                    },
                    selectYear: function() {
                        return a.datepicker._selectMonthYear(d, this, "Y"),
                        !1
                    }
                };
                a(this).bind(this.getAttribute("data-event"), b[this.getAttribute("data-handler")])
            })
        },
        _generateHTML: function(a) {
            var b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O = new Date,
            P = this._daylightSavingAdjust(new Date(O.getFullYear(), O.getMonth(), O.getDate())),
            Q = this._get(a, "isRTL"),
            R = this._get(a, "showButtonPanel"),
            S = this._get(a, "hideIfNoPrevNext"),
            T = this._get(a, "navigationAsDateFormat"),
            U = this._getNumberOfMonths(a),
            V = this._get(a, "showCurrentAtPos"),
            W = this._get(a, "stepMonths"),
            X = 1 !== U[0] || 1 !== U[1],
            Y = this._daylightSavingAdjust(a.currentDay ? new Date(a.currentYear, a.currentMonth, a.currentDay) : new Date(9999, 9, 9)),
            Z = this._getMinMaxDate(a, "min"),
            $ = this._getMinMaxDate(a, "max"),
            _ = a.drawMonth - V,
            ab = a.drawYear;
            if (0 > _ && (_ += 12, ab--), $) for (b = this._daylightSavingAdjust(new Date($.getFullYear(), $.getMonth() - U[0] * U[1] + 1, $.getDate())), b = Z && Z > b ? Z: b; this._daylightSavingAdjust(new Date(ab, _, 1)) > b;) _--,
            0 > _ && (_ = 11, ab--);
            for (a.drawMonth = _, a.drawYear = ab, c = this._get(a, "prevText"), c = T ? this.formatDate(c, this._daylightSavingAdjust(new Date(ab, _ - W, 1)), this._getFormatConfig(a)) : c, d = this._canAdjustMonth(a, -1, ab, _) ? "<a class='ui-datepicker-prev ui-corner-all' data-handler='prev' data-event='click' title='" + c + "'><span class='ui-icon ui-icon-circle-triangle-" + (Q ? "e": "w") + "'>" + c + "</span></a>": S ? "": "<a class='ui-datepicker-prev ui-corner-all ui-state-disabled' title='" + c + "'><span class='ui-icon ui-icon-circle-triangle-" + (Q ? "e": "w") + "'>" + c + "</span></a>", e = this._get(a, "nextText"), e = T ? this.formatDate(e, this._daylightSavingAdjust(new Date(ab, _ + W, 1)), this._getFormatConfig(a)) : e, f = this._canAdjustMonth(a, 1, ab, _) ? "<a class='ui-datepicker-next ui-corner-all' data-handler='next' data-event='click' title='" + e + "'><span class='ui-icon ui-icon-circle-triangle-" + (Q ? "w": "e") + "'>" + e + "</span></a>": S ? "": "<a class='ui-datepicker-next ui-corner-all ui-state-disabled' title='" + e + "'><span class='ui-icon ui-icon-circle-triangle-" + (Q ? "w": "e") + "'>" + e + "</span></a>", g = this._get(a, "currentText"), h = this._get(a, "gotoCurrent") && a.currentDay ? Y: P, g = T ? this.formatDate(g, h, this._getFormatConfig(a)) : g, i = a.inline ? "": "<button type='button' class='ui-datepicker-close ui-state-default ui-priority-primary ui-corner-all' data-handler='hide' data-event='click'>" + this._get(a, "closeText") + "</button>", j = R ? "<div class='ui-datepicker-buttonpane ui-widget-content'>" + (Q ? i: "") + (this._isInRange(a, h) ? "<button type='button' class='ui-datepicker-current ui-state-default ui-priority-secondary ui-corner-all' data-handler='today' data-event='click'>" + g + "</button>": "") + (Q ? "": i) + "</div>": "", k = parseInt(this._get(a, "firstDay"), 10), k = isNaN(k) ? 0 : k, l = this._get(a, "showWeek"), m = this._get(a, "dayNames"), n = this._get(a, "dayNamesMin"), o = this._get(a, "monthNames"), p = this._get(a, "monthNamesShort"), q = this._get(a, "beforeShowDay"), r = this._get(a, "showOtherMonths"), s = this._get(a, "selectOtherMonths"), t = this._getDefaultDate(a), u = "", w = 0; U[0] > w; w++) {
                for (x = "", this.maxRows = 4, y = 0; U[1] > y; y++) {
                    if (z = this._daylightSavingAdjust(new Date(ab, _, a.selectedDay)), A = " ui-corner-all", B = "", X) {
                        if (B += "<div class='ui-datepicker-group", U[1] > 1) switch (y) {
                        case 0:
                            B += " ui-datepicker-group-first",
                            A = " ui-corner-" + (Q ? "right": "left");
                            break;
                        case U[1] - 1 : B += " ui-datepicker-group-last",
                            A = " ui-corner-" + (Q ? "left": "right");
                            break;
                        default:
                            B += " ui-datepicker-group-middle",
                            A = ""
                        }
                        B += "'>"
                    }
                    for (B += "<div class='ui-datepicker-header ui-widget-header ui-helper-clearfix" + A + "'>" + (/all|left/.test(A) && 0 === w ? Q ? f: d: "") + (/all|right/.test(A) && 0 === w ? Q ? d: f: "") + this._generateMonthYearHeader(a, _, ab, Z, $, w > 0 || y > 0, o, p) + "</div><table class='ui-datepicker-calendar'><thead><tr>", C = l ? "<th class='ui-datepicker-week-col'>" + this._get(a, "weekHeader") + "</th>": "", v = 0; 7 > v; v++) D = (v + k) % 7,
                    C += "<th scope='col'" + ((v + k + 6) % 7 >= 5 ? " class='ui-datepicker-week-end'": "") + "><span title='" + m[D] + "'>" + n[D] + "</span></th>";
                    for (B += C + "</tr></thead><tbody>", E = this._getDaysInMonth(ab, _), ab === a.selectedYear && _ === a.selectedMonth && (a.selectedDay = Math.min(a.selectedDay, E)), F = (this._getFirstDayOfMonth(ab, _) - k + 7) % 7, G = Math.ceil((F + E) / 7), H = X && this.maxRows > G ? this.maxRows: G, this.maxRows = H, I = this._daylightSavingAdjust(new Date(ab, _, 1 - F)), J = 0; H > J; J++) {
                        for (B += "<tr>", K = l ? "<td class='ui-datepicker-week-col'>" + this._get(a, "calculateWeek")(I) + "</td>": "", v = 0; 7 > v; v++) L = q ? q.apply(a.input ? a.input[0] : null, [I]) : [!0, ""],
                        M = I.getMonth() !== _,
                        N = M && !s || !L[0] || Z && Z > I || $ && I > $,
                        K += "<td class='" + ((v + k + 6) % 7 >= 5 ? " ui-datepicker-week-end": "") + (M ? " ui-datepicker-other-month": "") + (I.getTime() === z.getTime() && _ === a.selectedMonth && a._keyEvent || t.getTime() === I.getTime() && t.getTime() === z.getTime() ? " " + this._dayOverClass: "") + (N ? " " + this._unselectableClass + " ui-state-disabled": "") + (M && !r ? "": " " + L[1] + (I.getTime() === Y.getTime() ? " " + this._currentClass: "") + (I.getTime() === P.getTime() ? " ui-datepicker-today": "")) + "'" + (M && !r || !L[2] ? "": " title='" + L[2].replace(/'/g, "&#39;") + "'") + (N ? "": " data-handler='selectDay' data-event='click' data-month='" + I.getMonth() + "' data-year='" + I.getFullYear() + "'") + ">" + (M && !r ? "&#xa0;": N ? "<span class='ui-state-default'>" + I.getDate() + "</span>": "<a class='ui-state-default" + (I.getTime() === P.getTime() ? " ui-state-highlight": "") + (I.getTime() === Y.getTime() ? " ui-state-active": "") + (M ? " ui-priority-secondary": "") + "' href='#'>" + I.getDate() + "</a>") + "</td>",
                        I.setDate(I.getDate() + 1),
                        I = this._daylightSavingAdjust(I);
                        B += K + "</tr>"
                    }
                    _++,
                    _ > 11 && (_ = 0, ab++),
                    B += "</tbody></table>" + (X ? "</div>" + (U[0] > 0 && y === U[1] - 1 ? "<div class='ui-datepicker-row-break'></div>": "") : ""),
                    x += B
                }
                u += x
            }
            return u += j,
            a._keyEvent = !1,
            u
        },
        _generateMonthYearHeader: function(a, b, c, d, e, f, g, h) {
            var i, j, k, l, m, n, o, p, q = this._get(a, "changeMonth"),
            r = this._get(a, "changeYear"),
            s = this._get(a, "showMonthAfterYear"),
            t = "<div class='ui-datepicker-title'>",
            u = "";
            if (f || !q) u += "<span class='ui-datepicker-month'>" + g[b] + "</span>";
            else {
                for (i = d && d.getFullYear() === c, j = e && e.getFullYear() === c, u += "<select class='ui-datepicker-month' data-handler='selectMonth' data-event='change'>", k = 0; 12 > k; k++)(!i || k >= d.getMonth()) && (!j || e.getMonth() >= k) && (u += "<option value='" + k + "'" + (k === b ? " selected='selected'": "") + ">" + h[k] + "</option>");
                u += "</select>"
            }
            if (s || (t += u + (!f && q && r ? "": "&#xa0;")), !a.yearshtml) if (a.yearshtml = "", f || !r) t += "<span class='ui-datepicker-year'>" + c + "</span>";
            else {
                for (l = this._get(a, "yearRange").split(":"), m = (new Date).getFullYear(), n = function(a) {
                    var b = a.match(/c[+\-].*/) ? c + parseInt(a.substring(1), 10) : a.match(/[+\-].*/) ? m + parseInt(a, 10) : parseInt(a, 10);
                    return isNaN(b) ? m: b
                },
                o = n(l[0]), p = Math.max(o, n(l[1] || "")), o = d ? Math.max(o, d.getFullYear()) : o, p = e ? Math.min(p, e.getFullYear()) : p, a.yearshtml += "<select class='ui-datepicker-year' data-handler='selectYear' data-event='change'>"; p >= o; o++) a.yearshtml += "<option value='" + o + "'" + (o === c ? " selected='selected'": "") + ">" + o + "</option>";
                a.yearshtml += "</select>",
                t += a.yearshtml,
                a.yearshtml = null
            }
            return t += this._get(a, "yearSuffix"),
            s && (t += (!f && q && r ? "": "&#xa0;") + u),
            t += "</div>"
        },
        _adjustInstDate: function(a, b, c) {
            var d = a.drawYear + ("Y" === c ? b: 0),
            e = a.drawMonth + ("M" === c ? b: 0),
            f = Math.min(a.selectedDay, this._getDaysInMonth(d, e)) + ("D" === c ? b: 0),
            g = this._restrictMinMax(a, this._daylightSavingAdjust(new Date(d, e, f)));
            a.selectedDay = g.getDate(),
            a.drawMonth = a.selectedMonth = g.getMonth(),
            a.drawYear = a.selectedYear = g.getFullYear(),
            ("M" === c || "Y" === c) && this._notifyChange(a)
        },
        _restrictMinMax: function(a, b) {
            var c = this._getMinMaxDate(a, "min"),
            d = this._getMinMaxDate(a, "max"),
            e = c && c > b ? c: b;
            return d && e > d ? d: e
        },
        _notifyChange: function(a) {
            var b = this._get(a, "onChangeMonthYear");
            b && b.apply(a.input ? a.input[0] : null, [a.selectedYear, a.selectedMonth + 1, a])
        },
        _getNumberOfMonths: function(a) {
            var b = this._get(a, "numberOfMonths");
            return null == b ? [1, 1] : "number" == typeof b ? [1, b] : b
        },
        _getMinMaxDate: function(a, b) {
            return this._determineDate(a, this._get(a, b + "Date"), null)
        },
        _getDaysInMonth: function(a, b) {
            return 32 - this._daylightSavingAdjust(new Date(a, b, 32)).getDate()
        },
        _getFirstDayOfMonth: function(a, b) {
            return new Date(a, b, 1).getDay()
        },
        _canAdjustMonth: function(a, b, c, d) {
            var e = this._getNumberOfMonths(a),
            f = this._daylightSavingAdjust(new Date(c, d + (0 > b ? b: e[0] * e[1]), 1));
            return 0 > b && f.setDate(this._getDaysInMonth(f.getFullYear(), f.getMonth())),
            this._isInRange(a, f)
        },
        _isInRange: function(a, b) {
            var c, d, e = this._getMinMaxDate(a, "min"),
            f = this._getMinMaxDate(a, "max"),
            g = null,
            h = null,
            i = this._get(a, "yearRange");
            return i && (c = i.split(":"), d = (new Date).getFullYear(), g = parseInt(c[0], 10), h = parseInt(c[1], 10), c[0].match(/[+\-].*/) && (g += d), c[1].match(/[+\-].*/) && (h += d)),
            (!e || b.getTime() >= e.getTime()) && (!f || b.getTime() <= f.getTime()) && (!g || b.getFullYear() >= g) && (!h || h >= b.getFullYear())
        },
        _getFormatConfig: function(a) {
            var b = this._get(a, "shortYearCutoff");
            return b = "string" != typeof b ? b: (new Date).getFullYear() % 100 + parseInt(b, 10),
            {
                shortYearCutoff: b,
                dayNamesShort: this._get(a, "dayNamesShort"),
                dayNames: this._get(a, "dayNames"),
                monthNamesShort: this._get(a, "monthNamesShort"),
                monthNames: this._get(a, "monthNames")
            }
        },
        _formatDate: function(a, b, c, d) {
            b || (a.currentDay = a.selectedDay, a.currentMonth = a.selectedMonth, a.currentYear = a.selectedYear);
            var e = b ? "object" == typeof b ? b: this._daylightSavingAdjust(new Date(d, c, b)) : this._daylightSavingAdjust(new Date(a.currentYear, a.currentMonth, a.currentDay));
            return this.formatDate(this._get(a, "dateFormat"), e, this._getFormatConfig(a))
        }
    }),
    a.fn.datepicker = function(b) {
        if (!this.length) return this;
        a.datepicker.initialized || (a(document).mousedown(a.datepicker._checkExternalClick), a.datepicker.initialized = !0),
        0 === a("#" + a.datepicker._mainDivId).length && a("body").append(a.datepicker.dpDiv);
        var c = Array.prototype.slice.call(arguments, 1);
        return "string" != typeof b || "isDisabled" !== b && "getDate" !== b && "widget" !== b ? "option" === b && 2 === arguments.length && "string" == typeof arguments[1] ? a.datepicker["_" + b + "Datepicker"].apply(a.datepicker, [this[0]].concat(c)) : this.each(function() {
            "string" == typeof b ? a.datepicker["_" + b + "Datepicker"].apply(a.datepicker, [this].concat(c)) : a.datepicker._attachDatepicker(this, b)
        }) : a.datepicker["_" + b + "Datepicker"].apply(a.datepicker, [this[0]].concat(c))
    },
    a.datepicker = new e,
    a.datepicker.initialized = !1,
    a.datepicker.uuid = (new Date).getTime(),
    a.datepicker.version = "1.11.2",
    a.datepicker
}),
function(a) {
    a.fn.zclip = function(b) {
        if ("object" == typeof b && !b.length) {
            var c = a.extend({
                path: "ZeroClipboard.swf",
                copy: null,
                beforeCopy: null,
                afterCopy: null,
                clickAfter: !0,
                setHandCursor: !0,
                setCSSEffects: !0
            },
            b);
            return this.each(function() {
                var b = a(this);
                if (b.is(":visible") && ("string" == typeof c.copy || a.isFunction(c.copy))) {
                    ZeroClipboard.setMoviePath(c.path);
                    var d = new ZeroClipboard.Client;
                    a.isFunction(c.copy) && b.bind("zClip_copy", c.copy),
                    a.isFunction(c.beforeCopy) && b.bind("zClip_beforeCopy", c.beforeCopy),
                    a.isFunction(c.afterCopy) && b.bind("zClip_afterCopy", c.afterCopy),
                    d.setHandCursor(c.setHandCursor),
                    d.setCSSEffects(c.setCSSEffects),
                    d.addEventListener("mouseOver",
                    function() {
                        b.trigger("mouseenter")
                    }),
                    d.addEventListener("mouseOut",
                    function() {
                        b.trigger("mouseleave")
                    }),
                    d.addEventListener("mouseDown",
                    function() {
                        b.trigger("mousedown"),
                        d.setText(a.isFunction(c.copy) ? b.triggerHandler("zClip_copy") : c.copy),
                        a.isFunction(c.beforeCopy) && b.trigger("zClip_beforeCopy")
                    }),
                    d.addEventListener("complete",
                    function(d, e) {
                        a.isFunction(c.afterCopy) ? b.trigger("zClip_afterCopy") : (e.length > 500 && (e = e.substr(0, 500) + "...\n\n(" + (e.length - 500) + " characters not shown)"), b.removeClass("hover"), alert("å¤åˆ¶æˆåŠŸï¼Œæ‚¨çš„IDï¼š\n\n " + e)),
                        c.clickAfter && b.trigger("click")
                    }),
                    d.glue(b[0], b.parent()[0]),
                    a(window).bind("load resize",
                    function() {
                        d.reposition()
                    })
                }
            })
        }
        return "string" == typeof b ? this.each(function() {
            var c = a(this);
            b = b.toLowerCase();
            var d = c.data("zclipId"),
            e = a("#" + d + ".zclip");
            "remove" == b ? (e.remove(), c.removeClass("active hover")) : "hide" == b ? (e.hide(), c.removeClass("active hover")) : "show" == b && e.show()
        }) : void 0
    }
} (jQuery);
var ZeroClipboard = {
    version: "1.0.7",
    clients: {},
    moviePath: "ZeroClipboard.swf",
    nextId: 1,
    $: function(a) {
        return "string" == typeof a && (a = document.getElementById(a)),
        a.addClass || (a.hide = function() {
            this.style.display = "none"
        },
        a.show = function() {
            this.style.display = ""
        },
        a.addClass = function(a) {
            this.removeClass(a),
            this.className += " " + a
        },
        a.removeClass = function(a) {
            for (var b = this.className.split(/\s+/), c = -1, d = 0; d < b.length; d++) b[d] == a && (c = d, d = b.length);
            return c > -1 && (b.splice(c, 1), this.className = b.join(" ")),
            this
        },
        a.hasClass = function(a) {
            return !! this.className.match(new RegExp("\\s*" + a + "\\s*"))
        }),
        a
    },
    setMoviePath: function(a) {
        this.moviePath = a
    },
    dispatch: function(a, b, c) {
        var d = this.clients[a];
        d && d.receiveEvent(b, c)
    },
    register: function(a, b) {
        this.clients[a] = b
    },
    getDOMObjectPosition: function(a, b) {
        var c = {
            left: 0,
            top: 0,
            width: a.width ? a.width: a.offsetWidth,
            height: a.height ? a.height: a.offsetHeight
        };
        return a && a != b && (c.left += a.offsetLeft, c.top += a.offsetTop),
        c
    },
    Client: function(a) {
        this.handlers = {},
        this.id = ZeroClipboard.nextId++,
        this.movieId = "ZeroClipboardMovie_" + this.id,
        ZeroClipboard.register(this.id, this),
        a && this.glue(a)
    }
};
ZeroClipboard.Client.prototype = {
    id: 0,
    ready: !1,
    movie: null,
    clipText: "",
    handCursorEnabled: !0,
    cssEffects: !0,
    handlers: null,
    glue: function(a, b, c) {
        this.domElement = ZeroClipboard.$(a);
        var d = 99;
        this.domElement.style.zIndex && (d = parseInt(this.domElement.style.zIndex, 10) + 1),
        "string" == typeof b ? b = ZeroClipboard.$(b) : "undefined" == typeof b && (b = document.getElementsByTagName("body")[0]);
        var e = ZeroClipboard.getDOMObjectPosition(this.domElement, b);
        this.div = document.createElement("div"),
        this.div.className = "zclip",
        this.div.id = "zclip-" + this.movieId,
        $(this.domElement).data("zclipId", "zclip-" + this.movieId);
        var f = this.div.style;
        if (f.position = "absolute", f.left = "" + e.left + "px", f.top = "" + e.top + "px", f.width = "" + e.width + "px", f.height = "" + e.height + "px", f.zIndex = d, "object" == typeof c) for (addedStyle in c) f[addedStyle] = c[addedStyle];
        b.appendChild(this.div),
        this.div.innerHTML = this.getHTML(e.width, e.height)
    },
    getHTML: function(a, b) {
        var c = "",
        d = "id=" + this.id + "&width=" + a + "&height=" + b;
        if (navigator.userAgent.match(/MSIE/)) {
            var e = location.href.match(/^https/i) ? "https://": "http://";
            c += '<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="' + e + 'download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0" width="' + a + '" height="' + b + '" id="' + this.movieId + '" align="middle"><param name="allowScriptAccess" value="sameDomain" /><param name="allowFullScreen" value="false" /><param name="movie" value="' + ZeroClipboard.moviePath + '" /><param name="loop" value="false" /><param name="menu" value="false" /><param name="quality" value="best" /><param name="bgcolor" value="#ffffff" /><param name="flashvars" value="' + d + '"/><param name="wmode" value="transparent"/></object>'
        } else c += '<embed id="' + this.movieId + '" src="' + ZeroClipboard.moviePath + '" loop="false" menu="false" quality="best" bgcolor="#ffffff" width="' + a + '" height="' + b + '" name="' + this.movieId + '" align="middle" allowScriptAccess="always" allowFullScreen="false" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" flashvars="' + d + '" wmode="transparent" />';
        return c
    },
    hide: function() {
        this.div && (this.div.style.left = "-2000px")
    },
    show: function() {
        this.reposition()
    },
    destroy: function() {
        if (this.domElement && this.div) {
            this.hide(),
            this.div.innerHTML = "";
            var a = document.getElementsByTagName("body")[0];
            try {
                a.removeChild(this.div)
            } catch(b) {}
            this.domElement = null,
            this.div = null
        }
    },
    reposition: function(a) {
        if (a && (this.domElement = ZeroClipboard.$(a), this.domElement || this.hide()), this.domElement && this.div) {
            var b = ZeroClipboard.getDOMObjectPosition(this.domElement),
            c = this.div.style;
            c.left = "" + b.left + "px",
            c.top = "" + b.top + "px"
        }
    },
    setText: function(a) {
        this.clipText = a,
        this.ready && this.movie.setText(a)
    },
    addEventListener: function(a, b) {
        a = a.toString().toLowerCase().replace(/^on/, ""),
        this.handlers[a] || (this.handlers[a] = []),
        this.handlers[a].push(b)
    },
    setHandCursor: function(a) {
        this.handCursorEnabled = a,
        this.ready && this.movie.setHandCursor(a)
    },
    setCSSEffects: function(a) {
        this.cssEffects = !!a
    },
    receiveEvent: function(a, b) {
        switch (a = a.toString().toLowerCase().replace(/^on/, "")) {
        case "load":
            if (this.movie = document.getElementById(this.movieId), !this.movie) {
                var c = this;
                return void setTimeout(function() {
                    c.receiveEvent("load", null)
                },
                1)
            }
            if (!this.ready && navigator.userAgent.match(/Firefox/) && navigator.userAgent.match(/Windows/)) {
                var c = this;
                return setTimeout(function() {
                    c.receiveEvent("load", null)
                },
                100),
                void(this.ready = !0)
            }
            this.ready = !0;
            try {
                this.movie.setText(this.clipText)
            } catch(d) {}
            try {
                this.movie.setHandCursor(this.handCursorEnabled)
            } catch(d) {}
            break;
        case "mouseover":
            this.domElement && this.cssEffects && (this.domElement.addClass("hover"), this.recoverActive && this.domElement.addClass("active"));
            break;
        case "mouseout":
            this.domElement && this.cssEffects && (this.recoverActive = !1, this.domElement.hasClass("active") && (this.domElement.removeClass("active"), this.recoverActive = !0), this.domElement.removeClass("hover"));
            break;
        case "mousedown":
            this.domElement && this.cssEffects && this.domElement.addClass("active");
            break;
        case "mouseup":
            this.domElement && this.cssEffects && (this.domElement.removeClass("active"), this.recoverActive = !1)
        }
        if (this.handlers[a]) for (var e = 0,
        f = this.handlers[a].length; f > e; e++) {
            var g = this.handlers[a][e];
            "function" == typeof g ? g(this, b) : "object" == typeof g && 2 == g.length ? g[0][g[1]](this, b) : "string" == typeof g && window[g](this, b)
        }
    }
};
var Ssp = {
    init: function() {
        Ssp.category = $("#category"),
        Ssp.loginWrap = $("#loginWrap"),
        Ssp.calendar(),
        Ssp.bindEvent(),
        Ssp.placeholder(),
        Ssp.copyId()
    },
    calendar: function() {
        {
            var a = {
                changeYear: !0,
                changeMonth: !0,
                dateFormat: "yy-mm-dd",
                minDate: "-92d",
                maxDate: "-1d",
                dayNamesMin: ["æ—¥", "ä¸€", "äºŒ", "ä¸‰", "å››", "äº”", "å…­"],
                monthNamesShort: ["1æœˆ", "2æœˆ", "3æœˆ", "4æœˆ", "5æœˆ", "6æœˆ", "7æœˆ", "8æœˆ", "9æœˆ", "10æœˆ", "11æœˆ", "12æœˆ"],
                firstDay: 1,
                yearRange: "2015:2050"
            };
            $("#datepickerFrome").datepicker(a),
            $("#datepickerTo").datepicker(a)
        }
    },
    placeholder: function() {
        "placeholder" in document.createElement("input") || $(":input[placeholder]").each(function() {
            var a = $(this),
            b = a.attr("placeholder");
            a.wrap($("<div></div>").css({
                position: "relative",
                zoom: "1",
                border: "none",
                background: "none",
                padding: "none",
                margin: "none"
            })); {
                var c = a.position(),
                d = a.outerHeight(!0),
                e = a.css("padding-left");
                $("<span></span>").text(b).css({
                    position: "absolute",
                    left: c.left,
                    top: c.top,
                    height: d,
                    lineHeight: d + "px",
                    paddingLeft: e,
                    color: "#aaa"
                }).appendTo(a.parent())
            }
        })
    },
    copyId: function() {
        try {
            $(".copyid a").zclip({
                path: "/statics/js/ZeroClipboard.swf",
                copy: function() {
                    return $(this).parent(".copyid").find("em").text()
                }
            })
        } catch(a) {
            console.log("ä½ æ²¡æœ‰å®‰è£…flashï¼Œè¯·æ‰‹åŠ¨å¤åˆ¶ã€‚")
        }
    },
    bindEvent: function() {
        var a = $("#optionTab"),
        b = Ssp.loginWrap,
        c = $("#charts"),
        d = c.find(".chartbox .chartlist"),
        e = $("#optInfo");
        e.on("click", ".enter",
        function(a) {
            return $(this).parent().toggleClass("active").siblings(".active").removeClass("active"),
            e.find(".loginline").toggle(!e.children().hasClass("active")),
            a.preventDefault(),
            !1
        }),
        //$(".bg-t").on("click",
        //function(a) {
        //    return e ? (e.find(".active").removeClass("active"), e.find(".loginline").show(), a.preventDefault(), !1) : void 0
        //}),
        //e.find(".agree_box").bind("click",
        //function(a) {
        //    return $(this).toggleClass("active"),
        //    a.preventDefault(),
        //    !1
        //}),
        b.find(".user").bind("click",
        function(a) {
            return b.find(".setting").toggle(),
            a.preventDefault(),
            !1
        }),
        //a.find(".optiontab").on("click", "a",
        //function(b) {
        //    $(this).addClass("active").siblings("a").removeClass("active");
        //    var c = $(this).index();
        //    return a.find(".textarea").removeClass("show").eq(c).addClass("show"),
        //    b.preventDefault(),
        //    !1
        //}),
        c.children(".chartab").on("click", "li",
        function(a) {
            $(this).addClass("cur").siblings("li").removeClass("cur");
            var b = $(this).index();
            return d.removeClass("chart_show").eq(b).addClass("chart_show"),
            a.preventDefault(),
            !1
        }),
        //$("#pop").bind("click",
        //function(a) {
        //    return $(this).removeClass("pop_show"),
        //    a.preventDefault(),
        //    !1
        //}),
        $("#appContents .tcol2 a,#adContents .tcol3 a").bind("click",
        function(a) {
            return $(this).toggleClass("on"),
            a.preventDefault(),
            !1
        })
    }
};
$(function() {
    Ssp.init(),
    $("#protectNews li:even").addClass("even")
});
