function build_opiton_tag(year, month) {
    var html_tag = `
      <option value="/invoices/${year}/${month}">
          ${year} 年 ${month} 月
      </option>
    `
    return html_tag
};

$(function add_option_tag() {
  var now = new Date();
  var options = []
  for (var i = 0; i < 3; i++) {
    option = build_opiton_tag(now.getFullYear(), (now.getMonth() + 1) - i)
    $('#link_to_past_month').append(option)
  }
});

$('#link_to_past_month').change(function() {
  if ($(this).val() != '') {
    window.location.href = $(this).val();
  }
});
