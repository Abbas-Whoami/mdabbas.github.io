const revealElements = document.querySelectorAll('.reveal');
const navLinks = document.querySelectorAll('[data-nav]');
const pageNav = document.body.dataset.nav;
const profileImage = document.querySelector('[data-profile-image]');
const bookingForm = document.querySelector('[data-whatsapp-booking-form]');
const projectCarousel = document.querySelector('[data-project-carousel]');
const articleCarousel = document.querySelector('[data-article-carousel]');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  const fxStage = document.createElement('div');
  fxStage.className = 'fx-stage';
  fxStage.setAttribute('aria-hidden', 'true');
  fxStage.innerHTML = `
    <span class="fx-ribbon fx-ribbon-a"></span>
    <span class="fx-ribbon fx-ribbon-b"></span>
    <span class="fx-ribbon fx-ribbon-c"></span>
  `;
  document.body.appendChild(fxStage);

  const fxProgress = document.createElement('div');
  fxProgress.className = 'fx-progress';
  fxProgress.setAttribute('aria-hidden', 'true');
  fxProgress.innerHTML = '<div class="fx-progress-bar" data-fx-progress></div>';
  document.body.appendChild(fxProgress);

  const progressBar = fxProgress.querySelector('[data-fx-progress]');

  const updateScrollProgress = () => {
    if (!progressBar) {
      return;
    }

    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const progress = maxScroll > 0 ? Math.min(1, Math.max(0, window.scrollY / maxScroll)) : 0;
    progressBar.style.transform = `scaleX(${progress})`;
  };

  const updatePointer = (x, y) => {
    document.body.style.setProperty('--pointer-x', `${x}px`);
    document.body.style.setProperty('--pointer-y', `${y}px`);
  };

  let burstResetTimer;
  let actionResetTimer;

  const triggerActionFx = (x, y, intensity = 1) => {
    document.body.style.setProperty('--action-x', `${x}px`);
    document.body.style.setProperty('--action-y', `${y}px`);
    document.body.classList.add('fx-action-active');
    fxStage.classList.add('fx-stage-burst');

    const pulse = document.createElement('span');
    pulse.className = 'fx-action-pulse';
    pulse.style.setProperty('--pulse-x', `${x}px`);
    pulse.style.setProperty('--pulse-y', `${y}px`);
    pulse.style.setProperty('--pulse-size', `${Math.round(160 + Math.min(120, intensity * 90))}px`);
    fxStage.appendChild(pulse);
    pulse.addEventListener('animationend', () => pulse.remove(), { once: true });

    clearTimeout(actionResetTimer);
    clearTimeout(burstResetTimer);
    actionResetTimer = setTimeout(() => {
      document.body.classList.remove('fx-action-active');
    }, 240);
    burstResetTimer = setTimeout(() => {
      fxStage.classList.remove('fx-stage-burst');
    }, 420);
  };

  updatePointer(window.innerWidth * 0.5, window.innerHeight * 0.24);
  updateScrollProgress();

  window.addEventListener('scroll', updateScrollProgress, { passive: true });
  window.addEventListener('resize', updateScrollProgress);

  window.addEventListener('pointermove', (event) => {
    if (event.pointerType === 'mouse' || event.pointerType === 'pen') {
      updatePointer(event.clientX, event.clientY);
    }
  });

  document.addEventListener('pointerdown', (event) => {
    triggerActionFx(event.clientX, event.clientY, 1.15);
  });

  window.addEventListener('keydown', (event) => {
    if (event.key !== 'Enter' && event.key !== ' ') {
      return;
    }

    const activeElement = document.activeElement;
    if (!activeElement || !(activeElement instanceof HTMLElement)) {
      return;
    }

    const rect = activeElement.getBoundingClientRect();
    const x = rect.left + rect.width * 0.5;
    const y = rect.top + rect.height * 0.5;
    triggerActionFx(x, y, 1.3);
  });
}

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

const initializeCarousel = ({
  carousel,
  trackSelector,
  slideSelector,
  prevSelector,
  nextSelector,
  dotSelector,
  dotDataKey,
}) => {
  if (!carousel) {
    return;
  }

  const track = carousel.querySelector(trackSelector);
  const slides = carousel.querySelectorAll(slideSelector);
  const prevButton = carousel.querySelector(prevSelector);
  const nextButton = carousel.querySelector(nextSelector);
  const dotButtons = carousel.querySelectorAll(dotSelector);

  if (!track || !slides.length) {
    return;
  }

  let currentSlideIndex = 0;

  const updateCarousel = () => {
    track.style.transform = `translateX(-${currentSlideIndex * 100}%)`;

    if (prevButton) {
      prevButton.disabled = currentSlideIndex === 0;
    }

    if (nextButton) {
      nextButton.disabled = currentSlideIndex === slides.length - 1;
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
      currentSlideIndex = Math.min(slides.length - 1, currentSlideIndex + 1);
      updateCarousel();
    });
  }

  dotButtons.forEach((dotButton) => {
    dotButton.addEventListener('click', () => {
      const requestedIndex = Number(dotButton.dataset[dotDataKey]);
      if (Number.isInteger(requestedIndex) && requestedIndex >= 0 && requestedIndex < slides.length) {
        currentSlideIndex = requestedIndex;
        updateCarousel();
      }
    });
  });

  updateCarousel();
};

initializeCarousel({
  carousel: projectCarousel,
  trackSelector: '[data-project-track]',
  slideSelector: '[data-project-slide]',
  prevSelector: '[data-project-prev]',
  nextSelector: '[data-project-next]',
  dotSelector: '[data-project-dot]',
  dotDataKey: 'projectDot',
});

initializeCarousel({
  carousel: articleCarousel,
  trackSelector: '[data-article-track]',
  slideSelector: '[data-article-slide]',
  prevSelector: '[data-article-prev]',
  nextSelector: '[data-article-next]',
  dotSelector: '[data-article-dot]',
  dotDataKey: 'articleDot',
});