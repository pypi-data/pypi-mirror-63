(window["webpackJsonpstreamlit-browser"]=window["webpackJsonpstreamlit-browser"]||[]).push([[38],{3080:function(e,t,n){"use strict";n.r(t);var a=n(72),l=n(5),r=n(10),o=n(13),i=n(11),s=n(12),u=n(0),c=n.n(u),p=n(1632),d=n(16),f=function(e){function t(){var e,n;Object(l.a)(this,t);for(var r=arguments.length,s=new Array(r),u=0;u<r;u++)s[u]=arguments[u];return(n=Object(o.a)(this,(e=Object(i.a)(t)).call.apply(e,[this].concat(s)))).state={value:n.props.element.get("default")},n.setWidgetValue=function(e){var t=n.props.element.get("id");n.props.widgetMgr.setIntValue(t,n.state.value,e)},n.onChange=function(e){if(0!==e.value.length){var t=Object(a.a)(e.value,1)[0];n.setState({value:parseInt(t.value,10)},function(){return n.setWidgetValue({fromUi:!0})})}else Object(d.d)("No value selected!")},n.filterOptions=function(e,t){return e.filter(function(e){return e.label.includes(t.toString())})},n.render=function(){var e={width:n.props.width},t=n.props.element.get("label"),a=n.props.element.get("options"),l=n.props.disabled,r=[{label:a.size>0?a.get(n.state.value):"No options to select.",value:n.state.value.toString()}];0===a.size&&(a=["No options to select."],l=!0);var o=[];return a.forEach(function(e,t){return o.push({label:e,value:t.toString()})}),c.a.createElement("div",{className:"Widget row-widget stSelectbox",style:e},c.a.createElement("label",null,t),c.a.createElement(p.Select,{clearable:!1,disabled:l,labelKey:"label",onChange:n.onChange,options:o,filterOptions:n.filterOptions,value:r,valueKey:"value"}))},n}return Object(s.a)(t,e),Object(r.a)(t,[{key:"componentDidMount",value:function(){this.setWidgetValue({fromUi:!1})}}]),t}(c.a.PureComponent);n.d(t,"default",function(){return f})}}]);
//# sourceMappingURL=38.6f5d0ce8.chunk.js.map