/*! For license information please see chunk.797adc460247afe933d8.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[140],{118:function(e,t,i){"use strict";i(3),i(119),i(47);var n=i(61),a=i(5),s=i(4);Object(a.a)({is:"paper-icon-button",_template:s.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        padding: 8px;
        outline: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        cursor: pointer;
        z-index: 0;
        line-height: 1;

        width: 40px;
        height: 40px;

        /*
          NOTE: Both values are needed, since some phones require the value to
          be \`transparent\`.
        */
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        -webkit-tap-highlight-color: transparent;

        /* Because of polymer/2558, this style has lower specificity than * */
        box-sizing: border-box !important;

        @apply --paper-icon-button;
      }

      :host #ink {
        color: var(--paper-icon-button-ink-color, var(--primary-text-color));
        opacity: 0.6;
      }

      :host([disabled]) {
        color: var(--paper-icon-button-disabled-text, var(--disabled-text-color));
        pointer-events: none;
        cursor: auto;

        @apply --paper-icon-button-disabled;
      }

      :host([hidden]) {
        display: none !important;
      }

      :host(:hover) {
        @apply --paper-icon-button-hover;
      }

      iron-icon {
        --iron-icon-width: 100%;
        --iron-icon-height: 100%;
      }
    </style>

    <iron-icon id="icon" src="[[src]]" icon="[[icon]]"
               alt$="[[alt]]"></iron-icon>
  `,hostAttributes:{role:"button",tabindex:"0"},behaviors:[n.a],registered:function(){this._template.setAttribute("strip-whitespace","")},properties:{src:{type:String},icon:{type:String},alt:{type:String,observer:"_altChanged"}},_altChanged:function(e,t){var i=this.getAttribute("aria-label");i&&t!=i||this.setAttribute("aria-label",e)}})},134:function(e,t,i){"use strict";i(3);const n={properties:{animationConfig:{type:Object},entryAnimation:{observer:"_entryAnimationChanged",type:String},exitAnimation:{observer:"_exitAnimationChanged",type:String}},_entryAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.entry=[{name:this.entryAnimation,node:this}]},_exitAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.exit=[{name:this.exitAnimation,node:this}]},_copyProperties:function(e,t){for(var i in t)e[i]=t[i]},_cloneConfig:function(e){var t={isClone:!0};return this._copyProperties(t,e),t},_getAnimationConfigRecursive:function(e,t,i){var n;if(this.animationConfig)if(this.animationConfig.value&&"function"==typeof this.animationConfig.value)this._warn(this._logf("playAnimation","Please put 'animationConfig' inside of your components 'properties' object instead of outside of it."));else if(n=e?this.animationConfig[e]:this.animationConfig,Array.isArray(n)||(n=[n]),n)for(var a,s=0;a=n[s];s++)if(a.animatable)a.animatable._getAnimationConfigRecursive(a.type||e,t,i);else if(a.id){var r=t[a.id];r?(r.isClone||(t[a.id]=this._cloneConfig(r),r=t[a.id]),this._copyProperties(r,a)):t[a.id]=a}else i.push(a)},getAnimationConfig:function(e){var t={},i=[];for(var n in this._getAnimationConfigRecursive(e,t,i),t)i.push(t[n]);return i}};i.d(t,"a",function(){return a});const a=[n,{_configureAnimations:function(e){var t=[],i=[];if(e.length>0)for(let s,r=0;s=e[r];r++){let e=document.createElement(s.name);if(e.isNeonAnimation){let t=null;e.configure||(e.configure=function(e){return null}),t=e.configure(s),i.push({result:t,config:s,neonAnimation:e})}else console.warn(this.is+":",s.name,"not found!")}for(var n=0;n<i.length;n++){let e=i[n].result,s=i[n].config,r=i[n].neonAnimation;try{"function"!=typeof e.cancel&&(e=document.timeline.play(e))}catch(a){e=null,console.warn("Couldnt play","(",s.name,").",a)}e&&t.push({neonAnimation:r,config:s,animation:e})}return t},_shouldComplete:function(e){for(var t=!0,i=0;i<e.length;i++)if("finished"!=e[i].animation.playState){t=!1;break}return t},_complete:function(e){for(var t=0;t<e.length;t++)e[t].neonAnimation.complete(e[t].config);for(t=0;t<e.length;t++)e[t].animation.cancel()},playAnimation:function(e,t){var i=this.getAnimationConfig(e);if(i){this._active=this._active||{},this._active[e]&&(this._complete(this._active[e]),delete this._active[e]);var n=this._configureAnimations(i);if(0!=n.length){this._active[e]=n;for(var a=0;a<n.length;a++)n[a].animation.onfinish=function(){this._shouldComplete(n)&&(this._complete(n),delete this._active[e],this.fire("neon-animation-finish",t,{bubbles:!1}))}.bind(this)}else this.fire("neon-animation-finish",t,{bubbles:!1})}},cancelAnimation:function(){for(var e in this._active){var t=this._active[e];for(var i in t)t[i].animation.cancel()}this._active={}}}]},201:function(e,t,i){"use strict";i.d(t,"b",function(){return s}),i.d(t,"a",function(){return r});i(3);var n=i(95),a=i(1);const s={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(e,t){t&&(e?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(e){this.closingReason=this.closingReason||{},this.closingReason.confirmed=e},_onDialogClick:function(e){for(var t=Object(a.a)(e).path,i=0,n=t.indexOf(this);i<n;i++){var s=t[i];if(s.hasAttribute&&(s.hasAttribute("dialog-dismiss")||s.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(s.hasAttribute("dialog-confirm")),this.close(),e.stopPropagation();break}}}},r=[n.a,s]},202:function(e,t,i){"use strict";i(3),i(72),i(162);var n=i(5),a=i(4),s=i(141);const r=a.a`
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
`;r.setAttribute("strip-whitespace",""),Object(n.a)({_template:r,is:"paper-spinner",behaviors:[s.a]})},209:function(e,t,i){"use strict";i(3),i(51),i(47),i(52),i(94);const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(n.content)},210:function(e,t,i){"use strict";i(3),i(209);var n=i(134),a=i(201),s=i(5),r=i(4);Object(s.a)({_template:r.a`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[a.a,n.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},265:function(e,t,i){"use strict";i(3),i(51);var n=i(38),a=i(65),s=i(5),r=i(1),o=i(4);Object(s.a)({_template:o.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        width: 400px;
        border: 1px solid;
        padding: 2px;
        -moz-appearance: textarea;
        -webkit-appearance: textarea;
        overflow: hidden;
      }

      .mirror-text {
        visibility: hidden;
        word-wrap: break-word;
        @apply --iron-autogrow-textarea;
      }

      .fit {
        @apply --layout-fit;
      }

      textarea {
        position: relative;
        outline: none;
        border: none;
        resize: none;
        background: inherit;
        color: inherit;
        /* see comments in template */
        width: 100%;
        height: 100%;
        font-size: inherit;
        font-family: inherit;
        line-height: inherit;
        text-align: inherit;
        @apply --iron-autogrow-textarea;
      }

      textarea::-webkit-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea::-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-ms-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }
    </style>

    <!-- the mirror sizes the input/textarea so it grows with typing -->
    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->
    <div id="mirror" class="mirror-text" aria-hidden="true">&nbsp;</div>

    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->
    <div class="textarea-container fit">
      <textarea id="textarea" name\$="[[name]]" aria-label\$="[[label]]" autocomplete\$="[[autocomplete]]" autofocus\$="[[autofocus]]" inputmode\$="[[inputmode]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" required\$="[[required]]" disabled\$="[[disabled]]" rows\$="[[rows]]" minlength\$="[[minlength]]" maxlength\$="[[maxlength]]"></textarea>
    </div>
`,is:"iron-autogrow-textarea",behaviors:[a.a,n.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(e){this.$.textarea.selectionStart=e},set selectionEnd(e){this.$.textarea.selectionEnd=e},attached:function(){navigator.userAgent.match(/iP(?:[oa]d|hone)/)&&(this.$.textarea.style.marginLeft="-3px")},validate:function(){var e=this.$.textarea.validity.valid;return e&&(this.required&&""===this.value?e=!1:this.hasValidator()&&(e=a.a.validate.call(this,this.value))),this.invalid=!e,this.fire("iron-input-validate"),e},_bindValueChanged:function(e){this.value=e},_valueChanged:function(e){var t=this.textarea;t&&(t.value!==e&&(t.value=e||0===e?e:""),this.bindValue=e,this.$.mirror.innerHTML=this._valueForMirror(),this.fire("bind-value-changed",{value:this.bindValue}))},_onInput:function(e){var t=Object(r.a)(e).path;this.value=t?t[0].value:e.target.value},_constrain:function(e){var t;for(e=e||[""],t=this.maxRows>0&&e.length>this.maxRows?e.slice(0,this.maxRows):e.slice(0);this.rows>0&&t.length<this.rows;)t.push("");return t.join("<br/>")+"&#160;"},_valueForMirror:function(){var e=this.textarea;if(e)return this.tokens=e&&e.value?e.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""],this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});i(124),i(125),i(126);var l=i(64),h=i(104);Object(s.a)({_template:o.a`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
        display: none !important;
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container no-label-float$="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <iron-autogrow-textarea class="paper-input-input" slot="input" id$="[[_inputId]]" aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" bind-value="{{value}}" invalid="{{invalid}}" validator$="[[validator]]" disabled$="[[disabled]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" autocapitalize$="[[autocapitalize]]" rows$="[[rows]]" max-rows$="[[maxRows]]" on-change="_onChange"></iron-autogrow-textarea>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
`,is:"paper-textarea",behaviors:[h.a,l.a],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(e){this.$.input.textarea.selectionStart=e},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(e){this.$.input.textarea.selectionEnd=e},_ariaLabelledByChanged:function(e){this._focusableElement.setAttribute("aria-labelledby",e)},_ariaDescribedByChanged:function(e){this._focusableElement.setAttribute("aria-describedby",e)},get _focusableElement(){return this.inputElement.textarea}})},380:function(e,t,i){"use strict";i.d(t,"a",function(){return r});var n=i(14),a=i(9);const s=new WeakMap,r=Object(a.f)((...e)=>t=>{let i=s.get(t);void 0===i&&(i={lastRenderedIndex:2147483647,values:[]},s.set(t,i));const a=i.values;let r=a.length;i.values=e;for(let s=0;s<e.length&&!(s>i.lastRenderedIndex);s++){const o=e[s];if(Object(n.h)(o)||"function"!=typeof o.then){t.setValue(o),i.lastRenderedIndex=s;break}s<r&&o===a[s]||(i.lastRenderedIndex=2147483647,r=0,Promise.resolve(o).then(e=>{const n=i.values.indexOf(o);n>-1&&n<i.lastRenderedIndex&&(i.lastRenderedIndex=n,t.setValue(e),t.commit())}))}})},417:function(e,t,i){"use strict";var n=i(0);customElements.define("round-slider",class extends n.a{static get properties(){return{value:{type:Number},high:{type:Number},low:{type:Number},min:{type:Number},max:{type:Number},step:{type:Number},startAngle:{type:Number},arcLength:{type:Number},handleSize:{type:Number},handleZoom:{type:Number},disabled:{type:Boolean},dragging:{type:Boolean,reflect:!0},rtl:{type:Boolean},_scale:{type:Number}}}constructor(){super(),this.min=0,this.max=100,this.step=1,this.startAngle=135,this.arcLength=270,this.handleSize=6,this.handleZoom=1.5,this.disabled=!1,this.dragging=!1,this.rtl=!1,this._scale=1}get _start(){return this.startAngle*Math.PI/180}get _len(){return Math.min(this.arcLength*Math.PI/180,2*Math.PI-.01)}get _end(){return this._start+this._len}get _enabled(){return!(this.disabled||null==this.value&&(null==this.high||null==this.low)||null!=this.value&&(this.value>this.max||this.value<this.min)||null!=this.high&&(this.high>this.max||this.high<this.min)||null!=this.low&&(this.low>this.max||this.low<this.min))}_angleInside(e){let t=(this.startAngle+this.arcLength/2-e+180+360)%360-180;return t<this.arcLength/2&&t>-this.arcLength/2}_angle2xy(e){return this.rtl?{x:-Math.cos(e),y:Math.sin(e)}:{x:Math.cos(e),y:Math.sin(e)}}_xy2angle(e,t){return this.rtl&&(e=-e),(Math.atan2(t,e)-this._start+2*Math.PI)%(2*Math.PI)}_value2angle(e){const t=(e-this.min)/(this.max-this.min);return this._start+t*this._len}_angle2value(e){return Math.round((e/this._len*(this.max-this.min)+this.min)/this.step)*this.step}get _boundaries(){const e=this._angle2xy(this._start),t=this._angle2xy(this._end);let i=1;this._angleInside(270)||(i=Math.max(-e.y,-t.y));let n=1;this._angleInside(90)||(n=Math.max(e.y,t.y));let a=1;this._angleInside(180)||(a=Math.max(-e.x,-t.x));let s=1;return this._angleInside(0)||(s=Math.max(e.x,t.x)),{up:i,down:n,left:a,right:s,height:i+n,width:a+s}}dragStart(e){let t=e.target;if(this._rotation&&"focus"!==this._rotation.type)return;if(t.classList.contains("overflow")&&(t=t.nextElementSibling),!t.classList.contains("handle"))return;t.setAttribute("stroke-width",2*this.handleSize*this.handleZoom*this._scale);const i="high"===t.id?this.low:this.min,n="low"===t.id?this.high:this.max;this._rotation={handle:t,min:i,max:n,start:this[t.id],type:e.type},this.dragging=!0}dragEnd(e){if(!this._rotation)return;const t=this._rotation.handle;t.setAttribute("stroke-width",2*this.handleSize*this._scale),this._rotation=!1,this.dragging=!1,t.blur();let i=new CustomEvent("value-changed",{detail:{[t.id]:this[t.id]}});this.dispatchEvent(i),this.low&&this.low>=.99*this.max?this._reverseOrder=!0:this._reverseOrder=!1}drag(e){if(!this._rotation)return;if("focus"===this._rotation.type)return;e.preventDefault();const t="touchmove"===e.type?e.touches[0].clientX:e.clientX,i="touchmove"===e.type?e.touches[0].clientY:e.clientY,n=this.shadowRoot.querySelector("svg").getBoundingClientRect(),a=this._boundaries,s=t-(n.left+a.left*n.width/a.width),r=i-(n.top+a.up*n.height/a.height),o=this._xy2angle(s,r),l=this._angle2value(o);this._dragpos(l)}_dragpos(e){if(e<this._rotation.min||e>this._rotation.max)return;const t=this._rotation.handle;this[t.id]=e;let i=new CustomEvent("value-changing",{detail:{[t.id]:e}});this.dispatchEvent(i)}_keyStep(e){if(!this._rotation)return;const t=this._rotation.handle;"ArrowLeft"===e.key&&(this.rtl?this._dragpos(this[t.id]+this.step):this._dragpos(this[t.id]-this.step)),"ArrowRight"===e.key&&(this.rtl?this._dragpos(this[t.id]-this.step):this._dragpos(this[t.id]+this.step))}firstUpdated(){document.addEventListener("mouseup",this.dragEnd.bind(this)),document.addEventListener("touchend",this.dragEnd.bind(this),{passive:!1}),document.addEventListener("mousemove",this.drag.bind(this)),document.addEventListener("touchmove",this.drag.bind(this),{passive:!1}),document.addEventListener("keydown",this._keyStep.bind(this))}updated(e){if(this.shadowRoot.querySelector("svg")&&void 0!==this.shadowRoot.querySelector("svg").style.vectorEffect)return;e.has("_scale")&&1!=this._scale&&this.shadowRoot.querySelector("svg").querySelectorAll("path").forEach(e=>{if(e.getAttribute("stroke-width"))return;const t=parseFloat(getComputedStyle(e).getPropertyValue("stroke-width"));e.style.strokeWidth=`${t*this._scale}px`});const t=this.shadowRoot.querySelector("svg").getBoundingClientRect(),i=Math.max(t.width,t.height);this._scale=2/i}_renderArc(e,t){const i=t-e;return e=this._angle2xy(e),t=this._angle2xy(t+.001),`\n      M ${e.x} ${e.y}\n      A 1 1,\n        0,\n        ${i>Math.PI?"1":"0"} ${this.rtl?"0":"1"},\n        ${t.x} ${t.y}\n    `}_renderHandle(e){const t=this._value2angle(this[e]),i=this._angle2xy(t);return n.j`
      <g class="${e} handle">
        <path
          id=${e}
          class="overflow"
          d="
          M ${i.x} ${i.y}
          L ${i.x+.001} ${i.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke="rgba(0,0,0,0)"
          stroke-width="${4*this.handleSize*this._scale}"
          />
        <path
          id=${e}
          class="handle"
          d="
          M ${i.x} ${i.y}
          L ${i.x+.001} ${i.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke-width="${2*this.handleSize*this._scale}"
          tabindex="0"
          @focus=${this.dragStart}
          @blur=${this.dragEnd}
          />
        </g>
      `}render(){const e=this._boundaries;return n.f`
      <svg
        @mousedown=${this.dragStart}
        @touchstart=${this.dragStart}
        xmln="http://www.w3.org/2000/svg"
        viewBox="${-e.left} ${-e.up} ${e.width} ${e.height}"
        style="margin: ${this.handleSize*this.handleZoom}px;"
        focusable="false"
      >
        <g class="slider">
          <path
            class="path"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
          />
          ${this._enabled?n.j`
              <path
                class="bar"
                vector-effect="non-scaling-stroke"
                d=${this._renderArc(this._value2angle(null!=this.low?this.low:this.min),this._value2angle(null!=this.high?this.high:this.value))}
              />`:""}
        </g>

        <g class="handles">
        ${this._enabled?null!=this.low?this._reverseOrder?n.f`${this._renderHandle("high")} ${this._renderHandle("low")}`:n.f`${this._renderHandle("low")} ${this._renderHandle("high")}`:n.f`${this._renderHandle("value")}`:""}
        </g>
      </svg>
    `}static get styles(){return n.c`
      :host {
        display: inline-block;
        width: 100%;
      }
      svg {
        overflow: visible;
      }
      .slider {
        fill: none;
        stroke-width: var(--round-slider-path-width, 3);
        stroke-linecap: var(--round-slider-linecap, round);
      }
      .path {
        stroke: var(--round-slider-path-color, lightgray);
      }
      .bar {
        stroke: var(--round-slider-bar-color, deepskyblue);
      }
      g.handles {
        stroke: var(--round-slider-handle-color, var(--round-slider-bar-color, deepskyblue));
        stroke-linecap: round;
      }
      g.low.handle {
        stroke: var(--round-slider-low-handle-color);
      }
      g.high.handle {
        stroke: var(--round-slider-high-handle-color);
      }
      .handle:focus {
        outline: unset;
      }
    `}})},441:function(e,t){e.exports=function e(t){return Object.freeze(t),Object.getOwnPropertyNames(t).forEach(function(i){!t.hasOwnProperty(i)||null===t[i]||"object"!=typeof t[i]&&"function"!=typeof t[i]||Object.isFrozen(t[i])||e(t[i])}),t}},61:function(e,t,i){"use strict";i.d(t,"b",function(){return r}),i.d(t,"a",function(){return o});i(3);var n=i(60),a=i(38),s=i(73);const r={observers:["_focusedChanged(receivedFocusFromKeyboard)"],_focusedChanged:function(e){e&&this.ensureRipple(),this.hasRipple()&&(this._ripple.holdDown=e)},_createRipple:function(){var e=s.a._createRipple();return e.id="ink",e.setAttribute("center",""),e.classList.add("circle"),e}},o=[n.a,a.a,s.a,r]},73:function(e,t,i){"use strict";i.d(t,"a",function(){return s});i(3),i(105);var n=i(60),a=i(1);const s={properties:{noink:{type:Boolean,observer:"_noinkChanged"},_rippleContainer:{type:Object}},_buttonStateChanged:function(){this.focused&&this.ensureRipple()},_downHandler:function(e){n.b._downHandler.call(this,e),this.pressed&&this.ensureRipple(e)},ensureRipple:function(e){if(!this.hasRipple()){this._ripple=this._createRipple(),this._ripple.noink=this.noink;var t=this._rippleContainer||this.root;if(t&&Object(a.a)(t).appendChild(this._ripple),e){var i=Object(a.a)(this._rippleContainer||this),n=Object(a.a)(e).rootTarget;i.deepContains(n)&&this._ripple.uiDownAction(e)}}},getRipple:function(){return this.ensureRipple(),this._ripple},hasRipple:function(){return Boolean(this._ripple)},_createRipple:function(){return document.createElement("paper-ripple")},_noinkChanged:function(e){this.hasRipple()&&(this._ripple.noink=e)}}}}]);
//# sourceMappingURL=chunk.797adc460247afe933d8.js.map