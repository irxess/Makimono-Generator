if(navigator.userAgent.indexOf('iPhone') > -1) {
  // Prevent mobile safari from zooming in on inputs with text smaller than 16px.
  // This is an ugly hack. But, reduces annoyance, and 16px selectively is excessive and ugly (just scale all the text if you need any of it to be larger, all is the same size after all).
  document
    .querySelector("[name=viewport]")
    .setAttribute("content", "width=device-width, initial-scale=1, maximum-scale=1");
}
