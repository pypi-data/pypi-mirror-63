(window["webpackJsonpstreamlit-browser"]=window["webpackJsonpstreamlit-browser"]||[]).push([[29],{3063:function(e,t,r){},3072:function(e,t,r){"use strict";r.r(t);var a=r(42),n=r(5),s=r(13),l=r(11),o=r(12),c=r(210),i=r.n(c),u=r(3051),d=r(81),p=r(214),m=r(0),f=r.n(m),g=r(4);r(3063);function v(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),r.push.apply(r,a)}return r}function y(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?v(r,!0).forEach(function(t){Object(a.a)(e,t,r[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):v(r).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))})}return e}var b=function(e){function t(e){var r;return Object(n.a)(this,t),(r=Object(s.a)(this,Object(l.a)(t).call(this,e))).currentUploadCanceller=void 0,r.dropHandler=function(e,t,a){var n=r.props.element.get("maxUploadSizeMb");if(t.length>0){var s="".concat(t[0].type," files are not allowed");r.setState({status:"ERROR",errorMessage:s})}else{var l=1024*n*1024,o=!0,c=!1,u=void 0;try{for(var d,p=e[Symbol.iterator]();!(o=(d=p.next()).done);o=!0){if(d.value.size>l){var m="The max file size allowed is ".concat(n,"MB");return void r.setState({status:"ERROR",errorMessage:m})}}}catch(C){c=!0,u=C}finally{try{o||null==p.return||p.return()}finally{if(c)throw u}}r.currentUploadCanceller=i.a.CancelToken.source();var f=[],g=!0,v=!1,y=void 0;try{for(var b,O=e[Symbol.iterator]();!(g=(b=O.next()).done);g=!0){var E=b.value,U=r.props.uploadClient.uploadFile(r.props.element.get("id"),E,void 0,r.currentUploadCanceller.token);f.push(U)}}catch(C){v=!0,y=C}finally{try{g||null==O.return||O.return()}finally{if(v)throw y}}r.setState({acceptedFiles:e,status:"UPLOADING"}),Promise.all(f).then(function(){r.currentUploadCanceller=void 0,r.setState({status:"UPLOADED"})}).catch(function(e){i.a.isCancel(e)?(r.currentUploadCanceller=void 0,r.setState({status:"UPLOADED"})):r.setState({status:"ERROR",errorMessage:e?e.toString():"Unknown error"})})}},r.reset=function(){r.setState({status:"READY",errorMessage:void 0,acceptedFiles:[]})},r.renderErrorMessage=function(){var e=r.state.errorMessage;return f.a.createElement("div",{className:"uploadStatus uploadError"},f.a.createElement("span",{className:"body"},f.a.createElement(d.a,{className:"icon",type:"warning"})," ",e),f.a.createElement(g.Button,{outline:!0,size:"sm",onClick:r.reset},"OK"))},r.renderUploadingMessage=function(){return f.a.createElement("div",{className:"uploadStatus uploadProgress"},f.a.createElement("span",{className:"body"},f.a.createElement(g.Spinner,{color:"secondary",size:"sm"})," Uploading..."),f.a.createElement(g.Button,{outline:!0,size:"sm",onClick:r.cancelCurrentUpload},"Cancel"))},r.cancelCurrentUpload=function(){null!=r.currentUploadCanceller&&(r.currentUploadCanceller.cancel(),r.currentUploadCanceller=void 0)},r.renderFileUploader=function(){var e=r.state,t=e.status,a=e.errorMessage,n=r.props.element.get("type").toArray().map(function(e){return"."+e}),s=p.d;return"UPLOADED"===t&&((s=y({},s)).ContentMessage=y({},s.ContentMessage),s.ContentMessage.style=y({},s.ContentMessage.style),s.ContentMessage.style.visibility="hidden",s.ContentMessage.style.overflow="hidden",s.ContentMessage.style.height="0.625rem"),f.a.createElement(f.a.Fragment,null,"UPLOADED"===t?f.a.createElement("div",{className:"uploadOverlay uploadDone"},f.a.createElement("span",{className:"body"},r.state.acceptedFiles[0].name)):null,f.a.createElement(u.FileUploader,{onDrop:r.dropHandler,errorMessage:a,accept:0===n.length?void 0:n,disabled:r.props.disabled,overrides:s}))},r.render=function(){var e=r.state.status,t=r.props.element.get("label");return f.a.createElement("div",{className:"Widget stFileUploader"},f.a.createElement("label",null,t),"ERROR"===e?r.renderErrorMessage():"UPLOADING"===e?r.renderUploadingMessage():r.renderFileUploader())},r.state={status:"READY",errorMessage:void 0,acceptedFiles:[]},r}return Object(o.a)(t,e),t}(f.a.PureComponent);r.d(t,"default",function(){return b})}}]);
//# sourceMappingURL=29.222b2c70.chunk.js.map