(self.webpackJsonp=self.webpackJsonp||[]).push([[121],{789:function(e,a,l){"use strict";l.r(a);l(164);var r=l(4),t=l(32);l(140),l(107);customElements.define("ha-panel-iframe",class extends t.a{static get template(){return r.a`
      <style include="ha-style">
        iframe {
          border: 0;
          width: 100%;
          height: calc(100% - 64px);
          background-color: var(--primary-background-color);
        }
      </style>
      <app-toolbar>
        <ha-menu-button hass="[[hass]]" narrow="[[narrow]]"></ha-menu-button>
        <div main-title>[[panel.title]]</div>
      </app-toolbar>

      <iframe
        src="[[panel.config.url]]"
        sandbox="allow-forms allow-popups allow-pointer-lock allow-same-origin allow-scripts"
        allowfullscreen="true"
        webkitallowfullscreen="true"
        mozallowfullscreen="true"
      ></iframe>
    `}static get properties(){return{hass:Object,narrow:Boolean,panel:Object}}})}}]);
//# sourceMappingURL=chunk.e3829c52f1b22a1c6ccb.js.map