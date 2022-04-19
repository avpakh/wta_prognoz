/*
 Highcharts JS v8.1.2 (2020-06-16)

 X-range series

 (c) 2010-2019 Torstein Honsi, Lars A. V. Cabrera

 License: www.highcharts.com/license
*/
(function(b){"object"===typeof module&&module.exports?(b["default"]=b,module.exports=b):"function"===typeof define&&define.amd?define("highcharts/modules/xrange",["highcharts"],function(h){b(h);b.Highcharts=h;return b}):b("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(b){function h(b,l,h,p){b.hasOwnProperty(l)||(b[l]=p.apply(null,h))}b=b?b._modules:{};h(b,"modules/xrange.src.js",[b["parts/Axis.js"],b["parts/Globals.js"],b["parts/Color.js"],b["parts/Point.js"],b["parts/Utilities.js"]],
function(b,l,h,p,g){var x=h.parse;h=g.addEvent;var r=g.clamp,B=g.correctFloat,C=g.defined,y=g.find,t=g.isNumber,v=g.isObject,u=g.merge,w=g.pick;g=g.seriesType;var z=l.seriesTypes.column,A=l.seriesTypes,D=l.Series;g("xrange","column",{colorByPoint:!0,dataLabels:{formatter:function(){var a=this.point.partialFill;v(a)&&(a=a.amount);if(t(a)&&0<a)return B(100*a)+"%"},inside:!0,verticalAlign:"middle"},tooltip:{headerFormat:'<span style="font-size: 10px">{point.x} - {point.x2}</span><br/>',pointFormat:'<span style="color:{point.color}">\u25cf</span> {series.name}: <b>{point.yCategory}</b><br/>'},
borderRadius:3,pointRange:0},{type:"xrange",parallelArrays:["x","x2","y"],requireSorting:!1,animate:A.line.prototype.animate,cropShoulder:1,getExtremesFromAll:!0,autoIncrement:l.noop,buildKDTree:l.noop,init:function(){A.column.prototype.init.apply(this,arguments);this.options.stacking=void 0},getColumnMetrics:function(){function a(){f.series.forEach(function(a){var c=a.xAxis;a.xAxis=a.yAxis;a.yAxis=c})}var f=this.chart;a();var d=z.prototype.getColumnMetrics.call(this);a();return d},cropData:function(a,
f,d,m){f=D.prototype.cropData.call(this,this.x2Data,f,d,m);f.xData=a.slice(f.start,f.end);return f},findPointIndex:function(a){var f=this.cropped,d=this.cropStart,m=this.points,c=a.id;if(c)var e=(e=y(m,function(a){return a.id===c}))?e.index:void 0;"undefined"===typeof e&&(e=(e=y(m,function(c){return c.x===a.x&&c.x2===a.x2&&!c.touched}))?e.index:void 0);f&&t(e)&&t(d)&&e>=d&&(e-=d);return e},translatePoint:function(a){var f=this.xAxis,d=this.yAxis,m=this.columnMetrics,c=this.options,e=c.minPointLength||
0,b=a.plotX,g=w(a.x2,a.x+(a.len||0)),k=f.translate(g,0,0,0,1);g=Math.abs(k-b);var h=this.chart.inverted,l=w(c.borderWidth,1)%2/2,n=m.offset,q=Math.round(m.width);e&&(e-=g,0>e&&(e=0),b-=e/2,k+=e/2);b=Math.max(b,-10);k=r(k,-10,f.len+10);C(a.options.pointWidth)&&(n-=(Math.ceil(a.options.pointWidth)-q)/2,q=Math.ceil(a.options.pointWidth));c.pointPlacement&&t(a.plotY)&&d.categories&&(a.plotY=d.translate(a.y,0,1,0,1,c.pointPlacement));a.shapeArgs={x:Math.floor(Math.min(b,k))+l,y:Math.floor(a.plotY+n)+l,
width:Math.round(Math.abs(k-b)),height:q,r:this.options.borderRadius};c=a.shapeArgs.x;e=c+a.shapeArgs.width;0>c||e>f.len?(c=r(c,0,f.len),e=r(e,0,f.len),k=e-c,a.dlBox=u(a.shapeArgs,{x:c,width:e-c,centerX:k?k/2:null})):a.dlBox=null;c=a.tooltipPos;e=h?1:0;k=h?0:1;m=this.columnMetrics?this.columnMetrics.offset:-m.width/2;c[e]=r(c[e]+g/2*(f.reversed?-1:1)*(h?-1:1),0,f.len-1);c[k]=r(c[k]+(h?-1:1)*m,0,d.len-1);if(m=a.partialFill)v(m)&&(m=m.amount),t(m)||(m=0),d=a.shapeArgs,a.partShapeArgs={x:d.x,y:d.y,width:d.width,
height:d.height,r:this.options.borderRadius},b=Math.max(Math.round(g*m+a.plotX-b),0),a.clipRectArgs={x:f.reversed?d.x+g-b:d.x,y:d.y,width:b,height:d.height}},translate:function(){z.prototype.translate.apply(this,arguments);this.points.forEach(function(a){this.translatePoint(a)},this)},drawPoint:function(a,f){var d=this.options,b=this.chart.renderer,c=a.graphic,e=a.shapeType,g=a.shapeArgs,h=a.partShapeArgs,k=a.clipRectArgs,l=a.partialFill,p=d.stacking&&!d.borderRadius,n=a.state,q=d.states[n||"normal"]||
{},r="undefined"===typeof n?"attr":f;n=this.pointAttribs(a,n);q=w(this.chart.options.chart.animation,q.animation);if(a.isNull||!1===a.visible)c&&(a.graphic=c.destroy());else{if(c)c.rect[f](g);else a.graphic=c=b.g("point").addClass(a.getClassName()).add(a.group||this.group),c.rect=b[e](u(g)).addClass(a.getClassName()).addClass("highcharts-partfill-original").add(c);h&&(c.partRect?(c.partRect[f](u(h)),c.partialClipRect[f](u(k))):(c.partialClipRect=b.clipRect(k.x,k.y,k.width,k.height),c.partRect=b[e](h).addClass("highcharts-partfill-overlay").add(c).clip(c.partialClipRect)));
this.chart.styledMode||(c.rect[f](n,q).shadow(d.shadow,null,p),h&&(v(l)||(l={}),v(d.partialFill)&&(l=u(l,d.partialFill)),a=l.fill||x(n.fill).brighten(-.3).get()||x(a.color||this.color).brighten(-.3).get(),n.fill=a,c.partRect[r](n,q).shadow(d.shadow,null,p)))}},drawPoints:function(){var a=this,f=a.getAnimationVerb();a.points.forEach(function(b){a.drawPoint(b,f)})},getAnimationVerb:function(){return this.chart.pointCount<(this.options.animationLimit||250)?"animate":"attr"}},{resolveColor:function(){var a=
this.series;if(a.options.colorByPoint&&!this.options.color){var b=a.options.colors||a.chart.options.colors;var d=this.y%(b?b.length:a.chart.options.chart.colorCount);b=b&&b[d];a.chart.styledMode||(this.color=b);this.options.colorIndex||(this.colorIndex=d)}else this.color||(this.color=a.color)},init:function(){p.prototype.init.apply(this,arguments);this.y||(this.y=0);return this},setState:function(){p.prototype.setState.apply(this,arguments);this.series.drawPoint(this,this.series.getAnimationVerb())},
getLabelConfig:function(){var a=p.prototype.getLabelConfig.call(this),b=this.series.yAxis.categories;a.x2=this.x2;a.yCategory=this.yCategory=b&&b[this.y];return a},tooltipDateKeys:["x","x2"],isValid:function(){return"number"===typeof this.x&&"number"===typeof this.x2}});h(b,"afterGetSeriesExtremes",function(){var a=this.series,b;if(this.isXAxis){var d=w(this.dataMax,-Number.MAX_VALUE);a.forEach(function(a){a.x2Data&&a.x2Data.forEach(function(a){a>d&&(d=a,b=!0)})});b&&(this.dataMax=d)}});""});h(b,
"masters/modules/xrange.src.js",[],function(){})});
