/*! For license information please see chunk.343250d34984683f285d.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[122,7],{120:function(e,t,i){"use strict";i.d(t,"a",function(){return r});i(3);var s=i(60),n=i(38);const r=[s.a,n.a,{hostAttributes:{role:"option",tabindex:"0"}}]},135:function(e,t,i){"use strict";i(51),i(72),i(47),i(52);const s=document.createElement("template");s.setAttribute("style","display: none;"),s.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(s.content)},187:function(e,t,i){"use strict";i.d(t,"a",function(){return n});var s=i(205);const n=e=>void 0===e.attributes.friendly_name?Object(s.a)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||""},189:function(e,t,i){"use strict";i.d(t,"a",function(){return r});i(119);const s=customElements.get("iron-icon");let n=!1;class r extends s{constructor(...e){var t,i,s;super(...e),s=void 0,(i="_iconsetName")in(t=this)?Object.defineProperty(t,i,{value:s,enumerable:!0,configurable:!0,writable:!0}):t[i]=s}listen(e,t,s){super.listen(e,t,s),n||"mdi"!==this._iconsetName||(n=!0,i.e(89).then(i.bind(null,244)))}}customElements.define("ha-icon",r)},191:function(e,t,i){"use strict";var s=i(8);t.a=Object(s.a)(e=>(class extends e{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(e){return e}}))},192:function(e,t,i){"use strict";i.d(t,"a",function(){return r});var s=i(132);const n={alert:"hass:alert",alexa:"hass:amazon-alexa",automation:"hass:robot",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:settings",conversation:"hass:text-to-speech",counter:"hass:counter",device_tracker:"hass:account",fan:"hass:fan",google_assistant:"hass:google-assistant",group:"hass:google-circles-communities",history_graph:"hass:chart-line",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:toggle-switch-outline",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",persistent_notification:"hass:bell",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:palette",script:"hass:script-text",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weather:"hass:weather-cloudy",weblink:"hass:open-in-new",zone:"hass:map-marker-radius"},r=(e,t)=>{if(e in n)return n[e];switch(e){case"alarm_control_panel":switch(t){case"armed_home":return"hass:bell-plus";case"armed_night":return"hass:bell-sleep";case"disarmed":return"hass:bell-outline";case"triggered":return"hass:bell-ring";default:return"hass:bell"}case"binary_sensor":return t&&"off"===t?"hass:radiobox-blank":"hass:checkbox-marked-circle";case"cover":return"closed"===t?"hass:window-closed":"hass:window-open";case"lock":return t&&"unlocked"===t?"hass:lock-open":"hass:lock";case"media_player":return t&&"off"!==t&&"idle"!==t?"hass:cast-connected":"hass:cast";case"zwave":switch(t){case"dead":return"hass:emoticon-dead";case"sleeping":return"hass:sleep";case"initializing":return"hass:timer-sand";default:return"hass:z-wave"}default:return console.warn("Unable to find icon for domain "+e+" ("+t+")"),s.a}}},193:function(e,t,i){"use strict";i(3),i(51),i(47),i(52);var s=i(5),n=i(4);Object(s.a)({_template:n.a`
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
`,is:"paper-item-body"})},195:function(e,t,i){"use strict";i.d(t,"a",function(){return n});var s=i(130);const n=e=>Object(s.a)(e.entity_id)},199:function(e,t,i){"use strict";i.d(t,"a",function(){return n});var s=i(9);const n=Object(s.f)(e=>t=>{if(void 0===e&&t instanceof s.a){if(e!==t.value){const e=t.committer.name;t.committer.element.removeAttribute(e)}}else t.setValue(e)})},200:function(e,t,i){"use strict";i(118),i(76),i(158),i(193),i(219);var s=i(133),n=(i(203),i(187)),r=i(0),a=i(12),o=i(130);function l(e){var t,i=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var s={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(s.decorators=e.decorators),"field"===e.kind&&(s.initializer=e.value),s}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function d(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var s=i.call(e,t||"default");if("object"!=typeof s)return s;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t,i){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var s=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=f(e)););return e}(e,t);if(s){var n=Object.getOwnPropertyDescriptor(s,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function f(e){return(f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let _=function(e,t,i,s){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(s){t.forEach(function(t){var n=t.placement;if(t.kind===s&&("static"===n||"prototype"===n)){var r="static"===n?e:i;this.defineClassElement(r,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var s=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===s?void 0:s.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],s=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!d(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),s.push.apply(s,t.finishers)},this),!t)return{elements:i,finishers:s};var r=this.decorateConstructor(i,t);return s.push.apply(s,r.finishers),r.finishers=s,r},addElementPlacement:function(e,t,i){var s=t[e.placement];if(!i&&-1!==s.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");s.push(e.key)},decorateElement:function(e,t){for(var i=[],s=[],n=e.decorators,r=n.length-1;r>=0;r--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var o=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[r])(o)||o);e=l.element,this.addElementPlacement(e,t),l.finisher&&s.push(l.finisher);var h=l.extras;if(h){for(var d=0;d<h.length;d++)this.addElementPlacement(h[d],t);i.push.apply(i,h)}}return{element:e,finishers:s,extras:i}},decorateConstructor:function(e,t){for(var i=[],s=t.length-1;s>=0;s--){var n=this.fromClassDescriptor(e),r=this.toClassDescriptor((0,t[s])(n)||n);if(void 0!==r.finisher&&i.push(r.finisher),void 0!==r.elements){e=r.elements;for(var a=0;a<e.length-1;a++)for(var o=a+1;o<e.length;o++)if(e[a].key===e[o].key&&e[a].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=p(e.key),s=String(e.placement);if("static"!==s&&"prototype"!==s&&"own"!==s)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+s+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var r={kind:t,key:i,placement:s,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),r.initializer=e.initializer),r},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=u(e,"finisher"),s=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:s}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=u(e,"finisher"),s=this.toElementDescriptors(e.elements);return{elements:s,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var s=(0,t[i])(e);if(void 0!==s){if("function"!=typeof s)throw new TypeError("Finishers must return a constructor.");e=s}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(s)for(var r=0;r<s.length;r++)n=s[r](n);var a=t(function(e){n.initializeInstanceElements(e,o.elements)},i),o=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===r.key&&e.placement===r.placement},s=0;s<e.length;s++){var n,r=e[s];if("method"===r.kind&&(n=t.find(i)))if(c(r.descriptor)||c(n.descriptor)){if(d(r)||d(n))throw new ReferenceError("Duplicated methods ("+r.key+") can't be decorated.");n.descriptor=r.descriptor}else{if(d(r)){if(d(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+r.key+").");n.decorators=r.decorators}h(r,n)}else t.push(r)}return t}(a.d.map(l)),e);return n.initializeClassElements(a.F,o.elements),n.runClassFinishers(a.F,o.finishers)}(null,function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[Object(r.g)({type:Boolean})],key:"autofocus",value:void 0},{kind:"field",decorators:[Object(r.g)({type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[Object(r.g)({type:Boolean,attribute:"allow-custom-entity"})],key:"allowCustomEntity",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"label",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"value",value:void 0},{kind:"field",decorators:[Object(r.g)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[Object(r.g)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[Object(r.g)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"entityFilter",value:void 0},{kind:"field",decorators:[Object(r.g)({type:Boolean})],key:"_opened",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_hass",value:void 0},{kind:"field",key:"_getStates",value(){return Object(s.a)((e,t,i,s,n)=>{let r=[];if(!e)return[];let a=Object.keys(e.states);return t&&(a=a.filter(e=>t.includes(Object(o.a)(e)))),i&&(a=a.filter(e=>!i.includes(Object(o.a)(e)))),r=a.sort().map(t=>e.states[t]),n&&(r=r.filter(e=>e.entity_id===this.value||e.attributes.device_class&&n.includes(e.attributes.device_class))),s&&(r=r.filter(e=>e.entity_id===this.value||s(e))),r})}},{kind:"method",key:"updated",value:function(e){m(f(i.prototype),"updated",this).call(this,e),e.has("hass")&&!this._opened&&(this._hass=this.hass)}},{kind:"method",key:"render",value:function(){const e=this._getStates(this._hass,this.includeDomains,this.excludeDomains,this.entityFilter,this.includeDeviceClasses);return r.f`
      <vaadin-combo-box-light
        item-value-path="entity_id"
        item-label-path="entity_id"
        .items=${e}
        .value=${this._value}
        .allowCustomValue=${this.allowCustomEntity}
        .renderer=${(e,t,i)=>{e.firstElementChild||(e.innerHTML='\n      <style>\n        paper-icon-item {\n          margin: -10px;\n          padding: 0;\n        }\n      </style>\n      <paper-icon-item>\n        <state-badge state-obj="[[item]]" slot="item-icon"></state-badge>\n        <paper-item-body two-line="">\n          <div class=\'name\'>[[_computeStateName(item)]]</div>\n          <div secondary>[[item.entity_id]]</div>\n        </paper-item-body>\n      </paper-icon-item>\n    '),e.querySelector("state-badge").stateObj=i.item,e.querySelector(".name").textContent=Object(n.a)(i.item),e.querySelector("[secondary]").textContent=i.item.entity_id}}
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
          ${this.value?r.f`
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
          ${e.length>0?r.f`
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
    `}},{kind:"method",key:"_clearValue",value:function(e){e.stopPropagation(),this._setValue("")}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_valueChanged",value:function(e){const t=e.detail.value;t!==this._value&&this._setValue(t)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout(()=>{Object(a.a)(this,"value-changed",{value:e}),Object(a.a)(this,"change")},0)}},{kind:"get",static:!0,key:"styles",value:function(){return r.c`
      paper-input > paper-icon-button {
        width: 24px;
        height: 24px;
        padding: 2px;
        color: var(--secondary-text-color);
      }
      [hidden] {
        display: none;
      }
    `}}]}},r.a);customElements.define("ha-entity-picker",_)},202:function(e,t,i){"use strict";i(3),i(72),i(162);var s=i(5),n=i(4),r=i(141);const a=n.a`
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
`;a.setAttribute("strip-whitespace",""),Object(s.a)({_template:a,is:"paper-spinner",behaviors:[r.a]})},203:function(e,t,i){"use strict";var s=i(0),n=(i(189),i(195)),r=i(206),a=i(232),o=i(199),l=i(233);function h(e){var t,i=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var s={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(s.decorators=e.decorators),"field"===e.kind&&(s.initializer=e.value),s}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var s=i.call(e,t||"default");if("object"!=typeof s)return s;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}let f=function(e,t,i,s){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(s){t.forEach(function(t){var n=t.placement;if(t.kind===s&&("static"===n||"prototype"===n)){var r="static"===n?e:i;this.defineClassElement(r,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var s=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===s?void 0:s.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],s=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!c(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),s.push.apply(s,t.finishers)},this),!t)return{elements:i,finishers:s};var r=this.decorateConstructor(i,t);return s.push.apply(s,r.finishers),r.finishers=s,r},addElementPlacement:function(e,t,i){var s=t[e.placement];if(!i&&-1!==s.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");s.push(e.key)},decorateElement:function(e,t){for(var i=[],s=[],n=e.decorators,r=n.length-1;r>=0;r--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var o=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[r])(o)||o);e=l.element,this.addElementPlacement(e,t),l.finisher&&s.push(l.finisher);var h=l.extras;if(h){for(var d=0;d<h.length;d++)this.addElementPlacement(h[d],t);i.push.apply(i,h)}}return{element:e,finishers:s,extras:i}},decorateConstructor:function(e,t){for(var i=[],s=t.length-1;s>=0;s--){var n=this.fromClassDescriptor(e),r=this.toClassDescriptor((0,t[s])(n)||n);if(void 0!==r.finisher&&i.push(r.finisher),void 0!==r.elements){e=r.elements;for(var a=0;a<e.length-1;a++)for(var o=a+1;o<e.length;o++)if(e[a].key===e[o].key&&e[a].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=m(e.key),s=String(e.placement);if("static"!==s&&"prototype"!==s&&"own"!==s)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+s+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var r={kind:t,key:i,placement:s,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),r.initializer=e.initializer),r},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=p(e,"finisher"),s=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:s}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher"),s=this.toElementDescriptors(e.elements);return{elements:s,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var s=(0,t[i])(e);if(void 0!==s){if("function"!=typeof s)throw new TypeError("Finishers must return a constructor.");e=s}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(s)for(var r=0;r<s.length;r++)n=s[r](n);var a=t(function(e){n.initializeInstanceElements(e,o.elements)},i),o=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===r.key&&e.placement===r.placement},s=0;s<e.length;s++){var n,r=e[s];if("method"===r.kind&&(n=t.find(i)))if(u(r.descriptor)||u(n.descriptor)){if(c(r)||c(n))throw new ReferenceError("Duplicated methods ("+r.key+") can't be decorated.");n.descriptor=r.descriptor}else{if(c(r)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+r.key+").");n.decorators=r.decorators}d(r,n)}else t.push(r)}return t}(a.d.map(h)),e);return n.initializeClassElements(a.F,o.elements),n.runClassFinishers(a.F,o.finishers)}(null,function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[Object(s.g)()],key:"stateObj",value:void 0},{kind:"field",decorators:[Object(s.g)()],key:"overrideIcon",value:void 0},{kind:"field",decorators:[Object(s.g)()],key:"overrideImage",value:void 0},{kind:"field",decorators:[Object(s.g)({type:Boolean})],key:"stateColor",value:void 0},{kind:"field",decorators:[Object(s.h)("ha-icon")],key:"_icon",value:void 0},{kind:"method",key:"render",value:function(){const e=this.stateObj;if(!e)return s.f``;const t=Object(n.a)(e);return s.f`
      <ha-icon
        id="icon"
        data-domain=${Object(o.a)(this.stateColor||"light"===t&&!1!==this.stateColor?t:void 0)}
        data-state=${Object(a.a)(e)}
        .icon=${this.overrideIcon||Object(r.a)(e)}
      ></ha-icon>
    `}},{kind:"method",key:"updated",value:function(e){if(!e.has("stateObj")||!this.stateObj)return;const t=this.stateObj,i={color:"",filter:""},s={backgroundImage:""};if(t)if(t.attributes.entity_picture&&!this.overrideIcon||this.overrideImage){let e=this.overrideImage||t.attributes.entity_picture;this.hass&&(e=this.hass.hassUrl(e)),s.backgroundImage=`url(${e})`,i.display="none"}else{if(t.attributes.hs_color&&!1!==this.stateColor){const e=t.attributes.hs_color[0],s=t.attributes.hs_color[1];s>10&&(i.color=`hsl(${e}, 100%, ${100-s/2}%)`)}if(t.attributes.brightness&&!1!==this.stateColor){const e=t.attributes.brightness;if("number"!=typeof e){const i=`Type error: state-badge expected number, but type of ${t.entity_id}.attributes.brightness is ${typeof e} (${e})`;console.warn(i)}i.filter=`brightness(${(e+245)/5}%)`}}Object.assign(this._icon.style,i),Object.assign(this.style,s)}},{kind:"get",static:!0,key:"styles",value:function(){return s.c`
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
    `}}]}},s.a);customElements.define("state-badge",f)},205:function(e,t,i){"use strict";i.d(t,"a",function(){return s});const s=e=>e.substr(e.indexOf(".")+1)},206:function(e,t,i){"use strict";var s=i(132);var n=i(130),r=i(192);const a={humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge",power:"hass:flash",signal_strength:"hass:wifi"};i.d(t,"a",function(){return l});const o={binary_sensor:e=>{const t=e.state&&"off"===e.state;switch(e.attributes.device_class){case"battery":return t?"hass:battery":"hass:battery-outline";case"cold":return t?"hass:thermometer":"hass:snowflake";case"connectivity":return t?"hass:server-network-off":"hass:server-network";case"door":return t?"hass:door-closed":"hass:door-open";case"garage_door":return t?"hass:garage":"hass:garage-open";case"gas":case"power":case"problem":case"safety":case"smoke":return t?"hass:shield-check":"hass:alert";case"heat":return t?"hass:thermometer":"hass:fire";case"light":return t?"hass:brightness-5":"hass:brightness-7";case"lock":return t?"hass:lock":"hass:lock-open";case"moisture":return t?"hass:water-off":"hass:water";case"motion":return t?"hass:walk":"hass:run";case"occupancy":return t?"hass:home-outline":"hass:home";case"opening":return t?"hass:square":"hass:square-outline";case"plug":return t?"hass:power-plug-off":"hass:power-plug";case"presence":return t?"hass:home-outline":"hass:home";case"sound":return t?"hass:music-note-off":"hass:music-note";case"vibration":return t?"hass:crop-portrait":"hass:vibrate";case"window":return t?"hass:window-closed":"hass:window-open";default:return t?"hass:radiobox-blank":"hass:checkbox-marked-circle"}},cover:e=>{const t="closed"!==e.state;switch(e.attributes.device_class){case"garage":return t?"hass:garage-open":"hass:garage";case"door":return t?"hass:door-open":"hass:door-closed";case"shutter":return t?"hass:window-shutter-open":"hass:window-shutter";case"blind":return t?"hass:blinds-open":"hass:blinds";case"window":return t?"hass:window-open":"hass:window-closed";default:return Object(r.a)("cover",e.state)}},sensor:e=>{const t=e.attributes.device_class;if(t&&t in a)return a[t];if("battery"===t){const t=Number(e.state);if(isNaN(t))return"hass:battery-unknown";const i=10*Math.round(t/10);return i>=100?"hass:battery":i<=0?"hass:battery-alert":`hass:battery-${i}`}const i=e.attributes.unit_of_measurement;return i===s.j||i===s.k?"hass:thermometer":Object(r.a)("sensor")},input_datetime:e=>e.attributes.has_date?e.attributes.has_time?Object(r.a)("input_datetime"):"hass:calendar":"hass:clock"},l=e=>{if(!e)return s.a;if(e.attributes.icon)return e.attributes.icon;const t=Object(n.a)(e.entity_id);return t in o?o[t](e):Object(r.a)(t,e.state)}},216:function(e,t,i){"use strict";i.d(t,"a",function(){return n});i(3);var s=i(1);const n={properties:{scrollTarget:{type:HTMLElement,value:function(){return this._defaultScrollTarget}}},observers:["_scrollTargetChanged(scrollTarget, isAttached)"],_shouldHaveListener:!0,_scrollTargetChanged:function(e,t){if(this._oldScrollTarget&&(this._toggleScrollListener(!1,this._oldScrollTarget),this._oldScrollTarget=null),t)if("document"===e)this.scrollTarget=this._doc;else if("string"==typeof e){var i=this.domHost;this.scrollTarget=i&&i.$?i.$[e]:Object(s.a)(this.ownerDocument).querySelector("#"+e)}else this._isValidScrollTarget()&&(this._oldScrollTarget=e,this._toggleScrollListener(this._shouldHaveListener,e))},_scrollHandler:function(){},get _defaultScrollTarget(){return this._doc},get _doc(){return this.ownerDocument.documentElement},get _scrollTop(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageYOffset:this.scrollTarget.scrollTop:0},get _scrollLeft(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageXOffset:this.scrollTarget.scrollLeft:0},set _scrollTop(e){this.scrollTarget===this._doc?window.scrollTo(window.pageXOffset,e):this._isValidScrollTarget()&&(this.scrollTarget.scrollTop=e)},set _scrollLeft(e){this.scrollTarget===this._doc?window.scrollTo(e,window.pageYOffset):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=e)},scroll:function(e,t){var i;"object"==typeof e?(i=e.left,t=e.top):i=e,i=i||0,t=t||0,this.scrollTarget===this._doc?window.scrollTo(i,t):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=i,this.scrollTarget.scrollTop=t)},get _scrollTargetWidth(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerWidth:this.scrollTarget.offsetWidth:0},get _scrollTargetHeight(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerHeight:this.scrollTarget.offsetHeight:0},_isValidScrollTarget:function(){return this.scrollTarget instanceof HTMLElement},_toggleScrollListener:function(e,t){var i=t===this._doc?window:t;e?this._boundScrollHandler||(this._boundScrollHandler=this._scrollHandler.bind(this),i.addEventListener("scroll",this._boundScrollHandler)):this._boundScrollHandler&&(i.removeEventListener("scroll",this._boundScrollHandler),this._boundScrollHandler=null)},toggleScrollListener:function(e){this._shouldHaveListener=e,this._toggleScrollListener(e,this.scrollTarget)}}},223:function(e,t,i){"use strict";i.d(t,"a",function(){return s}),i.d(t,"c",function(){return n}),i.d(t,"b",function(){return r});const s=function(){try{(new Date).toLocaleDateString("i")}catch(e){return"RangeError"===e.name}return!1}(),n=function(){try{(new Date).toLocaleTimeString("i")}catch(e){return"RangeError"===e.name}return!1}(),r=function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()},224:function(e,t,i){"use strict";var s={},n=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,r="[^\\s]+",a=/\[([^]*?)\]/gm,o=function(){};function l(e,t){for(var i=[],s=0,n=e.length;s<n;s++)i.push(e[s].substr(0,t));return i}function h(e){return function(t,i,s){var n=s[e].indexOf(i.charAt(0).toUpperCase()+i.substr(1).toLowerCase());~n&&(t.month=n)}}function d(e,t){for(e=String(e),t=t||2;e.length<t;)e="0"+e;return e}var c=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],u=["January","February","March","April","May","June","July","August","September","October","November","December"],p=l(u,3),m=l(c,3);s.i18n={dayNamesShort:m,dayNames:c,monthNamesShort:p,monthNames:u,amPm:["am","pm"],DoFn:function(e){return e+["th","st","nd","rd"][e%10>3?0:(e-e%10!=10)*e%10]}};var f={D:function(e){return e.getDate()},DD:function(e){return d(e.getDate())},Do:function(e,t){return t.DoFn(e.getDate())},d:function(e){return e.getDay()},dd:function(e){return d(e.getDay())},ddd:function(e,t){return t.dayNamesShort[e.getDay()]},dddd:function(e,t){return t.dayNames[e.getDay()]},M:function(e){return e.getMonth()+1},MM:function(e){return d(e.getMonth()+1)},MMM:function(e,t){return t.monthNamesShort[e.getMonth()]},MMMM:function(e,t){return t.monthNames[e.getMonth()]},YY:function(e){return d(String(e.getFullYear()),4).substr(2)},YYYY:function(e){return d(e.getFullYear(),4)},h:function(e){return e.getHours()%12||12},hh:function(e){return d(e.getHours()%12||12)},H:function(e){return e.getHours()},HH:function(e){return d(e.getHours())},m:function(e){return e.getMinutes()},mm:function(e){return d(e.getMinutes())},s:function(e){return e.getSeconds()},ss:function(e){return d(e.getSeconds())},S:function(e){return Math.round(e.getMilliseconds()/100)},SS:function(e){return d(Math.round(e.getMilliseconds()/10),2)},SSS:function(e){return d(e.getMilliseconds(),3)},a:function(e,t){return e.getHours()<12?t.amPm[0]:t.amPm[1]},A:function(e,t){return e.getHours()<12?t.amPm[0].toUpperCase():t.amPm[1].toUpperCase()},ZZ:function(e){var t=e.getTimezoneOffset();return(t>0?"-":"+")+d(100*Math.floor(Math.abs(t)/60)+Math.abs(t)%60,4)}},_={D:["\\d\\d?",function(e,t){e.day=t}],Do:["\\d\\d?"+r,function(e,t){e.day=parseInt(t,10)}],M:["\\d\\d?",function(e,t){e.month=t-1}],YY:["\\d\\d?",function(e,t){var i=+(""+(new Date).getFullYear()).substr(0,2);e.year=""+(t>68?i-1:i)+t}],h:["\\d\\d?",function(e,t){e.hour=t}],m:["\\d\\d?",function(e,t){e.minute=t}],s:["\\d\\d?",function(e,t){e.second=t}],YYYY:["\\d{4}",function(e,t){e.year=t}],S:["\\d",function(e,t){e.millisecond=100*t}],SS:["\\d{2}",function(e,t){e.millisecond=10*t}],SSS:["\\d{3}",function(e,t){e.millisecond=t}],d:["\\d\\d?",o],ddd:[r,o],MMM:[r,h("monthNamesShort")],MMMM:[r,h("monthNames")],a:[r,function(e,t,i){var s=t.toLowerCase();s===i.amPm[0]?e.isPm=!1:s===i.amPm[1]&&(e.isPm=!0)}],ZZ:["[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z",function(e,t){var i,s=(t+"").match(/([+-]|\d\d)/gi);s&&(i=60*s[1]+parseInt(s[2],10),e.timezoneOffset="+"===s[0]?i:-i)}]};_.dd=_.d,_.dddd=_.ddd,_.DD=_.D,_.mm=_.m,_.hh=_.H=_.HH=_.h,_.MM=_.M,_.ss=_.s,_.A=_.a,s.masks={default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"},s.format=function(e,t,i){var r=i||s.i18n;if("number"==typeof e&&(e=new Date(e)),"[object Date]"!==Object.prototype.toString.call(e)||isNaN(e.getTime()))throw new Error("Invalid Date in fecha.format");t=s.masks[t]||t||s.masks.default;var o=[];return(t=(t=t.replace(a,function(e,t){return o.push(t),"??"})).replace(n,function(t){return t in f?f[t](e,r):t.slice(1,t.length-1)})).replace(/\?\?/g,function(){return o.shift()})},s.parse=function(e,t,i){var r=i||s.i18n;if("string"!=typeof t)throw new Error("Invalid format in fecha.parse");if(t=s.masks[t]||t,e.length>1e3)return null;var a,o={},l=[],h=(a=t,a.replace(/[|\\{()[^$+*?.-]/g,"\\$&")).replace(n,function(e){if(_[e]){var t=_[e];return l.push(t[1]),"("+t[0]+")"}return e}),d=e.match(new RegExp(h,"i"));if(!d)return null;for(var c=1;c<d.length;c++)l[c-1](o,d[c],r);var u,p=new Date;return!0===o.isPm&&null!=o.hour&&12!=+o.hour?o.hour=+o.hour+12:!1===o.isPm&&12==+o.hour&&(o.hour=0),null!=o.timezoneOffset?(o.minute=+(o.minute||0)-+o.timezoneOffset,u=new Date(Date.UTC(o.year||p.getFullYear(),o.month||0,o.day||1,o.hour||0,o.minute||0,o.second||0,o.millisecond||0))):u=new Date(o.year||p.getFullYear(),o.month||0,o.day||1,o.hour||0,o.minute||0,o.second||0,o.millisecond||0),u},t.a=s},232:function(e,t,i){"use strict";i.d(t,"a",function(){return s});const s=e=>{const t=e.entity_id.split(".")[0];let i=e.state;return"climate"===t&&(i=e.attributes.hvac_action),i}},233:function(e,t,i){"use strict";i.d(t,"a",function(){return s});const s=i(0).c`
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

  ha-icon[data-domain="climate"][data-state="drying"] {
    color: var(--dry-color, #efbd07);
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
`},249:function(e,t,i){"use strict";i(3),i(51);var s=i(5),n=i(1),r=i(4),a=i(144);Object(s.a)({_template:r.a`
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
`,is:"app-header-layout",behaviors:[a.a],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return Object(n.a)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var e=this.header;if(this.isAttached&&e){this.$.wrapper.classList.remove("initializing"),e.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var t=e.offsetHeight;this.hasScrollingRegion?(e.style.left="",e.style.right=""):requestAnimationFrame(function(){var t=this.getBoundingClientRect(),i=document.documentElement.clientWidth-t.right;e.style.left=t.left+"px",e.style.right=i+"px"}.bind(this));var i=this.$.contentContainer.style;e.fixed&&!e.condenses&&this.hasScrollingRegion?(i.marginTop=t+"px",i.paddingTop=""):(i.paddingTop=t+"px",i.marginTop="")}}})},251:function(e,t,i){"use strict";i.d(t,"a",function(){return r}),i.d(t,"b",function(){return a});var s=i(224),n=i(223);const r=n.c?(e,t)=>e.toLocaleTimeString(t,{hour:"numeric",minute:"2-digit"}):e=>s.a.format(e,"shortTime"),a=n.c?(e,t)=>e.toLocaleTimeString(t,{hour:"numeric",minute:"2-digit",second:"2-digit"}):e=>s.a.format(e,"mediumTime")},253:function(e,t,i){"use strict";i(3),i(51);var s=i(5),n=i(1),r=i(4),a=i(144),o=i(278);Object(s.a)({_template:r.a`
    <style>
      :host {
        position: relative;
        display: block;
        transition-timing-function: linear;
        transition-property: -webkit-transform;
        transition-property: transform;
      }

      :host::before {
        position: absolute;
        right: 0px;
        bottom: -5px;
        left: 0px;
        width: 100%;
        height: 5px;
        content: "";
        transition: opacity 0.4s;
        pointer-events: none;
        opacity: 0;
        box-shadow: inset 0px 5px 6px -3px rgba(0, 0, 0, 0.4);
        will-change: opacity;
        @apply --app-header-shadow;
      }

      :host([shadow])::before {
        opacity: 1;
      }

      #background {
        @apply --layout-fit;
        overflow: hidden;
      }

      #backgroundFrontLayer,
      #backgroundRearLayer {
        @apply --layout-fit;
        height: 100%;
        pointer-events: none;
        background-size: cover;
      }

      #backgroundFrontLayer {
        @apply --app-header-background-front-layer;
      }

      #backgroundRearLayer {
        opacity: 0;
        @apply --app-header-background-rear-layer;
      }

      #contentContainer {
        position: relative;
        width: 100%;
        height: 100%;
      }

      :host([disabled]),
      :host([disabled])::after,
      :host([disabled]) #backgroundFrontLayer,
      :host([disabled]) #backgroundRearLayer,
      /* Silent scrolling should not run CSS transitions */
      :host([silent-scroll]),
      :host([silent-scroll])::after,
      :host([silent-scroll]) #backgroundFrontLayer,
      :host([silent-scroll]) #backgroundRearLayer {
        transition: none !important;
      }

      :host([disabled]) ::slotted(app-toolbar:first-of-type),
      :host([disabled]) ::slotted([sticky]),
      /* Silent scrolling should not run CSS transitions */
      :host([silent-scroll]) ::slotted(app-toolbar:first-of-type),
      :host([silent-scroll]) ::slotted([sticky]) {
        transition: none !important;
      }

    </style>
    <div id="contentContainer">
      <slot id="slot"></slot>
    </div>
`,is:"app-header",behaviors:[o.a,a.a],properties:{condenses:{type:Boolean,value:!1},fixed:{type:Boolean,value:!1},reveals:{type:Boolean,value:!1},shadow:{type:Boolean,reflectToAttribute:!0,value:!1}},observers:["_configChanged(isAttached, condenses, fixed)"],_height:0,_dHeight:0,_stickyElTop:0,_stickyElRef:null,_top:0,_progress:0,_wasScrollingDown:!1,_initScrollTop:0,_initTimestamp:0,_lastTimestamp:0,_lastScrollTop:0,get _maxHeaderTop(){return this.fixed?this._dHeight:this._height+5},get _stickyEl(){if(this._stickyElRef)return this._stickyElRef;for(var e,t=Object(n.a)(this.$.slot).getDistributedNodes(),i=0;e=t[i];i++)if(e.nodeType===Node.ELEMENT_NODE){if(e.hasAttribute("sticky")){this._stickyElRef=e;break}this._stickyElRef||(this._stickyElRef=e)}return this._stickyElRef},_configChanged:function(){this.resetLayout(),this._notifyLayoutChanged()},_updateLayoutStates:function(){if(0!==this.offsetWidth||0!==this.offsetHeight){var e=this._clampedScrollTop,t=0===this._height||0===e,i=this.disabled;this._height=this.offsetHeight,this._stickyElRef=null,this.disabled=!0,t||this._updateScrollState(0,!0),this._mayMove()?this._dHeight=this._stickyEl?this._height-this._stickyEl.offsetHeight:0:this._dHeight=0,this._stickyElTop=this._stickyEl?this._stickyEl.offsetTop:0,this._setUpEffect(),t?this._updateScrollState(e,!0):(this._updateScrollState(this._lastScrollTop,!0),this._layoutIfDirty()),this.disabled=i}},_updateScrollState:function(e,t){if(0!==this._height){var i=0,s=0,n=this._top,r=(this._lastScrollTop,this._maxHeaderTop),a=e-this._lastScrollTop,o=Math.abs(a),l=e>this._lastScrollTop,h=performance.now();if(this._mayMove()&&(s=this._clamp(this.reveals?n+a:e,0,r)),e>=this._dHeight&&(s=this.condenses&&!this.fixed?Math.max(this._dHeight,s):s,this.style.transitionDuration="0ms"),this.reveals&&!this.disabled&&o<100&&((h-this._initTimestamp>300||this._wasScrollingDown!==l)&&(this._initScrollTop=e,this._initTimestamp=h),e>=r))if(Math.abs(this._initScrollTop-e)>30||o>10){l&&e>=r?s=r:!l&&e>=this._dHeight&&(s=this.condenses&&!this.fixed?this._dHeight:0);var d=a/(h-this._lastTimestamp);this.style.transitionDuration=this._clamp((s-n)/d,0,300)+"ms"}else s=this._top;i=0===this._dHeight?e>0?1:0:s/this._dHeight,t||(this._lastScrollTop=e,this._top=s,this._wasScrollingDown=l,this._lastTimestamp=h),(t||i!==this._progress||n!==s||0===e)&&(this._progress=i,this._runEffects(i,s),this._transformHeader(s))}},_mayMove:function(){return this.condenses||!this.fixed},willCondense:function(){return this._dHeight>0&&this.condenses},isOnScreen:function(){return 0!==this._height&&this._top<this._height},isContentBelow:function(){return 0===this._top?this._clampedScrollTop>0:this._clampedScrollTop-this._maxHeaderTop>=0},_transformHeader:function(e){this.translate3d(0,-e+"px",0),this._stickyEl&&this.translate3d(0,this.condenses&&e>=this._stickyElTop?Math.min(e,this._dHeight)-this._stickyElTop+"px":0,0,this._stickyEl)},_clamp:function(e,t,i){return Math.min(i,Math.max(t,e))},_ensureBgContainers:function(){this._bgContainer||(this._bgContainer=document.createElement("div"),this._bgContainer.id="background",this._bgRear=document.createElement("div"),this._bgRear.id="backgroundRearLayer",this._bgContainer.appendChild(this._bgRear),this._bgFront=document.createElement("div"),this._bgFront.id="backgroundFrontLayer",this._bgContainer.appendChild(this._bgFront),Object(n.a)(this.root).insertBefore(this._bgContainer,this.$.contentContainer))},_getDOMRef:function(e){switch(e){case"backgroundFrontLayer":return this._ensureBgContainers(),this._bgFront;case"backgroundRearLayer":return this._ensureBgContainers(),this._bgRear;case"background":return this._ensureBgContainers(),this._bgContainer;case"mainTitle":return Object(n.a)(this).querySelector("[main-title]");case"condensedTitle":return Object(n.a)(this).querySelector("[condensed-title]")}return null},getScrollState:function(){return{progress:this._progress,top:this._top}}})},270:function(e,t,i){"use strict";i.r(t),i.d(t,"Layout1d",function(){return n});var s=i(274);class n extends s.a{constructor(e){super(e),this._physicalItems=new Map,this._newPhysicalItems=new Map,this._metrics=new Map,this._anchorIdx=null,this._anchorPos=null,this._stable=!0,this._needsRemeasure=!1,this._nMeasured=0,this._tMeasured=0,this._estimate=!0}updateItemSizes(e){Object.keys(e).forEach(t=>{const i=e[t],s=this._getMetrics(Number(t)),n=s[this._sizeDim];s.width=i.width+(i.marginLeft||0)+(i.marginRight||0),s.height=i.height+(i.marginTop||0)+(i.marginBottom||0);const r=s[this._sizeDim],a=this._getPhysicalItem(Number(t));if(a){let e;void 0!==r&&(a.size=r,void 0===n?(e=r,this._nMeasured++):e=r-n),this._tMeasured=this._tMeasured+e}}),this._nMeasured?(this._updateItemSize(),this._scheduleReflow()):console.warn("No items measured yet.")}_updateItemSize(){this._itemSize[this._sizeDim]=Math.round(this._tMeasured/this._nMeasured)}_getMetrics(e){return this._metrics[e]=this._metrics[e]||{}}_getPhysicalItem(e){return this._newPhysicalItems.get(e)||this._physicalItems.get(e)}_getSize(e){const t=this._getPhysicalItem(e);return t&&t.size}_getPosition(e){const t=this._physicalItems.get(e);return t?t.pos:e*this._delta+this._spacing}_calculateAnchor(e,t){return 0===e?0:t>this._scrollSize-this._viewDim1?this._totalItems-1:Math.max(0,Math.min(this._totalItems-1,Math.floor((e+t)/2/this._delta)))}_getAnchor(e,t){if(0===this._physicalItems.size)return this._calculateAnchor(e,t);if(this._first<0)return console.error("_getAnchor: negative _first"),this._calculateAnchor(e,t);if(this._last<0)return console.error("_getAnchor: negative _last"),this._calculateAnchor(e,t);const i=this._getPhysicalItem(this._first),s=this._getPhysicalItem(this._last),n=i.pos,r=n+i.size,a=s.pos,o=a+s.size;if(o<e)return this._calculateAnchor(e,t);if(n>t)return this._calculateAnchor(e,t);if(n>=e||r>=e)return this._first;if(o<=t||a<=t)return this._last;let l=this._last,h=this._first;for(;;){const i=Math.round((l+h)/2),s=this._physicalItems.get(i),n=s.pos,r=n+s.size;if(n>=e&&n<=t||r>=e&&r<=t)return i;r<e?h=i+1:n>t&&(l=i-1)}}_getActiveItems(){if(0===this._viewDim1||0===this._totalItems)this._clearItems();else{const e=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang),t=Math.max(0,e-this._viewDim1-2*this._overhang);this._getItems(t,e)}}_clearItems(){this._first=-1,this._last=-1,this._physicalMin=0,this._physicalMax=0;const e=this._newPhysicalItems;this._newPhysicalItems=this._physicalItems,this._newPhysicalItems.clear(),this._physicalItems=e,this._stable=!0}_getItems(e,t){const i=this._newPhysicalItems;null!==this._anchorIdx&&null!==this._anchorPos||(this._anchorIdx=this._getAnchor(e,t),this._anchorPos=this._getPosition(this._anchorIdx));let s=this._getSize(this._anchorIdx);void 0===s&&(s=this._itemDim1);let n=0;for(this._anchorPos+s+this._spacing<e&&(n=e-(this._anchorPos+s+this._spacing)),this._anchorPos>t&&(n=t-this._anchorPos),n&&(this._scrollPosition-=n,e-=n,t-=n,this._scrollError+=n),i.set(this._anchorIdx,{pos:this._anchorPos,size:s}),this._first=this._last=this._anchorIdx,this._physicalMin=this._physicalMax=this._anchorPos,this._stable=!0;this._physicalMin>e&&this._first>0;){let e=this._getSize(--this._first);void 0===e&&(this._stable=!1,e=this._itemDim1);const t=this._physicalMin-=e+this._spacing;if(i.set(this._first,{pos:t,size:e}),!1===this._stable&&!1===this._estimate)break}for(;this._physicalMax<t&&this._last<this._totalItems;){let e=this._getSize(this._last);if(void 0===e&&(this._stable=!1,e=this._itemDim1),i.set(this._last++,{pos:this._physicalMax,size:e}),!1===this._stable&&!1===this._estimate)break;this._physicalMax+=e+this._spacing}this._last--;const r=this._calculateError();r&&(this._physicalMin-=r,this._physicalMax-=r,this._anchorPos-=r,this._scrollPosition-=r,i.forEach(e=>e.pos-=r),this._scrollError+=r),this._stable&&(this._newPhysicalItems=this._physicalItems,this._newPhysicalItems.clear(),this._physicalItems=i)}_calculateError(){return 0===this._first?this._physicalMin:this._physicalMin<=0?this._physicalMin-this._first*this._delta:this._last===this._totalItems-1?this._physicalMax-this._scrollSize:this._physicalMax>=this._scrollSize?this._physicalMax-this._scrollSize+(this._totalItems-1-this._last)*this._delta:0}_updateScrollSize(){super._updateScrollSize(),this._scrollSize=Math.max(this._physicalMax,this._scrollSize)}_reflow(){const{_first:e,_last:t,_scrollSize:i}=this;this._updateScrollSize(),this._getActiveItems(),this._scrollIfNeeded(),this._scrollSize!==i&&this._emitScrollSize(),this._updateVisibleIndices(),this._emitRange(),-1===this._first&&-1===this._last?this._resetReflowState():this._first!==e||this._last!==t||this._needsRemeasure?(this._emitChildPositions(),this._emitScrollError()):(this._emitChildPositions(),this._emitScrollError(),this._resetReflowState())}_resetReflowState(){this._anchorIdx=null,this._anchorPos=null,this._stable=!0}_getItemPosition(e){return{[this._positionDim]:this._getPosition(e),[this._secondaryPositionDim]:0}}_getItemSize(e){return{[this._sizeDim]:this._getSize(e)||this._itemDim1,[this._secondarySizeDim]:this._itemDim2}}_viewDim2Changed(){this._needsRemeasure=!0,this._scheduleReflow()}_emitRange(){const e=this._needsRemeasure,t=this._stable;this._needsRemeasure=!1,super._emitRange({remeasure:e,stable:t})}}},274:function(e,t,i){"use strict";let s;async function n(){return s||async function(){s=window.EventTarget;try{new s}catch(e){s=(await i.e(201).then(i.t.bind(null,842,7))).EventTarget}return s}()}i.d(t,"a",function(){return r});class r{constructor(e){this._latestCoords={left:0,top:0},this._direction="vertical",this._viewportSize={width:0,height:0},this._pendingReflow=!1,this._scrollToIndex=-1,this._scrollToAnchor=0,this._eventTargetPromise=n().then(e=>this._eventTarget=new e),this._physicalMin=0,this._physicalMax=0,this._first=-1,this._last=-1,this._itemSize={width:100,height:100},this._spacing=0,this._sizeDim="height",this._secondarySizeDim="width",this._positionDim="top",this._secondaryPositionDim="left",this._scrollPosition=0,this._scrollError=0,this._totalItems=0,this._scrollSize=1,this._overhang=150,Object.assign(this,e)}get totalItems(){return this._totalItems}set totalItems(e){e!==this._totalItems&&(this._totalItems=e,this._scheduleReflow())}get direction(){return this._direction}set direction(e){(e="horizontal"===e?e:"vertical")!==this._direction&&(this._direction=e,this._sizeDim="horizontal"===e?"width":"height",this._secondarySizeDim="horizontal"===e?"height":"width",this._positionDim="horizontal"===e?"left":"top",this._secondaryPositionDim="horizontal"===e?"top":"left",this._scheduleReflow())}get itemSize(){return this._itemSize}set itemSize(e){const{_itemDim1:t,_itemDim2:i}=this;Object.assign(this._itemSize,e),t===this._itemDim1&&i===this._itemDim2||(i!==this._itemDim2?this._itemDim2Changed():this._scheduleReflow())}get spacing(){return this._spacing}set spacing(e){e!==this._spacing&&(this._spacing=e,this._scheduleReflow())}get viewportSize(){return this._viewportSize}set viewportSize(e){const{_viewDim1:t,_viewDim2:i}=this;Object.assign(this._viewportSize,e),i!==this._viewDim2?this._viewDim2Changed():t!==this._viewDim1&&this._checkThresholds()}get viewportScroll(){return this._latestCoords}set viewportScroll(e){Object.assign(this._latestCoords,e);const t=this._scrollPosition;this._scrollPosition=this._latestCoords[this._positionDim],t!==this._scrollPosition&&(this._scrollPositionChanged(t,this._scrollPosition),this._updateVisibleIndices()),this._checkThresholds()}reflowIfNeeded(){this._pendingReflow&&(this._pendingReflow=!1,this._reflow())}scrollToIndex(e,t="start"){if(Number.isFinite(e)){switch(e=Math.min(this.totalItems,Math.max(0,e)),this._scrollToIndex=e,"nearest"===t&&(t=e>this._first+this._num/2?"end":"start"),t){case"start":this._scrollToAnchor=0;break;case"center":this._scrollToAnchor=.5;break;case"end":this._scrollToAnchor=1;break;default:throw new TypeError("position must be one of: start, center, end, nearest")}this._scheduleReflow(),this.reflowIfNeeded()}}async dispatchEvent(...e){await this._eventTargetPromise,this._eventTarget.dispatchEvent(...e)}async addEventListener(...e){await this._eventTargetPromise,this._eventTarget.addEventListener(...e)}async removeEventListener(...e){await this._eventTargetPromise,this._eventTarget.removeEventListener(...e)}updateItemSizes(e){}_itemDim2Changed(){}_viewDim2Changed(){}_getItemSize(e){return{[this._sizeDim]:this._itemDim1,[this._secondarySizeDim]:this._itemDim2}}get _delta(){return this._itemDim1+this._spacing}get _itemDim1(){return this._itemSize[this._sizeDim]}get _itemDim2(){return this._itemSize[this._secondarySizeDim]}get _viewDim1(){return this._viewportSize[this._sizeDim]}get _viewDim2(){return this._viewportSize[this._secondarySizeDim]}_scheduleReflow(){this._pendingReflow=!0}_reflow(){const{_first:e,_last:t,_scrollSize:i}=this;this._updateScrollSize(),this._getActiveItems(),this._scrollIfNeeded(),this._scrollSize!==i&&this._emitScrollSize(),-1===this._first&&-1===this._last?this._emitRange():(this._first!==e||this._last!==t||this._spacingChanged)&&(this._emitRange(),this._emitChildPositions()),this._emitScrollError()}_updateScrollSize(){this._scrollSize=Math.max(1,this._totalItems*this._delta)}_scrollIfNeeded(){if(-1===this._scrollToIndex)return;const e=this._scrollToIndex,t=this._scrollToAnchor,i=this._getItemPosition(e)[this._positionDim],s=this._getItemSize(e)[this._sizeDim],n=this._scrollPosition+this._viewDim1*t,r=i+s*t,a=Math.floor(Math.min(this._scrollSize-this._viewDim1,Math.max(0,this._scrollPosition-n+r)));this._scrollError+=this._scrollPosition-a,this._scrollPosition=a}_emitRange(e){const t=Object.assign({first:this._first,last:this._last,num:this._num,stable:!0,firstVisible:this._firstVisible,lastVisible:this._lastVisible},e);this.dispatchEvent(new CustomEvent("rangechange",{detail:t}))}_emitScrollSize(){const e={[this._sizeDim]:this._scrollSize};this.dispatchEvent(new CustomEvent("scrollsizechange",{detail:e}))}_emitScrollError(){if(this._scrollError){const e={[this._positionDim]:this._scrollError,[this._secondaryPositionDim]:0};this.dispatchEvent(new CustomEvent("scrollerrorchange",{detail:e})),this._scrollError=0}}_emitChildPositions(){const e={};for(let t=this._first;t<=this._last;t++)e[t]=this._getItemPosition(t);this.dispatchEvent(new CustomEvent("itempositionchange",{detail:e}))}get _num(){return-1===this._first||-1===this._last?0:this._last-this._first+1}_checkThresholds(){if(0===this._viewDim1&&this._num>0)this._scheduleReflow();else{const e=Math.max(0,this._scrollPosition-this._overhang),t=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang);(this._physicalMin>e||this._physicalMax<t)&&this._scheduleReflow()}}_updateVisibleIndices(){let e=this._firstVisible,t=this._lastVisible;for(let i=this._first;i<=this._last;i++){const s=this._getItemPosition(i)[this._positionDim];s<=this._scrollPosition&&(e=i),s<this._scrollPosition+this._viewDim1&&(t=i)}e>t||e===this._firstVisible&&t===this._lastVisible||(this._firstVisible=e,this._lastVisible=t,this._emitRange())}_scrollPositionChanged(e,t){const i=this._scrollSize-this._viewDim1;(e<i||t<i)&&(this._scrollToIndex=-1)}}},278:function(e,t,i){"use strict";i.d(t,"a",function(){return r});i(3);var s=i(216),n=i(279);const r=[s.a,{properties:{effects:{type:String},effectsConfig:{type:Object,value:function(){return{}}},disabled:{type:Boolean,reflectToAttribute:!0,value:!1},threshold:{type:Number,value:0},thresholdTriggered:{type:Boolean,notify:!0,readOnly:!0,reflectToAttribute:!0}},observers:["_effectsChanged(effects, effectsConfig, isAttached)"],_updateScrollState:function(e){},isOnScreen:function(){return!1},isContentBelow:function(){return!1},_effectsRunFn:null,_effects:null,get _clampedScrollTop(){return Math.max(0,this._scrollTop)},attached:function(){this._scrollStateChanged()},detached:function(){this._tearDownEffects()},createEffect:function(e,t){var i=n.a[e];if(!i)throw new ReferenceError(this._getUndefinedMsg(e));var s=this._boundEffect(i,t||{});return s.setUp(),s},_effectsChanged:function(e,t,i){this._tearDownEffects(),e&&i&&(e.split(" ").forEach(function(e){var i;""!==e&&((i=n.a[e])?this._effects.push(this._boundEffect(i,t[e])):console.warn(this._getUndefinedMsg(e)))},this),this._setUpEffect())},_layoutIfDirty:function(){return this.offsetWidth},_boundEffect:function(e,t){t=t||{};var i=parseFloat(t.startsAt||0),s=parseFloat(t.endsAt||1),n=s-i,r=function(){},a=0===i&&1===s?e.run:function(t,s){e.run.call(this,Math.max(0,(t-i)/n),s)};return{setUp:e.setUp?e.setUp.bind(this,t):r,run:e.run?a.bind(this):r,tearDown:e.tearDown?e.tearDown.bind(this):r}},_setUpEffect:function(){this.isAttached&&this._effects&&(this._effectsRunFn=[],this._effects.forEach(function(e){!1!==e.setUp()&&this._effectsRunFn.push(e.run)},this))},_tearDownEffects:function(){this._effects&&this._effects.forEach(function(e){e.tearDown()}),this._effectsRunFn=[],this._effects=[]},_runEffects:function(e,t){this._effectsRunFn&&this._effectsRunFn.forEach(function(i){i(e,t)})},_scrollHandler:function(){this._scrollStateChanged()},_scrollStateChanged:function(){if(!this.disabled){var e=this._clampedScrollTop;this._updateScrollState(e),this.threshold>0&&this._setThresholdTriggered(e>=this.threshold)}},_getDOMRef:function(e){console.warn("_getDOMRef","`"+e+"` is undefined")},_getUndefinedMsg:function(e){return"Scroll effect `"+e+"` is undefined. Did you forget to import app-layout/app-scroll-effects/effects/"+e+".html ?"}}]},279:function(e,t,i){"use strict";i.d(t,"a",function(){return s}),i.d(t,"b",function(){return n});i(3);const s={};const n=function(e,t){if(null!=s[e])throw new Error("effect `"+e+"` is already registered.");s[e]=t}},299:function(e,t,i){"use strict";i.d(t,"a",function(){return n});var s=i(224);const n=i(223).a?(e,t)=>e.toLocaleDateString(t,{year:"numeric",month:"long",day:"numeric"}):e=>s.a.format(e,"longDate")},307:function(e,t,i){"use strict";var s=i(9);class n{constructor(e){this._createElementFn=null,this._updateElementFn=null,this._recycleElementFn=null,this._elementKeyFn=null,this._items=[],this._totalItems=null,this._needsReset=!1,this._needsRemeasure=!1,this._active=new Map,this._prevActive=new Map,this._keyToChild=new Map,this._childToKey=new WeakMap,this._indexToMeasure={},this.__incremental=!1,this._measureCallback=null,this._num=1/0,this._first=0,this._last=0,this._prevFirst=0,this._prevLast=0,this._pendingRender=null,this._container=null,this._ordered=[],e&&Object.assign(this,e)}get container(){return this._container}set container(e){e!==this._container&&(this._container&&this._ordered.forEach(e=>this._removeChild(e)),this._container=e,e?this._ordered.forEach(e=>this._insertBefore(e,null)):(this._ordered.length=0,this._active.clear(),this._prevActive.clear()),this.requestReset())}get createElement(){return this._createElementFn}set createElement(e){e!==this._createElementFn&&(this._createElementFn=e,this._keyToChild.clear(),this.requestReset())}get updateElement(){return this._updateElementFn}set updateElement(e){e!==this._updateElementFn&&(this._updateElementFn=e,this.requestReset())}get recycleElement(){return this._recycleElementFn}set recycleElement(e){e!==this._recycleElementFn&&(this._recycleElementFn=e,this.requestReset())}get elementKey(){return this._elementKeyFn}set elementKey(e){e!==this._elementKeyFn&&(this._elementKeyFn=e,this._keyToChild.clear(),this.requestReset())}get first(){return this._first}set first(e){if("number"!=typeof e)throw new Error("New value must be a number.");const t=Math.max(0,Math.min(e,this.totalItems-this._num));t!==this._first&&(this._first=t,this._scheduleRender())}get num(){return this._num}set num(e){if("number"!=typeof e)throw new Error("New value must be a number.");e!==this._num&&(this._num=e,this.first=this._first,this._scheduleRender())}get items(){return this._items}set items(e){e!==this._items&&Array.isArray(e)&&(this._items=e,this.requestReset())}get totalItems(){return null===this._totalItems?this._items.length:this._totalItems}set totalItems(e){if("number"!=typeof e&&null!==e)throw new Error("New value must be a number.");e!==this._totalItems&&(this._totalItems=e,this.first=this._first,this.requestReset())}get _incremental(){return this.__incremental}set _incremental(e){e!==this.__incremental&&(this.__incremental=e,this._scheduleRender())}requestRemeasure(){this._needsRemeasure=!0,this._scheduleRender()}_shouldRender(){return Boolean(this.container&&this.createElement)}async _scheduleRender(){this._pendingRender||(this._pendingRender=!0,await Promise.resolve(),this._pendingRender=!1,this._shouldRender()&&this._render())}requestReset(){this._needsReset=!0,this._scheduleRender()}get _toMeasure(){return this._ordered.reduce((e,t,i)=>{const s=this._first+i;return(this._needsReset||this._needsRemeasure||s<this._prevFirst||s>this._prevLast)&&(e.indices.push(s),e.children.push(t)),e},{indices:[],children:[]})}async _measureChildren({indices:e,children:t}){await new Promise(e=>{requestAnimationFrame(e)});const i=t.map(e=>this._measureChild(e)).reduce((t,i,s)=>(t[e[s]]=this._indexToMeasure[e[s]]=i,t),{});this._measureCallback(i)}async _render(){const e=this._first!==this._prevFirst||this._num!==this._prevNum;(e||this._needsReset)&&(this._last=this._first+Math.min(this._num,this.totalItems-this._first)-1,(this._num||this._prevNum)&&(this._needsReset?this._reset(this._first,this._last):(this._discardHead(),this._discardTail(),this._addHead(),this._addTail()))),(this._needsRemeasure||this._needsReset)&&(this._indexToMeasure={});const t=this._num>0&&this._measureCallback&&(e||this._needsRemeasure||this._needsReset)?this._toMeasure:null;this._incremental||(this._prevActive.forEach((e,t)=>this._unassignChild(t,e)),this._prevActive.clear()),this._prevFirst=this._first,this._prevLast=this._last,this._prevNum=this._num,this._needsReset=!1,this._needsRemeasure=!1,this._didRender(),t&&await this._measureChildren(t)}_didRender(){}_discardHead(){const e=this._ordered;for(let t=this._prevFirst;e.length&&t<this._first;t++)this._unassignChild(e.shift(),t)}_discardTail(){const e=this._ordered;for(let t=this._prevLast;e.length&&t>this._last;t--)this._unassignChild(e.pop(),t)}_addHead(){const e=this._first;for(let t=Math.min(this._last,this._prevFirst-1);t>=e;t--){const e=this._assignChild(t);this._insertBefore(e,this._firstChild),this.updateElement&&this.updateElement(e,this._items[t],t),this._ordered.unshift(e)}}_addTail(){const e=Math.max(this._first,this._prevLast+1),t=this._last;for(let i=e;i<=t;i++){const e=this._assignChild(i);this._insertBefore(e,null),this.updateElement&&this.updateElement(e,this._items[i],i),this._ordered.push(e)}}_reset(e,t){const i=this._active;this._active=this._prevActive,this._prevActive=i,this._ordered.length=0;let s=this._firstChild;for(let n=e;n<=t;n++){const e=this._assignChild(n);this._ordered.push(e),s?s===this._node(e)?s=this._nextSibling(e):this._insertBefore(e,s):this._childIsAttached(e)||this._insertBefore(e,null),this.updateElement&&this.updateElement(e,this._items[n],n)}}_assignChild(e){const t=this.elementKey?this.elementKey(e):e;let i;return(i=this._keyToChild.get(t))?this._prevActive.delete(i):(i=this.createElement(this._items[e],e),this._keyToChild.set(t,i),this._childToKey.set(i,t)),this._showChild(i),this._active.set(i,e),i}_unassignChild(e,t){if(this._hideChild(e),this._incremental)this._active.delete(e),this._prevActive.set(e,t);else{const i=this._childToKey.get(e);this._childToKey.delete(e),this._keyToChild.delete(i),this._active.delete(e),this.recycleElement?this.recycleElement(e,t):this._node(e).parentNode&&this._removeChild(e)}}get _firstChild(){return this._ordered.length&&this._childIsAttached(this._ordered[0])?this._node(this._ordered[0]):null}_node(e){return e}_nextSibling(e){return e.nextSibling}_insertBefore(e,t){this._container.insertBefore(e,t)}_removeChild(e){e.parentNode.removeChild(e)}_childIsAttached(e){const t=this._node(e);return t&&t.parentNode===this._container}_hideChild(e){e instanceof HTMLElement&&(e.style.display="none")}_showChild(e){e instanceof HTMLElement&&(e.style.display=null)}_measureChild(e){const{width:t,height:i}=e.getBoundingClientRect();return Object.assign({width:t,height:i},function(e){const t=window.getComputedStyle(e);return{marginTop:r(t.marginTop),marginRight:r(t.marginRight),marginBottom:r(t.marginBottom),marginLeft:r(t.marginLeft)}}(e))}}function r(e){const t=e?parseFloat(e):NaN;return Number.isNaN(t)?0:t}const a=e=>(class extends e{constructor(e){const{part:t,renderItem:i,useShadowDOM:s,layout:n}=e,r=t.startNode.parentNode;super({container:r,scrollTarget:e.scrollTarget||r,useShadowDOM:s,layout:n}),this._pool=[],this._renderItem=i,this._hostPart=t}createElement(){return this._pool.pop()||new s.b(this._hostPart.options)}updateElement(e,t,i){e.setValue(this._renderItem(t,i)),e.commit()}recycleElement(e){this._pool.push(e)}get _kids(){return this._ordered.map(e=>e.startNode.nextElementSibling)}_node(e){return e.startNode}_nextSibling(e){return e.endNode.nextSibling}_insertBefore(e,t){if(null===t&&(t=this._hostPart.endNode),this._childIsAttached(e)){const i=e.endNode.nextSibling;if(t!==e.startNode&&t!==i)for(let s=e.startNode;s!==i;){const e=s.nextSibling;super._insertBefore(s,t),s=e}}else e.startNode=Object(s.e)(),e.endNode=Object(s.e)(),super._insertBefore(e.startNode,t),super._insertBefore(e.endNode,t)}_hideChild(e){let t=e.startNode;for(;t&&t!==e.endNode;)super._hideChild(t),t=t.nextSibling}_showChild(e){let t=e.startNode;for(;t&&t!==e.endNode;)super._showChild(t),t=t.nextSibling}_measureChild(e){return super._measureChild(e.startNode.nextElementSibling)}});class o extends(a(n)){}const l=new WeakMap;Object(s.f)(e=>async t=>{let i=l.get(t);i||(t.startNode.isConnected||await Promise.resolve(),i=new o({part:t,renderItem:e.renderItem}),l.set(t,i));const{first:s,num:n,totalItems:r}=e;Object.assign(i,{first:s,num:n,totalItems:r})});let h;async function d(){return h||async function(){h=window.ResizeObserver;try{new h(function(){})}catch(e){h=(await i.e(195).then(i.bind(null,841))).default}return h}()}const c="uni-virtualizer-host";let u=null;function p(e,t){return`\n    ${e} {\n      display: block;\n      position: relative;\n      contain: strict;\n      height: 150px;\n      overflow: auto;\n    }\n    ${t} {\n      box-sizing: border-box;\n    }`}class m extends Event{constructor(e,t){super(e,t),this._first=Math.floor(t.first||0),this._last=Math.floor(t.last||0),this._firstVisible=Math.floor(t.firstVisible||0),this._lastVisible=Math.floor(t.lastVisible||0)}get first(){return this._first}get last(){return this._last}get firstVisible(){return this._firstVisible}get lastVisible(){return this._lastVisible}}class f extends n{constructor(e){super({}),this._needsUpdateView=!1,this._layout=null,this._lazyLoadDefaultLayout=!0,this._scrollTarget=null,this._sizer=null,this._scrollSize=null,this._scrollErr=null,this._childrenPos=null,this._containerElement=null,this._containerInlineStyle=null,this._containerStylesheet=null,this._useShadowDOM=!0,this._containerSize=null,this._containerRO=null,this._childrenRO=null,this._skipNextChildrenSizeChanged=!1,this._scrollToIndex=null,this._num=0,this._first=-1,this._last=-1,this._prevFirst=-1,this._prevLast=-1,e&&Object.assign(this,e)}get container(){return super.container}set container(e){super.container=e,this._initResizeObservers().then(()=>{const t=this._containerElement,i=e&&e.nodeType===Node.DOCUMENT_FRAGMENT_NODE?e.host:e;t!==i&&(this._containerRO.disconnect(),this._containerSize=null,t?(this._containerInlineStyle?t.setAttribute("style",this._containerInlineStyle):t.removeAttribute("style"),this._containerInlineStyle=null,t===this._scrollTarget&&(t.removeEventListener("scroll",this,{passive:!0}),this._sizer&&this._sizer.remove())):addEventListener("scroll",this,{passive:!0}),this._containerElement=i,i&&(this._containerInlineStyle=i.getAttribute("style")||null,this._applyContainerStyles(),i===this._scrollTarget&&(this._sizer=this._sizer||this._createContainerSizer(),this._container.prepend(this._sizer)),this._scheduleUpdateView(),this._containerRO.observe(i)))})}get layout(){return this._layout}set layout(e){e!==this._layout&&(this._layout&&(this._measureCallback=null,this._layout.removeEventListener("scrollsizechange",this),this._layout.removeEventListener("scrollerrorchange",this),this._layout.removeEventListener("itempositionchange",this),this._layout.removeEventListener("rangechange",this),this._containerElement&&this._sizeContainer(void 0)),this._layout=e,this._layout&&("function"==typeof this._layout.updateItemSizes&&(this._measureCallback=this._layout.updateItemSizes.bind(this._layout),this.requestRemeasure()),this._layout.addEventListener("scrollsizechange",this),this._layout.addEventListener("scrollerrorchange",this),this._layout.addEventListener("itempositionchange",this),this._layout.addEventListener("rangechange",this),this._scheduleUpdateView()))}get scrollTarget(){return this._scrollTarget}set scrollTarget(e){e===window&&(e=null),this._scrollTarget!==e&&(this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this,{passive:!0}),this._sizer&&this._scrollTarget===this._containerElement&&this._sizer.remove()),this._scrollTarget=e,e&&(e.addEventListener("scroll",this,{passive:!0}),e===this._containerElement&&(this._sizer=this._sizer||this._createContainerSizer(),this._container.prepend(this._sizer))))}get useShadowDOM(){return this._useShadowDOM}set useShadowDOM(e){this._useShadowDOM!==e&&(this._useShadowDOM=Boolean(e),this._containerStylesheet&&(this._containerStylesheet.parentElement.removeChild(this._containerStylesheet),this._containerStylesheet=null),this._applyContainerStyles())}set scrollToIndex(e){this._scrollToIndex=e,this._scheduleUpdateView()}async _render(){if(!this._lazyLoadDefaultLayout||this._layout){for(this._childrenRO.disconnect(),this._layout.totalItems=this.totalItems,this._needsUpdateView&&(this._needsUpdateView=!1,this._updateView()),null!==this._scrollToIndex&&(this._layout.scrollToIndex(this._scrollToIndex.index,this._scrollToIndex.position),this._scrollToIndex=null),this._layout.reflowIfNeeded();this._pendingRender&&(this._pendingRender=!1),this._sizeContainer(this._scrollSize),this._scrollErr&&(this._correctScrollError(this._scrollErr),this._scrollErr=null),await super._render(),this._layout.reflowIfNeeded(),this._pendingRender;);this._skipNextChildrenSizeChanged=!0,this._kids.forEach(e=>this._childrenRO.observe(e))}else{this._lazyLoadDefaultLayout=!1;const{Layout1d:e}=await Promise.resolve().then(i.bind(null,270));this.layout=new e({})}}_didRender(){this._childrenPos&&(this._positionChildren(this._childrenPos),this._childrenPos=null)}handleEvent(e){switch(e.type){case"scroll":this._scrollTarget&&e.target!==this._scrollTarget||this._scheduleUpdateView();break;case"scrollsizechange":this._scrollSize=e.detail,this._scheduleRender();break;case"scrollerrorchange":this._scrollErr=e.detail,this._scheduleRender();break;case"itempositionchange":this._childrenPos=e.detail,this._scheduleRender();break;case"rangechange":this._adjustRange(e.detail);break;default:console.warn("event not handled",e)}}async _initResizeObservers(){if(null===this._containerRO){const e=await d();this._containerRO=new e(e=>this._containerSizeChanged(e[0].contentRect)),this._childrenRO=new e(()=>this._childrenSizeChanged())}}_applyContainerStyles(){if(this._useShadowDOM){if(null===this._containerStylesheet){(this._containerStylesheet=document.createElement("style")).textContent=p(":host","::slotted(*)")}const e=this._containerElement.shadowRoot||this._containerElement.attachShadow({mode:"open"}),t=e.querySelector("slot:not([name])");e.appendChild(this._containerStylesheet),t||e.appendChild(document.createElement("slot"))}else u||((u=document.createElement("style")).textContent=p(`.${c}`,`.${c} > *`),document.head.appendChild(u)),this._containerElement&&this._containerElement.classList.add(c)}_createContainerSizer(){const e=document.createElement("div");return Object.assign(e.style,{position:"absolute",margin:"-2px 0 0 0",padding:0,visibility:"hidden",fontSize:"2px"}),e.innerHTML="&nbsp;",e}get _kids(){return this._ordered}_scheduleUpdateView(){this._needsUpdateView=!0,this._scheduleRender()}_updateView(){let e,t,i,s;if(this._scrollTarget===this._containerElement)e=this._containerSize.width,t=this._containerSize.height,s=this._containerElement.scrollLeft,i=this._containerElement.scrollTop;else{const n=this._containerElement.getBoundingClientRect(),r=this._scrollTarget?this._scrollTarget.getBoundingClientRect():{top:n.top+scrollY,left:n.left+scrollX,width:innerWidth,height:innerHeight},a=r.width,o=r.height,l=Math.max(0,Math.min(a,n.left-r.left)),h=Math.max(0,Math.min(o,n.top-r.top));e=("vertical"===this._layout.direction?Math.max(0,Math.min(a,n.right-r.left)):a)-l,t=("vertical"===this._layout.direction?o:Math.max(0,Math.min(o,n.bottom-r.top)))-h,s=Math.max(0,-(n.left-r.left)),i=Math.max(0,-(n.top-r.top))}this._layout.viewportSize={width:e,height:t},this._layout.viewportScroll={top:i,left:s}}_sizeContainer(e){if(this._scrollTarget===this._containerElement){const t=e&&e.width?e.width-1:0,i=e&&e.height?e.height-1:0;this._sizer.style.transform=`translate(${t}px, ${i}px)`}else{const t=this._containerElement.style;t.minWidth=e&&e.width?e.width+"px":null,t.minHeight=e&&e.height?e.height+"px":null}}_positionChildren(e){const t=this._kids;Object.keys(e).forEach(i=>{const s=i-this._first,n=t[s];if(n){const{top:t,left:s}=e[i];n.style.position="absolute",n.style.transform=`translate(${s}px, ${t}px)`}})}_adjustRange(e){this.num=e.num,this.first=e.first;const t=this._firstVisible!==e.firstVisible||this._lastVisible!==e.lastVisible;this._firstVisible=e.firstVisible,this._lastVisible=e.lastVisible,this._incremental=!e.stable,e.remeasure?this.requestRemeasure():(e.stable||t)&&this._notifyRange()}_shouldRender(){if(!super._shouldRender()||!this._containerElement||!this._layout&&!this._lazyLoadDefaultLayout)return!1;if(null===this._containerSize){const{width:e,height:t}=this._containerElement.getBoundingClientRect();this._containerSize={width:e,height:t}}return this._containerSize.width>0||this._containerSize.height>0}_correctScrollError(e){this._scrollTarget?(this._scrollTarget.scrollTop-=e.top,this._scrollTarget.scrollLeft-=e.left):window.scroll(window.scrollX-e.left,window.scrollY-e.top)}_notifyRange(){const{first:e,num:t}=this,i=e+t-1;this._container.dispatchEvent(new m("rangechange",{first:e,last:i,firstVisible:this._firstVisible,lastVisible:this._lastVisible}))}_containerSizeChanged(e){const{width:t,height:i}=e;this._containerSize={width:t,height:i},this._scheduleUpdateView()}_childrenSizeChanged(){this._skipNextChildrenSizeChanged?this._skipNextChildrenSizeChanged=!1:this.requestRemeasure()}}class _ extends(a(f)){}const g=new WeakMap,v=Object(s.f)(e=>async t=>{let i=g.get(t);if(!i){t.startNode.isConnected||await Promise.resolve();const{renderItem:s,layout:n,scrollTarget:r,useShadowDOM:a}=e;i=new _({part:t,renderItem:s,layout:n,scrollTarget:r,useShadowDOM:a}),g.set(t,i)}Object.assign(i,{items:e.items,totalItems:void 0===e.totalItems?null:e.totalItems,scrollToIndex:void 0===e.scrollToIndex?null:e.scrollToIndex})});i(270),i(274);var y=i(16),b=i(0);let w=class extends b.a{constructor(){super(),this.renderRoot=this}get renderItem(){return this._renderItem}set renderItem(e){e!==this.renderItem&&(this._renderItem=e,this.requestUpdate())}async scrollToIndex(e,t="start"){this._scrollToIndex={index:e,position:t},this.requestUpdate(),await this.updateComplete,this._scrollToIndex=null}render(){return b.f`${v({items:this.items,renderItem:this._renderItem,scrollTarget:this.scrollTarget,scrollToIndex:this._scrollToIndex,useShadowDOM:!0})}`}};y.b([Object(b.g)()],w.prototype,"_renderItem",void 0),y.b([Object(b.g)()],w.prototype,"items",void 0),y.b([Object(b.g)()],w.prototype,"scrollTarget",void 0),w=y.b([Object(b.d)("lit-virtualizer")],w),i.d(t,"a",function(){return v})},474:function(e,t,i){"use strict";i(411);var s=i(4);const n=s.a`<dom-module id="material-date-picker-overlay" theme-for="vaadin-date-picker-overlay">
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
</dom-module>`;document.head.appendChild(n.content);var r=i(425),a=i(413);class o extends(Object(a.a)(r.a)){static get is(){return"vaadin-date-picker-overlay"}}customElements.define(o.is,o);i(227),i(269),i(265),i(412);const l=s.a`<dom-module id="material-button" theme-for="vaadin-button">
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
</dom-module>`;document.head.appendChild(l.content);var h=i(32),d=i(54),c=i(239);const u=e=>(class extends((e=>(class extends e{static get properties(){var e={tabindex:{type:Number,value:0,reflectToAttribute:!0,observer:"_tabindexChanged"}};return window.ShadyDOM&&(e.tabIndex=e.tabindex),e}}))(e)){static get properties(){return{autofocus:{type:Boolean},_previousTabIndex:{type:Number},disabled:{type:Boolean,observer:"_disabledChanged",reflectToAttribute:!0},_isShiftTabbing:{type:Boolean}}}ready(){this.addEventListener("focusin",e=>{e.composedPath()[0]===this?this._focus(e):-1===e.composedPath().indexOf(this.focusElement)||this.disabled||this._setFocused(!0)}),this.addEventListener("focusout",e=>this._setFocused(!1)),super.ready();const e=e=>{e.composed||e.target.dispatchEvent(new CustomEvent(e.type,{bubbles:!0,composed:!0,cancelable:!1}))};this.shadowRoot.addEventListener("focusin",e),this.shadowRoot.addEventListener("focusout",e),this.addEventListener("keydown",e=>{if(!e.defaultPrevented&&9===e.keyCode)if(e.shiftKey)this._isShiftTabbing=!0,HTMLElement.prototype.focus.apply(this),this._setFocused(!1),setTimeout(()=>this._isShiftTabbing=!1,0);else{const e=window.navigator.userAgent.match(/Firefox\/(\d\d\.\d)/);if(e&&parseFloat(e[1])>=63&&parseFloat(e[1])<66&&this.parentNode&&this.nextSibling){const e=document.createElement("input");e.style.position="absolute",e.style.opacity=0,e.tabIndex=this.tabIndex,this.parentNode.insertBefore(e,this.nextSibling),e.focus(),e.addEventListener("focusout",()=>this.parentNode.removeChild(e))}}}),!this.autofocus||this.focused||this.disabled||window.requestAnimationFrame(()=>{this._focus(),this._setFocused(!0),this.setAttribute("focus-ring","")}),this._boundKeydownListener=this._bodyKeydownListener.bind(this),this._boundKeyupListener=this._bodyKeyupListener.bind(this)}connectedCallback(){super.connectedCallback(),document.body.addEventListener("keydown",this._boundKeydownListener,!0),document.body.addEventListener("keyup",this._boundKeyupListener,!0)}disconnectedCallback(){super.disconnectedCallback(),document.body.removeEventListener("keydown",this._boundKeydownListener,!0),document.body.removeEventListener("keyup",this._boundKeyupListener,!0),this.hasAttribute("focused")&&this._setFocused(!1)}_setFocused(e){e?this.setAttribute("focused",""):this.removeAttribute("focused"),e&&this._tabPressed?this.setAttribute("focus-ring",""):this.removeAttribute("focus-ring")}_bodyKeydownListener(e){this._tabPressed=9===e.keyCode}_bodyKeyupListener(){this._tabPressed=!1}get focusElement(){return window.console.warn(`Please implement the 'focusElement' property in <${this.localName}>`),this}_focus(e){this._isShiftTabbing||(this.focusElement.focus(),this._setFocused(!0))}focus(){this.focusElement&&!this.disabled&&(this.focusElement.focus(),this._setFocused(!0))}blur(){this.focusElement.blur(),this._setFocused(!1)}_disabledChanged(e){this.focusElement.disabled=e,e?(this.blur(),this._previousTabIndex=this.tabindex,this.tabindex=-1,this.setAttribute("aria-disabled","true")):(void 0!==this._previousTabIndex&&(this.tabindex=this._previousTabIndex),this.removeAttribute("aria-disabled"))}_tabindexChanged(e){void 0!==e&&(this.focusElement.tabIndex=e),this.disabled&&this.tabindex&&(-1!==this.tabindex&&(this._previousTabIndex=this.tabindex),this.tabindex=e=void 0),window.ShadyDOM&&this.setProperties({tabIndex:e,tabindex:e})}click(){this.disabled||super.click()}});var p=i(11),m=i(22),f=i(24);const _=/\/\*\*\s+vaadin-dev-mode:start([\s\S]*)vaadin-dev-mode:end\s+\*\*\//i,g=window.Vaadin&&window.Vaadin.Flow&&window.Vaadin.Flow.clients;function v(e,t){if("function"!=typeof e)return;const i=_.exec(e.toString());if(i)try{e=new Function(i[1])}catch(s){console.log("vaadin-development-mode-detector: uncommentAndRun() failed",s)}return e(t)}window.Vaadin=window.Vaadin||{};const y=function(e,t){if(window.Vaadin.developmentMode)return v(e,t)};function b(){}void 0===window.Vaadin.developmentMode&&(window.Vaadin.developmentMode=function(){try{return!!localStorage.getItem("vaadin.developmentmode.force")||["localhost","127.0.0.1"].indexOf(window.location.hostname)>=0&&(g?!function(){if(g){const e=Object.keys(g).map(e=>g[e]).filter(e=>e.productionMode);if(e.length>0)return!0}return!1}():!v(function(){return!0}))}catch(e){return!1}}());const w=function(){return y(b)};let x;window.Vaadin||(window.Vaadin={}),window.Vaadin.registrations=window.Vaadin.registrations||[],window.Vaadin.developmentModeCallback=window.Vaadin.developmentModeCallback||{},window.Vaadin.developmentModeCallback["vaadin-usage-statistics"]=function(){w&&w()};const k=e=>(class extends e{static _finalizeClass(){super._finalizeClass(),this.is&&(window.Vaadin.registrations.push(this),window.Vaadin.developmentModeCallback&&(x=m.a.debounce(x,p.b,()=>{window.Vaadin.developmentModeCallback["vaadin-usage-statistics"]()}),Object(f.a)(x)))}ready(){super.ready(),null===document.doctype&&console.warn('Vaadin components require the "standards mode" declaration. Please add <!DOCTYPE html> to the HTML document.')}});var D=i(39);class E extends(k(u(Object(c.a)(Object(d.a)(h.a))))){static get template(){return s.a`
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
`}static get is(){return"vaadin-button"}static get version(){return"2.2.1"}ready(){super.ready(),this.setAttribute("role","button"),this.$.button.setAttribute("role","presentation"),this._addActiveListeners()}disconnectedCallback(){super.disconnectedCallback(),this.hasAttribute("active")&&this.removeAttribute("active")}_addActiveListeners(){Object(D.b)(this,"down",()=>!this.disabled&&this.setAttribute("active","")),Object(D.b)(this,"up",()=>this.removeAttribute("active")),this.addEventListener("keydown",e=>!this.disabled&&[13,32].indexOf(e.keyCode)>=0&&this.setAttribute("active","")),this.addEventListener("keyup",()=>this.removeAttribute("active")),this.addEventListener("blur",()=>this.removeAttribute("active"))}get focusElement(){return this.$.button}}customElements.define(E.is,E);const S=s.a`<dom-module id="material-date-picker-overlay-content" theme-for="vaadin-date-picker-overlay-content">
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
</dom-module>`;document.head.appendChild(S.content);i(148);var C=i(33),T=i(102),I=i(350);i(97);const M=class{static _getISOWeekNumber(e){var t=e.getDay();0===t&&(t=7);var i=4-t,s=new Date(e.getTime()+24*i*3600*1e3),n=new Date(0,0);n.setFullYear(s.getFullYear());var r=s.getTime()-n.getTime(),a=Math.round(r/864e5);return Math.floor(a/7+1)}static _dateEquals(e,t){return e instanceof Date&&t instanceof Date&&e.getFullYear()===t.getFullYear()&&e.getMonth()===t.getMonth()&&e.getDate()===t.getDate()}static _dateAllowed(e,t,i){return(!t||e>=t)&&(!i||e<=i)}static _getClosestDate(e,t){return t.filter(e=>void 0!==e).reduce((t,i)=>{return i?t?Math.abs(e.getTime()-i.getTime())<Math.abs(t.getTime()-e.getTime())?i:t:i:t})}static _extractDateParts(e){return{day:e.getDate(),month:e.getMonth(),year:e.getFullYear()}}};class O extends(Object(c.a)(Object(d.a)(h.a))){static get template(){return s.a`
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
`}static get is(){return"vaadin-month-calendar"}static get properties(){return{month:{type:Date,value:new Date},selectedDate:{type:Date,notify:!0},focusedDate:Date,showWeekNumbers:{type:Boolean,value:!1},i18n:{type:Object},ignoreTaps:Boolean,_notTapping:Boolean,minDate:{type:Date,value:null},maxDate:{type:Date,value:null},_days:{type:Array,computed:"_getDays(month, i18n.firstDayOfWeek, minDate, maxDate)"},disabled:{type:Boolean,reflectToAttribute:!0,computed:"_isDisabled(month, minDate, maxDate)"}}}static get observers(){return["_showWeekNumbersChanged(showWeekNumbers, i18n.firstDayOfWeek)"]}_dateEquals(e,t){return M._dateEquals(e,t)}_dateAllowed(e,t,i){return M._dateAllowed(e,t,i)}_isDisabled(e,t,i){var s=new Date(0,0);s.setFullYear(e.getFullYear()),s.setMonth(e.getMonth()),s.setDate(1);var n=new Date(0,0);return n.setFullYear(e.getFullYear()),n.setMonth(e.getMonth()+1),n.setDate(0),!(t&&i&&t.getMonth()===i.getMonth()&&t.getMonth()===e.getMonth()&&i.getDate()-t.getDate()>=0)&&(!this._dateAllowed(s,t,i)&&!this._dateAllowed(n,t,i))}_getTitle(e,t){if(void 0!==e&&void 0!==t)return this.i18n.formatTitle(t[e.getMonth()],e.getFullYear())}_onMonthGridTouchStart(){this._notTapping=!1,setTimeout(()=>this._notTapping=!0,300)}_dateAdd(e,t){e.setDate(e.getDate()+t)}_applyFirstDayOfWeek(e,t){if(void 0!==e&&void 0!==t)return e.slice(t).concat(e.slice(0,t))}_getWeekDayNames(e,t,i,s){if(void 0!==e&&void 0!==t&&void 0!==i&&void 0!==s)return e=this._applyFirstDayOfWeek(e,s),t=this._applyFirstDayOfWeek(t,s),e=e.map((e,i)=>({weekDay:e,weekDayShort:t[i]}))}_getDate(e){return e?e.getDate():""}_showWeekNumbersChanged(e,t){e&&1===t?this.setAttribute("week-numbers",""):this.removeAttribute("week-numbers")}_showWeekSeparator(e,t){return e&&1===t}_isToday(e){return this._dateEquals(new Date,e)}_getDays(e,t){if(void 0!==e&&void 0!==t){var i=new Date(0,0);for(i.setFullYear(e.getFullYear()),i.setMonth(e.getMonth()),i.setDate(1);i.getDay()!==t;)this._dateAdd(i,-1);for(var s=[],n=i.getMonth(),r=e.getMonth();i.getMonth()===r||i.getMonth()===n;)s.push(i.getMonth()===r?new Date(i.getTime()):null),this._dateAdd(i,1);return s}}_getWeekNumber(e,t){if(void 0!==e&&void 0!==t)return e||(e=t.reduce((e,t)=>!e&&t?t:e)),M._getISOWeekNumber(e)}_getWeekNumbers(e){return e.map(t=>this._getWeekNumber(t,e)).filter((e,t,i)=>i.indexOf(e)===t)}_handleTap(e){this.ignoreTaps||this._notTapping||!e.target.date||e.target.hasAttribute("disabled")||(this.selectedDate=e.target.date,this.dispatchEvent(new CustomEvent("date-tap",{bubbles:!0,composed:!0})))}_preventDefault(e){e.preventDefault()}_getRole(e){return e?"button":"presentation"}_getAriaLabel(e){if(!e)return"";var t=this._getDate(e)+" "+this.i18n.monthNames[e.getMonth()]+" "+e.getFullYear()+", "+this.i18n.weekdays[e.getDay()];return this._isToday(e)&&(t+=", "+this.i18n.today),t}_getAriaDisabled(e,t,i){if(void 0!==e&&void 0!==t&&void 0!==i)return this._dateAllowed(e,t,i)?"false":"true"}}customElements.define(O.is,O);var z=i(34),A=i(66);class P extends h.a{static get template(){return s.a`
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
`}static get is(){return"vaadin-infinite-scroller"}static get properties(){return{bufferSize:{type:Number,value:20},_initialScroll:{value:5e5},_initialIndex:{value:0},_buffers:Array,_preventScrollEvent:Boolean,_mayHaveMomentum:Boolean,_initialized:Boolean,active:{type:Boolean,observer:"_activated"}}}ready(){super.ready(),this._buffers=Array.prototype.slice.call(this.root.querySelectorAll(".buffer")),this.$.fullHeight.style.height=2*this._initialScroll+"px";var e=this.querySelector("template");this._TemplateClass=Object(z.b)(e,this,{forwardHostProp:function(e,t){"index"!==e&&this._buffers.forEach(i=>{[].forEach.call(i.children,i=>{i._itemWrapper.instance[e]=t})})}}),navigator.userAgent.toLowerCase().indexOf("firefox")>-1&&(this.$.scroller.tabIndex=-1)}_activated(e){e&&!this._initialized&&(this._createPool(),this._initialized=!0)}_finishInit(){this._initDone||(this._buffers.forEach(e=>{[].forEach.call(e.children,e=>this._ensureStampedInstance(e._itemWrapper))},this),this._buffers[0].translateY||this._reset(),this._initDone=!0)}_translateBuffer(e){var t=e?1:0;this._buffers[t].translateY=this._buffers[t?0:1].translateY+this._bufferHeight*(t?-1:1),this._buffers[t].style.transform="translate3d(0, "+this._buffers[t].translateY+"px, 0)",this._buffers[t].updated=!1,this._buffers.reverse()}_scroll(){if(!this._scrollDisabled){var e=this.$.scroller.scrollTop;(e<this._bufferHeight||e>2*this._initialScroll-this._bufferHeight)&&(this._initialIndex=~~this.position,this._reset());var t=this.root.querySelector(".buffer").offsetTop,i=e>this._buffers[1].translateY+this.itemHeight+t,s=e<this._buffers[0].translateY+this.itemHeight+t;(i||s)&&(this._translateBuffer(s),this._updateClones()),this._preventScrollEvent||(this.dispatchEvent(new CustomEvent("custom-scroll",{bubbles:!1,composed:!0})),this._mayHaveMomentum=!0),this._preventScrollEvent=!1,this._debouncerScrollFinish=m.a.debounce(this._debouncerScrollFinish,p.d.after(200),()=>{var e=this.$.scroller.getBoundingClientRect();this._isVisible(this._buffers[0],e)||this._isVisible(this._buffers[1],e)||(this.position=this.position)})}}set position(e){this._preventScrollEvent=!0,e>this._firstIndex&&e<this._firstIndex+2*this.bufferSize?this.$.scroller.scrollTop=this.itemHeight*(e-this._firstIndex)+this._buffers[0].translateY:(this._initialIndex=~~e,this._reset(),this._scrollDisabled=!0,this.$.scroller.scrollTop+=e%1*this.itemHeight,this._scrollDisabled=!1),this._mayHaveMomentum&&(this.$.scroller.classList.add("notouchscroll"),this._mayHaveMomentum=!1,setTimeout(()=>{this.$.scroller.classList.remove("notouchscroll")},10))}get position(){return(this.$.scroller.scrollTop-this._buffers[0].translateY)/this.itemHeight+this._firstIndex}get itemHeight(){if(!this._itemHeightVal){window.ShadyCSS&&window.ShadyCSS.nativeCss||this.updateStyles();const e=window.ShadyCSS?window.ShadyCSS.getComputedStyleValue(this,"--vaadin-infinite-scroller-item-height"):getComputedStyle(this).getPropertyValue("--vaadin-infinite-scroller-item-height"),t="background-position";this.$.fullHeight.style.setProperty(t,e);const i=getComputedStyle(this.$.fullHeight).getPropertyValue(t);this.$.fullHeight.style.removeProperty(t),this._itemHeightVal=parseFloat(i)}return this._itemHeightVal}get _bufferHeight(){return this.itemHeight*this.bufferSize}_reset(){this._scrollDisabled=!0,this.$.scroller.scrollTop=this._initialScroll,this._buffers[0].translateY=this._initialScroll-this._bufferHeight,this._buffers[1].translateY=this._initialScroll,this._buffers.forEach(e=>{e.style.transform="translate3d(0, "+e.translateY+"px, 0)"}),this._buffers[0].updated=this._buffers[1].updated=!1,this._updateClones(!0),this._debouncerUpdateClones=m.a.debounce(this._debouncerUpdateClones,p.d.after(200),()=>{this._buffers[0].updated=this._buffers[1].updated=!1,this._updateClones()}),this._scrollDisabled=!1}_createPool(){var e=this.getBoundingClientRect();this._buffers.forEach(t=>{for(var i=0;i<this.bufferSize;i++){const i=document.createElement("div");i.style.height=this.itemHeight+"px",i.instance={};const s="vaadin-infinite-scroller-item-content-"+(P._contentIndex=P._contentIndex+1||0),n=document.createElement("slot");n.setAttribute("name",s),n._itemWrapper=i,t.appendChild(n),i.setAttribute("slot",s),this.appendChild(i),Object(f.b)(),setTimeout(()=>{this._isVisible(i,e)&&this._ensureStampedInstance(i)},1)}},this),setTimeout(()=>{Object(A.a)(this,this._finishInit.bind(this))},1)}_ensureStampedInstance(e){if(!e.firstElementChild){var t=e.instance;e.instance=new this._TemplateClass({}),e.appendChild(e.instance.root),Object.keys(t).forEach(i=>{e.instance.set(i,t[i])})}}_updateClones(e){this._firstIndex=~~((this._buffers[0].translateY-this._initialScroll)/this.itemHeight)+this._initialIndex;var t=e?this.$.scroller.getBoundingClientRect():void 0;this._buffers.forEach((i,s)=>{if(!i.updated){var n=this._firstIndex+this.bufferSize*s;[].forEach.call(i.children,(i,s)=>{const r=i._itemWrapper;e&&!this._isVisible(r,t)||(r.instance.index=n+s)}),i.updated=!0}},this)}_isVisible(e,t){var i=e.getBoundingClientRect();return i.bottom>t.top&&i.top<t.bottom}}customElements.define(P.is,P);i(81);const L=document.createElement("template");L.innerHTML='<dom-module id="vaadin-date-picker-overlay-styles" theme-for="vaadin-date-picker-overlay">\n  <template>\n    <style>\n      :host {\n        align-items: flex-start;\n        justify-content: flex-start;\n      }\n\n      :host([bottom-aligned]) {\n        justify-content: flex-end;\n      }\n\n      :host([right-aligned]) {\n        align-items: flex-end;\n      }\n\n      :host([right-aligned][dir="rtl"]) {\n        align-items: flex-start;\n      }\n\n      [part="overlay"] {\n        display: flex;\n        flex: auto;\n      }\n\n      [part~="content"] {\n        flex: auto;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(L.content);class F extends(Object(c.a)(Object(I.a)(Object(d.a)(h.a)))){static get template(){return s.a`
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
`}static get is(){return"vaadin-date-picker-overlay-content"}static get properties(){return{selectedDate:{type:Date,notify:!0},focusedDate:{type:Date,notify:!0,observer:"_focusedDateChanged"},_focusedMonthDate:Number,initialPosition:{type:Date,observer:"_initialPositionChanged"},_originDate:{value:new Date},_visibleMonthIndex:Number,_desktopMode:Boolean,_translateX:{observer:"_translateXChanged"},_yearScrollerWidth:{value:50},i18n:{type:Object},showWeekNumbers:{type:Boolean},_ignoreTaps:Boolean,_notTapping:Boolean,minDate:Date,maxDate:Date,_focused:Boolean,label:String}}ready(){super.ready(),this.setAttribute("tabindex",0),this.addEventListener("keydown",this._onKeydown.bind(this)),Object(D.b)(this,"tap",this._stopPropagation),this.addEventListener("focus",this._onOverlayFocus.bind(this)),this.addEventListener("blur",this._onOverlayBlur.bind(this))}connectedCallback(){super.connectedCallback(),this._closeYearScroller(),this._toggleAnimateClass(!0),Object(D.e)(this.$.scrollers,"pan-y"),T.a.requestAvailability()}announceFocusedDate(){var e=this._currentlyFocusedDate(),t=[];M._dateEquals(e,new Date)&&t.push(this.i18n.today),t=t.concat([this.i18n.weekdays[e.getDay()],e.getDate(),this.i18n.monthNames[e.getMonth()],e.getFullYear()]),this.showWeekNumbers&&1===this.i18n.firstDayOfWeek&&(t.push(this.i18n.week),t.push(M._getISOWeekNumber(e))),this.dispatchEvent(new CustomEvent("iron-announce",{bubbles:!0,composed:!0,detail:{text:t.join(" ")}}))}focusCancel(){this.$.cancelButton.focus()}scrollToDate(e,t){this._scrollToPosition(this._differenceInMonths(e,this._originDate),t)}_focusedDateChanged(e){this.revealDate(e)}_isCurrentYear(e){return 0===e}_isSelectedYear(e,t){if(t)return t.getFullYear()===this._originDate.getFullYear()+e}revealDate(e){if(e){var t=this._differenceInMonths(e,this._originDate),i=this.$.monthScroller.position>t,s=this.$.monthScroller.clientHeight/this.$.monthScroller.itemHeight,n=this.$.monthScroller.position+s-1<t;i?this._scrollToPosition(t,!0):n&&this._scrollToPosition(t-s+1,!0)}}_onOverlayFocus(){this._focused=!0}_onOverlayBlur(){this._focused=!1}_initialPositionChanged(e){this.scrollToDate(e)}_repositionYearScroller(){this._visibleMonthIndex=Math.floor(this.$.monthScroller.position),this.$.yearScroller.position=(this.$.monthScroller.position+this._originDate.getMonth())/12}_repositionMonthScroller(){this.$.monthScroller.position=12*this.$.yearScroller.position-this._originDate.getMonth(),this._visibleMonthIndex=Math.floor(this.$.monthScroller.position)}_onMonthScroll(){this._repositionYearScroller(),this._doIgnoreTaps()}_onYearScroll(){this._repositionMonthScroller(),this._doIgnoreTaps()}_onYearScrollTouchStart(){this._notTapping=!1,setTimeout(()=>this._notTapping=!0,300),this._repositionMonthScroller()}_onMonthScrollTouchStart(){this._repositionYearScroller()}_doIgnoreTaps(){this._ignoreTaps=!0,this._debouncer=m.a.debounce(this._debouncer,p.d.after(300),()=>this._ignoreTaps=!1)}_formatDisplayed(e,t,i){return e?t(M._extractDateParts(e)):i}_onTodayTap(){var e=new Date;Math.abs(this.$.monthScroller.position-this._differenceInMonths(e,this._originDate))<.001?(this.selectedDate=e,this._close()):this._scrollToCurrentMonth()}_scrollToCurrentMonth(){this.focusedDate&&(this.focusedDate=new Date),this.scrollToDate(new Date,!0)}_showClear(e){return!!e}_onYearTap(e){if(!this._ignoreTaps&&!this._notTapping){var t=(e.detail.y-(this.$.yearScroller.getBoundingClientRect().top+this.$.yearScroller.clientHeight/2))/this.$.yearScroller.itemHeight;this._scrollToPosition(this.$.monthScroller.position+12*t,!0)}}_scrollToPosition(e,t){if(void 0===this._targetPosition){if(!t)return this.$.monthScroller.position=e,this._targetPosition=void 0,void this._repositionYearScroller();this._targetPosition=e;var i=t?300:0,s=0,n=this.$.monthScroller.position,r=e=>{var t=e-(s=s||e);if(t<i){var a=((e,t,i,s)=>(e/=s/2)<1?i/2*e*e+t:-i/2*(--e*(e-2)-1)+t)(t,n,this._targetPosition-n,i);this.$.monthScroller.position=a,window.requestAnimationFrame(r)}else this.dispatchEvent(new CustomEvent("scroll-animation-finished",{bubbles:!0,composed:!0,detail:{position:this._targetPosition,oldPosition:n}})),this.$.monthScroller.position=this._targetPosition,this._targetPosition=void 0;setTimeout(this._repositionYearScroller.bind(this),1)};window.requestAnimationFrame(r)}else this._targetPosition=e}_limit(e,t){return Math.min(t.max,Math.max(t.min,e))}_handleTrack(e){if(!(Math.abs(e.detail.dx)<10||Math.abs(e.detail.ddy)>10)){Math.abs(e.detail.ddx)>this._yearScrollerWidth/3&&this._toggleAnimateClass(!0);var t=this._translateX+e.detail.ddx;this._translateX=this._limit(t,{min:0,max:this._yearScrollerWidth})}}_track(e){if(!this._desktopMode)switch(e.detail.state){case"start":this._toggleAnimateClass(!1);break;case"track":this._handleTrack(e);break;case"end":this._toggleAnimateClass(!0),this._translateX>=this._yearScrollerWidth/2?this._closeYearScroller():this._openYearScroller()}}_toggleAnimateClass(e){e?this.classList.add("animate"):this.classList.remove("animate")}_toggleYearScroller(){this._isYearScrollerVisible()?this._closeYearScroller():this._openYearScroller()}_openYearScroller(){this._translateX=0,this.setAttribute("years-visible","")}_closeYearScroller(){this.removeAttribute("years-visible"),this._translateX=this._yearScrollerWidth}_isYearScrollerVisible(){return this._translateX<this._yearScrollerWidth/2}_translateXChanged(e){this._desktopMode||(this.$.monthScroller.style.transform="translateX("+(e-this._yearScrollerWidth)+"px)",this.$.yearScroller.style.transform="translateX("+e+"px)")}_yearAfterXYears(e){var t=new Date(this._originDate);return t.setFullYear(parseInt(e)+this._originDate.getFullYear()),t.getFullYear()}_yearAfterXMonths(e){return this._dateAfterXMonths(e).getFullYear()}_dateAfterXMonths(e){var t=new Date(this._originDate);return t.setDate(1),t.setMonth(parseInt(e)+this._originDate.getMonth()),t}_differenceInMonths(e,t){return 12*(e.getFullYear()-t.getFullYear())-t.getMonth()+e.getMonth()}_differenceInYears(e,t){return this._differenceInMonths(e,t)/12}_clear(){this.selectedDate=""}_close(){const e=this.getRootNode().host,t=e?e.getRootNode().host:null;t&&(t.opened=!1),this.dispatchEvent(new CustomEvent("close",{bubbles:!0,composed:!0}))}_cancel(){this.focusedDate=this.selectedDate,this._close()}_preventDefault(e){e.preventDefault()}_eventKey(e){for(var t=["down","up","right","left","enter","space","home","end","pageup","pagedown","tab","esc"],i=0;i<t.length;i++){var s=t[i];if(C.a.keyboardEventMatchesKeys(e,s))return s}}_onKeydown(e){var t=this._currentlyFocusedDate();const i=e.composedPath().indexOf(this.$.todayButton)>=0,s=e.composedPath().indexOf(this.$.cancelButton)>=0,n=!i&&!s;var r=this._eventKey(e);if("tab"===r){e.stopPropagation();const t=this.hasAttribute("fullscreen"),r=e.shiftKey;t?e.preventDefault():r&&n||!r&&s?(e.preventDefault(),this.dispatchEvent(new CustomEvent("focus-input",{bubbles:!0,composed:!0}))):r&&i?(this._focused=!0,setTimeout(()=>this.revealDate(this.focusedDate),1)):this._focused=!1}else if(r)switch(e.preventDefault(),e.stopPropagation(),r){case"down":this._moveFocusByDays(7),this.focus();break;case"up":this._moveFocusByDays(-7),this.focus();break;case"right":n&&this._moveFocusByDays(1);break;case"left":n&&this._moveFocusByDays(-1);break;case"enter":n||s?this._close():i&&this._onTodayTap();break;case"space":if(s)this._close();else if(i)this._onTodayTap();else{var a=this.focusedDate;M._dateEquals(a,this.selectedDate)?(this.selectedDate="",this.focusedDate=a):this.selectedDate=a}break;case"home":this._moveFocusInsideMonth(t,"minDate");break;case"end":this._moveFocusInsideMonth(t,"maxDate");break;case"pagedown":this._moveFocusByMonths(e.shiftKey?12:1);break;case"pageup":this._moveFocusByMonths(e.shiftKey?-12:-1);break;case"esc":this._cancel()}}_currentlyFocusedDate(){return this.focusedDate||this.selectedDate||this.initialPosition||new Date}_focusDate(e){this.focusedDate=e,this._focusedMonthDate=e.getDate()}_focusClosestDate(e){this._focusDate(M._getClosestDate(e,[this.minDate,this.maxDate]))}_moveFocusByDays(e){var t=this._currentlyFocusedDate(),i=new Date(0,0);i.setFullYear(t.getFullYear()),i.setMonth(t.getMonth()),i.setDate(t.getDate()+e),this._dateAllowed(i,this.minDate,this.maxDate)?this._focusDate(i):this._dateAllowed(t,this.minDate,this.maxDate)?e>0?this._focusDate(this.maxDate):this._focusDate(this.minDate):this._focusClosestDate(t)}_moveFocusByMonths(e){var t=this._currentlyFocusedDate(),i=new Date(0,0);i.setFullYear(t.getFullYear()),i.setMonth(t.getMonth()+e);var s=i.getMonth();i.setDate(this._focusedMonthDate||(this._focusedMonthDate=t.getDate())),i.getMonth()!==s&&i.setDate(0),this._dateAllowed(i,this.minDate,this.maxDate)?this.focusedDate=i:this._dateAllowed(t,this.minDate,this.maxDate)?e>0?this._focusDate(this.maxDate):this._focusDate(this.minDate):this._focusClosestDate(t)}_moveFocusInsideMonth(e,t){var i=new Date(0,0);i.setFullYear(e.getFullYear()),"minDate"===t?(i.setMonth(e.getMonth()),i.setDate(1)):(i.setMonth(e.getMonth()+1),i.setDate(0)),this._dateAllowed(i,this.minDate,this.maxDate)?this._focusDate(i):this._dateAllowed(e,this.minDate,this.maxDate)?this._focusDate(this[t]):this._focusClosestDate(e)}_dateAllowed(e,t,i){return(!t||e>=t)&&(!i||e<=i)}_isTodayAllowed(e,t){var i=new Date,s=new Date(0,0);return s.setFullYear(i.getFullYear()),s.setMonth(i.getMonth()),s.setDate(i.getDate()),this._dateAllowed(s,e,t)}_stopPropagation(e){e.stopPropagation()}}customElements.define(F.is,F);const $=s.a`<dom-module id="material-date-picker-month-calendar" theme-for="vaadin-month-calendar">
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
</dom-module>`;document.head.appendChild($.content);const R=document.createElement("template");R.innerHTML='<dom-module id="material-required-field">\n  <template>\n    <style>\n      [part="label"] {\n        display: block;\n        position: absolute;\n        top: 8px;\n        font-size: 1em;\n        line-height: 1;\n        height: 20px;\n        margin-bottom: -4px;\n        white-space: nowrap;\n        overflow-x: hidden;\n        text-overflow: ellipsis;\n        color: var(--material-secondary-text-color);\n        transform-origin: 0 75%;\n        transform: scale(0.75);\n      }\n\n      :host([required]) [part="label"]::after {\n        content: " *";\n        color: inherit;\n      }\n\n      :host([invalid]) [part="label"] {\n        color: var(--material-error-text-color);\n      }\n\n      [part="error-message"] {\n        font-size: .75em;\n        line-height: 1;\n        color: var(--material-error-text-color);\n      }\n\n      /* Margin that doesn’t reserve space when there’s no error message */\n      [part="error-message"]:not(:empty)::before {\n        content: "";\n        display: block;\n        height: 6px;\n      }\n\n      :host(:not([invalid])) [part="error-message"] {\n        margin-top: 0;\n        max-height: 0;\n        overflow: hidden;\n      }\n\n      :host([invalid]) [part="error-message"] {\n        animation: reveal 0.2s;\n      }\n\n      @keyframes reveal {\n        0% {\n          opacity: 0;\n        }\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(R.content);const j=document.createElement("template");j.innerHTML='<dom-module id="material-field-button">\n  <template>\n    <style>\n      /* TODO(platosha): align icon sizes with other elements */\n      [part$="button"] {\n        flex: none;\n        width: 24px;\n        height: 24px;\n        padding: 4px;\n        color: var(--material-secondary-text-color);\n        font-size: var(--material-icon-font-size);\n        line-height: 24px;\n        text-align: center;\n      }\n\n      :host(:not([readonly])) [part$="button"] {\n        cursor: pointer;\n      }\n\n      :host(:not([readonly])) [part$="button"]:hover {\n        color: var(--material-text-color);\n      }\n\n      :host([disabled]) [part$="button"],\n      :host([readonly]) [part$="button"] {\n        color: var(--material-disabled-text-color);\n      }\n\n      :host([disabled]) [part="clear-button"] {\n        display: none;\n      }\n\n      [part$="button"]::before {\n        font-family: "material-icons";\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(j.content);const V=s.a`<dom-module id="material-text-field" theme-for="vaadin-text-field">
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
</dom-module>`;document.head.appendChild(V.content);const N=document.createElement("template");N.innerHTML='<dom-module id="vaadin-text-field-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: inline-flex;\n        outline: none;\n      }\n\n      :host::before {\n        content: "\\2003";\n        width: 0;\n        display: inline-block;\n        /* Size and position this element on the same vertical position as the input-field element\n           to make vertical align for the host element work as expected */\n      }\n\n      :host([hidden]) {\n        display: none !important;\n      }\n\n      .vaadin-text-field-container,\n      .vaadin-text-area-container {\n        display: flex;\n        flex-direction: column;\n        min-width: 100%;\n        max-width: 100%;\n        width: var(--vaadin-text-field-default-width, 12em);\n      }\n\n      [part="label"]:empty {\n        display: none;\n      }\n\n      [part="input-field"] {\n        display: flex;\n        align-items: center;\n        flex: auto;\n      }\n\n      .vaadin-text-field-container [part="input-field"] {\n        flex-grow: 0;\n      }\n\n      /* Reset the native input styles */\n      [part="value"],\n      [part="input-field"] ::slotted(input),\n      [part="input-field"] ::slotted(textarea) {\n        -webkit-appearance: none;\n        -moz-appearance: none;\n        outline: none;\n        margin: 0;\n        padding: 0;\n        border: 0;\n        border-radius: 0;\n        min-width: 0;\n        font: inherit;\n        font-size: 1em;\n        line-height: normal;\n        color: inherit;\n        background-color: transparent;\n        /* Disable default invalid style in Firefox */\n        box-shadow: none;\n      }\n\n      [part="input-field"] ::slotted(*) {\n        flex: none;\n      }\n\n      [part="value"],\n      [part="input-field"] ::slotted(input),\n      [part="input-field"] ::slotted(textarea),\n      /* Slotted by vaadin-select-text-field */\n      [part="input-field"] ::slotted([part="value"]) {\n        flex: auto;\n        white-space: nowrap;\n        overflow: hidden;\n        width: 100%;\n        height: 100%;\n      }\n\n      [part="input-field"] ::slotted(textarea) {\n        resize: none;\n      }\n\n      [part="value"]::-ms-clear,\n      [part="input-field"] ::slotted(input)::-ms-clear {\n        display: none;\n      }\n\n      [part="clear-button"] {\n        cursor: default;\n      }\n\n      [part="clear-button"]::before {\n        content: "✕";\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(N.content);const B={default:["list","autofocus","pattern","autocapitalize","autocorrect","maxlength","minlength","name","placeholder","autocomplete","title"],accessible:["disabled","readonly","required","invalid"]},Y={DEFAULT:"default",ACCESSIBLE:"accessible"},H=e=>(class extends(u(e)){static get properties(){return{autocomplete:{type:String},autocorrect:{type:String},autocapitalize:{type:String},autoselect:{type:Boolean,value:!1},clearButtonVisible:{type:Boolean,value:!1},errorMessage:{type:String,value:""},label:{type:String,value:"",observer:"_labelChanged"},maxlength:{type:Number},minlength:{type:Number},name:{type:String},placeholder:{type:String},readonly:{type:Boolean,reflectToAttribute:!0},required:{type:Boolean,reflectToAttribute:!0},value:{type:String,value:"",observer:"_valueChanged",notify:!0},invalid:{type:Boolean,reflectToAttribute:!0,notify:!0,value:!1},hasValue:{type:Boolean,reflectToAttribute:!0},preventInvalidInput:{type:Boolean},_labelId:{type:String},_errorId:{type:String}}}static get observers(){return["_stateChanged(disabled, readonly, clearButtonVisible, hasValue)","_hostPropsChanged("+B.default.join(", ")+")","_hostAccessiblePropsChanged("+B.accessible.join(", ")+")","_getActiveErrorId(invalid, errorMessage, _errorId)","_getActiveLabelId(label, _labelId)"]}constructor(){super(),this._createMethodObserver("__constraintsChanged(required, minlength, maxlength, pattern, min, max, step)")}get focusElement(){if(!this.shadowRoot)return;const e=this.querySelector(`${this._slottedTagName}[slot="${this._slottedTagName}"]`);return e||this.shadowRoot.querySelector('[part="value"]')}get inputElement(){return this.focusElement}get _slottedTagName(){return"input"}_onInput(e){if(this.__preventInput)return e.stopImmediatePropagation(),void(this.__preventInput=!1);if(this.preventInvalidInput){const e=this.inputElement;if(e.value.length>0&&!this.checkValidity())return e.value=this.value||"",this.setAttribute("input-prevented",""),void(this._inputDebouncer=m.a.debounce(this._inputDebouncer,p.d.after(200),()=>{this.removeAttribute("input-prevented")}))}this.__userInput=!0,this.value=e.target.value}_stateChanged(e,t,i,s){!e&&!t&&i&&s?this.$.clearButton.removeAttribute("hidden"):this.$.clearButton.setAttribute("hidden",!0)}_onChange(e){if(this._valueClearing)return;const t=new CustomEvent("change",{detail:{sourceEvent:e},bubbles:e.bubbles,cancelable:e.cancelable});this.dispatchEvent(t)}_valueChanged(e,t){""===e&&void 0===t||(this.hasValue=""!==e&&null!=e,this.__userInput?this.__userInput=!1:(void 0!==e?this.inputElement.value=e:this.value=this.inputElement.value="",this.invalid&&this.validate()))}_labelChanged(e){""!==e&&null!=e?this.setAttribute("has-label",""):this.removeAttribute("has-label")}_onSlotChange(){const e=this.querySelector(`${this._slottedTagName}[slot="${this._slottedTagName}"]`);this.value&&(this.inputElement.value=this.value,this.validate()),e&&!this._slottedInput?(this._validateSlottedValue(e),this._addInputListeners(e),this._addIEListeners(e),this._slottedInput=e):!e&&this._slottedInput&&(this._removeInputListeners(this._slottedInput),this._removeIEListeners(this._slottedInput),this._slottedInput=void 0),Object.keys(Y).map(e=>Y[e]).forEach(e=>this._propagateHostAttributes(B[e].map(e=>this[e]),e))}_hostPropsChanged(...e){this._propagateHostAttributes(e,Y.DEFAULT)}_hostAccessiblePropsChanged(...e){this._propagateHostAttributes(e,Y.ACCESSIBLE)}_validateSlottedValue(e){e.value!==this.value&&(console.warn("Please define value on the vaadin-text-field component!"),e.value="")}_propagateHostAttributes(e,t){const i=this.inputElement,s=B[t];"accessible"===t?s.forEach((t,s)=>{this._setOrToggleAttribute(t,e[s],i),this._setOrToggleAttribute(`aria-${t}`,e[s],i)}):s.forEach((t,s)=>{this._setOrToggleAttribute(t,e[s],i)})}_setOrToggleAttribute(e,t,i){e&&i&&(t?i.setAttribute(e,"boolean"==typeof t?"":t):i.removeAttribute(e))}__constraintsChanged(e,t,i,s,n,r,a){if(!this.invalid)return;const o=e=>!e&&0!==e;e||t||i||s||!o(n)||!o(r)?this.validate():this.invalid=!1}checkValidity(){return this.required||this.pattern||this.maxlength||this.minlength?this.inputElement.checkValidity():!this.invalid}_addInputListeners(e){e.addEventListener("input",this._boundOnInput),e.addEventListener("change",this._boundOnChange),e.addEventListener("blur",this._boundOnBlur),e.addEventListener("focus",this._boundOnFocus)}_removeInputListeners(e){e.removeEventListener("input",this._boundOnInput),e.removeEventListener("change",this._boundOnChange),e.removeEventListener("blur",this._boundOnBlur),e.removeEventListener("focus",this._boundOnFocus)}ready(){super.ready(),this._boundOnInput=this._onInput.bind(this),this._boundOnChange=this._onChange.bind(this),this._boundOnBlur=this._onBlur.bind(this),this._boundOnFocus=this._onFocus.bind(this);const e=this.shadowRoot.querySelector('[part="value"]');this._slottedInput=this.querySelector(`${this._slottedTagName}[slot="${this._slottedTagName}"]`),this._addInputListeners(e),this._addIEListeners(e),this._slottedInput&&(this._addIEListeners(this._slottedInput),this._addInputListeners(this._slottedInput)),this.shadowRoot.querySelector('[name="input"], [name="textarea"]').addEventListener("slotchange",this._onSlotChange.bind(this)),window.ShadyCSS&&window.ShadyCSS.nativeCss||this.updateStyles(),this.$.clearButton.addEventListener("mousedown",()=>this._valueClearing=!0),this.$.clearButton.addEventListener("click",this._onClearButtonClick.bind(this)),this.addEventListener("keydown",this._onKeyDown.bind(this));var t=H._uniqueId=1+H._uniqueId||0;this._errorId=`${this.constructor.is}-error-${t}`,this._labelId=`${this.constructor.is}-label-${t}`}validate(){return!(this.invalid=!this.checkValidity())}clear(){this.value=""}_onBlur(){this.validate()}_onFocus(){this.autoselect&&(this.inputElement.select(),setTimeout(()=>{this.inputElement.setSelectionRange(0,9999)}))}_onClearButtonClick(e){this.inputElement.focus(),this.clear(),this._valueClearing=!1,this.inputElement.dispatchEvent(new Event("change",{bubbles:!this._slottedInput}))}_onKeyDown(e){27===e.keyCode&&this.clearButtonVisible&&this.clear()}_addIEListeners(e){navigator.userAgent.match(/Trident/)&&(this._shouldPreventInput=(()=>{this.__preventInput=!0,requestAnimationFrame(()=>{this.__preventInput=!1})}),e.addEventListener("focusin",this._shouldPreventInput),e.addEventListener("focusout",this._shouldPreventInput),this._createPropertyObserver("placeholder",this._shouldPreventInput))}_removeIEListeners(e){navigator.userAgent.match(/Trident/)&&(e.removeEventListener("focusin",this._shouldPreventInput),e.removeEventListener("focusout",this._shouldPreventInput))}_getActiveErrorId(e,t,i){this._setOrToggleAttribute("aria-describedby",t&&e?i:void 0,this.inputElement)}_getActiveLabelId(e,t){this._setOrToggleAttribute("aria-labelledby",e?t:void 0,this.inputElement)}_getErrorMessageAriaHidden(e,t,i){return(!(t&&e?i:void 0)).toString()}attributeChangedCallback(e,t,i){if(super.attributeChangedCallback(e,t,i),window.ShadyCSS&&window.ShadyCSS.nativeCss||!/^(focused|focus-ring|invalid|disabled|placeholder|has-value)$/.test(e)||this.updateStyles(),/^((?!chrome|android).)*safari/i.test(navigator.userAgent)&&this.root){const e="-webkit-backface-visibility";this.root.querySelectorAll("*").forEach(t=>{t.style[e]="visible",t.style[e]=""})}}});class q extends(k(H(Object(c.a)(h.a)))){static get template(){return s.a`
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
`}static get is(){return"vaadin-text-field"}static get version(){return"2.3.10"}static get properties(){return{list:{type:String},pattern:{type:String},title:{type:String}}}}customElements.define(q.is,q);const W=s.a`<dom-module id="material-date-picker" theme-for="vaadin-date-picker">
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
</dom-module>`;document.head.appendChild(W.content);var U=i(108),K=i(78);const X=e=>(class extends(Object(K.b)([U.a],e)){static get properties(){return{_selectedDate:{type:Date},_focusedDate:Date,value:{type:String,observer:"_valueChanged",notify:!0,value:""},required:{type:Boolean,value:!1},name:{type:String},initialPosition:String,label:String,opened:{type:Boolean,reflectToAttribute:!0,notify:!0,observer:"_openedChanged"},showWeekNumbers:{type:Boolean},_fullscreen:{value:!1,observer:"_fullscreenChanged"},_fullscreenMediaQuery:{value:"(max-width: 420px), (max-height: 420px)"},_touchPrevented:Array,i18n:{type:Object,value:()=>({monthNames:["January","February","March","April","May","June","July","August","September","October","November","December"],weekdays:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],weekdaysShort:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],firstDayOfWeek:0,week:"Week",calendar:"Calendar",clear:"Clear",today:"Today",cancel:"Cancel",formatDate:e=>{const t=String(e.year).replace(/\d+/,e=>"0000".substr(e.length)+e);return[e.month+1,e.day,t].join("/")},parseDate:e=>{const t=e.split("/"),i=new Date;let s,n=i.getMonth(),r=i.getFullYear();if(3===t.length?(r=parseInt(t[2]),t[2].length<3&&r>=0&&(r+=r<50?2e3:1900),n=parseInt(t[0])-1,s=parseInt(t[1])):2===t.length?(n=parseInt(t[0])-1,s=parseInt(t[1])):1===t.length&&(s=parseInt(t[0])),void 0!==s)return{day:s,month:n,year:r}},formatTitle:(e,t)=>e+" "+t})},min:{type:String,observer:"_minChanged"},max:{type:String,observer:"_maxChanged"},_minDate:{type:Date,value:""},_maxDate:{type:Date,value:""},_noInput:{type:Boolean,computed:"_isNoInput(_fullscreen, _ios, i18n, i18n.*)"},_ios:{type:Boolean,value:navigator.userAgent.match(/iP(?:hone|ad;(?: U;)? CPU) OS (\d+)/)},_webkitOverflowScroll:{type:Boolean,value:""===document.createElement("div").style.webkitOverflowScrolling},_ignoreAnnounce:{value:!0},_focusOverlayOnOpen:Boolean,_overlayInitialized:Boolean}}static get observers(){return["_updateHasValue(value)","_selectedDateChanged(_selectedDate, i18n.formatDate)","_focusedDateChanged(_focusedDate, i18n.formatDate)","_announceFocusedDate(_focusedDate, opened, _ignoreAnnounce)"]}ready(){super.ready(),this._boundOnScroll=this._onScroll.bind(this),this._boundFocus=this._focus.bind(this),this._boundUpdateAlignmentAndPosition=this._updateAlignmentAndPosition.bind(this);const e=e=>{const t=e.composedPath(),i=t.indexOf(this._inputElement);return 1===t.slice(0,i).filter(e=>e.getAttribute&&"clear-button"===e.getAttribute("part")).length};Object(D.b)(this,"tap",t=>{e(t)||this.open()}),this.addEventListener("touchend",t=>{e(t)||t.preventDefault()}),this.addEventListener("keydown",this._onKeydown.bind(this)),this.addEventListener("input",this._onUserInput.bind(this)),this.addEventListener("focus",e=>this._noInput&&e.target.blur()),this.addEventListener("blur",e=>!this.opened&&this.validate())}_initOverlay(){this.$.overlay.removeAttribute("disable-upgrade"),this._overlayInitialized=!0,this.$.overlay.addEventListener("opened-changed",e=>this.opened=e.detail.value),this._overlayContent.addEventListener("close",this._close.bind(this)),this._overlayContent.addEventListener("focus-input",this._focusAndSelect.bind(this)),this.$.overlay.addEventListener("vaadin-overlay-escape-press",this._boundFocus),this._overlayContent.addEventListener("focus",()=>this.focusElement._setFocused(!0)),this.$.overlay.addEventListener("vaadin-overlay-close",this._onVaadinOverlayClose.bind(this))}disconnectedCallback(){super.disconnectedCallback(),this._overlayInitialized&&this.$.overlay.removeEventListener("vaadin-overlay-escape-press",this._boundFocus),this.opened=!1}open(){this.disabled||this.readonly||(this.opened=!0)}_close(e){e&&e.stopPropagation(),this._focus(),this.close()}close(){this._overlayInitialized&&this.$.overlay.close()}get _inputElement(){return this._input()}get _nativeInput(){if(this._inputElement)return this._inputElement.focusElement?this._inputElement.focusElement:this._inputElement.inputElement?this._inputElement.inputElement:window.unwrap?window.unwrap(this._inputElement):this._inputElement}_parseDate(e){var t=/^([-+]\d{1}|\d{2,4}|[-+]\d{6})-(\d{1,2})-(\d{1,2})$/.exec(e);if(t){var i=new Date(0,0);return i.setFullYear(parseInt(t[1],10)),i.setMonth(parseInt(t[2],10)-1),i.setDate(parseInt(t[3],10)),i}}_isNoInput(e,t,i){return!this._inputElement||e||t||!i.parseDate}_formatISO(e){if(!(e instanceof Date))return"";const t=(e,t="00")=>(t+e).substr((t+e).length-t.length);let i="",s="0000",n=e.getFullYear();return n<0?(n=-n,i="-",s="000000"):e.getFullYear()>=1e4&&(i="+",s="000000"),[i+t(n,s),t(e.getMonth()+1),t(e.getDate())].join("-")}_openedChanged(e){e&&!this._overlayInitialized&&this._initOverlay(),this._overlayInitialized&&(this.$.overlay.opened=e),e&&this._updateAlignmentAndPosition()}_selectedDateChanged(e,t){if(void 0===e||void 0===t)return;this.__userInputOccurred&&(this.__dispatchChange=!0);const i=e&&t(M._extractDateParts(e)),s=this._formatISO(e);this._inputValue=e?i:"",s!==this.value&&(this.validate(),this.value=s),this.__userInputOccurred=!1,this.__dispatchChange=!1,this._ignoreFocusedDateChange=!0,this._focusedDate=e,this._ignoreFocusedDateChange=!1}_focusedDateChanged(e,t){void 0!==e&&void 0!==t&&(this.__userInputOccurred=!0,this._ignoreFocusedDateChange||this._noInput||(this._inputValue=e?t(M._extractDateParts(e)):""))}_updateHasValue(e){e?this.setAttribute("has-value",""):this.removeAttribute("has-value")}__getOverlayTheme(e,t){if(t)return e}_handleDateChange(e,t,i){if(t){var s=this._parseDate(t);s?M._dateEquals(this[e],s)||(this[e]=s,this.value&&this.validate()):this.value=i}else this[e]=""}_valueChanged(e,t){this.__dispatchChange&&this.dispatchEvent(new CustomEvent("change",{bubbles:!0})),this._handleDateChange("_selectedDate",e,t)}_minChanged(e,t){this._handleDateChange("_minDate",e,t)}_maxChanged(e,t){this._handleDateChange("_maxDate",e,t)}_updateAlignmentAndPosition(){if(this._overlayInitialized){if(!this._fullscreen){const e=this._inputElement.getBoundingClientRect(),t=e.top>window.innerHeight/2;if(e.left+this.clientWidth/2>window.innerWidth/2){const t=Math.min(window.innerWidth,document.documentElement.clientWidth);this.$.overlay.setAttribute("right-aligned",""),this.$.overlay.style.removeProperty("left"),this.$.overlay.style.right=t-e.right+"px"}else this.$.overlay.removeAttribute("right-aligned"),this.$.overlay.style.removeProperty("right"),this.$.overlay.style.left=e.left+"px";if(t){const t=Math.min(window.innerHeight,document.documentElement.clientHeight);this.$.overlay.setAttribute("bottom-aligned",""),this.$.overlay.style.removeProperty("top"),this.$.overlay.style.bottom=t-e.top+"px"}else this.$.overlay.removeAttribute("bottom-aligned"),this.$.overlay.style.removeProperty("bottom"),this.$.overlay.style.top=e.bottom+"px"}this.$.overlay.setAttribute("dir",getComputedStyle(this._inputElement).getPropertyValue("direction")),this._overlayContent._repositionYearScroller()}}_fullscreenChanged(){this._overlayInitialized&&this.$.overlay.opened&&this._updateAlignmentAndPosition()}_onOverlayOpened(){this._openedWithFocusRing=this.hasAttribute("focus-ring")||this.focusElement&&this.focusElement.hasAttribute("focus-ring");var e=this._parseDate(this.initialPosition),t=this._selectedDate||this._overlayContent.initialPosition||e||new Date;e||M._dateAllowed(t,this._minDate,this._maxDate)?this._overlayContent.initialPosition=t:this._overlayContent.initialPosition=M._getClosestDate(t,[this._minDate,this._maxDate]),this._overlayContent.scrollToDate(this._overlayContent.focusedDate||this._overlayContent.initialPosition),this._ignoreFocusedDateChange=!0,this._overlayContent.focusedDate=this._overlayContent.focusedDate||this._overlayContent.initialPosition,this._ignoreFocusedDateChange=!1,window.addEventListener("scroll",this._boundOnScroll,!0),this.addEventListener("iron-resize",this._boundUpdateAlignmentAndPosition),this._webkitOverflowScroll&&(this._touchPrevented=this._preventWebkitOverflowScrollingTouch(this.parentElement)),this._focusOverlayOnOpen?(this._overlayContent.focus(),this._focusOverlayOnOpen=!1):this._focus(),this._noInput&&this.focusElement&&this.focusElement.blur(),this.updateStyles(),this._ignoreAnnounce=!1}_preventWebkitOverflowScrollingTouch(e){for(var t=[];e;){if("touch"===window.getComputedStyle(e).webkitOverflowScrolling){var i=e.style.webkitOverflowScrolling;e.style.webkitOverflowScrolling="auto",t.push({element:e,oldInlineValue:i})}e=e.parentElement}return t}_onOverlayClosed(){if(this._ignoreAnnounce=!0,window.removeEventListener("scroll",this._boundOnScroll,!0),this.removeEventListener("iron-resize",this._boundUpdateAlignmentAndPosition),this._touchPrevented&&(this._touchPrevented.forEach(e=>e.element.style.webkitOverflowScrolling=e.oldInlineValue),this._touchPrevented=[]),this.updateStyles(),this._ignoreFocusedDateChange=!0,this.i18n.parseDate){var e=this._inputValue||"";const t=this.i18n.parseDate(e),i=t&&this._parseDate(`${t.year}-${t.month+1}-${t.day}`);this._isValidDate(i)?this._selectedDate=i:(this._selectedDate=null,this._inputValue=e)}else this._focusedDate&&(this._selectedDate=this._focusedDate);this._ignoreFocusedDateChange=!1,this._nativeInput&&this._nativeInput.selectionStart&&(this._nativeInput.selectionStart=this._nativeInput.selectionEnd),!this.value&&this.validate()}validate(){return!(this.invalid=!this.checkValidity(this._inputValue))}checkValidity(){const e=!this._inputValue||this._selectedDate&&this._inputValue===this.i18n.formatDate(M._extractDateParts(this._selectedDate)),t=!this._selectedDate||M._dateAllowed(this._selectedDate,this._minDate,this._maxDate);let i=!0;return this._inputElement&&(this._inputElement.checkValidity?(this._inputElement.__forceCheckValidity=!0,i=this._inputElement.checkValidity(),this._inputElement.__forceCheckValidity=!1):this._inputElement.validate&&(i=this._inputElement.validate())),e&&t&&i}_onScroll(e){e.target!==window&&this._overlayContent.contains(e.target)||this._updateAlignmentAndPosition()}_focus(){this._noInput?this._overlayInitialized&&this._overlayContent.focus():this._inputElement.focus()}_focusAndSelect(){this._focus(),this._setSelectionRange(0,this._inputValue.length)}_setSelectionRange(e,t){this._nativeInput&&this._nativeInput.setSelectionRange&&this._nativeInput.setSelectionRange(e,t)}_eventKey(e){for(var t=["down","up","enter","esc","tab"],i=0;i<t.length;i++){var s=t[i];if(C.a.keyboardEventMatchesKeys(e,s))return s}}_isValidDate(e){return e&&!isNaN(e.getTime())}_onKeydown(e){if(this._noInput){-1===[9].indexOf(e.keyCode)&&e.preventDefault()}switch(this._eventKey(e)){case"down":case"up":e.preventDefault(),this.opened?(this._overlayContent.focus(),this._overlayContent._onKeydown(e)):(this._focusOverlayOnOpen=!0,this.open());break;case"enter":{const e=this.i18n.parseDate(this._inputValue),t=e&&this._parseDate(e.year+"-"+(e.month+1)+"-"+e.day);this._overlayInitialized&&this._overlayContent.focusedDate&&this._isValidDate(t)&&(this._selectedDate=this._overlayContent.focusedDate),this.close();break}case"esc":this._focusedDate=this._selectedDate,this._close();break;case"tab":this.opened&&(e.preventDefault(),this._setSelectionRange(0,0),e.shiftKey?this._overlayContent.focusCancel():(this._overlayContent.focus(),this._overlayContent.revealDate(this._focusedDate)))}}_onUserInput(e){!this.opened&&this._inputElement.value&&this.open(),this._userInputValueChanged()}_userInputValueChanged(e){if(this.opened&&this._inputValue){const e=this.i18n.parseDate&&this.i18n.parseDate(this._inputValue),t=e&&this._parseDate(`${e.year}-${e.month+1}-${e.day}`);this._isValidDate(t)&&(this._ignoreFocusedDateChange=!0,M._dateEquals(t,this._focusedDate)||(this._focusedDate=t),this._ignoreFocusedDateChange=!1)}}_announceFocusedDate(e,t,i){t&&!i&&this._overlayContent.announceFocusedDate()}get _overlayContent(){return this.$.overlay.content.querySelector("#overlay-content")}});class J extends(k(u(Object(c.a)(Object(I.a)(X(Object(d.a)(h.a))))))){static get template(){return s.a`
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
`}static get is(){return"vaadin-date-picker"}static get version(){return"4.0.7"}static get properties(){return{clearButtonVisible:{type:Boolean,value:!1},disabled:{type:Boolean,value:!1,reflectToAttribute:!0},errorMessage:String,placeholder:String,readonly:{type:Boolean,value:!1,reflectToAttribute:!0},invalid:{type:Boolean,reflectToAttribute:!0,notify:!0,value:!1},_userInputValue:String}}static get observers(){return["_userInputValueChanged(_userInputValue)","_setClearButtonLabel(i18n.clear)"]}ready(){super.ready(),Object(A.a)(this,()=>this._inputElement.validate=(()=>{})),this._inputElement.addEventListener("change",()=>{""===this._inputElement.value&&(this.__dispatchChange=!0,this.value="",this.validate(),this.__dispatchChange=!1)})}_onVaadinOverlayClose(e){this._openedWithFocusRing&&this.hasAttribute("focused")?this.focusElement.setAttribute("focus-ring",""):this.hasAttribute("focused")||this.focusElement.blur(),e.detail.sourceEvent&&-1!==e.detail.sourceEvent.composedPath().indexOf(this)&&e.preventDefault()}_toggle(e){e.stopPropagation(),this[this._overlayInitialized&&this.$.overlay.opened?"close":"open"]()}_input(){return this.$.input}set _inputValue(e){this._inputElement.value=e}get _inputValue(){return this._inputElement.value}_getAriaExpanded(e){return Boolean(e).toString()}get focusElement(){return this._input()||this}_setClearButtonLabel(e){this._inputElement.shadowRoot.querySelector('[part="clear-button"]').setAttribute("aria-label",e)}}customElements.define(J.is,J)},625:function(e,t){const i=document.createElement("template");i.setAttribute("style","display: none;"),i.innerHTML='\n<dom-module id="ha-date-picker-text-field-styles" theme-for="vaadin-text-field">\n  <template>\n    <style>\n      :host {\n        padding: 8px 0 11px 0;\n        margin: 0;\n      }\n\n      [part~="label"] {\n        top: 6px;\n        font-size: var(--paper-font-subhead_-_font-size);\n        color: var(--paper-input-container-color, var(--secondary-text-color));\n      }\n\n      :host([focused]) [part~="label"] {\n        color: var(--paper-input-container-focus-color, var(--primary-color));\n      }\n\n      [part~="input-field"] {\n        color: var(--primary-text-color);\n        top: 3px;\n      }\n\n      [part~="input-field"]::before, [part~="input-field"]::after {\n        background-color: var(--paper-input-container-color, var(--secondary-text-color));\n        opacity: 1;\n      }\n\n      :host([focused]) [part~="input-field"]::before, :host([focused]) [part~="input-field"]::after {\n        background-color: var(--paper-input-container-focus-color, var(--primary-color));\n      }\n\n      [part~="value"] {\n        font-size: var(--paper-font-subhead_-_font-size);\n        height: 24px;\n        padding-top: 4px;\n        padding-bottom: 0;\n      }\n    </style>\n  </template>\n</dom-module>\n<dom-module id="ha-date-picker-button-styles" theme-for="vaadin-button">\n  <template>\n    <style>\n      :host([part~="today-button"]) [part~="button"]::before {\n        content: "⦿";\n        color: var(--primary-color);\n      }\n\n      [part~="button"] {\n        font-family: inherit;\n        font-size: var(--paper-font-subhead_-_font-size);\n        border: none;\n        background: transparent;\n        cursor: pointer;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n        color: inherit;\n      }\n\n      [part~="button"]:focus {\n        outline: none;\n      }\n    </style>\n  </template>\n</dom-module>\n<dom-module id="ha-date-picker-overlay-styles" theme-for="vaadin-date-picker-overlay">\n  <template>\n    <style include="vaadin-date-picker-overlay-default-theme">\n      [part~="toolbar"] {\n        padding: 0.3em;\n        background-color: var(--secondary-background-color);\n      }\n\n      [part="years"] {\n        background-color: var(--secondary-text-color);\n        --material-body-text-color: var(--primary-background-color);\n      }\n\n      [part="overlay"] {\n        background-color: var(--primary-background-color);\n        --material-body-text-color: var(--secondary-text-color);\n      }\n\n    </style>\n  </template>\n</dom-module>\n<dom-module id="ha-date-picker-month-styles" theme-for="vaadin-month-calendar">\n  <template>\n    <style include="vaadin-month-calendar-default-theme">\n      [part="date"][today] {\n        color: var(--primary-color);\n      }\n    </style>\n  </template>\n</dom-module>\n',document.head.appendChild(i.content)},885:function(e,t,i){"use strict";i.r(t);i(249),i(253),i(164),i(118),i(76),i(202);var s=i(4),n=i(32);i(474),i(140),i(200),i(625),i(107);const r={},a="*";customElements.define("ha-logbook-data",class extends n.a{static get properties(){return{hass:{type:Object,observer:"hassChanged"},filterDate:{type:String,observer:"filterDataChanged"},filterPeriod:{type:Number,observer:"filterDataChanged"},filterEntity:{type:String,observer:"filterDataChanged"},isLoading:{type:Boolean,value:!0,readOnly:!0,notify:!0},entries:{type:Object,value:null,readOnly:!0,notify:!0}}}hassChanged(e,t){!t&&this.filterDate&&this.updateData()}filterDataChanged(e,t){void 0!==t&&this.updateData()}updateData(){this.hass&&(this._setIsLoading(!0),this.getData(this.filterDate,this.filterPeriod,this.filterEntity).then(e=>{this._setEntries(e),this._setIsLoading(!1)}))}getData(e,t,i){return i||(i=a),r[t]||(r[t]=[]),r[t][e]||(r[t][e]=[]),r[t][e][i]?r[t][e][i]:i!==a&&r[t][e][a]?r[t][e][a].then(function(e){return e.filter(function(e){return e.entity_id===i})}):(r[t][e][i]=this._getFromServer(e,t,i),r[t][e][i])}_getFromServer(e,t,i){let s="logbook/"+e+"?period="+t;return i!==a&&(s+="&entity="+i),this.hass.callApi("GET",s).then(function(e){return e.reverse(),e},function(){return null})}refreshLogbook(){r[this.filterPeriod][this.filterDate]=[],this.updateData()}});i(189);var o=i(251),l=i(299),h=i(192),d=i(206),c=i(106),u=i(0),p=i(12),m=i(307);function f(e){var t,i=b(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var s={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(s.decorators=e.decorators),"field"===e.kind&&(s.initializer=e.value),s}function _(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function g(e){return e.decorators&&e.decorators.length}function v(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function b(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var s=i.call(e,t||"default");if("object"!=typeof s)return s;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}let w=function(e,t,i,s){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(s){t.forEach(function(t){var n=t.placement;if(t.kind===s&&("static"===n||"prototype"===n)){var r="static"===n?e:i;this.defineClassElement(r,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var s=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===s?void 0:s.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],s=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!g(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),s.push.apply(s,t.finishers)},this),!t)return{elements:i,finishers:s};var r=this.decorateConstructor(i,t);return s.push.apply(s,r.finishers),r.finishers=s,r},addElementPlacement:function(e,t,i){var s=t[e.placement];if(!i&&-1!==s.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");s.push(e.key)},decorateElement:function(e,t){for(var i=[],s=[],n=e.decorators,r=n.length-1;r>=0;r--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var o=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[r])(o)||o);e=l.element,this.addElementPlacement(e,t),l.finisher&&s.push(l.finisher);var h=l.extras;if(h){for(var d=0;d<h.length;d++)this.addElementPlacement(h[d],t);i.push.apply(i,h)}}return{element:e,finishers:s,extras:i}},decorateConstructor:function(e,t){for(var i=[],s=t.length-1;s>=0;s--){var n=this.fromClassDescriptor(e),r=this.toClassDescriptor((0,t[s])(n)||n);if(void 0!==r.finisher&&i.push(r.finisher),void 0!==r.elements){e=r.elements;for(var a=0;a<e.length-1;a++)for(var o=a+1;o<e.length;o++)if(e[a].key===e[o].key&&e[a].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=b(e.key),s=String(e.placement);if("static"!==s&&"prototype"!==s&&"own"!==s)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+s+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var r={kind:t,key:i,placement:s,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),r.initializer=e.initializer),r},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=y(e,"finisher"),s=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:s}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=y(e,"finisher"),s=this.toElementDescriptors(e.elements);return{elements:s,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var s=(0,t[i])(e);if(void 0!==s){if("function"!=typeof s)throw new TypeError("Finishers must return a constructor.");e=s}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(s)for(var r=0;r<s.length;r++)n=s[r](n);var a=t(function(e){n.initializeInstanceElements(e,o.elements)},i),o=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===r.key&&e.placement===r.placement},s=0;s<e.length;s++){var n,r=e[s];if("method"===r.kind&&(n=t.find(i)))if(v(r.descriptor)||v(n.descriptor)){if(g(r)||g(n))throw new ReferenceError("Duplicated methods ("+r.key+") can't be decorated.");n.descriptor=r.descriptor}else{if(g(r)){if(g(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+r.key+").");n.decorators=r.decorators}_(r,n)}else t.push(r)}return t}(a.d.map(f)),e);return n.initializeClassElements(a.F,o.elements),n.runClassFinishers(a.F,o.finishers)}(null,function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(u.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(u.g)()],key:"entries",value:()=>[]},{kind:"field",decorators:[Object(u.g)({attribute:"rtl",type:Boolean,reflect:!0})],key:"_rtl",value:()=>!1},{kind:"method",key:"shouldUpdate",value:function(e){const t=e.get("hass"),i=void 0===t||t.language!==this.hass.language;return e.has("entries")||i}},{kind:"method",key:"updated",value:function(e){this._rtl=Object(c.a)(this.hass)}},{kind:"method",key:"render",value:function(){var e;return(null===(e=this.entries)||void 0===e?void 0:e.length)?u.f`
      <div>
        ${Object(m.a)({items:this.entries,renderItem:(e,t)=>this._renderLogbookItem(e,t)})}
      </div>
    `:u.f`
        ${this.hass.localize("ui.panel.logbook.entries_not_found")}
      `}},{kind:"method",key:"_renderLogbookItem",value:function(e,t){if(!t)return u.f``;const i=this.entries[t-1],s=e.entity_id?this.hass.states[e.entity_id]:void 0;return u.f`
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
            .icon=${s?Object(d.a)(s):Object(h.a)(e.domain)}
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

      .uni-virtualizer-host {
        display: block;
        position: relative;
        contain: strict;
        height: 100%;
        overflow: auto;
        padding: 0 16px;
      }

      .uni-virtualizer-host > * {
        box-sizing: border-box;
      }
    `}}]}},u.a);customElements.define("ha-logbook",w);var x=i(191);customElements.define("ha-panel-logbook",class extends(Object(x.a)(n.a)){static get template(){return s.a`
      <style include="ha-style">
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
          align-items: flex-end;
          padding: 0 16px;
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
            padding-bottom: 11px;
          }
          --paper-input-suffix: {
            height: 24px;
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
          --paper-input-suffix: {
            height: 24px;
          }
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
            <paper-listbox slot="dropdown-content" selected="{{_periodIndex}}">
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
      </app-header-layout>
    `}static get properties(){return{hass:Object,narrow:{type:Boolean,reflectToAttribute:!0},_currentDate:{type:String,value:function(){const e=new Date;return new Date(Date.UTC(e.getFullYear(),e.getMonth(),e.getDate())).toISOString().split("T")[0]}},_periodIndex:{type:Number,value:0},_entityId:{type:String,value:""},entityId:{type:String,value:"",readOnly:!0},isLoading:{type:Boolean},entries:{type:Array},datePicker:{type:Object},rtl:{type:Boolean,reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}connectedCallback(){super.connectedCallback(),this.$.picker.set("i18n.parseDate",null),this.$.picker.set("i18n.formatDate",e=>Object(l.a)(new Date(e.year,e.month,e.day),this.hass.language))}_computeFilterDate(e){if(e){var t=e.split("-");return t[1]=parseInt(t[1])-1,new Date(t[0],t[1],t[2]).toISOString()}}_computeFilterDays(e){switch(e){case 1:return 3;case 2:return 7;default:return 1}}_entityPicked(e){this._setEntityId(e.target.value)}refreshLogbook(){this.shadowRoot.querySelector("ha-logbook-data").refreshLogbook()}_computeRTL(e){return Object(c.a)(e)}})}}]);
//# sourceMappingURL=chunk.343250d34984683f285d.js.map