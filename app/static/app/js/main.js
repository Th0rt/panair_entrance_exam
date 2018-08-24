$('#link_to_past_month').change(function() {
  if ($(this).val() != '') {
    window.location.href = $(this).val();
  }
});
