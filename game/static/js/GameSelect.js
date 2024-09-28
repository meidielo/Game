document.querySelectorAll('.carousel-container').forEach(container => {
    const carousel = container.querySelector('.carousel');
    const prevBtn = container.querySelector('.prev-btn');
    const nextBtn = container.querySelector('.next-btn');
  
    let scrollAmount = 0;
  
    prevBtn.addEventListener('click', () => {
      carousel.scrollBy({
        top: 0,
        left: -140, // Adjust the scroll step
        behavior: 'smooth'
      });
    });
  
    nextBtn.addEventListener('click', () => {
      carousel.scrollBy({
        top: 0,
        left: 140, // Adjust the scroll step
        behavior: 'smooth'
      });
    });
  });
  