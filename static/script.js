$(function() {
  $('div.bigbox > div').each(function() {
    $(this).hide();
  });

  function showTab(name) {
    var old = $('div.bigbox > div:visible');
    function fadeIn() { $('#' + name).fadeIn('fast'); }
    old.length ? old.fadeOut('fast', fadeIn) : fadeIn();
  }

  $('body').hide().fadeIn(1000);
  showTab(document.location.hash.substring(1) || 'problem');

  $('ul.navigation a').each(function() {
    $(this).click(function() {
      showTab(this.href.split('#', 2)[1]);
    });
  });
});
