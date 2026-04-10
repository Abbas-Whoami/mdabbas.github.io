const revealElements = document.querySelectorAll('.reveal');
const navLinks = document.querySelectorAll('[data-nav]');
const pageNav = document.body.dataset.nav;
const profileImage = document.querySelector('[data-profile-image]');

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