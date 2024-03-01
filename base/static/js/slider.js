let currentSlide = 0;

function showSlide(index) {
  const slider = document.querySelector('.slider');
  const slides = document.querySelectorAll('.slide');

  if (index >= slides.length) {
    currentSlide = 0;
  } else if (index < 0) {
    currentSlide = slides.length - 1;
  } else {
    currentSlide = index;
  }

  const translateValue = -currentSlide * 100 + '%';
  slider.style.transform = 'translateX(' + translateValue + ')';
}

function changeSlide(n) {
  showSlide(currentSlide + n);
}

// Auto slide change (optional)
// setInterval(function() {
//   changeSlide(1);
// }, 5000);
