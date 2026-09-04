// Small UX helpers (progressive enhancement only — every action still
// works via plain form POSTs / full page loads, per the "no localStorage
// only" requirement).
document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss alerts after 5 seconds
  document.querySelectorAll('.alert').forEach(function (alertEl) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });
});
