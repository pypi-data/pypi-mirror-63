/*! For license information please see chunk.74446008f98c4637e61c.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[131,18,190],{112:function(e,t,i){"use strict";i.d(t,"a",function(){return a});i(3);var n=i(55),s=i(34);const a=[n.a,s.a,{hostAttributes:{role:"option",tabindex:"0"}}]},115:function(e,t,i){"use strict";i(3);var n=i(94),s=i(60),a=i(5),r=i(1),o=i(4);Object(a.a)({_template:o.a`
    <style>
      :host {
        display: inline-block;
      }
    </style>
    <slot id="content"></slot>
`,is:"iron-input",behaviors:[s.a],properties:{bindValue:{type:String,value:""},value:{type:String,computed:"_computeValue(bindValue)"},allowedPattern:{type:String},autoValidate:{type:Boolean,value:!1},_inputElement:Object},observers:["_bindValueChanged(bindValue, _inputElement)"],listeners:{input:"_onInput",keypress:"_onKeypress"},created:function(){n.a.requestAvailability(),this._previousValidInput="",this._patternAlreadyChecked=!1},attached:function(){this._observer=Object(r.a)(this).observeNodes(function(e){this._initSlottedInput()}.bind(this))},detached:function(){this._observer&&(Object(r.a)(this).unobserveNodes(this._observer),this._observer=null)},get inputElement(){return this._inputElement},_initSlottedInput:function(){this._inputElement=this.getEffectiveChildren()[0],this.inputElement&&this.inputElement.value&&(this.bindValue=this.inputElement.value),this.fire("iron-input-ready")},get _patternRegExp(){var e;if(this.allowedPattern)e=new RegExp(this.allowedPattern);else switch(this.inputElement.type){case"number":e=/[0-9.,e-]/}return e},_bindValueChanged:function(e,t){t&&(void 0===e?t.value=null:e!==t.value&&(this.inputElement.value=e),this.autoValidate&&this.validate(),this.fire("bind-value-changed",{value:e}))},_onInput:function(){this.allowedPattern&&!this._patternAlreadyChecked&&(this._checkPatternValidity()||(this._announceInvalidCharacter("Invalid string of characters not entered."),this.inputElement.value=this._previousValidInput));this.bindValue=this._previousValidInput=this.inputElement.value,this._patternAlreadyChecked=!1},_isPrintable:function(e){var t=8==e.keyCode||9==e.keyCode||13==e.keyCode||27==e.keyCode,i=19==e.keyCode||20==e.keyCode||45==e.keyCode||46==e.keyCode||144==e.keyCode||145==e.keyCode||e.keyCode>32&&e.keyCode<41||e.keyCode>111&&e.keyCode<124;return!(t||0==e.charCode&&i)},_onKeypress:function(e){if(this.allowedPattern||"number"===this.inputElement.type){var t=this._patternRegExp;if(t&&!(e.metaKey||e.ctrlKey||e.altKey)){this._patternAlreadyChecked=!0;var i=String.fromCharCode(e.charCode);this._isPrintable(e)&&!t.test(i)&&(e.preventDefault(),this._announceInvalidCharacter("Invalid character "+i+" not entered."))}}},_checkPatternValidity:function(){var e=this._patternRegExp;if(!e)return!0;for(var t=0;t<this.inputElement.value.length;t++)if(!e.test(this.inputElement.value[t]))return!1;return!0},validate:function(){if(!this.inputElement)return this.invalid=!1,!0;var e=this.inputElement.checkValidity();return e&&(this.required&&""===this.bindValue?e=!1:this.hasValidator()&&(e=s.a.validate.call(this,this.bindValue))),this.invalid=!e,this.fire("iron-input-validate"),e},_announceInvalidCharacter:function(e){this.fire("iron-announce",{text:e})},_computeValue:function(e){return e}})},125:function(e,t,i){"use strict";i(46),i(68),i(42),i(47);const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(n.content)},150:function(e,t,i){"use strict";i(3),i(46),i(47),i(125);var n=i(5),s=i(4),a=i(112);Object(n.a)({_template:s.a`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[a.a]})},179:function(e,t,i){"use strict";var n=i(8);t.a=Object(n.a)(e=>(class extends e{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(e){return e}}))},180:function(e,t,i){"use strict";i.d(t,"a",function(){return s});var n=i(195);const s=e=>void 0===e.attributes.friendly_name?Object(n.a)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||""},183:function(e,t,i){"use strict";i.d(t,"a",function(){return a});i(111);const n=customElements.get("iron-icon");let s=!1;class a extends n{constructor(...e){var t,i,n;super(...e),n=void 0,(i="_iconsetName")in(t=this)?Object.defineProperty(t,i,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[i]=n}listen(e,t,n){super.listen(e,t,n),s||"mdi"!==this._iconsetName||(s=!0,i.e(88).then(i.bind(null,225)))}}customElements.define("ha-icon",a)},184:function(e,t,i){"use strict";i.d(t,"a",function(){return s});var n=i(122);const s=e=>Object(n.a)(e.entity_id)},185:function(e,t,i){"use strict";i.d(t,"a",function(){return a});var n=i(121);const s={alert:"hass:alert",alexa:"hass:amazon-alexa",automation:"hass:robot",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:settings",conversation:"hass:text-to-speech",counter:"hass:counter",device_tracker:"hass:account",fan:"hass:fan",google_assistant:"hass:google-assistant",group:"hass:google-circles-communities",history_graph:"hass:chart-line",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:drawing",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",persistent_notification:"hass:bell",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:palette",script:"hass:script-text",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weather:"hass:weather-cloudy",weblink:"hass:open-in-new",zone:"hass:map-marker-radius"},a=(e,t)=>{if(e in s)return s[e];switch(e){case"alarm_control_panel":switch(t){case"armed_home":return"hass:bell-plus";case"armed_night":return"hass:bell-sleep";case"disarmed":return"hass:bell-outline";case"triggered":return"hass:bell-ring";default:return"hass:bell"}case"binary_sensor":return t&&"off"===t?"hass:radiobox-blank":"hass:checkbox-marked-circle";case"cover":return"closed"===t?"hass:window-closed":"hass:window-open";case"lock":return t&&"unlocked"===t?"hass:lock-open":"hass:lock";case"media_player":return t&&"off"!==t&&"idle"!==t?"hass:cast-connected":"hass:cast";case"zwave":switch(t){case"dead":return"hass:emoticon-dead";case"sleeping":return"hass:sleep";case"initializing":return"hass:timer-sand";default:return"hass:z-wave"}default:return console.warn("Unable to find icon for domain "+e+" ("+t+")"),n.a}}},190:function(e,t,i){"use strict";i(3),i(46),i(42),i(47);var n=i(5),s=i(4);Object(n.a)({_template:s.a`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},191:function(e,t,i){"use strict";var n=i(0),s=(i(183),i(184)),a=i(196),r=i(211),o=i(193),l=i(212);function d(e){var t,i=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var n=i.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}let f=function(e,t,i,n){var s=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(n){t.forEach(function(t){var s=t.placement;if(t.kind===n&&("static"===s||"prototype"===s)){var a="static"===s?e:i;this.defineClassElement(a,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var n=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],n=[],s={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,s)},this),e.forEach(function(e){if(!c(e))return i.push(e);var t=this.decorateElement(e,s);i.push(t.element),i.push.apply(i,t.extras),n.push.apply(n,t.finishers)},this),!t)return{elements:i,finishers:n};var a=this.decorateConstructor(i,t);return n.push.apply(n,a.finishers),a.finishers=n,a},addElementPlacement:function(e,t,i){var n=t[e.placement];if(!i&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var i=[],n=[],s=e.decorators,a=s.length-1;a>=0;a--){var r=t[e.placement];r.splice(r.indexOf(e.key),1);var o=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,s[a])(o)||o);e=l.element,this.addElementPlacement(e,t),l.finisher&&n.push(l.finisher);var d=l.extras;if(d){for(var h=0;h<d.length;h++)this.addElementPlacement(d[h],t);i.push.apply(i,d)}}return{element:e,finishers:n,extras:i}},decorateConstructor:function(e,t){for(var i=[],n=t.length-1;n>=0;n--){var s=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[n])(s)||s);if(void 0!==a.finisher&&i.push(a.finisher),void 0!==a.elements){e=a.elements;for(var r=0;r<e.length-1;r++)for(var o=r+1;o<e.length;o++)if(e[r].key===e[o].key&&e[r].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[r].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=m(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var s=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:i,placement:n,descriptor:Object.assign({},s)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(s,"get","The property descriptor of a field descriptor"),this.disallowProperty(s,"set","The property descriptor of a field descriptor"),this.disallowProperty(s,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=p(e,"finisher"),n=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:n}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher"),n=this.toElementDescriptors(e.elements);return{elements:n,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var n=(0,t[i])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(n)for(var a=0;a<n.length;a++)s=n[a](s);var r=t(function(e){s.initializeInstanceElements(e,o.elements)},i),o=s.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},n=0;n<e.length;n++){var s,a=e[n];if("method"===a.kind&&(s=t.find(i)))if(u(a.descriptor)||u(s.descriptor)){if(c(a)||c(s))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");s.descriptor=a.descriptor}else{if(c(a)){if(c(s))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");s.decorators=a.decorators}h(a,s)}else t.push(a)}return t}(r.d.map(d)),e);return s.initializeClassElements(r.F,o.elements),s.runClassFinishers(r.F,o.finishers)}(null,function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"stateObj",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"overrideIcon",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"overrideImage",value:void 0},{kind:"field",decorators:[Object(n.g)({type:Boolean})],key:"stateColor",value:void 0},{kind:"field",decorators:[Object(n.h)("ha-icon")],key:"_icon",value:void 0},{kind:"method",key:"render",value:function(){const e=this.stateObj;if(!e)return n.f``;const t=Object(s.a)(e);return n.f`
      <ha-icon
        id="icon"
        data-domain=${Object(o.a)(this.stateColor||"light"===t&&!1!==this.stateColor?t:void 0)}
        data-state=${Object(r.a)(e)}
        .icon=${this.overrideIcon||Object(a.a)(e)}
      ></ha-icon>
    `}},{kind:"method",key:"updated",value:function(e){if(!e.has("stateObj")||!this.stateObj)return;const t=this.stateObj,i={color:"",filter:""},n={backgroundImage:""};if(t)if(t.attributes.entity_picture&&!this.overrideIcon||this.overrideImage){let e=this.overrideImage||t.attributes.entity_picture;this.hass&&(e=this.hass.hassUrl(e)),n.backgroundImage=`url(${e})`,i.display="none"}else{if(t.attributes.hs_color&&!1!==this.stateColor){const e=t.attributes.hs_color[0],n=t.attributes.hs_color[1];n>10&&(i.color=`hsl(${e}, 100%, ${100-n/2}%)`)}if(t.attributes.brightness&&!1!==this.stateColor){const e=t.attributes.brightness;if("number"!=typeof e){const i=`Type error: state-badge expected number, but type of ${t.entity_id}.attributes.brightness is ${typeof e} (${e})`;console.warn(i)}i.filter=`brightness(${(e+245)/5}%)`}}Object.assign(this._icon.style,i),Object.assign(this.style,n)}},{kind:"get",static:!0,key:"styles",value:function(){return n.c`
      :host {
        position: relative;
        display: inline-block;
        width: 40px;
        color: var(--paper-item-icon-color, #44739e);
        border-radius: 50%;
        height: 40px;
        text-align: center;
        background-size: cover;
        line-height: 40px;
        vertical-align: middle;
      }

      ha-icon {
        transition: color 0.3s ease-in-out, filter 0.3s ease-in-out;
      }

      ${l.a}
    `}}]}},n.a);customElements.define("state-badge",f)},192:function(e,t,i){"use strict";i(3),i(68),i(154);var n=i(5),s=i(4),a=i(129);const r=s.a`
  <style include="paper-spinner-styles"></style>

  <div id="spinnerContainer" class-name="[[__computeContainerClasses(active, __coolingDown)]]" on-animationend="__reset" on-webkit-animation-end="__reset">
    <div class="spinner-layer layer-1">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-2">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-3">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-4">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>
  </div>
`;r.setAttribute("strip-whitespace",""),Object(n.a)({_template:r,is:"paper-spinner",behaviors:[a.a]})},193:function(e,t,i){"use strict";i.d(t,"a",function(){return s});var n=i(9);const s=Object(n.f)(e=>t=>{if(void 0===e&&t instanceof n.a){if(e!==t.value){const e=t.committer.name;t.committer.element.removeAttribute(e)}}else t.setValue(e)})},195:function(e,t,i){"use strict";i.d(t,"a",function(){return n});const n=e=>e.substr(e.indexOf(".")+1)},196:function(e,t,i){"use strict";var n=i(121);var s=i(122),a=i(185);const r={humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge",power:"hass:flash",signal_strength:"hass:wifi"};i.d(t,"a",function(){return l});const o={binary_sensor:e=>{const t=e.state&&"off"===e.state;switch(e.attributes.device_class){case"battery":return t?"hass:battery":"hass:battery-outline";case"cold":return t?"hass:thermometer":"hass:snowflake";case"connectivity":return t?"hass:server-network-off":"hass:server-network";case"door":return t?"hass:door-closed":"hass:door-open";case"garage_door":return t?"hass:garage":"hass:garage-open";case"gas":case"power":case"problem":case"safety":case"smoke":return t?"hass:shield-check":"hass:alert";case"heat":return t?"hass:thermometer":"hass:fire";case"light":return t?"hass:brightness-5":"hass:brightness-7";case"lock":return t?"hass:lock":"hass:lock-open";case"moisture":return t?"hass:water-off":"hass:water";case"motion":return t?"hass:walk":"hass:run";case"occupancy":return t?"hass:home-outline":"hass:home";case"opening":return t?"hass:square":"hass:square-outline";case"plug":return t?"hass:power-plug-off":"hass:power-plug";case"presence":return t?"hass:home-outline":"hass:home";case"sound":return t?"hass:music-note-off":"hass:music-note";case"vibration":return t?"hass:crop-portrait":"hass:vibrate";case"window":return t?"hass:window-closed":"hass:window-open";default:return t?"hass:radiobox-blank":"hass:checkbox-marked-circle"}},cover:e=>{const t="closed"!==e.state;switch(e.attributes.device_class){case"garage":return t?"hass:garage-open":"hass:garage";case"door":return t?"hass:door-open":"hass:door-closed";case"shutter":return t?"hass:window-shutter-open":"hass:window-shutter";case"blind":return t?"hass:blinds-open":"hass:blinds";case"window":return t?"hass:window-open":"hass:window-closed";default:return Object(a.a)("cover",e.state)}},sensor:e=>{const t=e.attributes.device_class;if(t&&t in r)return r[t];if("battery"===t){const t=Number(e.state);if(isNaN(t))return"hass:battery-unknown";const i=10*Math.round(t/10);return i>=100?"hass:battery":i<=0?"hass:battery-alert":`hass:battery-${i}`}const i=e.attributes.unit_of_measurement;return i===n.j||i===n.k?"hass:thermometer":Object(a.a)("sensor")},input_datetime:e=>e.attributes.has_date?e.attributes.has_time?Object(a.a)("input_datetime"):"hass:calendar":"hass:clock"},l=e=>{if(!e)return n.a;if(e.attributes.icon)return e.attributes.icon;const t=Object(s.a)(e.entity_id);return t in o?o[t](e):Object(a.a)(t,e.state)}},199:function(e,t,i){"use strict";i.d(t,"a",function(){return n}),i.d(t,"c",function(){return s}),i.d(t,"b",function(){return a});const n=function(){try{(new Date).toLocaleDateString("i")}catch(e){return"RangeError"===e.name}return!1}(),s=function(){try{(new Date).toLocaleTimeString("i")}catch(e){return"RangeError"===e.name}return!1}(),a=function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()},200:function(e,t,i){"use strict";var n={},s=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,a="[^\\s]+",r=/\[([^]*?)\]/gm,o=function(){};function l(e,t){for(var i=[],n=0,s=e.length;n<s;n++)i.push(e[n].substr(0,t));return i}function d(e){return function(t,i,n){var s=n[e].indexOf(i.charAt(0).toUpperCase()+i.substr(1).toLowerCase());~s&&(t.month=s)}}function h(e,t){for(e=String(e),t=t||2;e.length<t;)e="0"+e;return e}var c=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],u=["January","February","March","April","May","June","July","August","September","October","November","December"],p=l(u,3),m=l(c,3);n.i18n={dayNamesShort:m,dayNames:c,monthNamesShort:p,monthNames:u,amPm:["am","pm"],DoFn:function(e){return e+["th","st","nd","rd"][e%10>3?0:(e-e%10!=10)*e%10]}};var f={D:function(e){return e.getDate()},DD:function(e){return h(e.getDate())},Do:function(e,t){return t.DoFn(e.getDate())},d:function(e){return e.getDay()},dd:function(e){return h(e.getDay())},ddd:function(e,t){return t.dayNamesShort[e.getDay()]},dddd:function(e,t){return t.dayNames[e.getDay()]},M:function(e){return e.getMonth()+1},MM:function(e){return h(e.getMonth()+1)},MMM:function(e,t){return t.monthNamesShort[e.getMonth()]},MMMM:function(e,t){return t.monthNames[e.getMonth()]},YY:function(e){return h(String(e.getFullYear()),4).substr(2)},YYYY:function(e){return h(e.getFullYear(),4)},h:function(e){return e.getHours()%12||12},hh:function(e){return h(e.getHours()%12||12)},H:function(e){return e.getHours()},HH:function(e){return h(e.getHours())},m:function(e){return e.getMinutes()},mm:function(e){return h(e.getMinutes())},s:function(e){return e.getSeconds()},ss:function(e){return h(e.getSeconds())},S:function(e){return Math.round(e.getMilliseconds()/100)},SS:function(e){return h(Math.round(e.getMilliseconds()/10),2)},SSS:function(e){return h(e.getMilliseconds(),3)},a:function(e,t){return e.getHours()<12?t.amPm[0]:t.amPm[1]},A:function(e,t){return e.getHours()<12?t.amPm[0].toUpperCase():t.amPm[1].toUpperCase()},ZZ:function(e){var t=e.getTimezoneOffset();return(t>0?"-":"+")+h(100*Math.floor(Math.abs(t)/60)+Math.abs(t)%60,4)}},_={D:["\\d\\d?",function(e,t){e.day=t}],Do:["\\d\\d?"+a,function(e,t){e.day=parseInt(t,10)}],M:["\\d\\d?",function(e,t){e.month=t-1}],YY:["\\d\\d?",function(e,t){var i=+(""+(new Date).getFullYear()).substr(0,2);e.year=""+(t>68?i-1:i)+t}],h:["\\d\\d?",function(e,t){e.hour=t}],m:["\\d\\d?",function(e,t){e.minute=t}],s:["\\d\\d?",function(e,t){e.second=t}],YYYY:["\\d{4}",function(e,t){e.year=t}],S:["\\d",function(e,t){e.millisecond=100*t}],SS:["\\d{2}",function(e,t){e.millisecond=10*t}],SSS:["\\d{3}",function(e,t){e.millisecond=t}],d:["\\d\\d?",o],ddd:[a,o],MMM:[a,d("monthNamesShort")],MMMM:[a,d("monthNames")],a:[a,function(e,t,i){var n=t.toLowerCase();n===i.amPm[0]?e.isPm=!1:n===i.amPm[1]&&(e.isPm=!0)}],ZZ:["[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z",function(e,t){var i,n=(t+"").match(/([+-]|\d\d)/gi);n&&(i=60*n[1]+parseInt(n[2],10),e.timezoneOffset="+"===n[0]?i:-i)}]};_.dd=_.d,_.dddd=_.ddd,_.DD=_.D,_.mm=_.m,_.hh=_.H=_.HH=_.h,_.MM=_.M,_.ss=_.s,_.A=_.a,n.masks={default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"},n.format=function(e,t,i){var a=i||n.i18n;if("number"==typeof e&&(e=new Date(e)),"[object Date]"!==Object.prototype.toString.call(e)||isNaN(e.getTime()))throw new Error("Invalid Date in fecha.format");t=n.masks[t]||t||n.masks.default;var o=[];return(t=(t=t.replace(r,function(e,t){return o.push(t),"??"})).replace(s,function(t){return t in f?f[t](e,a):t.slice(1,t.length-1)})).replace(/\?\?/g,function(){return o.shift()})},n.parse=function(e,t,i){var a=i||n.i18n;if("string"!=typeof t)throw new Error("Invalid format in fecha.parse");if(t=n.masks[t]||t,e.length>1e3)return null;var r,o={},l=[],d=(r=t,r.replace(/[|\\{()[^$+*?.-]/g,"\\$&")).replace(s,function(e){if(_[e]){var t=_[e];return l.push(t[1]),"("+t[0]+")"}return e}),h=e.match(new RegExp(d,"i"));if(!h)return null;for(var c=1;c<h.length;c++)l[c-1](o,h[c],a);var u,p=new Date;return!0===o.isPm&&null!=o.hour&&12!=+o.hour?o.hour=+o.hour+12:!1===o.isPm&&12==+o.hour&&(o.hour=0),null!=o.timezoneOffset?(o.minute=+(o.minute||0)-+o.timezoneOffset,u=new Date(Date.UTC(o.year||p.getFullYear(),o.month||0,o.day||1,o.hour||0,o.minute||0,o.second||0,o.millisecond||0))):u=new Date(o.year||p.getFullYear(),o.month||0,o.day||1,o.hour||0,o.minute||0,o.second||0,o.millisecond||0),u},t.a=n},211:function(e,t,i){"use strict";i.d(t,"a",function(){return n});const n=e=>{const t=e.entity_id.split(".")[0];let i=e.state;return"climate"===t&&(i=e.attributes.hvac_action),i}},212:function(e,t,i){"use strict";i.d(t,"a",function(){return n});const n=i(0).c`
  ha-icon[data-domain="alert"][data-state="on"],
  ha-icon[data-domain="automation"][data-state="on"],
  ha-icon[data-domain="binary_sensor"][data-state="on"],
  ha-icon[data-domain="calendar"][data-state="on"],
  ha-icon[data-domain="camera"][data-state="streaming"],
  ha-icon[data-domain="cover"][data-state="open"],
  ha-icon[data-domain="fan"][data-state="on"],
  ha-icon[data-domain="light"][data-state="on"],
  ha-icon[data-domain="input_boolean"][data-state="on"],
  ha-icon[data-domain="lock"][data-state="unlocked"],
  ha-icon[data-domain="media_player"][data-state="paused"],
  ha-icon[data-domain="media_player"][data-state="playing"],
  ha-icon[data-domain="script"][data-state="running"],
  ha-icon[data-domain="sun"][data-state="above_horizon"],
  ha-icon[data-domain="switch"][data-state="on"],
  ha-icon[data-domain="timer"][data-state="active"],
  ha-icon[data-domain="vacuum"][data-state="cleaning"] {
    color: var(--paper-item-icon-active-color, #fdd835);
  }

  ha-icon[data-domain="climate"][data-state="cooling"] {
    color: var(--cool-color, #2b9af9);
  }

  ha-icon[data-domain="climate"][data-state="heating"] {
    color: var(--heat-color, #ff8100);
  }

  ha-icon[data-domain="alarm_control_panel"] {
    color: var(--alarm-color-armed, var(--label-badge-red));
  }

  ha-icon[data-domain="alarm_control_panel"][data-state="disarmed"] {
    color: var(--alarm-color-disarmed, var(--label-badge-green));
  }

  ha-icon[data-domain="alarm_control_panel"][data-state="pending"],
  ha-icon[data-domain="alarm_control_panel"][data-state="arming"] {
    color: var(--alarm-color-pending, var(--label-badge-yellow));
    animation: pulse 1s infinite;
  }

  ha-icon[data-domain="alarm_control_panel"][data-state="triggered"] {
    color: var(--alarm-color-triggered, var(--label-badge-red));
    animation: pulse 1s infinite;
  }

  @keyframes pulse {
    0% {
      opacity: 1;
    }
    100% {
      opacity: 0;
    }
  }

  ha-icon[data-domain="plant"][data-state="problem"],
  ha-icon[data-domain="zwave"][data-state="dead"] {
    color: var(--error-state-color, #db4437);
  }

  /* Color the icon if unavailable */
  ha-icon[data-state="unavailable"] {
    color: var(--state-icon-unavailable-color);
  }
`},215:function(e,t,i){"use strict";i.d(t,"a",function(){return a}),i.d(t,"b",function(){return r});var n=i(200),s=i(199);const a=s.c?(e,t)=>e.toLocaleTimeString(t,{hour:"numeric",minute:"2-digit"}):e=>n.a.format(e,"shortTime"),r=s.c?(e,t)=>e.toLocaleTimeString(t,{hour:"numeric",minute:"2-digit",second:"2-digit"}):e=>n.a.format(e,"mediumTime")},221:function(e,t,i){"use strict";i(110),i(72),i(150),i(190),i(239);var n=i(127),s=(i(191),i(180)),a=i(0),r=i(13),o=i(122);function l(e){var t,i=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var n=i.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t,i){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=f(e)););return e}(e,t);if(n){var s=Object.getOwnPropertyDescriptor(n,t);return s.get?s.get.call(i):s.value}})(e,t,i||e)}function f(e){return(f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let _=function(e,t,i,n){var s=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(n){t.forEach(function(t){var s=t.placement;if(t.kind===n&&("static"===s||"prototype"===s)){var a="static"===s?e:i;this.defineClassElement(a,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var n=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],n=[],s={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,s)},this),e.forEach(function(e){if(!h(e))return i.push(e);var t=this.decorateElement(e,s);i.push(t.element),i.push.apply(i,t.extras),n.push.apply(n,t.finishers)},this),!t)return{elements:i,finishers:n};var a=this.decorateConstructor(i,t);return n.push.apply(n,a.finishers),a.finishers=n,a},addElementPlacement:function(e,t,i){var n=t[e.placement];if(!i&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var i=[],n=[],s=e.decorators,a=s.length-1;a>=0;a--){var r=t[e.placement];r.splice(r.indexOf(e.key),1);var o=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,s[a])(o)||o);e=l.element,this.addElementPlacement(e,t),l.finisher&&n.push(l.finisher);var d=l.extras;if(d){for(var h=0;h<d.length;h++)this.addElementPlacement(d[h],t);i.push.apply(i,d)}}return{element:e,finishers:n,extras:i}},decorateConstructor:function(e,t){for(var i=[],n=t.length-1;n>=0;n--){var s=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[n])(s)||s);if(void 0!==a.finisher&&i.push(a.finisher),void 0!==a.elements){e=a.elements;for(var r=0;r<e.length-1;r++)for(var o=r+1;o<e.length;o++)if(e[r].key===e[o].key&&e[r].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[r].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=p(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var s=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:i,placement:n,descriptor:Object.assign({},s)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(s,"get","The property descriptor of a field descriptor"),this.disallowProperty(s,"set","The property descriptor of a field descriptor"),this.disallowProperty(s,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=u(e,"finisher"),n=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:n}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=u(e,"finisher"),n=this.toElementDescriptors(e.elements);return{elements:n,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var n=(0,t[i])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(n)for(var a=0;a<n.length;a++)s=n[a](s);var r=t(function(e){s.initializeInstanceElements(e,o.elements)},i),o=s.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},n=0;n<e.length;n++){var s,a=e[n];if("method"===a.kind&&(s=t.find(i)))if(c(a.descriptor)||c(s.descriptor)){if(h(a)||h(s))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");s.descriptor=a.descriptor}else{if(h(a)){if(h(s))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");s.decorators=a.decorators}d(a,s)}else t.push(a)}return t}(r.d.map(l)),e);return s.initializeClassElements(r.F,o.elements),s.runClassFinishers(r.F,o.finishers)}(null,function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[Object(a.g)({type:Boolean})],key:"autofocus",value:void 0},{kind:"field",decorators:[Object(a.g)({type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[Object(a.g)({type:Boolean,attribute:"allow-custom-entity"})],key:"allowCustomEntity",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"label",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"value",value:void 0},{kind:"field",decorators:[Object(a.g)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[Object(a.g)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[Object(a.g)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"entityFilter",value:void 0},{kind:"field",decorators:[Object(a.g)({type:Boolean})],key:"_opened",value:void 0},{kind:"field",decorators:[Object(a.g)()],key:"_hass",value:void 0},{kind:"field",key:"_getStates",value(){return Object(n.a)((e,t,i,n,s)=>{let a=[];if(!e)return[];let r=Object.keys(e.states);return t&&(r=r.filter(e=>t.includes(Object(o.a)(e)))),i&&(r=r.filter(e=>!i.includes(Object(o.a)(e)))),a=r.sort().map(t=>e.states[t]),s&&(a=a.filter(e=>e.entity_id===this.value||e.attributes.device_class&&s.includes(e.attributes.device_class))),n&&(a=a.filter(e=>e.entity_id===this.value||n(e))),a})}},{kind:"method",key:"updated",value:function(e){m(f(i.prototype),"updated",this).call(this,e),e.has("hass")&&!this._opened&&(this._hass=this.hass)}},{kind:"method",key:"render",value:function(){const e=this._getStates(this._hass,this.includeDomains,this.excludeDomains,this.entityFilter,this.includeDeviceClasses);return a.f`
      <vaadin-combo-box-light
        item-value-path="entity_id"
        item-label-path="entity_id"
        .items=${e}
        .value=${this._value}
        .allowCustomValue=${this.allowCustomEntity}
        .renderer=${(e,t,i)=>{e.firstElementChild||(e.innerHTML='\n      <style>\n        paper-icon-item {\n          margin: -10px;\n          padding: 0;\n        }\n      </style>\n      <paper-icon-item>\n        <state-badge state-obj="[[item]]" slot="item-icon"></state-badge>\n        <paper-item-body two-line="">\n          <div class=\'name\'>[[_computeStateName(item)]]</div>\n          <div secondary>[[item.entity_id]]</div>\n        </paper-item-body>\n      </paper-icon-item>\n    '),e.querySelector("state-badge").stateObj=i.item,e.querySelector(".name").textContent=Object(s.a)(i.item),e.querySelector("[secondary]").textContent=i.item.entity_id}}
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
      >
        <paper-input
          .autofocus=${this.autofocus}
          .label=${void 0===this.label&&this._hass?this._hass.localize("ui.components.entity.entity-picker.entity"):this.label}
          .value=${this._value}
          .disabled=${this.disabled}
          class="input"
          autocapitalize="none"
          autocomplete="off"
          autocorrect="off"
          spellcheck="false"
        >
          ${this.value?a.f`
                <paper-icon-button
                  aria-label=${this.hass.localize("ui.components.entity.entity-picker.clear")}
                  slot="suffix"
                  class="clear-button"
                  icon="hass:close"
                  @click=${this._clearValue}
                  no-ripple
                >
                  Clear
                </paper-icon-button>
              `:""}
          ${e.length>0?a.f`
                <paper-icon-button
                  aria-label=${this.hass.localize("ui.components.entity.entity-picker.show_entities")}
                  slot="suffix"
                  class="toggle-button"
                  .icon=${this._opened?"hass:menu-up":"hass:menu-down"}
                >
                  Toggle
                </paper-icon-button>
              `:""}
        </paper-input>
      </vaadin-combo-box-light>
    `}},{kind:"method",key:"_clearValue",value:function(e){e.stopPropagation(),this._setValue("")}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_valueChanged",value:function(e){const t=e.detail.value;t!==this._value&&this._setValue(t)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout(()=>{Object(r.a)(this,"value-changed",{value:e}),Object(r.a)(this,"change")},0)}},{kind:"get",static:!0,key:"styles",value:function(){return a.c`
      paper-input > paper-icon-button {
        width: 24px;
        height: 24px;
        padding: 2px;
        color: var(--secondary-text-color);
      }
      [hidden] {
        display: none;
      }
    `}}]}},a.a);customElements.define("ha-entity-picker",_)},226:function(e,t,i){"use strict";i(3),i(46);var n=i(5),s=i(1),a=i(4),r=i(135);Object(n.a)({_template:a.a`
    <style>
      :host {
        display: block;
        /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
        position: relative;
        z-index: 0;
      }

      #wrapper ::slotted([slot=header]) {
        @apply --layout-fixed-top;
        z-index: 1;
      }

      #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) {
        height: 100%;
      }

      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {
        position: absolute;
      }

      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) #wrapper #contentContainer {
        @apply --layout-fit;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
        position: relative;
      }

      :host([fullbleed]) {
        @apply --layout-vertical;
        @apply --layout-fit;
      }

      :host([fullbleed]) #wrapper,
      :host([fullbleed]) #wrapper #contentContainer {
        @apply --layout-vertical;
        @apply --layout-flex;
      }

      #contentContainer {
        /* Create a stacking context here so that all children appear below the header. */
        position: relative;
        z-index: 0;
      }

      @media print {
        :host([has-scrolling-region]) #wrapper #contentContainer {
          overflow-y: visible;
        }
      }

    </style>

    <div id="wrapper" class="initializing">
      <slot id="headerSlot" name="header"></slot>

      <div id="contentContainer">
        <slot></slot>
      </div>
    </div>
`,is:"app-header-layout",behaviors:[r.a],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return Object(s.a)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var e=this.header;if(this.isAttached&&e){this.$.wrapper.classList.remove("initializing"),e.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var t=e.offsetHeight;this.hasScrollingRegion?(e.style.left="",e.style.right=""):requestAnimationFrame(function(){var t=this.getBoundingClientRect(),i=document.documentElement.clientWidth-t.right;e.style.left=t.left+"px",e.style.right=i+"px"}.bind(this));var i=this.$.contentContainer.style;e.fixed&&!e.condenses&&this.hasScrollingRegion?(i.marginTop=t+"px",i.paddingTop=""):(i.paddingTop=t+"px",i.marginTop="")}}})},248:function(e,t,i){"use strict";i.d(t,"a",function(){return s});var n=i(200);const s=i(199).a?(e,t)=>e.toLocaleDateString(t,{year:"numeric",month:"long",day:"numeric"}):e=>n.a.format(e,"longDate")},310:function(e,t,i){"use strict";var n=i(11),s=i(21),a=i(23);const r=/\/\*\*\s+vaadin-dev-mode:start([\s\S]*)vaadin-dev-mode:end\s+\*\*\//i,o=window.Vaadin&&window.Vaadin.Flow&&window.Vaadin.Flow.clients;function l(e,t){if("function"!=typeof e)return;const i=r.exec(e.toString());if(i)try{e=new Function(i[1])}catch(n){console.log("vaadin-development-mode-detector: uncommentAndRun() failed",n)}return e(t)}window.Vaadin=window.Vaadin||{};const d=function(e,t){if(window.Vaadin.developmentMode)return l(e,t)};function h(){}void 0===window.Vaadin.developmentMode&&(window.Vaadin.developmentMode=function(){try{return!!localStorage.getItem("vaadin.developmentmode.force")||["localhost","127.0.0.1"].indexOf(window.location.hostname)>=0&&(o?!function(){if(o){const e=Object.keys(o).map(e=>o[e]).filter(e=>e.productionMode);if(e.length>0)return!0}return!1}():!l(function(){return!0}))}catch(e){return!1}}());const c=function(){return d(h)};let u;i.d(t,"a",function(){return p}),window.Vaadin||(window.Vaadin={}),window.Vaadin.registrations=window.Vaadin.registrations||[],window.Vaadin.developmentModeCallback=window.Vaadin.developmentModeCallback||{},window.Vaadin.developmentModeCallback["vaadin-usage-statistics"]=function(){c&&c()};const p=e=>(class extends e{static _finalizeClass(){super._finalizeClass(),this.is&&(window.Vaadin.registrations.push(this),window.Vaadin.developmentModeCallback&&(u=s.a.debounce(u,n.b,()=>{window.Vaadin.developmentModeCallback["vaadin-usage-statistics"]()}),Object(a.a)(u)))}ready(){super.ready(),null===document.doctype&&console.warn('Vaadin components require the "standards mode" declaration. Please add <!DOCTYPE html> to the HTML document.')}})},326:function(e,t,i){"use strict";i.d(t,"a",function(){return n});const n=e=>(class extends((e=>(class extends e{static get properties(){var e={tabindex:{type:Number,value:0,reflectToAttribute:!0,observer:"_tabindexChanged"}};return window.ShadyDOM&&(e.tabIndex=e.tabindex),e}}))(e)){static get properties(){return{autofocus:{type:Boolean},_previousTabIndex:{type:Number},disabled:{type:Boolean,observer:"_disabledChanged",reflectToAttribute:!0},_isShiftTabbing:{type:Boolean}}}ready(){this.addEventListener("focusin",e=>{e.composedPath()[0]===this?this._focus(e):-1===e.composedPath().indexOf(this.focusElement)||this.disabled||this._setFocused(!0)}),this.addEventListener("focusout",e=>this._setFocused(!1)),super.ready();const e=e=>{e.composed||e.target.dispatchEvent(new CustomEvent(e.type,{bubbles:!0,composed:!0,cancelable:!1}))};this.shadowRoot.addEventListener("focusin",e),this.shadowRoot.addEventListener("focusout",e),this.addEventListener("keydown",e=>{if(!e.defaultPrevented&&9===e.keyCode)if(e.shiftKey)this._isShiftTabbing=!0,HTMLElement.prototype.focus.apply(this),this._setFocused(!1),setTimeout(()=>this._isShiftTabbing=!1,0);else{const e=window.navigator.userAgent.match(/Firefox\/(\d\d\.\d)/);if(e&&parseFloat(e[1])>=63&&parseFloat(e[1])<66&&this.parentNode&&this.nextSibling){const e=document.createElement("input");e.style.position="absolute",e.style.opacity=0,e.tabIndex=this.tabIndex,this.parentNode.insertBefore(e,this.nextSibling),e.focus(),e.addEventListener("focusout",()=>this.parentNode.removeChild(e))}}}),!this.autofocus||this.focused||this.disabled||window.requestAnimationFrame(()=>{this._focus(),this._setFocused(!0),this.setAttribute("focus-ring","")}),this._boundKeydownListener=this._bodyKeydownListener.bind(this),this._boundKeyupListener=this._bodyKeyupListener.bind(this)}connectedCallback(){super.connectedCallback(),document.body.addEventListener("keydown",this._boundKeydownListener,!0),document.body.addEventListener("keyup",this._boundKeyupListener,!0)}disconnectedCallback(){super.disconnectedCallback(),document.body.removeEventListener("keydown",this._boundKeydownListener,!0),document.body.removeEventListener("keyup",this._boundKeyupListener,!0),this.hasAttribute("focused")&&this._setFocused(!1)}_setFocused(e){e?this.setAttribute("focused",""):this.removeAttribute("focused"),e&&this._tabPressed?this.setAttribute("focus-ring",""):this.removeAttribute("focus-ring")}_bodyKeydownListener(e){this._tabPressed=9===e.keyCode}_bodyKeyupListener(){this._tabPressed=!1}get focusElement(){return window.console.warn(`Please implement the 'focusElement' property in <${this.localName}>`),this}_focus(e){this._isShiftTabbing||(this.focusElement.focus(),this._setFocused(!0))}focus(){this.focusElement&&!this.disabled&&(this.focusElement.focus(),this._setFocused(!0))}blur(){this.focusElement.blur(),this._setFocused(!1)}_disabledChanged(e){this.focusElement.disabled=e,e?(this.blur(),this._previousTabIndex=this.tabindex,this.tabindex=-1,this.setAttribute("aria-disabled","true")):(void 0!==this._previousTabIndex&&(this.tabindex=this._previousTabIndex),this.removeAttribute("aria-disabled"))}_tabindexChanged(e){void 0!==e&&(this.focusElement.tabIndex=e),this.disabled&&this.tabindex&&(-1!==this.tabindex&&(this._previousTabIndex=this.tabindex),this.tabindex=e=void 0),window.ShadyDOM&&this.setProperties({tabIndex:e,tabindex:e})}click(){this.disabled||super.click()}})},340:function(e,t,i){"use strict";var n=i(29),s=i(48),a=i(218),r=i(326),o=i(310),l=i(4),d=i(35);class h extends(Object(o.a)(Object(r.a)(Object(a.a)(Object(s.a)(n.a))))){static get template(){return l.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        outline: none;
        white-space: nowrap;
      }

      :host([hidden]) {
        display: none !important;
      }

      /* Ensure the button is always aligned on the baseline */
      .vaadin-button-container::before {
        content: "\\2003";
        display: inline-block;
        width: 0;
      }

      .vaadin-button-container {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
        height: 100%;
        min-height: inherit;
        text-shadow: inherit;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      [part="prefix"],
      [part="suffix"] {
        flex: none;
      }

      [part="label"] {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      #button {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        cursor: inherit;
      }
    </style>
    <div class="vaadin-button-container">
      <div part="prefix">
        <slot name="prefix"></slot>
      </div>
      <div part="label">
        <slot></slot>
      </div>
      <div part="suffix">
        <slot name="suffix"></slot>
      </div>
    </div>
    <button id="button" type="button"></button>
`}static get is(){return"vaadin-button"}static get version(){return"2.2.1"}ready(){super.ready(),this.setAttribute("role","button"),this.$.button.setAttribute("role","presentation"),this._addActiveListeners()}disconnectedCallback(){super.disconnectedCallback(),this.hasAttribute("active")&&this.removeAttribute("active")}_addActiveListeners(){Object(d.b)(this,"down",()=>!this.disabled&&this.setAttribute("active","")),Object(d.b)(this,"up",()=>this.removeAttribute("active")),this.addEventListener("keydown",e=>!this.disabled&&[13,32].indexOf(e.keyCode)>=0&&this.setAttribute("active","")),this.addEventListener("keyup",()=>this.removeAttribute("active")),this.addEventListener("blur",()=>this.removeAttribute("active"))}get focusElement(){return this.$.button}}customElements.define(h.is,h)},415:function(e,t,i){"use strict";i(352);var n=i(4);const s=n.a`<dom-module id="material-date-picker-overlay" theme-for="vaadin-date-picker-overlay">
  <template>
    <style include="material-overlay">
      :host([fullscreen]) {
        top: 0 !important;
        right: 0 !important;
        bottom: var(--vaadin-overlay-viewport-bottom) !important;
        left: 0 !important;
        align-items: stretch;
        justify-content: stretch;
      }

      [part="overlay"] {
        overflow: hidden;
        -webkit-overflow-scrolling: auto;
      }

      :host(:not([fullscreen])) [part="overlay"] {
        width: 360px;
        max-height: 500px;
        border-radius: 0 4px 4px;
      }

      :host(:not([fullscreen])[right-aligned]) [part="overlay"] {
        border-radius: 4px 0 4px 4px;
      }

      :host(:not([fullscreen])[bottom-aligned]) [part="overlay"] {
        border-radius: 4px;
      }

      :host(:not([fullscreen])[show-week-numbers]) [part="overlay"] {
        width: 396px;
      }

      [part="content"] {
        padding: 0;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(s.content);var a=i(357),r=i(353);class o extends(Object(r.a)(a.a)){static get is(){return"vaadin-date-picker-overlay"}}customElements.define(o.is,o);i(216),i(257),i(254),i(390);const l=n.a`<dom-module id="material-button" theme-for="vaadin-button">
  <template>
    <style>
      :host {
        padding: 8px;
        min-width: 64px;
        box-sizing: border-box;
        display: inline-flex;
        align-items: baseline;
        justify-content: center;
        border-radius: 4px;
        color: var(--material-primary-text-color);
        font-family: var(--material-font-family);
        text-transform: uppercase;
        font-size: var(--material-button-font-size);
        line-height: 20px;
        font-weight: 500;
        letter-spacing: 0.05em;
        white-space: nowrap;
        overflow: hidden;
        transition: box-shadow 0.2s;
        -webkit-tap-highlight-color: transparent;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }

      @-moz-document url-prefix() {
        :host {
          vertical-align: -13px;
        }
      }

      :host::before,
      :host::after {
        content: "";
        pointer-events: none;
        position: absolute;
        border-radius: inherit;
        opacity: 0;
        background-color: currentColor;
      }

      :host::before {
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        transition: opacity 0.5s;
      }

      :host::after {
        border-radius: 50%;
        width: 320px;
        height: 320px;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        transition: all 0.9s;
      }

      [part="label"] ::slotted(*) {
        vertical-align: middle;
      }

      :host(:hover)::before,
      :host([focus-ring])::before {
        opacity: 0.08;
        transition-duration: 0.2s;
      }

      :host([active])::before {
        opacity: 0.16;
        transition: opacity 0.4s;
      }

      :host([active])::after {
        transform: translate(-50%, -50%) scale(0.0000001); /* animation works weirdly with scale(0) */
        opacity: 0.1;
        transition: 0s;
      }

      :host(:hover:not([active]))::after {
        transform: translate(-50%, -50%) scale(1);
        opacity: 0;
      }

      :host([disabled]) {
        pointer-events: none;
        color: var(--material-disabled-text-color);
      }

      /* Contained and outline variants */
      :host([theme~="contained"]),
      :host([theme~="outlined"]) {
        padding: 8px 16px;
      }

      :host([theme~="outlined"]) {
        box-shadow: inset 0 0 0 1px var(--_material-button-outline-color, rgba(0, 0, 0, 0.2));
      }

      :host([theme~="contained"]:not([disabled])) {
        background-color: var(--material-primary-color);
        color: var(--material-primary-contrast-color);
        box-shadow: var(--material-shadow-elevation-2dp);
      }

      :host([theme~="contained"][disabled]) {
        background-color: var(--material-secondary-background-color);
      }

      :host([theme~="contained"]:hover) {
        box-shadow: var(--material-shadow-elevation-4dp);
      }

      :host([theme~="contained"][active]) {
        box-shadow: var(--material-shadow-elevation-8dp);
      }

      /* Icon alignment */

      [part] ::slotted(iron-icon) {
        display: block;
        width: 18px;
        height: 18px;
      }

      [part="prefix"] ::slotted(iron-icon) {
        margin-right: 8px;
        margin-left: -4px;
      }

      [part="suffix"] ::slotted(iron-icon) {
        margin-left: 8px;
        margin-right: -4px;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(l.content);i(340);const d=n.a`<dom-module id="material-date-picker-overlay-content" theme-for="vaadin-date-picker-overlay-content">
  <template>
    <style>
      :host {
        font-family: var(--material-font-family);
        font-size: var(--material-body-font-size);
        -webkit-text-size-adjust: 100%;
        line-height: 1.4;

        /* FIXME(platosha): fix the core styles and remove this override. */
        background: transparent;
      }

      :host([fullscreen]) {
        position: absolute;
      }

      /* Fullscreen Toolbar */

      [part="overlay-header"] {
        display: flex;
        align-items: baseline;
        position: relative;
        z-index: 2;
        color: var(--material-body-text-color);
        background: var(--material-secondary-background-color);
        border-bottom: 2px solid var(--material-primary-color);
        padding: 8px;
        box-shadow: var(--material-shadow-elevation-4dp);
      }

      /* FIXME(platosha): fix the core styles and remove this override. */
      [part="overlay-header"]:not([desktop]) {
        padding-bottom: 8px;
      }

      [part="label"] {
        padding: 0 8px;
        flex: auto;
      }

      [part="clear-button"],
      [part="toggle-button"] {
        font-family: 'material-icons';
        font-size: var(--material-icon-font-size);
        line-height: 24px;
        width: 24px;
        height: 24px;
        text-align: center;
      }

      [part="clear-button"],
      [part="toggle-button"],
      [part="years-toggle-button"] {
        padding: 8px;
        color: var(--material-secondary-text-color);
      }

      [part="clear-button"]:hover,
      [part="toggle-button"]:hover,
      [part="years-toggle-button"]:hover {
        color: inherit;
      }

      [part="clear-button"]::before {
        content: var(--material-icons-clear);
      }

      [part="toggle-button"]::before {
        content: var(--material-icons-calendar);
      }

      [part="years-toggle-button"] {
        position: static;
        padding: 4px 8px;
        font-size: var(--material-body-font-size);
        font-weight: 500;
        line-height: 24px;
        letter-spacing: 0.05em;
        color: var(--material-secondary-text-color);
      }

      [part="years-toggle-button"]::before {
        content: '';
        display: none;
      }

      [part="years-toggle-button"]::after {
        content: var(--material-icons-play);
        display: inline-block;
        width: 24px;
        font-family: 'material-icons';
        font-size: var(--material-icon-font-size);
        line-height: 24px;
        text-align: center;
        transition: transform 100ms cubic-bezier(.4, 0, .2, 1);
      }

      :host([years-visible]) [part="years-toggle-button"]::after {
        transform: rotate(90deg);
      }

      /* Month scroller */

      [part="months"] {
        --vaadin-infinite-scroller-item-height: 320px;
        text-align: center;
      }

      /* Year scroller */

      [part="years"] {
        z-index: 1;
        background: var(--material-secondary-text-color);
        color: var(--material-background-color);
        text-align: center;
      }

      [part="years"]::before {
        z-index: 2;
        border: 0;
        width: 8px;
        height: 8px;
        transform: translateX(-50%) rotate(-45deg);
        background: var(--material-background-color);
      }

      :host([years-visible]) [part="years"]::after {
        top: calc(20px + 16px);
        height: calc(100% - 20px - 16px);
      }

      [part="year-number"] {
        font-size: var(--material-small-font-size);
        line-height: 10px; /* NOTE(platosha): chosen to align years to months */
      }

      [part="year-separator"] {
        background-color: currentColor;
        width: 4px;
        height: 4px;
        border-radius: 50%;
        margin: calc(0.5 * var(--vaadin-infinite-scroller-item-height, 80px) - 0.5 * 10px - 0.5 * 4px) auto;
      }

      /* Bottom Bar */

      [part="toolbar"] {
        display: flex;
        justify-content: flex-end;
        padding: 8px 4px;
        border-top: 1px solid var(--material-divider-color);
      }

      [part="cancel-button"] {
        order: 1;
      }

      [part="today-button"] {
        order: 2;
      }

      [part="today-button"],
      [part="cancel-button"] {
        margin: 0 4px;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(d.content);var h=i(29),c=i(48),u=(i(139),i(30)),p=i(94),m=i(218),f=i(307);i(91);const _=class{static _getISOWeekNumber(e){var t=e.getDay();0===t&&(t=7);var i=4-t,n=new Date(e.getTime()+24*i*3600*1e3),s=new Date(0,0);s.setFullYear(n.getFullYear());var a=n.getTime()-s.getTime(),r=Math.round(a/864e5);return Math.floor(r/7+1)}static _dateEquals(e,t){return e instanceof Date&&t instanceof Date&&e.getFullYear()===t.getFullYear()&&e.getMonth()===t.getMonth()&&e.getDate()===t.getDate()}static _dateAllowed(e,t,i){return(!t||e>=t)&&(!i||e<=i)}static _getClosestDate(e,t){return t.filter(e=>void 0!==e).reduce((t,i)=>{return i?t?Math.abs(e.getTime()-i.getTime())<Math.abs(t.getTime()-e.getTime())?i:t:i:t})}static _extractDateParts(e){return{day:e.getDate(),month:e.getMonth(),year:e.getFullYear()}}};class v extends(Object(m.a)(Object(c.a)(h.a))){static get template(){return n.a`
    <style>
      :host {
        display: block;
      }

      [part="weekdays"],
      #days {
        display: flex;
        flex-wrap: wrap;
        flex-grow: 1;
      }

      #days-container,
      #weekdays-container {
        display: flex;
      }

      [part="week-numbers"] {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        flex-shrink: 0;
      }

      [part="week-numbers"][hidden],
      [part="weekday"][hidden] {
        display: none;
      }

      [part="weekday"],
      [part="date"] {
        /* Would use calc(100% / 7) but it doesn't work nice on IE */
        width: 14.285714286%;
      }

      [part="weekday"]:empty,
      [part="week-numbers"] {
        width: 12.5%;
        flex-shrink: 0;
      }
    </style>

    <div part="month-header" role="heading">[[_getTitle(month, i18n.monthNames)]]</div>
    <div id="monthGrid" on-tap="_handleTap" on-touchend="_preventDefault" on-touchstart="_onMonthGridTouchStart">
      <div id="weekdays-container">
        <div hidden="[[!_showWeekSeparator(showWeekNumbers, i18n.firstDayOfWeek)]]" part="weekday"></div>
        <div part="weekdays">
          <template is="dom-repeat" items="[[_getWeekDayNames(i18n.weekdays, i18n.weekdaysShort, showWeekNumbers, i18n.firstDayOfWeek)]]">
            <div part="weekday" role="heading" aria-label\$="[[item.weekDay]]">[[item.weekDayShort]]</div>
          </template>
        </div>
      </div>
      <div id="days-container">
        <div part="week-numbers" hidden="[[!_showWeekSeparator(showWeekNumbers, i18n.firstDayOfWeek)]]">
          <template is="dom-repeat" items="[[_getWeekNumbers(_days)]]">
            <div part="week-number" role="heading" aria-label\$="[[i18n.week]] [[item]]">[[item]]</div>
          </template>
        </div>
        <div id="days">
          <template is="dom-repeat" items="[[_days]]">
            <div part="date" today\$="[[_isToday(item)]]" selected\$="[[_dateEquals(item, selectedDate)]]" focused\$="[[_dateEquals(item, focusedDate)]]" date="[[item]]" disabled\$="[[!_dateAllowed(item, minDate, maxDate)]]" role\$="[[_getRole(item)]]" aria-label\$="[[_getAriaLabel(item)]]" aria-disabled\$="[[_getAriaDisabled(item, minDate, maxDate)]]">[[_getDate(item)]]</div>
          </template>
        </div>
      </div>
    </div>
`}static get is(){return"vaadin-month-calendar"}static get properties(){return{month:{type:Date,value:new Date},selectedDate:{type:Date,notify:!0},focusedDate:Date,showWeekNumbers:{type:Boolean,value:!1},i18n:{type:Object},ignoreTaps:Boolean,_notTapping:Boolean,minDate:{type:Date,value:null},maxDate:{type:Date,value:null},_days:{type:Array,computed:"_getDays(month, i18n.firstDayOfWeek, minDate, maxDate)"},disabled:{type:Boolean,reflectToAttribute:!0,computed:"_isDisabled(month, minDate, maxDate)"}}}static get observers(){return["_showWeekNumbersChanged(showWeekNumbers, i18n.firstDayOfWeek)"]}_dateEquals(e,t){return _._dateEquals(e,t)}_dateAllowed(e,t,i){return _._dateAllowed(e,t,i)}_isDisabled(e,t,i){var n=new Date(0,0);n.setFullYear(e.getFullYear()),n.setMonth(e.getMonth()),n.setDate(1);var s=new Date(0,0);return s.setFullYear(e.getFullYear()),s.setMonth(e.getMonth()+1),s.setDate(0),!(t&&i&&t.getMonth()===i.getMonth()&&t.getMonth()===e.getMonth()&&i.getDate()-t.getDate()>=0)&&(!this._dateAllowed(n,t,i)&&!this._dateAllowed(s,t,i))}_getTitle(e,t){if(void 0!==e&&void 0!==t)return this.i18n.formatTitle(t[e.getMonth()],e.getFullYear())}_onMonthGridTouchStart(){this._notTapping=!1,setTimeout(()=>this._notTapping=!0,300)}_dateAdd(e,t){e.setDate(e.getDate()+t)}_applyFirstDayOfWeek(e,t){if(void 0!==e&&void 0!==t)return e.slice(t).concat(e.slice(0,t))}_getWeekDayNames(e,t,i,n){if(void 0!==e&&void 0!==t&&void 0!==i&&void 0!==n)return e=this._applyFirstDayOfWeek(e,n),t=this._applyFirstDayOfWeek(t,n),e=e.map((e,i)=>({weekDay:e,weekDayShort:t[i]}))}_getDate(e){return e?e.getDate():""}_showWeekNumbersChanged(e,t){e&&1===t?this.setAttribute("week-numbers",""):this.removeAttribute("week-numbers")}_showWeekSeparator(e,t){return e&&1===t}_isToday(e){return this._dateEquals(new Date,e)}_getDays(e,t){if(void 0!==e&&void 0!==t){var i=new Date(0,0);for(i.setFullYear(e.getFullYear()),i.setMonth(e.getMonth()),i.setDate(1);i.getDay()!==t;)this._dateAdd(i,-1);for(var n=[],s=i.getMonth(),a=e.getMonth();i.getMonth()===a||i.getMonth()===s;)n.push(i.getMonth()===a?new Date(i.getTime()):null),this._dateAdd(i,1);return n}}_getWeekNumber(e,t){if(void 0!==e&&void 0!==t)return e||(e=t.reduce((e,t)=>!e&&t?t:e)),_._getISOWeekNumber(e)}_getWeekNumbers(e){return e.map(t=>this._getWeekNumber(t,e)).filter((e,t,i)=>i.indexOf(e)===t)}_handleTap(e){this.ignoreTaps||this._notTapping||!e.target.date||e.target.hasAttribute("disabled")||(this.selectedDate=e.target.date,this.dispatchEvent(new CustomEvent("date-tap",{bubbles:!0,composed:!0})))}_preventDefault(e){e.preventDefault()}_getRole(e){return e?"button":"presentation"}_getAriaLabel(e){if(!e)return"";var t=this._getDate(e)+" "+this.i18n.monthNames[e.getMonth()]+" "+e.getFullYear()+", "+this.i18n.weekdays[e.getDay()];return this._isToday(e)&&(t+=", "+this.i18n.today),t}_getAriaDisabled(e,t,i){if(void 0!==e&&void 0!==t&&void 0!==i)return this._dateAllowed(e,t,i)?"false":"true"}}customElements.define(v.is,v);var y=i(11),g=i(21),b=i(23),w=i(31),x=i(61);class k extends h.a{static get template(){return n.a`
    <style>
      :host {
        display: block;
        overflow: hidden;
        height: 500px;
      }

      #scroller {
        position: relative;
        height: 100%;
        overflow: auto;
        outline: none;
        margin-right: -40px;
        -webkit-overflow-scrolling: touch;
        -ms-overflow-style: none;
        overflow-x: hidden;
      }

      #scroller.notouchscroll {
        -webkit-overflow-scrolling: auto;
      }

      #scroller::-webkit-scrollbar {
        display: none;
      }

      .buffer {
        position: absolute;
        width: var(--vaadin-infinite-scroller-buffer-width, 100%);
        box-sizing: border-box;
        padding-right: 40px;
        top: var(--vaadin-infinite-scroller-buffer-offset, 0);
        animation: fadein 0.2s;
      }

      @keyframes fadein {
        from { opacity: 0; }
        to { opacity: 1; }
      }
    </style>

    <div id="scroller" on-scroll="_scroll">
      <div class="buffer"></div>
      <div class="buffer"></div>
      <div id="fullHeight"></div>
    </div>
`}static get is(){return"vaadin-infinite-scroller"}static get properties(){return{bufferSize:{type:Number,value:20},_initialScroll:{value:5e5},_initialIndex:{value:0},_buffers:Array,_preventScrollEvent:Boolean,_mayHaveMomentum:Boolean,_initialized:Boolean,active:{type:Boolean,observer:"_activated"}}}ready(){super.ready(),this._buffers=Array.prototype.slice.call(this.root.querySelectorAll(".buffer")),this.$.fullHeight.style.height=2*this._initialScroll+"px";var e=this.querySelector("template");this._TemplateClass=Object(w.b)(e,this,{forwardHostProp:function(e,t){"index"!==e&&this._buffers.forEach(i=>{[].forEach.call(i.children,i=>{i._itemWrapper.instance[e]=t})})}}),navigator.userAgent.toLowerCase().indexOf("firefox")>-1&&(this.$.scroller.tabIndex=-1)}_activated(e){e&&!this._initialized&&(this._createPool(),this._initialized=!0)}_finishInit(){this._initDone||(this._buffers.forEach(e=>{[].forEach.call(e.children,e=>this._ensureStampedInstance(e._itemWrapper))},this),this._buffers[0].translateY||this._reset(),this._initDone=!0)}_translateBuffer(e){var t=e?1:0;this._buffers[t].translateY=this._buffers[t?0:1].translateY+this._bufferHeight*(t?-1:1),this._buffers[t].style.transform="translate3d(0, "+this._buffers[t].translateY+"px, 0)",this._buffers[t].updated=!1,this._buffers.reverse()}_scroll(){if(!this._scrollDisabled){var e=this.$.scroller.scrollTop;(e<this._bufferHeight||e>2*this._initialScroll-this._bufferHeight)&&(this._initialIndex=~~this.position,this._reset());var t=this.root.querySelector(".buffer").offsetTop,i=e>this._buffers[1].translateY+this.itemHeight+t,n=e<this._buffers[0].translateY+this.itemHeight+t;(i||n)&&(this._translateBuffer(n),this._updateClones()),this._preventScrollEvent||(this.dispatchEvent(new CustomEvent("custom-scroll",{bubbles:!1,composed:!0})),this._mayHaveMomentum=!0),this._preventScrollEvent=!1,this._debouncerScrollFinish=g.a.debounce(this._debouncerScrollFinish,y.d.after(200),()=>{var e=this.$.scroller.getBoundingClientRect();this._isVisible(this._buffers[0],e)||this._isVisible(this._buffers[1],e)||(this.position=this.position)})}}set position(e){this._preventScrollEvent=!0,e>this._firstIndex&&e<this._firstIndex+2*this.bufferSize?this.$.scroller.scrollTop=this.itemHeight*(e-this._firstIndex)+this._buffers[0].translateY:(this._initialIndex=~~e,this._reset(),this._scrollDisabled=!0,this.$.scroller.scrollTop+=e%1*this.itemHeight,this._scrollDisabled=!1),this._mayHaveMomentum&&(this.$.scroller.classList.add("notouchscroll"),this._mayHaveMomentum=!1,setTimeout(()=>{this.$.scroller.classList.remove("notouchscroll")},10))}get position(){return(this.$.scroller.scrollTop-this._buffers[0].translateY)/this.itemHeight+this._firstIndex}get itemHeight(){if(!this._itemHeightVal){window.ShadyCSS&&window.ShadyCSS.nativeCss||this.updateStyles();const e=window.ShadyCSS?window.ShadyCSS.getComputedStyleValue(this,"--vaadin-infinite-scroller-item-height"):getComputedStyle(this).getPropertyValue("--vaadin-infinite-scroller-item-height"),t="background-position";this.$.fullHeight.style.setProperty(t,e);const i=getComputedStyle(this.$.fullHeight).getPropertyValue(t);this.$.fullHeight.style.removeProperty(t),this._itemHeightVal=parseFloat(i)}return this._itemHeightVal}get _bufferHeight(){return this.itemHeight*this.bufferSize}_reset(){this._scrollDisabled=!0,this.$.scroller.scrollTop=this._initialScroll,this._buffers[0].translateY=this._initialScroll-this._bufferHeight,this._buffers[1].translateY=this._initialScroll,this._buffers.forEach(e=>{e.style.transform="translate3d(0, "+e.translateY+"px, 0)"}),this._buffers[0].updated=this._buffers[1].updated=!1,this._updateClones(!0),this._debouncerUpdateClones=g.a.debounce(this._debouncerUpdateClones,y.d.after(200),()=>{this._buffers[0].updated=this._buffers[1].updated=!1,this._updateClones()}),this._scrollDisabled=!1}_createPool(){var e=this.getBoundingClientRect();this._buffers.forEach(t=>{for(var i=0;i<this.bufferSize;i++){const i=document.createElement("div");i.style.height=this.itemHeight+"px",i.instance={};const n="vaadin-infinite-scroller-item-content-"+(k._contentIndex=k._contentIndex+1||0),s=document.createElement("slot");s.setAttribute("name",n),s._itemWrapper=i,t.appendChild(s),i.setAttribute("slot",n),this.appendChild(i),Object(b.b)(),setTimeout(()=>{this._isVisible(i,e)&&this._ensureStampedInstance(i)},1)}},this),setTimeout(()=>{Object(x.a)(this,this._finishInit.bind(this))},1)}_ensureStampedInstance(e){if(!e.firstElementChild){var t=e.instance;e.instance=new this._TemplateClass({}),e.appendChild(e.instance.root),Object.keys(t).forEach(i=>{e.instance.set(i,t[i])})}}_updateClones(e){this._firstIndex=~~((this._buffers[0].translateY-this._initialScroll)/this.itemHeight)+this._initialIndex;var t=e?this.$.scroller.getBoundingClientRect():void 0;this._buffers.forEach((i,n)=>{if(!i.updated){var s=this._firstIndex+this.bufferSize*n;[].forEach.call(i.children,(i,n)=>{const a=i._itemWrapper;e&&!this._isVisible(a,t)||(a.instance.index=s+n)}),i.updated=!0}},this)}_isVisible(e,t){var i=e.getBoundingClientRect();return i.bottom>t.top&&i.top<t.bottom}}customElements.define(k.is,k);i(76);const D=document.createElement("template");D.innerHTML='<dom-module id="vaadin-date-picker-overlay-styles" theme-for="vaadin-date-picker-overlay">\n  <template>\n    <style>\n      :host {\n        align-items: flex-start;\n        justify-content: flex-start;\n      }\n\n      :host([bottom-aligned]) {\n        justify-content: flex-end;\n      }\n\n      :host([right-aligned]) {\n        align-items: flex-end;\n      }\n\n      :host([right-aligned][dir="rtl"]) {\n        align-items: flex-start;\n      }\n\n      [part="overlay"] {\n        display: flex;\n        flex: auto;\n      }\n\n      [part~="content"] {\n        flex: auto;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(D.content);var E=i(35);class S extends(Object(m.a)(Object(f.a)(Object(c.a)(h.a)))){static get template(){return n.a`
    <style>
      :host {
        display: flex;
        flex-direction: column;
        height: 100%;
        width: 100%;
        outline: none;
        background: #fff;
      }

      [part="overlay-header"] {
        display: flex;
        flex-shrink: 0;
        flex-wrap: nowrap;
        align-items: center;
      }

      :host(:not([fullscreen])) [part="overlay-header"] {
        display: none;
      }

      [part="label"] {
        flex-grow: 1;
      }

      [part="clear-button"]:not([showclear]) {
        display: none;
      }

      [part="years-toggle-button"] {
        display: flex;
      }

      [part="years-toggle-button"][desktop] {
        display: none;
      }

      :host(:not([years-visible])) [part="years-toggle-button"]::before {
        transform: rotate(180deg);
      }

      #scrollers {
        display: flex;
        height: 100%;
        width: 100%;
        position: relative;
        overflow: hidden;
      }

      [part="months"],
      [part="years"] {
        height: 100%;
      }

      [part="months"] {
        --vaadin-infinite-scroller-item-height: 270px;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
      }

      #scrollers[desktop] [part="months"] {
        right: 50px;
        transform: none !important;
      }

      [part="years"] {
        --vaadin-infinite-scroller-item-height: 80px;
        width: 50px;
        position: absolute;
        right: 0;
        transform: translateX(100%);
        -webkit-tap-highlight-color: transparent;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        /* Center the year scroller position. */
        --vaadin-infinite-scroller-buffer-offset: 50%;
      }

      #scrollers[desktop] [part="years"] {
        position: absolute;
        transform: none !important;
      }

      [part="years"]::before {
        content: '';
        display: block;
        background: transparent;
        width: 0;
        height: 0;
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        border-width: 6px;
        border-style: solid;
        border-color: transparent;
        border-left-color: #000;
      }

      :host(.animate) [part="months"],
      :host(.animate) [part="years"] {
        transition: all 200ms;
      }

      [part="toolbar"] {
        display: flex;
        justify-content: space-between;
        z-index: 2;
        flex-shrink: 0;
      }

      [part~="overlay-header"]:not([desktop]) {
        padding-bottom: 40px;
      }

      [part~="years-toggle-button"] {
        position: absolute;
        top: auto;
        right: 8px;
        bottom: 0;
        z-index: 1;
        padding: 8px;
      }

      #announcer {
        display: inline-block;
        position: fixed;
        clip: rect(0, 0, 0, 0);
        clip-path: inset(100%);
      }
    </style>

    <div id="announcer" role="alert" aria-live="polite">
      [[i18n.calendar]]
    </div>

    <div part="overlay-header" on-touchend="_preventDefault" desktop\$="[[_desktopMode]]" aria-hidden="true">
      <div part="label">[[_formatDisplayed(selectedDate, i18n.formatDate, label)]]</div>
      <div part="clear-button" on-tap="_clear" showclear\$="[[_showClear(selectedDate)]]"></div>
      <div part="toggle-button" on-tap="_cancel"></div>

      <div part="years-toggle-button" desktop\$="[[_desktopMode]]" on-tap="_toggleYearScroller" aria-hidden="true">
        [[_yearAfterXMonths(_visibleMonthIndex)]]
      </div>
    </div>

    <div id="scrollers" desktop\$="[[_desktopMode]]" on-track="_track">
      <vaadin-infinite-scroller id="monthScroller" on-custom-scroll="_onMonthScroll" on-touchstart="_onMonthScrollTouchStart" buffer-size="3" active="[[initialPosition]]" part="months">
        <template>
          <vaadin-month-calendar i18n="[[i18n]]" month="[[_dateAfterXMonths(index)]]" selected-date="{{selectedDate}}" focused-date="[[focusedDate]]" ignore-taps="[[_ignoreTaps]]" show-week-numbers="[[showWeekNumbers]]" min-date="[[minDate]]" max-date="[[maxDate]]" focused\$="[[_focused]]" part="month" theme\$="[[theme]]">
          </vaadin-month-calendar>
        </template>
      </vaadin-infinite-scroller>
      <vaadin-infinite-scroller id="yearScroller" on-tap="_onYearTap" on-custom-scroll="_onYearScroll" on-touchstart="_onYearScrollTouchStart" buffer-size="12" active="[[initialPosition]]" part="years">
        <template>
          <div part="year-number" role="button" current\$="[[_isCurrentYear(index)]]" selected\$="[[_isSelectedYear(index, selectedDate)]]">
            [[_yearAfterXYears(index)]]
          </div>
          <div part="year-separator" aria-hidden="true"></div>
        </template>
      </vaadin-infinite-scroller>
    </div>

    <div on-touchend="_preventDefault" role="toolbar" part="toolbar">
      <vaadin-button id="todayButton" part="today-button" disabled="[[!_isTodayAllowed(minDate, maxDate)]]" on-tap="_onTodayTap">
        [[i18n.today]]
      </vaadin-button>
      <vaadin-button id="cancelButton" part="cancel-button" on-tap="_cancel">
        [[i18n.cancel]]
      </vaadin-button>
    </div>

    <iron-media-query query="(min-width: 375px)" query-matches="{{_desktopMode}}"></iron-media-query>
`}static get is(){return"vaadin-date-picker-overlay-content"}static get properties(){return{selectedDate:{type:Date,notify:!0},focusedDate:{type:Date,notify:!0,observer:"_focusedDateChanged"},_focusedMonthDate:Number,initialPosition:{type:Date,observer:"_initialPositionChanged"},_originDate:{value:new Date},_visibleMonthIndex:Number,_desktopMode:Boolean,_translateX:{observer:"_translateXChanged"},_yearScrollerWidth:{value:50},i18n:{type:Object},showWeekNumbers:{type:Boolean},_ignoreTaps:Boolean,_notTapping:Boolean,minDate:Date,maxDate:Date,_focused:Boolean,label:String}}ready(){super.ready(),this.setAttribute("tabindex",0),this.addEventListener("keydown",this._onKeydown.bind(this)),Object(E.b)(this,"tap",this._stopPropagation),this.addEventListener("focus",this._onOverlayFocus.bind(this)),this.addEventListener("blur",this._onOverlayBlur.bind(this))}connectedCallback(){super.connectedCallback(),this._closeYearScroller(),this._toggleAnimateClass(!0),Object(E.f)(this.$.scrollers,"pan-y"),p.a.requestAvailability()}announceFocusedDate(){var e=this._currentlyFocusedDate(),t=[];_._dateEquals(e,new Date)&&t.push(this.i18n.today),t=t.concat([this.i18n.weekdays[e.getDay()],e.getDate(),this.i18n.monthNames[e.getMonth()],e.getFullYear()]),this.showWeekNumbers&&1===this.i18n.firstDayOfWeek&&(t.push(this.i18n.week),t.push(_._getISOWeekNumber(e))),this.dispatchEvent(new CustomEvent("iron-announce",{bubbles:!0,composed:!0,detail:{text:t.join(" ")}}))}focusCancel(){this.$.cancelButton.focus()}scrollToDate(e,t){this._scrollToPosition(this._differenceInMonths(e,this._originDate),t)}_focusedDateChanged(e){this.revealDate(e)}_isCurrentYear(e){return 0===e}_isSelectedYear(e,t){if(t)return t.getFullYear()===this._originDate.getFullYear()+e}revealDate(e){if(e){var t=this._differenceInMonths(e,this._originDate),i=this.$.monthScroller.position>t,n=this.$.monthScroller.clientHeight/this.$.monthScroller.itemHeight,s=this.$.monthScroller.position+n-1<t;i?this._scrollToPosition(t,!0):s&&this._scrollToPosition(t-n+1,!0)}}_onOverlayFocus(){this._focused=!0}_onOverlayBlur(){this._focused=!1}_initialPositionChanged(e){this.scrollToDate(e)}_repositionYearScroller(){this._visibleMonthIndex=Math.floor(this.$.monthScroller.position),this.$.yearScroller.position=(this.$.monthScroller.position+this._originDate.getMonth())/12}_repositionMonthScroller(){this.$.monthScroller.position=12*this.$.yearScroller.position-this._originDate.getMonth(),this._visibleMonthIndex=Math.floor(this.$.monthScroller.position)}_onMonthScroll(){this._repositionYearScroller(),this._doIgnoreTaps()}_onYearScroll(){this._repositionMonthScroller(),this._doIgnoreTaps()}_onYearScrollTouchStart(){this._notTapping=!1,setTimeout(()=>this._notTapping=!0,300),this._repositionMonthScroller()}_onMonthScrollTouchStart(){this._repositionYearScroller()}_doIgnoreTaps(){this._ignoreTaps=!0,this._debouncer=g.a.debounce(this._debouncer,y.d.after(300),()=>this._ignoreTaps=!1)}_formatDisplayed(e,t,i){return e?t(_._extractDateParts(e)):i}_onTodayTap(){var e=new Date;Math.abs(this.$.monthScroller.position-this._differenceInMonths(e,this._originDate))<.001?(this.selectedDate=e,this._close()):this._scrollToCurrentMonth()}_scrollToCurrentMonth(){this.focusedDate&&(this.focusedDate=new Date),this.scrollToDate(new Date,!0)}_showClear(e){return!!e}_onYearTap(e){if(!this._ignoreTaps&&!this._notTapping){var t=(e.detail.y-(this.$.yearScroller.getBoundingClientRect().top+this.$.yearScroller.clientHeight/2))/this.$.yearScroller.itemHeight;this._scrollToPosition(this.$.monthScroller.position+12*t,!0)}}_scrollToPosition(e,t){if(void 0===this._targetPosition){if(!t)return this.$.monthScroller.position=e,this._targetPosition=void 0,void this._repositionYearScroller();this._targetPosition=e;var i=t?300:0,n=0,s=this.$.monthScroller.position,a=e=>{var t=e-(n=n||e);if(t<i){var r=((e,t,i,n)=>(e/=n/2)<1?i/2*e*e+t:-i/2*(--e*(e-2)-1)+t)(t,s,this._targetPosition-s,i);this.$.monthScroller.position=r,window.requestAnimationFrame(a)}else this.dispatchEvent(new CustomEvent("scroll-animation-finished",{bubbles:!0,composed:!0,detail:{position:this._targetPosition,oldPosition:s}})),this.$.monthScroller.position=this._targetPosition,this._targetPosition=void 0;setTimeout(this._repositionYearScroller.bind(this),1)};window.requestAnimationFrame(a)}else this._targetPosition=e}_limit(e,t){return Math.min(t.max,Math.max(t.min,e))}_handleTrack(e){if(!(Math.abs(e.detail.dx)<10||Math.abs(e.detail.ddy)>10)){Math.abs(e.detail.ddx)>this._yearScrollerWidth/3&&this._toggleAnimateClass(!0);var t=this._translateX+e.detail.ddx;this._translateX=this._limit(t,{min:0,max:this._yearScrollerWidth})}}_track(e){if(!this._desktopMode)switch(e.detail.state){case"start":this._toggleAnimateClass(!1);break;case"track":this._handleTrack(e);break;case"end":this._toggleAnimateClass(!0),this._translateX>=this._yearScrollerWidth/2?this._closeYearScroller():this._openYearScroller()}}_toggleAnimateClass(e){e?this.classList.add("animate"):this.classList.remove("animate")}_toggleYearScroller(){this._isYearScrollerVisible()?this._closeYearScroller():this._openYearScroller()}_openYearScroller(){this._translateX=0,this.setAttribute("years-visible","")}_closeYearScroller(){this.removeAttribute("years-visible"),this._translateX=this._yearScrollerWidth}_isYearScrollerVisible(){return this._translateX<this._yearScrollerWidth/2}_translateXChanged(e){this._desktopMode||(this.$.monthScroller.style.transform="translateX("+(e-this._yearScrollerWidth)+"px)",this.$.yearScroller.style.transform="translateX("+e+"px)")}_yearAfterXYears(e){var t=new Date(this._originDate);return t.setFullYear(parseInt(e)+this._originDate.getFullYear()),t.getFullYear()}_yearAfterXMonths(e){return this._dateAfterXMonths(e).getFullYear()}_dateAfterXMonths(e){var t=new Date(this._originDate);return t.setDate(1),t.setMonth(parseInt(e)+this._originDate.getMonth()),t}_differenceInMonths(e,t){return 12*(e.getFullYear()-t.getFullYear())-t.getMonth()+e.getMonth()}_differenceInYears(e,t){return this._differenceInMonths(e,t)/12}_clear(){this.selectedDate=""}_close(){const e=this.getRootNode().host,t=e?e.getRootNode().host:null;t&&(t.opened=!1),this.dispatchEvent(new CustomEvent("close",{bubbles:!0,composed:!0}))}_cancel(){this.focusedDate=this.selectedDate,this._close()}_preventDefault(e){e.preventDefault()}_eventKey(e){for(var t=["down","up","right","left","enter","space","home","end","pageup","pagedown","tab","esc"],i=0;i<t.length;i++){var n=t[i];if(u.a.keyboardEventMatchesKeys(e,n))return n}}_onKeydown(e){var t=this._currentlyFocusedDate();const i=e.composedPath().indexOf(this.$.todayButton)>=0,n=e.composedPath().indexOf(this.$.cancelButton)>=0,s=!i&&!n;var a=this._eventKey(e);if("tab"===a){e.stopPropagation();const t=this.hasAttribute("fullscreen"),a=e.shiftKey;t?e.preventDefault():a&&s||!a&&n?(e.preventDefault(),this.dispatchEvent(new CustomEvent("focus-input",{bubbles:!0,composed:!0}))):a&&i?(this._focused=!0,setTimeout(()=>this.revealDate(this.focusedDate),1)):this._focused=!1}else if(a)switch(e.preventDefault(),e.stopPropagation(),a){case"down":this._moveFocusByDays(7),this.focus();break;case"up":this._moveFocusByDays(-7),this.focus();break;case"right":s&&this._moveFocusByDays(1);break;case"left":s&&this._moveFocusByDays(-1);break;case"enter":s||n?this._close():i&&this._onTodayTap();break;case"space":if(n)this._close();else if(i)this._onTodayTap();else{var r=this.focusedDate;_._dateEquals(r,this.selectedDate)?(this.selectedDate="",this.focusedDate=r):this.selectedDate=r}break;case"home":this._moveFocusInsideMonth(t,"minDate");break;case"end":this._moveFocusInsideMonth(t,"maxDate");break;case"pagedown":this._moveFocusByMonths(e.shiftKey?12:1);break;case"pageup":this._moveFocusByMonths(e.shiftKey?-12:-1);break;case"esc":this._cancel()}}_currentlyFocusedDate(){return this.focusedDate||this.selectedDate||this.initialPosition||new Date}_focusDate(e){this.focusedDate=e,this._focusedMonthDate=e.getDate()}_focusClosestDate(e){this._focusDate(_._getClosestDate(e,[this.minDate,this.maxDate]))}_moveFocusByDays(e){var t=this._currentlyFocusedDate(),i=new Date(0,0);i.setFullYear(t.getFullYear()),i.setMonth(t.getMonth()),i.setDate(t.getDate()+e),this._dateAllowed(i,this.minDate,this.maxDate)?this._focusDate(i):this._dateAllowed(t,this.minDate,this.maxDate)?e>0?this._focusDate(this.maxDate):this._focusDate(this.minDate):this._focusClosestDate(t)}_moveFocusByMonths(e){var t=this._currentlyFocusedDate(),i=new Date(0,0);i.setFullYear(t.getFullYear()),i.setMonth(t.getMonth()+e);var n=i.getMonth();i.setDate(this._focusedMonthDate||(this._focusedMonthDate=t.getDate())),i.getMonth()!==n&&i.setDate(0),this._dateAllowed(i,this.minDate,this.maxDate)?this.focusedDate=i:this._dateAllowed(t,this.minDate,this.maxDate)?e>0?this._focusDate(this.maxDate):this._focusDate(this.minDate):this._focusClosestDate(t)}_moveFocusInsideMonth(e,t){var i=new Date(0,0);i.setFullYear(e.getFullYear()),"minDate"===t?(i.setMonth(e.getMonth()),i.setDate(1)):(i.setMonth(e.getMonth()+1),i.setDate(0)),this._dateAllowed(i,this.minDate,this.maxDate)?this._focusDate(i):this._dateAllowed(e,this.minDate,this.maxDate)?this._focusDate(this[t]):this._focusClosestDate(e)}_dateAllowed(e,t,i){return(!t||e>=t)&&(!i||e<=i)}_isTodayAllowed(e,t){var i=new Date,n=new Date(0,0);return n.setFullYear(i.getFullYear()),n.setMonth(i.getMonth()),n.setDate(i.getDate()),this._dateAllowed(n,e,t)}_stopPropagation(e){e.stopPropagation()}}customElements.define(S.is,S);const C=n.a`<dom-module id="material-date-picker-month-calendar" theme-for="vaadin-month-calendar">
  <template>
    <style>
      :host {
        color: var(--material-body-text-color);
        padding: 0 calc(50% / 8 - 0.5em + 8px);
      }

      :host([show-week-numbers]) {
        padding: 0 calc(50% / 9 - 0.5em + 8px);
      }

      [part="month-header"] {
        font-size: var(--material-h6-font-size);
        line-height: 1;
        padding-top: 20px;
        margin-bottom: 8px;
      }

      [part="week-number"],
      [part="weekday"] {
        font-size: var(--material-caption-font-size);
        line-height: 44px;
        height: 40px;
        color: var(--material-secondary-text-color);
      }

      :host([disabled]),
      :host([disabled]) [part="week-number"],
      :host([disabled]) [part="weekday"] {
        color: var(--material-disabled-text-color);
      }

      [part="date"] {
        position: relative;
        font-size: var(--material-body-font-size);
        line-height: 42px;
        height: 40px;
        cursor: default;
      }

      [part="date"]::after {
        content: '';
        position: absolute;
        z-index: -4;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 38px;
        height: 38px;
        box-sizing: border-box;
        border-radius: 50%;
        border: 2px solid transparent;
      }

      /* Today */

      [part="date"][today] {
        color: var(--material-primary-text-color);
      }

      /* Hover */

      [part="date"]:not([disabled]):hover::after {
        background-color: var(--material-secondary-background-color);
        border-color: var(--material-secondary-background-color);
        z-index: -3;
      }

      /* Hide for touch devices */
      @media (hover: none) {
        [part="date"]:not([disabled]):hover::after {
          background-color: transparent;
          border-color: transparent;
          z-index: -4;
        }
      }

      /* Selected */

      [part="date"][selected] {
        font-weight: 500;
      }

      [part="date"]:not([disabled])[selected]::after,
      [part="date"][selected]::after {
        background-color: transparent;
        border-color: currentColor;
        z-index: -2;
      }

      /* Focused */

      [part="date"]:not([disabled])[focused],
      [part="date"]:not([disabled]):active {
        color: var(--material-primary-contrast-color);
      }

      [part="date"]:not([disabled])[focused]::after,
      [part="date"]:not([disabled]):active::after {
        opacity: 0.7;
        background-color: var(--material-primary-color);
        border-color: var(--material-primary-color);
        z-index: -1;
      }

      [part="date"][disabled] {
        color: var(--material-disabled-text-color);
      }

      :host([focused]) [part="date"]:not([disabled])[focused]::after {
        opacity: 1;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(C.content);const I=document.createElement("template");I.innerHTML='<dom-module id="material-required-field">\n  <template>\n    <style>\n      [part="label"] {\n        display: block;\n        position: absolute;\n        top: 8px;\n        font-size: 1em;\n        line-height: 1;\n        height: 20px;\n        margin-bottom: -4px;\n        white-space: nowrap;\n        overflow-x: hidden;\n        text-overflow: ellipsis;\n        color: var(--material-secondary-text-color);\n        transform-origin: 0 75%;\n        transform: scale(0.75);\n      }\n\n      :host([required]) [part="label"]::after {\n        content: " *";\n        color: inherit;\n      }\n\n      :host([invalid]) [part="label"] {\n        color: var(--material-error-text-color);\n      }\n\n      [part="error-message"] {\n        font-size: .75em;\n        line-height: 1;\n        color: var(--material-error-text-color);\n      }\n\n      /* Margin that doesn’t reserve space when there’s no error message */\n      [part="error-message"]:not(:empty)::before {\n        content: "";\n        display: block;\n        height: 6px;\n      }\n\n      :host(:not([invalid])) [part="error-message"] {\n        margin-top: 0;\n        max-height: 0;\n        overflow: hidden;\n      }\n\n      :host([invalid]) [part="error-message"] {\n        animation: reveal 0.2s;\n      }\n\n      @keyframes reveal {\n        0% {\n          opacity: 0;\n        }\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(I.content);const T=document.createElement("template");T.innerHTML='<dom-module id="material-field-button">\n  <template>\n    <style>\n      /* TODO(platosha): align icon sizes with other elements */\n      [part$="button"] {\n        flex: none;\n        width: 24px;\n        height: 24px;\n        padding: 4px;\n        color: var(--material-secondary-text-color);\n        font-size: var(--material-icon-font-size);\n        line-height: 24px;\n        text-align: center;\n      }\n\n      :host(:not([readonly])) [part$="button"] {\n        cursor: pointer;\n      }\n\n      :host(:not([readonly])) [part$="button"]:hover {\n        color: var(--material-text-color);\n      }\n\n      :host([disabled]) [part$="button"],\n      :host([readonly]) [part$="button"] {\n        color: var(--material-disabled-text-color);\n      }\n\n      :host([disabled]) [part="clear-button"] {\n        display: none;\n      }\n\n      [part$="button"]::before {\n        font-family: "material-icons";\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(T.content);const z=n.a`<dom-module id="material-text-field" theme-for="vaadin-text-field">
  <template>
    <style include="material-required-field material-field-button">
      :host {
        display: inline-flex;
        position: relative;
        padding-top: 8px;
        margin-bottom: 8px;
        outline: none;
        color: var(--material-body-text-color);
        font-size: var(--material-body-font-size);
        line-height: 24px;
        font-family: var(--material-font-family);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }

      :host::before {
        line-height: 32px;
      }

      /* Strange gymnastics to make fields vertically align nicely in most cases
         (no label, with label, without prefix, with prefix, etc.) */

      :host([has-label]) {
        padding-top: 24px;
      }

      [part="label"]:empty {
        display: none;
      }

      [part="label"]:empty::before {
        content: " ";
        position: absolute;
      }

      [part="input-field"] {
        position: relative;
        top: -0.2px; /* NOTE(platosha): Adjusts for wrong flex baseline in Chrome & Safari */
        height: 32px;
        padding-left: 0;
        background-color: transparent;
        margin: 0;
      }

      [part="input-field"]::before,
      [part="input-field"]::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        transform-origin: 50% 0%;
        background-color: var(--_material-text-field-input-line-background-color, #000);
        opacity: var(--_material-text-field-input-line-opacity, 0.42);
      }

      [part="input-field"]::after {
        background-color: var(--material-primary-color);
        opacity: 0;
        height: 2px;
        bottom: 0;
        transform: scaleX(0);
        transition: opacity 0.175s;
      }

      :host([disabled]) [part="label"],
      :host([disabled]) [part="value"],
      :host([disabled]) [part="input-field"] ::slotted(input),
      :host([disabled]) [part="input-field"] ::slotted(textarea),
      :host([disabled]) [part="input-field"] ::slotted([part="value"]) {
        color: var(--material-disabled-text-color);
        -webkit-text-fill-color: var(--material-disabled-text-color);
      }

      [part="value"],
      :host([disabled]) [part="input-field"] ::slotted(input),
      :host([disabled]) [part="input-field"] ::slotted(textarea),
      /* Slotted by vaadin-select-text-field */
      [part="input-field"] ::slotted([part="value"]) {
        outline: none;
        margin: 0;
        border: 0;
        border-radius: 0;
        padding: 8px 0;
        width: 100%;
        height: 100%;
        font-family: inherit;
        font-size: 1em;
        line-height: inherit;
        color: inherit;
        background-color: transparent;
        /* Disable default invalid style in Firefox */
        box-shadow: none;
      }

      /* TODO: the text opacity should be 42%, but the disabled style is 38%.
      Would need to introduce another property for it if we want to be 100% accurate. */
      [part="value"]::-webkit-input-placeholder {
        color: var(--material-disabled-text-color);
        transition: opacity 0.175s 0.05s;
        opacity: 1;
      }

      [part="value"]:-ms-input-placeholder {
        color: var(--material-disabled-text-color);
      }

      [part="value"]::-moz-placeholder {
        color: var(--material-disabled-text-color);
        transition: opacity 0.175s 0.05s;
        opacity: 1;
      }

      [part="value"]::placeholder {
        color: var(--material-disabled-text-color);
        transition: opacity 0.175s 0.1s;
        opacity: 1;
      }

      :host([has-label]:not([focused]):not([invalid]):not([theme="always-float-label"])) [part="value"]::-webkit-input-placeholder {
        opacity: 0;
        transition-delay: 0;
      }

      :host([has-label]:not([focused]):not([invalid]):not([theme="always-float-label"])) [part="value"]::-moz-placeholder {
        opacity: 0;
        transition-delay: 0;
      }

      :host([has-label]:not([focused]):not([invalid]):not([theme="always-float-label"])) [part="value"]::placeholder {
        opacity: 0;
        transition-delay: 0;
      }

      /* IE11 doesn’t show the placeholder when the input is focused, so it’s basically useless for this theme */
      :host([has-label]) [part="value"]:-ms-input-placeholder {
        opacity: 0;
      }

      [part="label"] {
        transition: transform 0.175s, color 0.175s, width 0.175s;
        transition-timing-function: ease, ease, step-end;
      }

      /* TODO: using unsupported selector to fix IE11 (even thought the label element is scaled down,
         the 133% width still takes the same space as an unscaled element */
      ::-ms-backdrop,
      .vaadin-text-field-container {
        overflow: hidden;
      }

      /* Same fix for MS Edge ^^   */
      @supports (-ms-ime-align:auto) {
        .vaadin-text-field-container {
          overflow: hidden;
        }
      }

      :host(:hover:not([readonly]):not([invalid])) [part="input-field"]::before {
        opacity: var(--_material-text-field-input-line-hover-opacity, 0.87);
      }

      :host([focused]:not([invalid])) [part="label"] {
        color: var(--material-primary-text-color);
      }

      :host([focused]) [part="input-field"]::after,
      :host([invalid]) [part="input-field"]::after {
        opacity: 1;
        transform: none;
        transition: transform 0.175s, opacity 0.175s;
      }

      :host([invalid]) [part="input-field"]::after {
        background-color: var(--material-error-color);
      }

      :host([input-prevented]) [part="input-field"] {
        color: var(--material-error-text-color);
      }

      :host([disabled]) {
        pointer-events: none;
      }

      :host([disabled]) [part="input-field"] {
        color: var(--material-disabled-text-color);
      }

      :host([disabled]) [part="input-field"]::before {
        background-color: transparent;
        background-image: linear-gradient(90deg, var(--_material-text-field-input-line-background-color, #000) 0, var(--_material-text-field-input-line-background-color, #000) 2px, transparent 2px);
        background-size: 4px 1px;
        background-repeat: repeat-x;
      }

      /* Only target the visible floating label */
      :host([has-label]:not([has-value]):not([focused]):not([invalid]):not([theme~="always-float-label"])) [part="label"] {
        /* IE11 doesn’t work with calc inside the translate function, so we need to have a fixed pixel value instead of 50% + 16px */
        transform: scale(1) translateY(24px);
        transition-timing-function: ease, ease, step-start;
        pointer-events: none;
        left: auto;
        transition-delay: 0.1s;
      }

      /* Slotted content */

      [part="input-field"] ::slotted(*:not([part="value"]):not([part\$="-button"]):not(input):not(textarea)) {
        color: var(--material-secondary-text-color);
      }

      [part="clear-button"]::before {
        content: var(--material-icons-clear);
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(z.content);var O=i(326);const M=document.createElement("template");M.innerHTML='<dom-module id="vaadin-text-field-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: inline-flex;\n        outline: none;\n      }\n\n      :host::before {\n        content: "\\2003";\n        width: 0;\n        display: inline-block;\n        /* Size and position this element on the same vertical position as the input-field element\n           to make vertical align for the host element work as expected */\n      }\n\n      :host([hidden]) {\n        display: none !important;\n      }\n\n      .vaadin-text-field-container,\n      .vaadin-text-area-container {\n        display: flex;\n        flex-direction: column;\n        min-width: 100%;\n        max-width: 100%;\n        width: var(--vaadin-text-field-default-width, 12em);\n      }\n\n      [part="label"]:empty {\n        display: none;\n      }\n\n      [part="input-field"] {\n        display: flex;\n        align-items: center;\n        flex: auto;\n      }\n\n      .vaadin-text-field-container [part="input-field"] {\n        flex-grow: 0;\n      }\n\n      /* Reset the native input styles */\n      [part="value"],\n      [part="input-field"] ::slotted(input),\n      [part="input-field"] ::slotted(textarea) {\n        -webkit-appearance: none;\n        -moz-appearance: none;\n        outline: none;\n        margin: 0;\n        padding: 0;\n        border: 0;\n        border-radius: 0;\n        min-width: 0;\n        font: inherit;\n        font-size: 1em;\n        line-height: normal;\n        color: inherit;\n        background-color: transparent;\n        /* Disable default invalid style in Firefox */\n        box-shadow: none;\n      }\n\n      [part="input-field"] ::slotted(*) {\n        flex: none;\n      }\n\n      [part="value"],\n      [part="input-field"] ::slotted(input),\n      [part="input-field"] ::slotted(textarea),\n      /* Slotted by vaadin-select-text-field */\n      [part="input-field"] ::slotted([part="value"]) {\n        flex: auto;\n        white-space: nowrap;\n        overflow: hidden;\n        width: 100%;\n        height: 100%;\n      }\n\n      [part="input-field"] ::slotted(textarea) {\n        resize: none;\n      }\n\n      [part="value"]::-ms-clear,\n      [part="input-field"] ::slotted(input)::-ms-clear {\n        display: none;\n      }\n\n      [part="clear-button"] {\n        cursor: default;\n      }\n\n      [part="clear-button"]::before {\n        content: "✕";\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(M.content);const A={default:["list","autofocus","pattern","autocapitalize","autocorrect","maxlength","minlength","name","placeholder","autocomplete","title"],accessible:["disabled","readonly","required","invalid"]},P={DEFAULT:"default",ACCESSIBLE:"accessible"},$=e=>(class extends(Object(O.a)(e)){static get properties(){return{autocomplete:{type:String},autocorrect:{type:String},autocapitalize:{type:String},autoselect:{type:Boolean,value:!1},clearButtonVisible:{type:Boolean,value:!1},errorMessage:{type:String,value:""},label:{type:String,value:"",observer:"_labelChanged"},maxlength:{type:Number},minlength:{type:Number},name:{type:String},placeholder:{type:String},readonly:{type:Boolean,reflectToAttribute:!0},required:{type:Boolean,reflectToAttribute:!0},value:{type:String,value:"",observer:"_valueChanged",notify:!0},invalid:{type:Boolean,reflectToAttribute:!0,notify:!0,value:!1},hasValue:{type:Boolean,reflectToAttribute:!0},preventInvalidInput:{type:Boolean},_labelId:{type:String},_errorId:{type:String}}}static get observers(){return["_stateChanged(disabled, readonly, clearButtonVisible, hasValue)","_hostPropsChanged("+A.default.join(", ")+")","_hostAccessiblePropsChanged("+A.accessible.join(", ")+")","_getActiveErrorId(invalid, errorMessage, _errorId)","_getActiveLabelId(label, _labelId)"]}constructor(){super(),this._createMethodObserver("__constraintsChanged(required, minlength, maxlength, pattern, min, max, step)")}get focusElement(){if(!this.shadowRoot)return;const e=this.querySelector(`${this._slottedTagName}[slot="${this._slottedTagName}"]`);return e||this.shadowRoot.querySelector('[part="value"]')}get inputElement(){return this.focusElement}get _slottedTagName(){return"input"}_onInput(e){if(this.__preventInput)return e.stopImmediatePropagation(),void(this.__preventInput=!1);if(this.preventInvalidInput){const e=this.inputElement;if(e.value.length>0&&!this.checkValidity())return e.value=this.value||"",this.setAttribute("input-prevented",""),void(this._inputDebouncer=g.a.debounce(this._inputDebouncer,y.d.after(200),()=>{this.removeAttribute("input-prevented")}))}this.__userInput=!0,this.value=e.target.value}_stateChanged(e,t,i,n){!e&&!t&&i&&n?this.$.clearButton.removeAttribute("hidden"):this.$.clearButton.setAttribute("hidden",!0)}_onChange(e){if(this._valueClearing)return;const t=new CustomEvent("change",{detail:{sourceEvent:e},bubbles:e.bubbles,cancelable:e.cancelable});this.dispatchEvent(t)}_valueChanged(e,t){""===e&&void 0===t||(this.hasValue=""!==e&&null!=e,this.__userInput?this.__userInput=!1:(void 0!==e?this.inputElement.value=e:this.value=this.inputElement.value="",this.invalid&&this.validate()))}_labelChanged(e){""!==e&&null!=e?this.setAttribute("has-label",""):this.removeAttribute("has-label")}_onSlotChange(){const e=this.querySelector(`${this._slottedTagName}[slot="${this._slottedTagName}"]`);this.value&&(this.inputElement.value=this.value,this.validate()),e&&!this._slottedInput?(this._validateSlottedValue(e),this._addInputListeners(e),this._addIEListeners(e),this._slottedInput=e):!e&&this._slottedInput&&(this._removeInputListeners(this._slottedInput),this._removeIEListeners(this._slottedInput),this._slottedInput=void 0),Object.keys(P).map(e=>P[e]).forEach(e=>this._propagateHostAttributes(A[e].map(e=>this[e]),e))}_hostPropsChanged(...e){this._propagateHostAttributes(e,P.DEFAULT)}_hostAccessiblePropsChanged(...e){this._propagateHostAttributes(e,P.ACCESSIBLE)}_validateSlottedValue(e){e.value!==this.value&&(console.warn("Please define value on the vaadin-text-field component!"),e.value="")}_propagateHostAttributes(e,t){const i=this.inputElement,n=A[t];"accessible"===t?n.forEach((t,n)=>{this._setOrToggleAttribute(t,e[n],i),this._setOrToggleAttribute(`aria-${t}`,e[n],i)}):n.forEach((t,n)=>{this._setOrToggleAttribute(t,e[n],i)})}_setOrToggleAttribute(e,t,i){e&&i&&(t?i.setAttribute(e,"boolean"==typeof t?"":t):i.removeAttribute(e))}__constraintsChanged(e,t,i,n,s,a,r){if(!this.invalid)return;const o=e=>!e&&0!==e;e||t||i||n||!o(s)||!o(a)?this.validate():this.invalid=!1}checkValidity(){return this.required||this.pattern||this.maxlength||this.minlength?this.inputElement.checkValidity():!this.invalid}_addInputListeners(e){e.addEventListener("input",this._boundOnInput),e.addEventListener("change",this._boundOnChange),e.addEventListener("blur",this._boundOnBlur),e.addEventListener("focus",this._boundOnFocus)}_removeInputListeners(e){e.removeEventListener("input",this._boundOnInput),e.removeEventListener("change",this._boundOnChange),e.removeEventListener("blur",this._boundOnBlur),e.removeEventListener("focus",this._boundOnFocus)}ready(){super.ready(),this._boundOnInput=this._onInput.bind(this),this._boundOnChange=this._onChange.bind(this),this._boundOnBlur=this._onBlur.bind(this),this._boundOnFocus=this._onFocus.bind(this);const e=this.shadowRoot.querySelector('[part="value"]');this._slottedInput=this.querySelector(`${this._slottedTagName}[slot="${this._slottedTagName}"]`),this._addInputListeners(e),this._addIEListeners(e),this._slottedInput&&(this._addIEListeners(this._slottedInput),this._addInputListeners(this._slottedInput)),this.shadowRoot.querySelector('[name="input"], [name="textarea"]').addEventListener("slotchange",this._onSlotChange.bind(this)),window.ShadyCSS&&window.ShadyCSS.nativeCss||this.updateStyles(),this.$.clearButton.addEventListener("mousedown",()=>this._valueClearing=!0),this.$.clearButton.addEventListener("click",this._onClearButtonClick.bind(this)),this.addEventListener("keydown",this._onKeyDown.bind(this));var t=$._uniqueId=1+$._uniqueId||0;this._errorId=`${this.constructor.is}-error-${t}`,this._labelId=`${this.constructor.is}-label-${t}`}validate(){return!(this.invalid=!this.checkValidity())}clear(){this.value=""}_onBlur(){this.validate()}_onFocus(){this.autoselect&&(this.inputElement.select(),setTimeout(()=>{this.inputElement.setSelectionRange(0,9999)}))}_onClearButtonClick(e){this.inputElement.focus(),this.clear(),this._valueClearing=!1,this.inputElement.dispatchEvent(new Event("change",{bubbles:!this._slottedInput}))}_onKeyDown(e){27===e.keyCode&&this.clearButtonVisible&&this.clear()}_addIEListeners(e){navigator.userAgent.match(/Trident/)&&(this._shouldPreventInput=(()=>{this.__preventInput=!0,requestAnimationFrame(()=>{this.__preventInput=!1})}),e.addEventListener("focusin",this._shouldPreventInput),e.addEventListener("focusout",this._shouldPreventInput),this._createPropertyObserver("placeholder",this._shouldPreventInput))}_removeIEListeners(e){navigator.userAgent.match(/Trident/)&&(e.removeEventListener("focusin",this._shouldPreventInput),e.removeEventListener("focusout",this._shouldPreventInput))}_getActiveErrorId(e,t,i){this._setOrToggleAttribute("aria-describedby",t&&e?i:void 0,this.inputElement)}_getActiveLabelId(e,t){this._setOrToggleAttribute("aria-labelledby",e?t:void 0,this.inputElement)}_getErrorMessageAriaHidden(e,t,i){return(!(t&&e?i:void 0)).toString()}attributeChangedCallback(e,t,i){if(super.attributeChangedCallback(e,t,i),window.ShadyCSS&&window.ShadyCSS.nativeCss||!/^(focused|focus-ring|invalid|disabled|placeholder|has-value)$/.test(e)||this.updateStyles(),/^((?!chrome|android).)*safari/i.test(navigator.userAgent)&&this.root){const e="-webkit-backface-visibility";this.root.querySelectorAll("*").forEach(t=>{t.style[e]="visible",t.style[e]=""})}}});var F=i(310);class j extends(Object(F.a)($(Object(m.a)(h.a)))){static get template(){return n.a`
    <style include="vaadin-text-field-shared-styles">
      /* polymer-cli linter breaks with empty line */
    </style>

    <div class="vaadin-text-field-container">

      <label part="label" on-click="focus" id="[[_labelId]]">[[label]]</label>

      <div part="input-field">

        <slot name="prefix"></slot>

        <slot name="input">
          <input part="value">
        </slot>

        <div part="clear-button" id="clearButton" role="button" aria-label="Clear"></div>
        <slot name="suffix"></slot>

      </div>

      <div part="error-message" id="[[_errorId]]" aria-live="assertive" aria-hidden\$="[[_getErrorMessageAriaHidden(invalid, errorMessage, _errorId)]]">[[errorMessage]]</div>

    </div>
`}static get is(){return"vaadin-text-field"}static get version(){return"2.3.10"}static get properties(){return{list:{type:String},pattern:{type:String},title:{type:String}}}}customElements.define(j.is,j);const L=n.a`<dom-module id="material-date-picker" theme-for="vaadin-date-picker">
  <template>
    <style include="material-field-button">
      :host {
        display: inline-flex;
        -webkit-tap-highlight-color: transparent;
      }

      [part="clear-button"]::before {
        content: var(--material-icons-clear);
      }

      [part="toggle-button"]::before {
        content: var(--material-icons-calendar);
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(L.content);var R=i(97),V=i(74);const N=e=>(class extends(Object(V.b)([R.a],e)){static get properties(){return{_selectedDate:{type:Date},_focusedDate:Date,value:{type:String,observer:"_valueChanged",notify:!0,value:""},required:{type:Boolean,value:!1},name:{type:String},initialPosition:String,label:String,opened:{type:Boolean,reflectToAttribute:!0,notify:!0,observer:"_openedChanged"},showWeekNumbers:{type:Boolean},_fullscreen:{value:!1,observer:"_fullscreenChanged"},_fullscreenMediaQuery:{value:"(max-width: 420px), (max-height: 420px)"},_touchPrevented:Array,i18n:{type:Object,value:()=>({monthNames:["January","February","March","April","May","June","July","August","September","October","November","December"],weekdays:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],weekdaysShort:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],firstDayOfWeek:0,week:"Week",calendar:"Calendar",clear:"Clear",today:"Today",cancel:"Cancel",formatDate:e=>{const t=String(e.year).replace(/\d+/,e=>"0000".substr(e.length)+e);return[e.month+1,e.day,t].join("/")},parseDate:e=>{const t=e.split("/"),i=new Date;let n,s=i.getMonth(),a=i.getFullYear();if(3===t.length?(a=parseInt(t[2]),t[2].length<3&&a>=0&&(a+=a<50?2e3:1900),s=parseInt(t[0])-1,n=parseInt(t[1])):2===t.length?(s=parseInt(t[0])-1,n=parseInt(t[1])):1===t.length&&(n=parseInt(t[0])),void 0!==n)return{day:n,month:s,year:a}},formatTitle:(e,t)=>e+" "+t})},min:{type:String,observer:"_minChanged"},max:{type:String,observer:"_maxChanged"},_minDate:{type:Date,value:""},_maxDate:{type:Date,value:""},_noInput:{type:Boolean,computed:"_isNoInput(_fullscreen, _ios, i18n, i18n.*)"},_ios:{type:Boolean,value:navigator.userAgent.match(/iP(?:hone|ad;(?: U;)? CPU) OS (\d+)/)},_webkitOverflowScroll:{type:Boolean,value:""===document.createElement("div").style.webkitOverflowScrolling},_ignoreAnnounce:{value:!0},_focusOverlayOnOpen:Boolean,_overlayInitialized:Boolean}}static get observers(){return["_updateHasValue(value)","_selectedDateChanged(_selectedDate, i18n.formatDate)","_focusedDateChanged(_focusedDate, i18n.formatDate)","_announceFocusedDate(_focusedDate, opened, _ignoreAnnounce)"]}ready(){super.ready(),this._boundOnScroll=this._onScroll.bind(this),this._boundFocus=this._focus.bind(this),this._boundUpdateAlignmentAndPosition=this._updateAlignmentAndPosition.bind(this);const e=e=>{const t=e.composedPath(),i=t.indexOf(this._inputElement);return 1===t.slice(0,i).filter(e=>e.getAttribute&&"clear-button"===e.getAttribute("part")).length};Object(E.b)(this,"tap",t=>{e(t)||this.open()}),this.addEventListener("touchend",t=>{e(t)||t.preventDefault()}),this.addEventListener("keydown",this._onKeydown.bind(this)),this.addEventListener("input",this._onUserInput.bind(this)),this.addEventListener("focus",e=>this._noInput&&e.target.blur()),this.addEventListener("blur",e=>!this.opened&&this.validate())}_initOverlay(){this.$.overlay.removeAttribute("disable-upgrade"),this._overlayInitialized=!0,this.$.overlay.addEventListener("opened-changed",e=>this.opened=e.detail.value),this._overlayContent.addEventListener("close",this._close.bind(this)),this._overlayContent.addEventListener("focus-input",this._focusAndSelect.bind(this)),this.$.overlay.addEventListener("vaadin-overlay-escape-press",this._boundFocus),this._overlayContent.addEventListener("focus",()=>this.focusElement._setFocused(!0)),this.$.overlay.addEventListener("vaadin-overlay-close",this._onVaadinOverlayClose.bind(this))}disconnectedCallback(){super.disconnectedCallback(),this._overlayInitialized&&this.$.overlay.removeEventListener("vaadin-overlay-escape-press",this._boundFocus),this.opened=!1}open(){this.disabled||this.readonly||(this.opened=!0)}_close(e){e&&e.stopPropagation(),this._focus(),this.close()}close(){this._overlayInitialized&&this.$.overlay.close()}get _inputElement(){return this._input()}get _nativeInput(){if(this._inputElement)return this._inputElement.focusElement?this._inputElement.focusElement:this._inputElement.inputElement?this._inputElement.inputElement:window.unwrap?window.unwrap(this._inputElement):this._inputElement}_parseDate(e){var t=/^([-+]\d{1}|\d{2,4}|[-+]\d{6})-(\d{1,2})-(\d{1,2})$/.exec(e);if(t){var i=new Date(0,0);return i.setFullYear(parseInt(t[1],10)),i.setMonth(parseInt(t[2],10)-1),i.setDate(parseInt(t[3],10)),i}}_isNoInput(e,t,i){return!this._inputElement||e||t||!i.parseDate}_formatISO(e){if(!(e instanceof Date))return"";const t=(e,t="00")=>(t+e).substr((t+e).length-t.length);let i="",n="0000",s=e.getFullYear();return s<0?(s=-s,i="-",n="000000"):e.getFullYear()>=1e4&&(i="+",n="000000"),[i+t(s,n),t(e.getMonth()+1),t(e.getDate())].join("-")}_openedChanged(e){e&&!this._overlayInitialized&&this._initOverlay(),this._overlayInitialized&&(this.$.overlay.opened=e),e&&this._updateAlignmentAndPosition()}_selectedDateChanged(e,t){if(void 0===e||void 0===t)return;this.__userInputOccurred&&(this.__dispatchChange=!0);const i=e&&t(_._extractDateParts(e)),n=this._formatISO(e);this._inputValue=e?i:"",n!==this.value&&(this.validate(),this.value=n),this.__userInputOccurred=!1,this.__dispatchChange=!1,this._ignoreFocusedDateChange=!0,this._focusedDate=e,this._ignoreFocusedDateChange=!1}_focusedDateChanged(e,t){void 0!==e&&void 0!==t&&(this.__userInputOccurred=!0,this._ignoreFocusedDateChange||this._noInput||(this._inputValue=e?t(_._extractDateParts(e)):""))}_updateHasValue(e){e?this.setAttribute("has-value",""):this.removeAttribute("has-value")}__getOverlayTheme(e,t){if(t)return e}_handleDateChange(e,t,i){if(t){var n=this._parseDate(t);n?_._dateEquals(this[e],n)||(this[e]=n,this.value&&this.validate()):this.value=i}else this[e]=""}_valueChanged(e,t){this.__dispatchChange&&this.dispatchEvent(new CustomEvent("change",{bubbles:!0})),this._handleDateChange("_selectedDate",e,t)}_minChanged(e,t){this._handleDateChange("_minDate",e,t)}_maxChanged(e,t){this._handleDateChange("_maxDate",e,t)}_updateAlignmentAndPosition(){if(this._overlayInitialized){if(!this._fullscreen){const e=this._inputElement.getBoundingClientRect(),t=e.top>window.innerHeight/2;if(e.left+this.clientWidth/2>window.innerWidth/2){const t=Math.min(window.innerWidth,document.documentElement.clientWidth);this.$.overlay.setAttribute("right-aligned",""),this.$.overlay.style.removeProperty("left"),this.$.overlay.style.right=t-e.right+"px"}else this.$.overlay.removeAttribute("right-aligned"),this.$.overlay.style.removeProperty("right"),this.$.overlay.style.left=e.left+"px";if(t){const t=Math.min(window.innerHeight,document.documentElement.clientHeight);this.$.overlay.setAttribute("bottom-aligned",""),this.$.overlay.style.removeProperty("top"),this.$.overlay.style.bottom=t-e.top+"px"}else this.$.overlay.removeAttribute("bottom-aligned"),this.$.overlay.style.removeProperty("bottom"),this.$.overlay.style.top=e.bottom+"px"}this.$.overlay.setAttribute("dir",getComputedStyle(this._inputElement).getPropertyValue("direction")),this._overlayContent._repositionYearScroller()}}_fullscreenChanged(){this._overlayInitialized&&this.$.overlay.opened&&this._updateAlignmentAndPosition()}_onOverlayOpened(){this._openedWithFocusRing=this.hasAttribute("focus-ring")||this.focusElement&&this.focusElement.hasAttribute("focus-ring");var e=this._parseDate(this.initialPosition),t=this._selectedDate||this._overlayContent.initialPosition||e||new Date;e||_._dateAllowed(t,this._minDate,this._maxDate)?this._overlayContent.initialPosition=t:this._overlayContent.initialPosition=_._getClosestDate(t,[this._minDate,this._maxDate]),this._overlayContent.scrollToDate(this._overlayContent.focusedDate||this._overlayContent.initialPosition),this._ignoreFocusedDateChange=!0,this._overlayContent.focusedDate=this._overlayContent.focusedDate||this._overlayContent.initialPosition,this._ignoreFocusedDateChange=!1,window.addEventListener("scroll",this._boundOnScroll,!0),this.addEventListener("iron-resize",this._boundUpdateAlignmentAndPosition),this._webkitOverflowScroll&&(this._touchPrevented=this._preventWebkitOverflowScrollingTouch(this.parentElement)),this._focusOverlayOnOpen?(this._overlayContent.focus(),this._focusOverlayOnOpen=!1):this._focus(),this._noInput&&this.focusElement&&this.focusElement.blur(),this.updateStyles(),this._ignoreAnnounce=!1}_preventWebkitOverflowScrollingTouch(e){for(var t=[];e;){if("touch"===window.getComputedStyle(e).webkitOverflowScrolling){var i=e.style.webkitOverflowScrolling;e.style.webkitOverflowScrolling="auto",t.push({element:e,oldInlineValue:i})}e=e.parentElement}return t}_onOverlayClosed(){if(this._ignoreAnnounce=!0,window.removeEventListener("scroll",this._boundOnScroll,!0),this.removeEventListener("iron-resize",this._boundUpdateAlignmentAndPosition),this._touchPrevented&&(this._touchPrevented.forEach(e=>e.element.style.webkitOverflowScrolling=e.oldInlineValue),this._touchPrevented=[]),this.updateStyles(),this._ignoreFocusedDateChange=!0,this.i18n.parseDate){var e=this._inputValue||"";const t=this.i18n.parseDate(e),i=t&&this._parseDate(`${t.year}-${t.month+1}-${t.day}`);this._isValidDate(i)?this._selectedDate=i:(this._selectedDate=null,this._inputValue=e)}else this._focusedDate&&(this._selectedDate=this._focusedDate);this._ignoreFocusedDateChange=!1,this._nativeInput&&this._nativeInput.selectionStart&&(this._nativeInput.selectionStart=this._nativeInput.selectionEnd),!this.value&&this.validate()}validate(){return!(this.invalid=!this.checkValidity(this._inputValue))}checkValidity(){const e=!this._inputValue||this._selectedDate&&this._inputValue===this.i18n.formatDate(_._extractDateParts(this._selectedDate)),t=!this._selectedDate||_._dateAllowed(this._selectedDate,this._minDate,this._maxDate);let i=!0;return this._inputElement&&(this._inputElement.checkValidity?(this._inputElement.__forceCheckValidity=!0,i=this._inputElement.checkValidity(),this._inputElement.__forceCheckValidity=!1):this._inputElement.validate&&(i=this._inputElement.validate())),e&&t&&i}_onScroll(e){e.target!==window&&this._overlayContent.contains(e.target)||this._updateAlignmentAndPosition()}_focus(){this._noInput?this._overlayInitialized&&this._overlayContent.focus():this._inputElement.focus()}_focusAndSelect(){this._focus(),this._setSelectionRange(0,this._inputValue.length)}_setSelectionRange(e,t){this._nativeInput&&this._nativeInput.setSelectionRange&&this._nativeInput.setSelectionRange(e,t)}_eventKey(e){for(var t=["down","up","enter","esc","tab"],i=0;i<t.length;i++){var n=t[i];if(u.a.keyboardEventMatchesKeys(e,n))return n}}_isValidDate(e){return e&&!isNaN(e.getTime())}_onKeydown(e){if(this._noInput){-1===[9].indexOf(e.keyCode)&&e.preventDefault()}switch(this._eventKey(e)){case"down":case"up":e.preventDefault(),this.opened?(this._overlayContent.focus(),this._overlayContent._onKeydown(e)):(this._focusOverlayOnOpen=!0,this.open());break;case"enter":{const e=this.i18n.parseDate(this._inputValue),t=e&&this._parseDate(e.year+"-"+(e.month+1)+"-"+e.day);this._overlayInitialized&&this._overlayContent.focusedDate&&this._isValidDate(t)&&(this._selectedDate=this._overlayContent.focusedDate),this.close();break}case"esc":this._focusedDate=this._selectedDate,this._close();break;case"tab":this.opened&&(e.preventDefault(),this._setSelectionRange(0,0),e.shiftKey?this._overlayContent.focusCancel():(this._overlayContent.focus(),this._overlayContent.revealDate(this._focusedDate)))}}_onUserInput(e){!this.opened&&this._inputElement.value&&this.open(),this._userInputValueChanged()}_userInputValueChanged(e){if(this.opened&&this._inputValue){const e=this.i18n.parseDate&&this.i18n.parseDate(this._inputValue),t=e&&this._parseDate(`${e.year}-${e.month+1}-${e.day}`);this._isValidDate(t)&&(this._ignoreFocusedDateChange=!0,_._dateEquals(t,this._focusedDate)||(this._focusedDate=t),this._ignoreFocusedDateChange=!1)}}_announceFocusedDate(e,t,i){t&&!i&&this._overlayContent.announceFocusedDate()}get _overlayContent(){return this.$.overlay.content.querySelector("#overlay-content")}});class Y extends(Object(F.a)(Object(O.a)(Object(m.a)(Object(f.a)(N(Object(c.a)(h.a))))))){static get template(){return n.a`
    <style>
      :host {
        display: inline-block;
      }

      :host([hidden]) {
        display: none !important;
      }

      :host([opened]) {
        pointer-events: auto;
      }

      [part="text-field"] {
        width: 100%;
        min-width: 0;
      }
    </style>


    <vaadin-text-field id="input" role="application" autocomplete="off" on-focus="_focus" value="{{_userInputValue}}" invalid="[[invalid]]" label="[[label]]" name="[[name]]" placeholder="[[placeholder]]" required="[[required]]" disabled="[[disabled]]" readonly="[[readonly]]" error-message="[[errorMessage]]" clear-button-visible="[[clearButtonVisible]]" aria-label\$="[[label]]" part="text-field" theme\$="[[theme]]">
      <slot name="prefix" slot="prefix"></slot>
      <div part="toggle-button" slot="suffix" on-tap="_toggle" role="button" aria-label\$="[[i18n.calendar]]" aria-expanded\$="[[_getAriaExpanded(opened)]]"></div>
    </vaadin-text-field>

    <vaadin-date-picker-overlay id="overlay" fullscreen\$="[[_fullscreen]]" theme\$="[[__getOverlayTheme(theme, _overlayInitialized)]]" on-vaadin-overlay-open="_onOverlayOpened" on-vaadin-overlay-close="_onOverlayClosed" disable-upgrade="">
      <template>
        <vaadin-date-picker-overlay-content id="overlay-content" i18n="[[i18n]]" fullscreen\$="[[_fullscreen]]" label="[[label]]" selected-date="{{_selectedDate}}" slot="dropdown-content" focused-date="{{_focusedDate}}" show-week-numbers="[[showWeekNumbers]]" min-date="[[_minDate]]" max-date="[[_maxDate]]" role="dialog" on-date-tap="_close" part="overlay-content" theme\$="[[__getOverlayTheme(theme, _overlayInitialized)]]">
        </vaadin-date-picker-overlay-content>
      </template>
    </vaadin-date-picker-overlay>

    <iron-media-query query="[[_fullscreenMediaQuery]]" query-matches="{{_fullscreen}}">
    </iron-media-query>
`}static get is(){return"vaadin-date-picker"}static get version(){return"4.0.7"}static get properties(){return{clearButtonVisible:{type:Boolean,value:!1},disabled:{type:Boolean,value:!1,reflectToAttribute:!0},errorMessage:String,placeholder:String,readonly:{type:Boolean,value:!1,reflectToAttribute:!0},invalid:{type:Boolean,reflectToAttribute:!0,notify:!0,value:!1},_userInputValue:String}}static get observers(){return["_userInputValueChanged(_userInputValue)","_setClearButtonLabel(i18n.clear)"]}ready(){super.ready(),Object(x.a)(this,()=>this._inputElement.validate=(()=>{})),this._inputElement.addEventListener("change",()=>{""===this._inputElement.value&&(this.__dispatchChange=!0,this.value="",this.validate(),this.__dispatchChange=!1)})}_onVaadinOverlayClose(e){this._openedWithFocusRing&&this.hasAttribute("focused")?this.focusElement.setAttribute("focus-ring",""):this.hasAttribute("focused")||this.focusElement.blur(),e.detail.sourceEvent&&-1!==e.detail.sourceEvent.composedPath().indexOf(this)&&e.preventDefault()}_toggle(e){e.stopPropagation(),this[this._overlayInitialized&&this.$.overlay.opened?"close":"open"]()}_input(){return this.$.input}set _inputValue(e){this._inputElement.value=e}get _inputValue(){return this._inputElement.value}_getAriaExpanded(e){return Boolean(e).toString()}get focusElement(){return this._input()||this}_setClearButtonLabel(e){this._inputElement.shadowRoot.querySelector('[part="clear-button"]').setAttribute("aria-label",e)}}customElements.define(Y.is,Y)},518:function(e,t){const i=document.createElement("template");i.setAttribute("style","display: none;"),i.innerHTML='\n<dom-module id="ha-date-picker-text-field-styles" theme-for="vaadin-text-field">\n  <template>\n    <style>\n      :host {\n        padding: 8px 0;\n      }\n\n      [part~="label"] {\n        top: 6px;\n        font-size: var(--paper-font-subhead_-_font-size);\n        color: var(--paper-input-container-color, var(--secondary-text-color));\n      }\n\n      :host([focused]) [part~="label"] {\n        color: var(--paper-input-container-focus-color, var(--primary-color));\n      }\n\n      [part~="input-field"] {\n        color: var(--primary-text-color);\n        top: 3px;\n      }\n\n      [part~="input-field"]::before, [part~="input-field"]::after {\n        background-color: var(--paper-input-container-color, var(--secondary-text-color));\n        opacity: 1;\n      }\n\n      :host([focused]) [part~="input-field"]::before, :host([focused]) [part~="input-field"]::after {\n        background-color: var(--paper-input-container-focus-color, var(--primary-color));\n      }\n\n      [part~="value"] {\n        font-size: var(--paper-font-subhead_-_font-size);\n      }\n    </style>\n  </template>\n</dom-module>\n<dom-module id="ha-date-picker-button-styles" theme-for="vaadin-button">\n  <template>\n    <style>\n      :host([part~="today-button"]) [part~="button"]::before {\n        content: "⦿";\n        color: var(--primary-color);\n      }\n\n      [part~="button"] {\n        font-family: inherit;\n        font-size: var(--paper-font-subhead_-_font-size);\n        border: none;\n        background: transparent;\n        cursor: pointer;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n        color: inherit;\n      }\n\n      [part~="button"]:focus {\n        outline: none;\n      }\n    </style>\n  </template>\n</dom-module>\n<dom-module id="ha-date-picker-overlay-styles" theme-for="vaadin-date-picker-overlay">\n  <template>\n    <style include="vaadin-date-picker-overlay-default-theme">\n      [part~="toolbar"] {\n        padding: 0.3em;\n        background-color: var(--secondary-background-color);\n      }\n\n      [part="years"] {\n        background-color: var(--secondary-text-color);\n        --material-body-text-color: var(--primary-background-color);\n      }\n\n      [part="overlay"] {\n        background-color: var(--primary-background-color);\n        --material-body-text-color: var(--secondary-text-color);\n      }\n\n    </style>\n  </template>\n</dom-module>\n<dom-module id="ha-date-picker-month-styles" theme-for="vaadin-month-calendar">\n  <template>\n    <style include="vaadin-month-calendar-default-theme">\n      [part="date"][today] {\n        color: var(--primary-color);\n      }\n    </style>\n  </template>\n</dom-module>\n',document.head.appendChild(i.content)},577:function(e,t,i){"use strict";i.r(t),i.d(t,"Layout1d",function(){return s});var n=i(589);class s extends n.a{constructor(e){super(e),this._physicalItems=new Map,this._newPhysicalItems=new Map,this._metrics=new Map,this._anchorIdx=null,this._anchorPos=null,this._stable=!0,this._needsRemeasure=!1,this._nMeasured=0,this._tMeasured=0,this._estimate=!0}updateItemSizes(e){Object.keys(e).forEach(t=>{const i=e[t],n=this._getMetrics(Number(t)),s=n[this._sizeDim];n.width=i.width+(i.marginLeft||0)+(i.marginRight||0),n.height=i.height+(i.marginTop||0)+(i.marginBottom||0);const a=n[this._sizeDim],r=this._getPhysicalItem(Number(t));if(r){let e;void 0!==a&&(r.size=a,void 0===s?(e=a,this._nMeasured++):e=a-s),this._tMeasured=this._tMeasured+e}}),this._nMeasured?(this._updateItemSize(),this._scheduleReflow()):console.warn("No items measured yet.")}_updateItemSize(){this._itemSize[this._sizeDim]=Math.round(this._tMeasured/this._nMeasured)}_getMetrics(e){return this._metrics[e]=this._metrics[e]||{}}_getPhysicalItem(e){return this._newPhysicalItems.get(e)||this._physicalItems.get(e)}_getSize(e){const t=this._getPhysicalItem(e);return t&&t.size}_getPosition(e){const t=this._physicalItems.get(e);return t?t.pos:e*this._delta+this._spacing}_calculateAnchor(e,t){return 0===e?0:t>this._scrollSize-this._viewDim1?this._totalItems-1:Math.max(0,Math.min(this._totalItems-1,Math.floor((e+t)/2/this._delta)))}_getAnchor(e,t){if(0===this._physicalItems.size)return this._calculateAnchor(e,t);if(this._first<0)return console.error("_getAnchor: negative _first"),this._calculateAnchor(e,t);if(this._last<0)return console.error("_getAnchor: negative _last"),this._calculateAnchor(e,t);const i=this._getPhysicalItem(this._first),n=this._getPhysicalItem(this._last),s=i.pos,a=s+i.size,r=n.pos,o=r+n.size;if(o<e)return this._calculateAnchor(e,t);if(s>t)return this._calculateAnchor(e,t);if(s>=e||a>=e)return this._first;if(o<=t||r<=t)return this._last;let l=this._last,d=this._first;for(;;){const i=Math.round((l+d)/2),n=this._physicalItems.get(i),s=n.pos,a=s+n.size;if(s>=e&&s<=t||a>=e&&a<=t)return i;a<e?d=i+1:s>t&&(l=i-1)}}_getActiveItems(){if(0===this._viewDim1||0===this._totalItems)this._clearItems();else{const e=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang),t=Math.max(0,e-this._viewDim1-2*this._overhang);this._getItems(t,e)}}_clearItems(){this._first=-1,this._last=-1,this._physicalMin=0,this._physicalMax=0;const e=this._newPhysicalItems;this._newPhysicalItems=this._physicalItems,this._newPhysicalItems.clear(),this._physicalItems=e,this._stable=!0}_getItems(e,t){const i=this._newPhysicalItems;null!==this._anchorIdx&&null!==this._anchorPos||(this._anchorIdx=this._getAnchor(e,t),this._anchorPos=this._getPosition(this._anchorIdx));let n=this._getSize(this._anchorIdx);void 0===n&&(n=this._itemDim1);let s=0;for(this._anchorPos+n+this._spacing<e&&(s=e-(this._anchorPos+n+this._spacing)),this._anchorPos>t&&(s=t-this._anchorPos),s&&(this._scrollPosition-=s,e-=s,t-=s,this._scrollError+=s),i.set(this._anchorIdx,{pos:this._anchorPos,size:n}),this._first=this._last=this._anchorIdx,this._physicalMin=this._physicalMax=this._anchorPos,this._stable=!0;this._physicalMin>e&&this._first>0;){let e=this._getSize(--this._first);void 0===e&&(this._stable=!1,e=this._itemDim1);const t=this._physicalMin-=e+this._spacing;if(i.set(this._first,{pos:t,size:e}),!1===this._stable&&!1===this._estimate)break}for(;this._physicalMax<t&&this._last<this._totalItems;){let e=this._getSize(this._last);if(void 0===e&&(this._stable=!1,e=this._itemDim1),i.set(this._last++,{pos:this._physicalMax,size:e}),!1===this._stable&&!1===this._estimate)break;this._physicalMax+=e+this._spacing}this._last--;const a=this._calculateError();a&&(this._physicalMin-=a,this._physicalMax-=a,this._anchorPos-=a,this._scrollPosition-=a,i.forEach(e=>e.pos-=a),this._scrollError+=a),this._stable&&(this._newPhysicalItems=this._physicalItems,this._newPhysicalItems.clear(),this._physicalItems=i)}_calculateError(){return 0===this._first?this._physicalMin:this._physicalMin<=0?this._physicalMin-this._first*this._delta:this._last===this._totalItems-1?this._physicalMax-this._scrollSize:this._physicalMax>=this._scrollSize?this._physicalMax-this._scrollSize+(this._totalItems-1-this._last)*this._delta:0}_updateScrollSize(){super._updateScrollSize(),this._scrollSize=Math.max(this._physicalMax,this._scrollSize)}_reflow(){const{_first:e,_last:t,_scrollSize:i}=this;this._updateScrollSize(),this._getActiveItems(),this._scrollIfNeeded(),this._scrollSize!==i&&this._emitScrollSize(),this._updateVisibleIndices(),this._emitRange(),-1===this._first&&-1===this._last?this._resetReflowState():this._first!==e||this._last!==t||this._needsRemeasure?(this._emitChildPositions(),this._emitScrollError()):(this._emitChildPositions(),this._emitScrollError(),this._resetReflowState())}_resetReflowState(){this._anchorIdx=null,this._anchorPos=null,this._stable=!0}_getItemPosition(e){return{[this._positionDim]:this._getPosition(e),[this._secondaryPositionDim]:0}}_getItemSize(e){return{[this._sizeDim]:this._getSize(e)||this._itemDim1,[this._secondarySizeDim]:this._itemDim2}}_viewDim2Changed(){this._needsRemeasure=!0,this._scheduleReflow()}_emitRange(){const e=this._needsRemeasure,t=this._stable;this._needsRemeasure=!1,super._emitRange({remeasure:e,stable:t})}}},589:function(e,t,i){"use strict";let n;async function s(){return n||async function(){n=window.EventTarget;try{new n}catch(e){n=(await i.e(196).then(i.t.bind(null,808,7))).EventTarget}return n}()}i.d(t,"a",function(){return a});class a{constructor(e){this._latestCoords={left:0,top:0},this._direction="vertical",this._viewportSize={width:0,height:0},this._pendingReflow=!1,this._scrollToIndex=-1,this._scrollToAnchor=0,this._eventTargetPromise=s().then(e=>this._eventTarget=new e),this._physicalMin=0,this._physicalMax=0,this._first=-1,this._last=-1,this._itemSize={width:100,height:100},this._spacing=0,this._sizeDim="height",this._secondarySizeDim="width",this._positionDim="top",this._secondaryPositionDim="left",this._scrollPosition=0,this._scrollError=0,this._totalItems=0,this._scrollSize=1,this._overhang=150,Object.assign(this,e)}get totalItems(){return this._totalItems}set totalItems(e){e!==this._totalItems&&(this._totalItems=e,this._scheduleReflow())}get direction(){return this._direction}set direction(e){(e="horizontal"===e?e:"vertical")!==this._direction&&(this._direction=e,this._sizeDim="horizontal"===e?"width":"height",this._secondarySizeDim="horizontal"===e?"height":"width",this._positionDim="horizontal"===e?"left":"top",this._secondaryPositionDim="horizontal"===e?"top":"left",this._scheduleReflow())}get itemSize(){return this._itemSize}set itemSize(e){const{_itemDim1:t,_itemDim2:i}=this;Object.assign(this._itemSize,e),t===this._itemDim1&&i===this._itemDim2||(i!==this._itemDim2?this._itemDim2Changed():this._scheduleReflow())}get spacing(){return this._spacing}set spacing(e){e!==this._spacing&&(this._spacing=e,this._scheduleReflow())}get viewportSize(){return this._viewportSize}set viewportSize(e){const{_viewDim1:t,_viewDim2:i}=this;Object.assign(this._viewportSize,e),i!==this._viewDim2?this._viewDim2Changed():t!==this._viewDim1&&this._checkThresholds()}get viewportScroll(){return this._latestCoords}set viewportScroll(e){Object.assign(this._latestCoords,e);const t=this._scrollPosition;this._scrollPosition=this._latestCoords[this._positionDim],t!==this._scrollPosition&&(this._scrollPositionChanged(t,this._scrollPosition),this._updateVisibleIndices()),this._checkThresholds()}reflowIfNeeded(){this._pendingReflow&&(this._pendingReflow=!1,this._reflow())}scrollToIndex(e,t="start"){if(Number.isFinite(e)){switch(e=Math.min(this.totalItems,Math.max(0,e)),this._scrollToIndex=e,"nearest"===t&&(t=e>this._first+this._num/2?"end":"start"),t){case"start":this._scrollToAnchor=0;break;case"center":this._scrollToAnchor=.5;break;case"end":this._scrollToAnchor=1;break;default:throw new TypeError("position must be one of: start, center, end, nearest")}this._scheduleReflow(),this.reflowIfNeeded()}}async dispatchEvent(...e){await this._eventTargetPromise,this._eventTarget.dispatchEvent(...e)}async addEventListener(...e){await this._eventTargetPromise,this._eventTarget.addEventListener(...e)}async removeEventListener(...e){await this._eventTargetPromise,this._eventTarget.removeEventListener(...e)}updateItemSizes(e){}_itemDim2Changed(){}_viewDim2Changed(){}_getItemSize(e){return{[this._sizeDim]:this._itemDim1,[this._secondarySizeDim]:this._itemDim2}}get _delta(){return this._itemDim1+this._spacing}get _itemDim1(){return this._itemSize[this._sizeDim]}get _itemDim2(){return this._itemSize[this._secondarySizeDim]}get _viewDim1(){return this._viewportSize[this._sizeDim]}get _viewDim2(){return this._viewportSize[this._secondarySizeDim]}_scheduleReflow(){this._pendingReflow=!0}_reflow(){const{_first:e,_last:t,_scrollSize:i}=this;this._updateScrollSize(),this._getActiveItems(),this._scrollIfNeeded(),this._scrollSize!==i&&this._emitScrollSize(),-1===this._first&&-1===this._last?this._emitRange():(this._first!==e||this._last!==t||this._spacingChanged)&&(this._emitRange(),this._emitChildPositions()),this._emitScrollError()}_updateScrollSize(){this._scrollSize=Math.max(1,this._totalItems*this._delta)}_scrollIfNeeded(){if(-1===this._scrollToIndex)return;const e=this._scrollToIndex,t=this._scrollToAnchor,i=this._getItemPosition(e)[this._positionDim],n=this._getItemSize(e)[this._sizeDim],s=this._scrollPosition+this._viewDim1*t,a=i+n*t,r=Math.floor(Math.min(this._scrollSize-this._viewDim1,Math.max(0,this._scrollPosition-s+a)));this._scrollError+=this._scrollPosition-r,this._scrollPosition=r}_emitRange(e){const t=Object.assign({first:this._first,last:this._last,num:this._num,stable:!0,firstVisible:this._firstVisible,lastVisible:this._lastVisible},e);this.dispatchEvent(new CustomEvent("rangechange",{detail:t}))}_emitScrollSize(){const e={[this._sizeDim]:this._scrollSize};this.dispatchEvent(new CustomEvent("scrollsizechange",{detail:e}))}_emitScrollError(){if(this._scrollError){const e={[this._positionDim]:this._scrollError,[this._secondaryPositionDim]:0};this.dispatchEvent(new CustomEvent("scrollerrorchange",{detail:e})),this._scrollError=0}}_emitChildPositions(){const e={};for(let t=this._first;t<=this._last;t++)e[t]=this._getItemPosition(t);this.dispatchEvent(new CustomEvent("itempositionchange",{detail:e}))}get _num(){return-1===this._first||-1===this._last?0:this._last-this._first+1}_checkThresholds(){if(0===this._viewDim1&&this._num>0)this._scheduleReflow();else{const e=Math.max(0,this._scrollPosition-this._overhang),t=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang);(this._physicalMin>e||this._physicalMax<t)&&this._scheduleReflow()}}_updateVisibleIndices(){let e=this._firstVisible,t=this._lastVisible;for(let i=this._first;i<=this._last;i++){const n=this._getItemPosition(i)[this._positionDim];n<=this._scrollPosition&&(e=i),n<this._scrollPosition+this._viewDim1&&(t=i)}e>t||e===this._firstVisible&&t===this._lastVisible||(this._firstVisible=e,this._lastVisible=t,this._emitRange())}_scrollPositionChanged(e,t){const i=this._scrollSize-this._viewDim1;(e<i||t<i)&&(this._scrollToIndex=-1)}}},72:function(e,t,i){"use strict";i(3),i(115),i(116),i(117),i(118);var n=i(59),s=(i(41),i(5)),a=i(4),r=i(98);Object(s.a)({is:"paper-input",_template:a.a`
    <style>
      :host {
        display: block;
      }

      :host([focused]) {
        outline: none;
      }

      :host([hidden]) {
        display: none !important;
      }

      input {
        /* Firefox sets a min-width on the input, which can cause layout issues */
        min-width: 0;
      }

      /* In 1.x, the <input> is distributed to paper-input-container, which styles it.
      In 2.x the <iron-input> is distributed to paper-input-container, which styles
      it, but in order for this to work correctly, we need to reset some
      of the native input's properties to inherit (from the iron-input) */
      iron-input > input {
        @apply --paper-input-container-shared-input-style;
        font-family: inherit;
        font-weight: inherit;
        font-size: inherit;
        letter-spacing: inherit;
        word-spacing: inherit;
        line-height: inherit;
        text-shadow: inherit;
        color: inherit;
        cursor: inherit;
      }

      input:disabled {
        @apply --paper-input-container-input-disabled;
      }

      input::-webkit-outer-spin-button,
      input::-webkit-inner-spin-button {
        @apply --paper-input-container-input-webkit-spinner;
      }

      input::-webkit-clear-button {
        @apply --paper-input-container-input-webkit-clear;
      }

      input::-webkit-calendar-picker-indicator {
        @apply --paper-input-container-input-webkit-calendar-picker-indicator;
      }

      input::-webkit-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input:-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-ms-clear {
        @apply --paper-input-container-ms-clear;
      }

      input::-ms-reveal {
        @apply --paper-input-container-ms-reveal;
      }

      input:-ms-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container id="container" no-label-float="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <slot name="prefix" slot="prefix"></slot>

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <!-- Need to bind maxlength so that the paper-input-char-counter works correctly -->
      <iron-input bind-value="{{value}}" slot="input" class="input-element" id$="[[_inputId]]" maxlength$="[[maxlength]]" allowed-pattern="[[allowedPattern]]" invalid="{{invalid}}" validator="[[validator]]">
        <input aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" disabled$="[[disabled]]" title$="[[title]]" type$="[[type]]" pattern$="[[pattern]]" required$="[[required]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" min$="[[min]]" max$="[[max]]" step$="[[step]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" list$="[[list]]" size$="[[size]]" autocapitalize$="[[autocapitalize]]" autocorrect$="[[autocorrect]]" on-change="_onChange" tabindex$="[[tabIndex]]" autosave$="[[autosave]]" results$="[[results]]" accept$="[[accept]]" multiple$="[[multiple]]">
      </iron-input>

      <slot name="suffix" slot="suffix"></slot>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
  `,behaviors:[r.a,n.a],properties:{value:{type:String}},get _focusableElement(){return this.inputElement._inputElement},listeners:{"iron-input-ready":"_onIronInputReady"},_onIronInputReady:function(){this.$.nativeInput||(this.$.nativeInput=this.$$("input")),this.inputElement&&-1!==this._typesThatHaveText.indexOf(this.$.nativeInput.type)&&(this.alwaysFloatLabel=!0),this.inputElement.bindValue&&this.$.container._handleValueAndAutoValidate(this.inputElement)}})},832:function(e,t,i){"use strict";i.r(t);i(226),i(237),i(156),i(110),i(72),i(192);var n=i(4),s=i(29);i(415),i(131),i(221),i(518),i(99);const a={},r="*";customElements.define("ha-logbook-data",class extends s.a{static get properties(){return{hass:{type:Object,observer:"hassChanged"},filterDate:{type:String,observer:"filterDataChanged"},filterPeriod:{type:Number,observer:"filterDataChanged"},filterEntity:{type:String,observer:"filterDataChanged"},isLoading:{type:Boolean,value:!0,readOnly:!0,notify:!0},entries:{type:Object,value:null,readOnly:!0,notify:!0}}}hassChanged(e,t){!t&&this.filterDate&&this.updateData()}filterDataChanged(e,t){void 0!==t&&this.updateData()}updateData(){this.hass&&(this._setIsLoading(!0),this.getData(this.filterDate,this.filterPeriod,this.filterEntity).then(e=>{this._setEntries(e),this._setIsLoading(!1)}))}getData(e,t,i){return i||(i=r),a[t]||(a[t]=[]),a[t][e]||(a[t][e]=[]),a[t][e][i]?a[t][e][i]:i!==r&&a[t][e][r]?a[t][e][r].then(function(e){return e.filter(function(e){return e.entity_id===i})}):(a[t][e][i]=this._getFromServer(e,t,i),a[t][e][i])}_getFromServer(e,t,i){let n="logbook/"+e+"?period="+t;return i!==r&&(n+="&entity="+i),this.hass.callApi("GET",n).then(function(e){return e.reverse(),e},function(){return null})}refreshLogbook(){a[this.filterPeriod][this.filterDate]=[],this.updateData()}});i(183);var o=i(215),l=i(248),d=i(185),h=i(196),c=i(96),u=i(0),p=i(13),m=i(9);class f{constructor(e){this._createElementFn=null,this._updateElementFn=null,this._recycleElementFn=null,this._elementKeyFn=null,this._items=[],this._totalItems=null,this._needsReset=!1,this._needsRemeasure=!1,this._active=new Map,this._prevActive=new Map,this._keyToChild=new Map,this._childToKey=new WeakMap,this._indexToMeasure={},this.__incremental=!1,this._measureCallback=null,this._num=1/0,this._first=0,this._last=0,this._prevFirst=0,this._prevLast=0,this._pendingRender=null,this._container=null,this._ordered=[],e&&Object.assign(this,e)}get container(){return this._container}set container(e){e!==this._container&&(this._container&&this._ordered.forEach(e=>this._removeChild(e)),this._container=e,e?this._ordered.forEach(e=>this._insertBefore(e,null)):(this._ordered.length=0,this._active.clear(),this._prevActive.clear()),this.requestReset())}get createElement(){return this._createElementFn}set createElement(e){e!==this._createElementFn&&(this._createElementFn=e,this._keyToChild.clear(),this.requestReset())}get updateElement(){return this._updateElementFn}set updateElement(e){e!==this._updateElementFn&&(this._updateElementFn=e,this.requestReset())}get recycleElement(){return this._recycleElementFn}set recycleElement(e){e!==this._recycleElementFn&&(this._recycleElementFn=e,this.requestReset())}get elementKey(){return this._elementKeyFn}set elementKey(e){e!==this._elementKeyFn&&(this._elementKeyFn=e,this._keyToChild.clear(),this.requestReset())}get first(){return this._first}set first(e){if("number"!=typeof e)throw new Error("New value must be a number.");const t=Math.max(0,Math.min(e,this.totalItems-this._num));t!==this._first&&(this._first=t,this._scheduleRender())}get num(){return this._num}set num(e){if("number"!=typeof e)throw new Error("New value must be a number.");e!==this._num&&(this._num=e,this.first=this._first,this._scheduleRender())}get items(){return this._items}set items(e){e!==this._items&&Array.isArray(e)&&(this._items=e,this.requestReset())}get totalItems(){return null===this._totalItems?this._items.length:this._totalItems}set totalItems(e){if("number"!=typeof e&&null!==e)throw new Error("New value must be a number.");e!==this._totalItems&&(this._totalItems=e,this.first=this._first,this.requestReset())}get _incremental(){return this.__incremental}set _incremental(e){e!==this.__incremental&&(this.__incremental=e,this._scheduleRender())}requestRemeasure(){this._needsRemeasure=!0,this._scheduleRender()}_shouldRender(){return Boolean(this.container&&this.createElement)}async _scheduleRender(){this._pendingRender||(this._pendingRender=!0,await Promise.resolve(),this._pendingRender=!1,this._shouldRender()&&this._render())}requestReset(){this._needsReset=!0,this._scheduleRender()}get _toMeasure(){return this._ordered.reduce((e,t,i)=>{const n=this._first+i;return(this._needsReset||this._needsRemeasure||n<this._prevFirst||n>this._prevLast)&&(e.indices.push(n),e.children.push(t)),e},{indices:[],children:[]})}async _measureChildren({indices:e,children:t}){await new Promise(e=>{requestAnimationFrame(e)});const i=t.map(e=>this._measureChild(e)).reduce((t,i,n)=>(t[e[n]]=this._indexToMeasure[e[n]]=i,t),{});this._measureCallback(i)}async _render(){const e=this._first!==this._prevFirst||this._num!==this._prevNum;(e||this._needsReset)&&(this._last=this._first+Math.min(this._num,this.totalItems-this._first)-1,(this._num||this._prevNum)&&(this._needsReset?this._reset(this._first,this._last):(this._discardHead(),this._discardTail(),this._addHead(),this._addTail()))),(this._needsRemeasure||this._needsReset)&&(this._indexToMeasure={});const t=this._num>0&&this._measureCallback&&(e||this._needsRemeasure||this._needsReset)?this._toMeasure:null;this._incremental||(this._prevActive.forEach((e,t)=>this._unassignChild(t,e)),this._prevActive.clear()),this._prevFirst=this._first,this._prevLast=this._last,this._prevNum=this._num,this._needsReset=!1,this._needsRemeasure=!1,this._didRender(),t&&await this._measureChildren(t)}_didRender(){}_discardHead(){const e=this._ordered;for(let t=this._prevFirst;e.length&&t<this._first;t++)this._unassignChild(e.shift(),t)}_discardTail(){const e=this._ordered;for(let t=this._prevLast;e.length&&t>this._last;t--)this._unassignChild(e.pop(),t)}_addHead(){const e=this._first;for(let t=Math.min(this._last,this._prevFirst-1);t>=e;t--){const e=this._assignChild(t);this._insertBefore(e,this._firstChild),this.updateElement&&this.updateElement(e,this._items[t],t),this._ordered.unshift(e)}}_addTail(){const e=Math.max(this._first,this._prevLast+1),t=this._last;for(let i=e;i<=t;i++){const e=this._assignChild(i);this._insertBefore(e,null),this.updateElement&&this.updateElement(e,this._items[i],i),this._ordered.push(e)}}_reset(e,t){const i=this._active;this._active=this._prevActive,this._prevActive=i,this._ordered.length=0;let n=this._firstChild;for(let s=e;s<=t;s++){const e=this._assignChild(s);this._ordered.push(e),n?n===this._node(e)?n=this._nextSibling(e):this._insertBefore(e,n):this._childIsAttached(e)||this._insertBefore(e,null),this.updateElement&&this.updateElement(e,this._items[s],s)}}_assignChild(e){const t=this.elementKey?this.elementKey(e):e;let i;return(i=this._keyToChild.get(t))?this._prevActive.delete(i):(i=this.createElement(this._items[e],e),this._keyToChild.set(t,i),this._childToKey.set(i,t)),this._showChild(i),this._active.set(i,e),i}_unassignChild(e,t){if(this._hideChild(e),this._incremental)this._active.delete(e),this._prevActive.set(e,t);else{const i=this._childToKey.get(e);this._childToKey.delete(e),this._keyToChild.delete(i),this._active.delete(e),this.recycleElement?this.recycleElement(e,t):this._node(e).parentNode&&this._removeChild(e)}}get _firstChild(){return this._ordered.length&&this._childIsAttached(this._ordered[0])?this._node(this._ordered[0]):null}_node(e){return e}_nextSibling(e){return e.nextSibling}_insertBefore(e,t){this._container.insertBefore(e,t)}_removeChild(e){e.parentNode.removeChild(e)}_childIsAttached(e){const t=this._node(e);return t&&t.parentNode===this._container}_hideChild(e){e instanceof HTMLElement&&(e.style.display="none")}_showChild(e){e instanceof HTMLElement&&(e.style.display=null)}_measureChild(e){const{width:t,height:i}=e.getBoundingClientRect();return Object.assign({width:t,height:i},function(e){const t=window.getComputedStyle(e);return{marginTop:_(t.marginTop),marginRight:_(t.marginRight),marginBottom:_(t.marginBottom),marginLeft:_(t.marginLeft)}}(e))}}function _(e){const t=e?parseFloat(e):NaN;return Number.isNaN(t)?0:t}const v=e=>(class extends e{constructor(e){const{part:t,renderItem:i,useShadowDOM:n,layout:s}=e,a=t.startNode.parentNode;super({container:a,scrollTarget:e.scrollTarget||a,useShadowDOM:n,layout:s}),this._pool=[],this._renderItem=i,this._hostPart=t}createElement(){return this._pool.pop()||new m.b(this._hostPart.options)}updateElement(e,t,i){e.setValue(this._renderItem(t,i)),e.commit()}recycleElement(e){this._pool.push(e)}get _kids(){return this._ordered.map(e=>e.startNode.nextElementSibling)}_node(e){return e.startNode}_nextSibling(e){return e.endNode.nextSibling}_insertBefore(e,t){if(null===t&&(t=this._hostPart.endNode),this._childIsAttached(e)){const i=e.endNode.nextSibling;if(t!==e.startNode&&t!==i)for(let n=e.startNode;n!==i;){const e=n.nextSibling;super._insertBefore(n,t),n=e}}else e.startNode=Object(m.e)(),e.endNode=Object(m.e)(),super._insertBefore(e.startNode,t),super._insertBefore(e.endNode,t)}_hideChild(e){let t=e.startNode;for(;t&&t!==e.endNode;)super._hideChild(t),t=t.nextSibling}_showChild(e){let t=e.startNode;for(;t&&t!==e.endNode;)super._showChild(t),t=t.nextSibling}_measureChild(e){return super._measureChild(e.startNode.nextElementSibling)}});class y extends(v(f)){}const g=new WeakMap;Object(m.f)(e=>async t=>{let i=g.get(t);i||(t.startNode.isConnected||await Promise.resolve(),i=new y({part:t,renderItem:e.renderItem}),g.set(t,i));const{first:n,num:s,totalItems:a}=e;Object.assign(i,{first:n,num:s,totalItems:a})});let b;async function w(){return b||async function(){b=window.ResizeObserver;try{new b(function(){})}catch(e){b=(await i.e(194).then(i.bind(null,807))).default}return b}()}const x="uni-virtualizer-host";let k=null;function D(e,t){return`\n    ${e} {\n      display: block;\n      position: relative;\n      contain: strict;\n      height: 150px;\n      overflow: auto;\n    }\n    ${t} {\n      box-sizing: border-box;\n    }`}class E extends Event{constructor(e,t){super(e,t),this._first=Math.floor(t.first||0),this._last=Math.floor(t.last||0),this._firstVisible=Math.floor(t.firstVisible||0),this._lastVisible=Math.floor(t.lastVisible||0)}get first(){return this._first}get last(){return this._last}get firstVisible(){return this._firstVisible}get lastVisible(){return this._lastVisible}}class S extends f{constructor(e){super({}),this._needsUpdateView=!1,this._layout=null,this._lazyLoadDefaultLayout=!0,this._scrollTarget=null,this._sizer=null,this._scrollSize=null,this._scrollErr=null,this._childrenPos=null,this._containerElement=null,this._containerInlineStyle=null,this._containerStylesheet=null,this._useShadowDOM=!0,this._containerSize=null,this._containerRO=null,this._childrenRO=null,this._skipNextChildrenSizeChanged=!1,this._scrollToIndex=null,this._num=0,this._first=-1,this._last=-1,this._prevFirst=-1,this._prevLast=-1,e&&Object.assign(this,e)}get container(){return super.container}set container(e){super.container=e,this._initResizeObservers().then(()=>{const t=this._containerElement,i=e&&e.nodeType===Node.DOCUMENT_FRAGMENT_NODE?e.host:e;t!==i&&(this._containerRO.disconnect(),this._containerSize=null,t?(this._containerInlineStyle?t.setAttribute("style",this._containerInlineStyle):t.removeAttribute("style"),this._containerInlineStyle=null,t===this._scrollTarget&&(t.removeEventListener("scroll",this,{passive:!0}),this._sizer&&this._sizer.remove())):addEventListener("scroll",this,{passive:!0}),this._containerElement=i,i&&(this._containerInlineStyle=i.getAttribute("style")||null,this._applyContainerStyles(),i===this._scrollTarget&&(this._sizer=this._sizer||this._createContainerSizer(),this._container.prepend(this._sizer)),this._scheduleUpdateView(),this._containerRO.observe(i)))})}get layout(){return this._layout}set layout(e){e!==this._layout&&(this._layout&&(this._measureCallback=null,this._layout.removeEventListener("scrollsizechange",this),this._layout.removeEventListener("scrollerrorchange",this),this._layout.removeEventListener("itempositionchange",this),this._layout.removeEventListener("rangechange",this),this._containerElement&&this._sizeContainer(void 0)),this._layout=e,this._layout&&("function"==typeof this._layout.updateItemSizes&&(this._measureCallback=this._layout.updateItemSizes.bind(this._layout),this.requestRemeasure()),this._layout.addEventListener("scrollsizechange",this),this._layout.addEventListener("scrollerrorchange",this),this._layout.addEventListener("itempositionchange",this),this._layout.addEventListener("rangechange",this),this._scheduleUpdateView()))}get scrollTarget(){return this._scrollTarget}set scrollTarget(e){e===window&&(e=null),this._scrollTarget!==e&&(this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this,{passive:!0}),this._sizer&&this._scrollTarget===this._containerElement&&this._sizer.remove()),this._scrollTarget=e,e&&(e.addEventListener("scroll",this,{passive:!0}),e===this._containerElement&&(this._sizer=this._sizer||this._createContainerSizer(),this._container.prepend(this._sizer))))}get useShadowDOM(){return this._useShadowDOM}set useShadowDOM(e){this._useShadowDOM!==e&&(this._useShadowDOM=Boolean(e),this._containerStylesheet&&(this._containerStylesheet.parentElement.removeChild(this._containerStylesheet),this._containerStylesheet=null),this._applyContainerStyles())}set scrollToIndex(e){this._scrollToIndex=e,this._scheduleUpdateView()}async _render(){if(!this._lazyLoadDefaultLayout||this._layout){for(this._childrenRO.disconnect(),this._layout.totalItems=this.totalItems,this._needsUpdateView&&(this._needsUpdateView=!1,this._updateView()),null!==this._scrollToIndex&&(this._layout.scrollToIndex(this._scrollToIndex.index,this._scrollToIndex.position),this._scrollToIndex=null),this._layout.reflowIfNeeded();this._pendingRender&&(this._pendingRender=!1),this._sizeContainer(this._scrollSize),this._scrollErr&&(this._correctScrollError(this._scrollErr),this._scrollErr=null),await super._render(),this._layout.reflowIfNeeded(),this._pendingRender;);this._skipNextChildrenSizeChanged=!0,this._kids.forEach(e=>this._childrenRO.observe(e))}else{this._lazyLoadDefaultLayout=!1;const{Layout1d:e}=await Promise.resolve().then(i.bind(null,577));this.layout=new e({})}}_didRender(){this._childrenPos&&(this._positionChildren(this._childrenPos),this._childrenPos=null)}handleEvent(e){switch(e.type){case"scroll":this._scrollTarget&&e.target!==this._scrollTarget||this._scheduleUpdateView();break;case"scrollsizechange":this._scrollSize=e.detail,this._scheduleRender();break;case"scrollerrorchange":this._scrollErr=e.detail,this._scheduleRender();break;case"itempositionchange":this._childrenPos=e.detail,this._scheduleRender();break;case"rangechange":this._adjustRange(e.detail);break;default:console.warn("event not handled",e)}}async _initResizeObservers(){if(null===this._containerRO){const e=await w();this._containerRO=new e(e=>this._containerSizeChanged(e[0].contentRect)),this._childrenRO=new e(()=>this._childrenSizeChanged())}}_applyContainerStyles(){if(this._useShadowDOM){if(null===this._containerStylesheet){(this._containerStylesheet=document.createElement("style")).textContent=D(":host","::slotted(*)")}const e=this._containerElement.shadowRoot||this._containerElement.attachShadow({mode:"open"}),t=e.querySelector("slot:not([name])");e.appendChild(this._containerStylesheet),t||e.appendChild(document.createElement("slot"))}else k||((k=document.createElement("style")).textContent=D(`.${x}`,`.${x} > *`),document.head.appendChild(k)),this._containerElement&&this._containerElement.classList.add(x)}_createContainerSizer(){const e=document.createElement("div");return Object.assign(e.style,{position:"absolute",margin:"-2px 0 0 0",padding:0,visibility:"hidden",fontSize:"2px"}),e.innerHTML="&nbsp;",e}get _kids(){return this._ordered}_scheduleUpdateView(){this._needsUpdateView=!0,this._scheduleRender()}_updateView(){let e,t,i,n;if(this._scrollTarget===this._containerElement)e=this._containerSize.width,t=this._containerSize.height,n=this._containerElement.scrollLeft,i=this._containerElement.scrollTop;else{const s=this._containerElement.getBoundingClientRect(),a=this._scrollTarget?this._scrollTarget.getBoundingClientRect():{top:s.top+scrollY,left:s.left+scrollX,width:innerWidth,height:innerHeight},r=a.width,o=a.height,l=Math.max(0,Math.min(r,s.left-a.left)),d=Math.max(0,Math.min(o,s.top-a.top));e=("vertical"===this._layout.direction?Math.max(0,Math.min(r,s.right-a.left)):r)-l,t=("vertical"===this._layout.direction?o:Math.max(0,Math.min(o,s.bottom-a.top)))-d,n=Math.max(0,-(s.left-a.left)),i=Math.max(0,-(s.top-a.top))}this._layout.viewportSize={width:e,height:t},this._layout.viewportScroll={top:i,left:n}}_sizeContainer(e){if(this._scrollTarget===this._containerElement){const t=e&&e.width?e.width-1:0,i=e&&e.height?e.height-1:0;this._sizer.style.transform=`translate(${t}px, ${i}px)`}else{const t=this._containerElement.style;t.minWidth=e&&e.width?e.width+"px":null,t.minHeight=e&&e.height?e.height+"px":null}}_positionChildren(e){const t=this._kids;Object.keys(e).forEach(i=>{const n=i-this._first,s=t[n];if(s){const{top:t,left:n}=e[i];s.style.position="absolute",s.style.transform=`translate(${n}px, ${t}px)`}})}_adjustRange(e){this.num=e.num,this.first=e.first;const t=this._firstVisible!==e.firstVisible||this._lastVisible!==e.lastVisible;this._firstVisible=e.firstVisible,this._lastVisible=e.lastVisible,this._incremental=!e.stable,e.remeasure?this.requestRemeasure():(e.stable||t)&&this._notifyRange()}_shouldRender(){if(!super._shouldRender()||!this._containerElement||!this._layout&&!this._lazyLoadDefaultLayout)return!1;if(null===this._containerSize){const{width:e,height:t}=this._containerElement.getBoundingClientRect();this._containerSize={width:e,height:t}}return this._containerSize.width>0||this._containerSize.height>0}_correctScrollError(e){this._scrollTarget?(this._scrollTarget.scrollTop-=e.top,this._scrollTarget.scrollLeft-=e.left):window.scroll(window.scrollX-e.left,window.scrollY-e.top)}_notifyRange(){const{first:e,num:t}=this,i=e+t-1;this._container.dispatchEvent(new E("rangechange",{first:e,last:i,firstVisible:this._firstVisible,lastVisible:this._lastVisible}))}_containerSizeChanged(e){const{width:t,height:i}=e;this._containerSize={width:t,height:i},this._scheduleUpdateView()}_childrenSizeChanged(){this._skipNextChildrenSizeChanged?this._skipNextChildrenSizeChanged=!1:this.requestRemeasure()}}class C extends(v(S)){}const I=new WeakMap,T=Object(m.f)(e=>async t=>{let i=I.get(t);if(!i){t.startNode.isConnected||await Promise.resolve();const{renderItem:n,layout:s,scrollTarget:a,useShadowDOM:r}=e;i=new C({part:t,renderItem:n,layout:s,scrollTarget:a,useShadowDOM:r}),I.set(t,i)}Object.assign(i,{items:e.items,totalItems:void 0===e.totalItems?null:e.totalItems,scrollToIndex:void 0===e.scrollToIndex?null:e.scrollToIndex})});i(577),i(589);var z=i(17);let O=class extends u.a{constructor(){super(),this.renderRoot=this}get renderItem(){return this._renderItem}set renderItem(e){e!==this.renderItem&&(this._renderItem=e,this.requestUpdate())}async scrollToIndex(e,t="start"){this._scrollToIndex={index:e,position:t},this.requestUpdate(),await this.updateComplete,this._scrollToIndex=null}render(){return u.f`${T({items:this.items,renderItem:this._renderItem,scrollTarget:this.scrollTarget,scrollToIndex:this._scrollToIndex,useShadowDOM:!0})}`}};function M(e){var t,i=j(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function A(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function P(e){return e.decorators&&e.decorators.length}function $(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function F(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function j(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var n=i.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}z.c([Object(u.g)()],O.prototype,"_renderItem",void 0),z.c([Object(u.g)()],O.prototype,"items",void 0),z.c([Object(u.g)()],O.prototype,"scrollTarget",void 0),O=z.c([Object(u.d)("lit-virtualizer")],O);let L=function(e,t,i,n){var s=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(n){t.forEach(function(t){var s=t.placement;if(t.kind===n&&("static"===s||"prototype"===s)){var a="static"===s?e:i;this.defineClassElement(a,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var n=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],n=[],s={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,s)},this),e.forEach(function(e){if(!P(e))return i.push(e);var t=this.decorateElement(e,s);i.push(t.element),i.push.apply(i,t.extras),n.push.apply(n,t.finishers)},this),!t)return{elements:i,finishers:n};var a=this.decorateConstructor(i,t);return n.push.apply(n,a.finishers),a.finishers=n,a},addElementPlacement:function(e,t,i){var n=t[e.placement];if(!i&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var i=[],n=[],s=e.decorators,a=s.length-1;a>=0;a--){var r=t[e.placement];r.splice(r.indexOf(e.key),1);var o=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,s[a])(o)||o);e=l.element,this.addElementPlacement(e,t),l.finisher&&n.push(l.finisher);var d=l.extras;if(d){for(var h=0;h<d.length;h++)this.addElementPlacement(d[h],t);i.push.apply(i,d)}}return{element:e,finishers:n,extras:i}},decorateConstructor:function(e,t){for(var i=[],n=t.length-1;n>=0;n--){var s=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[n])(s)||s);if(void 0!==a.finisher&&i.push(a.finisher),void 0!==a.elements){e=a.elements;for(var r=0;r<e.length-1;r++)for(var o=r+1;o<e.length;o++)if(e[r].key===e[o].key&&e[r].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[r].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=j(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var s=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:i,placement:n,descriptor:Object.assign({},s)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(s,"get","The property descriptor of a field descriptor"),this.disallowProperty(s,"set","The property descriptor of a field descriptor"),this.disallowProperty(s,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=F(e,"finisher"),n=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:n}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=F(e,"finisher"),n=this.toElementDescriptors(e.elements);return{elements:n,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var n=(0,t[i])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(n)for(var a=0;a<n.length;a++)s=n[a](s);var r=t(function(e){s.initializeInstanceElements(e,o.elements)},i),o=s.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},n=0;n<e.length;n++){var s,a=e[n];if("method"===a.kind&&(s=t.find(i)))if($(a.descriptor)||$(s.descriptor)){if(P(a)||P(s))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");s.descriptor=a.descriptor}else{if(P(a)){if(P(s))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");s.decorators=a.decorators}A(a,s)}else t.push(a)}return t}(r.d.map(M)),e);return s.initializeClassElements(r.F,o.elements),s.runClassFinishers(r.F,o.finishers)}(null,function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(u.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(u.g)()],key:"entries",value:()=>[]},{kind:"field",decorators:[Object(u.g)({attribute:"rtl",type:Boolean,reflect:!0})],key:"_rtl",value:()=>!1},{kind:"method",key:"shouldUpdate",value:function(e){const t=e.get("hass"),i=void 0===t||t.language!==this.hass.language;return e.has("entries")||i}},{kind:"method",key:"updated",value:function(e){this._rtl=Object(c.a)(this.hass)}},{kind:"method",key:"render",value:function(){var e;return(null===(e=this.entries)||void 0===e?void 0:e.length)?u.f`
      <lit-virtualizer
        .items=${this.entries}
        .renderItem=${(e,t)=>this._renderLogbookItem(e,t)}
        style="height: 100%;"
      ></lit-virtualizer>
    `:u.f`
        ${this.hass.localize("ui.panel.logbook.entries_not_found")}
      `}},{kind:"method",key:"_renderLogbookItem",value:function(e,t){const i=this.entries[t-1],n=e.entity_id?this.hass.states[e.entity_id]:void 0;return u.f`
      <div>
        ${0===t||(null==e?void 0:e.when)&&(null==i?void 0:i.when)&&new Date(e.when).toDateString()!==new Date(i.when).toDateString()?u.f`
              <h4 class="date">
                ${Object(l.a)(new Date(e.when),this.hass.language)}
              </h4>
            `:u.f``}

        <div class="entry">
          <div class="time">
            ${Object(o.b)(new Date(e.when),this.hass.language)}
          </div>
          <ha-icon
            .icon=${n?Object(h.a)(n):Object(d.a)(e.domain)}
          ></ha-icon>
          <div class="message">
            ${e.entity_id?u.f`
                  <a
                    href="#"
                    @click=${this._entityClicked}
                    .entityId=${e.entity_id}
                    class="name"
                  >
                    ${e.name}
                  </a>
                `:u.f`
                  <span class="name">${e.name}</span>
                `}
            <span>${e.message}</span>
          </div>
        </div>
      </div>
    `}},{kind:"method",key:"_entityClicked",value:function(e){e.preventDefault(),Object(p.a)(this,"hass-more-info",{entityId:e.target.entityId})}},{kind:"get",static:!0,key:"styles",value:function(){return u.c`
      :host {
        display: block;
        height: 100%;
      }

      :host([rtl]) {
        direction: ltr;
      }

      .entry {
        display: flex;
        line-height: 2em;
      }

      .time {
        width: 65px;
        flex-shrink: 0;
        font-size: 0.8em;
        color: var(--secondary-text-color);
      }

      :host([rtl]) .date {
        direction: rtl;
      }

      ha-icon {
        margin: 0 8px 0 16px;
        flex-shrink: 0;
        color: var(--primary-text-color);
      }

      .message {
        color: var(--primary-text-color);
      }

      a {
        color: var(--primary-color);
      }
    `}}]}},u.a);customElements.define("ha-logbook",L);var R=i(179);customElements.define("ha-panel-logbook",class extends(Object(R.a)(s.a)){static get template(){return n.a`
      <style include="ha-style">
        .content {
          padding: 0 16px 0 16px;
        }

        ha-logbook {
          height: calc(100vh - 136px);
        }

        :host([narrow]) ha-logbook {
          height: calc(100vh - 198px);
        }

        paper-spinner {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
        }

        .wrap {
          margin-bottom: 24px;
        }

        .filters {
          display: flex;
          align-items: center;
        }

        :host([narrow]) .filters {
          flex-wrap: wrap;
        }

        vaadin-date-picker {
          max-width: 200px;
          margin-right: 16px;
        }

        :host([rtl]) vaadin-date-picker {
          margin-right: 0;
          margin-left: 16px;
        }

        paper-dropdown-menu {
          max-width: 100px;
          margin-right: 16px;
          --paper-input-container-label-floating: {
            padding-bottom: 10px;
          }
        }

        :host([rtl]) paper-dropdown-menu {
          text-align: right;
          margin-right: 0;
          margin-left: 16px;
        }

        paper-item {
          cursor: pointer;
          white-space: nowrap;
        }

        ha-entity-picker {
          display: inline-block;
          flex-grow: 1;
          max-width: 400px;
        }

        :host([narrow]) ha-entity-picker {
          max-width: none;
          width: 100%;
        }

        [hidden] {
          display: none !important;
        }
      </style>

      <ha-logbook-data
        hass="[[hass]]"
        is-loading="{{isLoading}}"
        entries="{{entries}}"
        filter-date="[[_computeFilterDate(_currentDate)]]"
        filter-period="[[_computeFilterDays(_periodIndex)]]"
        filter-entity="[[entityId]]"
      ></ha-logbook-data>

      <app-header-layout has-scrolling-region>
        <app-header slot="header" fixed>
          <app-toolbar>
            <ha-menu-button
              hass="[[hass]]"
              narrow="[[narrow]]"
            ></ha-menu-button>
            <div main-title>[[localize('panel.logbook')]]</div>
            <paper-icon-button
              icon="hass:refresh"
              on-click="refreshLogbook"
              hidden$="[[isLoading]]"
            ></paper-icon-button>
          </app-toolbar>
        </app-header>

        <div class="content">
          <paper-spinner
            active="[[isLoading]]"
            hidden$="[[!isLoading]]"
            alt="[[localize('ui.common.loading')]]"
          ></paper-spinner>

          <div class="filters">
            <vaadin-date-picker
              id="picker"
              value="{{_currentDate}}"
              label="[[localize('ui.panel.logbook.showing_entries')]]"
              disabled="[[isLoading]]"
              required
            ></vaadin-date-picker>

            <paper-dropdown-menu
              label-float
              label="[[localize('ui.panel.logbook.period')]]"
              disabled="[[isLoading]]"
            >
              <paper-listbox
                slot="dropdown-content"
                selected="{{_periodIndex}}"
              >
                <paper-item
                  >[[localize('ui.duration.day', 'count', 1)]]</paper-item
                >
                <paper-item
                  >[[localize('ui.duration.day', 'count', 3)]]</paper-item
                >
                <paper-item
                  >[[localize('ui.duration.week', 'count', 1)]]</paper-item
                >
              </paper-listbox>
            </paper-dropdown-menu>

            <ha-entity-picker
              hass="[[hass]]"
              value="{{_entityId}}"
              label="[[localize('ui.components.entity.entity-picker.entity')]]"
              disabled="[[isLoading]]"
              on-change="_entityPicked"
            ></ha-entity-picker>
          </div>

          <ha-logbook
            hass="[[hass]]"
            entries="[[entries]]"
            hidden$="[[isLoading]]"
          ></ha-logbook>
        </div>
      </app-header-layout>
    `}static get properties(){return{hass:Object,narrow:{type:Boolean,reflectToAttribute:!0},_currentDate:{type:String,value:function(){const e=new Date;return new Date(Date.UTC(e.getFullYear(),e.getMonth(),e.getDate())).toISOString().split("T")[0]}},_periodIndex:{type:Number,value:0},_entityId:{type:String,value:""},entityId:{type:String,value:"",readOnly:!0},isLoading:{type:Boolean},entries:{type:Array},datePicker:{type:Object},rtl:{type:Boolean,reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}connectedCallback(){super.connectedCallback(),this.$.picker.set("i18n.parseDate",null),this.$.picker.set("i18n.formatDate",e=>Object(l.a)(new Date(e.year,e.month,e.day),this.hass.language))}_computeFilterDate(e){if(e){var t=e.split("-");return t[1]=parseInt(t[1])-1,new Date(t[0],t[1],t[2]).toISOString()}}_computeFilterDays(e){switch(e){case 1:return 3;case 2:return 7;default:return 1}}_entityPicked(e){this._setEntityId(e.target.value)}refreshLogbook(){this.shadowRoot.querySelector("ha-logbook-data").refreshLogbook()}_computeRTL(e){return Object(c.a)(e)}})},94:function(e,t,i){"use strict";i.d(t,"a",function(){return a});i(3);var n=i(5),s=i(4);const a=Object(n.a)({_template:s.a`
    <style>
      :host {
        display: inline-block;
        position: fixed;
        clip: rect(0px,0px,0px,0px);
      }
    </style>
    <div aria-live$="[[mode]]">[[_text]]</div>
`,is:"iron-a11y-announcer",properties:{mode:{type:String,value:"polite"},_text:{type:String,value:""}},created:function(){a.instance||(a.instance=this),document.body.addEventListener("iron-announce",this._onIronAnnounce.bind(this))},announce:function(e){this._text="",this.async(function(){this._text=e},100)},_onIronAnnounce:function(e){e.detail&&e.detail.text&&this.announce(e.detail.text)}});a.instance=null,a.requestAvailability=function(){a.instance||(a.instance=document.createElement("iron-a11y-announcer")),document.body.appendChild(a.instance)}}}]);
//# sourceMappingURL=chunk.74446008f98c4637e61c.js.map