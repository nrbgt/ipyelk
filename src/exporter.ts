/**
 * Copyright (c) 2020 Dane Freeman.
 * Distributed under the terms of the Modified BSD License.
 */
import { WidgetModel, WidgetView } from '@jupyter-widgets/base';

import { unpack_models as deserialize } from '@jupyter-widgets/base';

import { ELK_DEBUG, NAME, VERSION } from '.';

import { ELKModel, ELKView } from './widget';

import elkRawCSS from '!!raw-loader!../style/diagram.css';

import materialRawCss from '!!raw-loader!@jupyterlab/apputils/style/materialcolors.css';

import labRawCss from '!!raw-loader!@jupyterlab/theme-light-extension/style/variables.css';

const STANDALONE_CSS = `
  ${materialRawCss}
  ${labRawCss}
  ${elkRawCSS.replace(/.jp-ElkView .sprotty /g, '')}
`;

const XML_HEADER = '<?xml version="1.0" standalone="no"?>';

export class ELKExporterModel extends WidgetModel {
  static model_name = 'ELKExporterModel';
  private _update_timeout: number;

  static serializers = {
    ...WidgetModel.serializers,
    diagram: { deserialize },
    app: { deserialize }
  };

  defaults() {
    let defaults = {
      ...super.defaults(),

      _model_name: ELKExporterModel.model_name,
      _model_module_version: VERSION,
      _view_module: NAME,
      _view_name: ELKExporterView.view_name,
      _view_module_version: VERSION,
      diagram: null,
      value: null,
      enabled: true,
      extra_css: '',
      padding: 20,
      app: null
    };
    return defaults;
  }

  get diagram(): ELKModel {
    return this.get('diagram');
  }

  get app(): WidgetModel {
    return this.get('app');
  }

  get app_raw_css(): string[] {
    return this.app?.get('raw_css') || [];
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.on('change:diagram', this._on_diagram_changed, this);
    this.on('change:app', this._on_app_changed, this);
    this._on_diagram_changed();
    this._on_app_changed();
  }

  _on_diagram_changed() {
    ELK_DEBUG && console.warn('[export] diagram changed', arguments);
    const { diagram } = this;
    if (diagram == null) {
      return;
    }
    this.diagram.layoutUpdated.connect(this._schedule_update, this);
    if (!this.get('enabled')) {
      return;
    }
    this._schedule_update();
  }

  _on_app_changed() {
    ELK_DEBUG && console.warn('[export] app changed', arguments);
    const { app } = this;
    if (app != null) {
      app.on('change:raw_css', this._schedule_update, this);
    }
  }

  async a_view() {
    if (!this.get('enabled')) {
      return;
    }
    const { views } = this.diagram;
    if (views == null) {
      return;
    }

    for (const promise of Object.values(views)) {
      const view = (await promise) as ELKView;
      if (view.el) {
        return view;
      }
    }
  }

  _schedule_update() {
    if (!this.get('enabled')) {
      return;
    }
    if (this._update_timeout != null) {
      window.clearInterval(this._update_timeout);
      this._update_timeout = null;
    }
    // does weird stuff with `this` apparently
    this._update_timeout = setTimeout(() => this._on_layout_updated(), 1000);
  }

  async _on_layout_updated() {
    if (!this.get('enabled')) {
      return;
    }
    const view = await this.a_view();
    const svg: HTMLElement = view?.el?.querySelector('svg');
    if (svg == null) {
      return;
    }
    const { outerHTML } = svg;
    const padding = this.get('padding');
    const raw_app_css = this.app_raw_css;
    const rawStyle = `
        ${STANDALONE_CSS}
        ${raw_app_css.join('\n')}
        ${this.get('extra_css') || ''}
    `.replace(/\/\*[.\n]*\*\//g, ' ');
    const style = `
      <style type="text/css">
        <![CDATA[
          ${rawStyle}
        ]]>
      </style>`;
    const g: SVGGElement = svg.querySelector('g');
    const transform = g.attributes['transform'].value;
    let scaleFactor = 1.0;
    const scale = transform.match(/scale\((.*?)\)/);
    if (scale != null) {
      scaleFactor = parseFloat(scale[1]);
    }
    const { width, height } = g.getBoundingClientRect();

    const withCSS = outerHTML
      .replace(
        /<svg([^>]+)>/,
        `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width / scaleFactor +
          padding} ${height / scaleFactor + padding}" $1>
          ${style}
        `
      )
      .replace(/ transform=".*?"/, '');
    this.set({ value: `${XML_HEADER}\n${withCSS}` });

    this.save_changes(view.callbacks);
  }
}

export class ELKExporterView extends WidgetView {
  static view_name = 'ELKExporterView';
  model: ELKExporterModel;
}
