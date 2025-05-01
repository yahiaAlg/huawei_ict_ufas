document.addEventListener('DOMContentLoaded', function() {
  // Function to equalize gallery card heights
  function equalizeGalleryCardHeights() {
    // Get all gallery cards
    const galleryCards = document.querySelectorAll('.gallery-card');
    
    if (galleryCards.length === 0) return;
    
    // Reset heights first to get actual minimum
    galleryCards.forEach(card => {
      card.style.height = 'auto';
    });
    
    // Find the minimum height
    let minHeight = Infinity;
    galleryCards.forEach(card => {
      const cardHeight = card.offsetHeight;
      if (cardHeight < minHeight) {
        minHeight = cardHeight;
      }
    });
    
    // Set all cards to the minimum height
    galleryCards.forEach(card => {
      card.style.height = minHeight + 'px';
    });
  }
  
  // Run on load
  equalizeGalleryCardHeights();
  
  // Run on window resize
  window.addEventListener('resize', equalizeGalleryCardHeights);
  
  // Run when images finish loading (for more accuracy)
  window.addEventListener('load', equalizeGalleryCardHeights);
});
