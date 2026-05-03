// GymFlow JS

// Auto-dismiss alerts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (el) {
      var alert = bootstrap.Alert.getOrCreateInstance(el);
      alert.close();
    });
  }, 4000);
});
