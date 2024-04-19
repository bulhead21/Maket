const container = {...document.querySelector('container').children};

container.forEach(() => {
  setTimeout(() => {
    item.style.opacity = 1;
  }, i*100);
})