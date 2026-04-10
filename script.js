const revealElements = document.querySelectorAll('.reveal');
const navLinks = document.querySelectorAll('[data-nav]');
const pageNav = document.body.dataset.nav;
const profileImage = document.querySelector('[data-profile-image]');
const bookingForm = document.querySelector('[data-whatsapp-booking-form]');
const articleCarousel = document.querySelector('[data-article-carousel]');

if (pageNav) {
  navLinks.forEach((link) => {
    link.classList.toggle('active', link.dataset.nav === pageNav);
  });
}

if ('IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('reveal-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.16,
    }
  );

  revealElements.forEach((element) => revealObserver.observe(element));
} else {
  revealElements.forEach((element) => element.classList.add('reveal-visible'));
}

if (profileImage) {
  const profileCandidates = ['IMG/profile.png', 'IMG/profile.jpg'];

  const tryProfileImage = (index) => {
    if (index >= profileCandidates.length) {
      return;
    }

    const probe = new Image();
    probe.onload = () => {
      profileImage.src = profileCandidates[index];
    };
    probe.onerror = () => {
      tryProfileImage(index + 1);
    };
    probe.src = profileCandidates[index];
  };

  tryProfileImage(0);
}

if (bookingForm) {
  const bookingDateInput = bookingForm.querySelector('input[name="bookingDate"]');
  const bookingStatus = bookingForm.querySelector('[data-booking-status]');

  if (bookingDateInput) {
    bookingDateInput.min = new Date().toISOString().split('T')[0];
  }

  bookingForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const whatsappNumber = (bookingForm.dataset.whatsappNumber || '').replace(/\D/g, '');
    const clientName = bookingForm.querySelector('input[name="clientName"]')?.value.trim() || '';
    const clientEmail = bookingForm.querySelector('input[name="clientEmail"]')?.value.trim() || 'Not provided';
    const bookingDate = bookingForm.querySelector('input[name="bookingDate"]')?.value || '';
    const bookingTime = bookingForm.querySelector('input[name="bookingTime"]')?.value || '';
    const workDescription = bookingForm.querySelector('textarea[name="workDescription"]')?.value.trim() || '';
    const selectedServices = [...bookingForm.querySelectorAll('input[name="serviceType"]:checked')].map(
      (checkbox) => checkbox.value
    );

    if (!whatsappNumber) {
      if (bookingStatus) {
        bookingStatus.textContent = 'Please set data-whatsapp-number before using booking.';
      }
      return;
    }

    if (!selectedServices.length) {
      if (bookingStatus) {
        bookingStatus.textContent = 'Please select at least one service type.';
      }
      return;
    }

    if (!clientName || !bookingDate || !bookingTime || !workDescription) {
      if (bookingStatus) {
        bookingStatus.textContent = 'Please fill all required fields before submitting.';
      }
      return;
    }

    const message = [
      'Hello Mohamed Abbas, I would like to book a consultation.',
      '',
      `Name: ${clientName}`,
      `Email: ${clientEmail}`,
      `Preferred Date: ${bookingDate}`,
      `Preferred Time: ${bookingTime}`,
      `Service Type: ${selectedServices.join(', ')}`,
      `Work Description: ${workDescription}`,
      '',
      `Source: ${window.location.href}`,
    ].join('\n');

    const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank', 'noopener,noreferrer');

    if (bookingStatus) {
      bookingStatus.textContent = 'WhatsApp opened with your booking details. Please send the message there.';
    }
  });
}

if (articleCarousel) {
  const articleTrack = articleCarousel.querySelector('[data-article-track]');
  const articleSlides = articleCarousel.querySelectorAll('[data-article-slide]');
  const prevButton = articleCarousel.querySelector('[data-article-prev]');
  const nextButton = articleCarousel.querySelector('[data-article-next]');
  const dotButtons = articleCarousel.querySelectorAll('[data-article-dot]');
  let currentSlideIndex = 0;

  const updateCarousel = () => {
    if (!articleTrack || !articleSlides.length) {
      return;
    }

    articleTrack.style.transform = `translateX(-${currentSlideIndex * 100}%)`;

    if (prevButton) {
      prevButton.disabled = currentSlideIndex === 0;
    }

    if (nextButton) {
      nextButton.disabled = currentSlideIndex === articleSlides.length - 1;
    }

    dotButtons.forEach((dotButton, index) => {
      dotButton.classList.toggle('carousel-dot-active', index === currentSlideIndex);
    });
  };

  if (prevButton) {
    prevButton.addEventListener('click', () => {
      currentSlideIndex = Math.max(0, currentSlideIndex - 1);
      updateCarousel();
    });
  }

  if (nextButton) {
    nextButton.addEventListener('click', () => {
      currentSlideIndex = Math.min(articleSlides.length - 1, currentSlideIndex + 1);
      updateCarousel();
    });
  }

  dotButtons.forEach((dotButton) => {
    dotButton.addEventListener('click', () => {
      const requestedIndex = Number(dotButton.dataset.articleDot);
      if (Number.isInteger(requestedIndex) && requestedIndex >= 0 && requestedIndex < articleSlides.length) {
        currentSlideIndex = requestedIndex;
        updateCarousel();
      }
    });
  });

  updateCarousel();
}