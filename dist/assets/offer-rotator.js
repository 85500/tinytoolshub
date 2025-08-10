document.addEventListener('DOMContentLoaded',()=>{
  const grids = document.querySelectorAll('section h2 + .grid');
  grids.forEach(grid=>{
    const cards=[...grid.children];
    for(let i=cards.length-1;i>0;i--){
      const j=Math.floor(Math.random()*(i+1));
      grid.insertBefore(cards[j], cards[i]);
    }
  });
});